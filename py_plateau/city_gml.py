#!/usr/bin/env python
# coding: utf-8

import os
import pdb
import traceback
from enum import Enum
from pathlib import Path

import geopandas as gpd
import lxml
import numpy as np
import open3d as o3d
from lxml import etree
from shapely.geometry import MultiPolygon, Polygon

from .building import Building, BuildingPolygon, BuildingTexture


class Subset(Enum):
    PLY = 1  # PLY file
    GEOJSON = 2  # GeoJSON file


def str2floats(x):
    """x y z -> [x, y, z]"""
    return np.array([float(i) for i in x.text.split(" ")])


class CityGml:
    """core:CityGml"""

    def __init__(self, filename, subset, to_srid, separate=False, lonlat=False):
        # filename
        self.filename = filename
        self.basename = os.path.splitext(os.path.basename(filename))[0]

        # params
        self.subset = subset
        self.lonlat = lonlat
        self.separate = separate

        # split from basename
        basenames = self.basename.split("_")
        # メッシュコード
        self.mesh_code = basenames[0]
        # 地物型 (bldg)
        self.object_name = basenames[1]
        # CRS 空間参照 ID (SRID)
        self.from_srid = basenames[2]
        self.to_srid = to_srid

        # lod
        self.lod = None

        # xml tree
        tree = etree.parse(filename)
        root = tree.getroot()
        self.tree = tree
        self.root = root

        # buildings
        self.obj_buildings = []

        # textures
        self.textures = []

    @staticmethod
    def get_bldg_properties(building, nsmap):
        properties = dict()
        try:
            # bldg:Building attribute=>gml:id
            attrib_id = "{%s}id" % nsmap["gml"]
            if attrib_id in building.attrib:
                properties["id"] = building.attrib[attrib_id]

            # gen:stringAttribute
            string_attributes = building.xpath("gen:stringAttribute", namespaces=nsmap)
            for string_attribute in string_attributes:
                properties[string_attribute.attrib["name"]] = string_attribute.getchildren()[0].text

            # bldg:measuredHeight
            measured_heights = building.xpath("bldg:measuredHeight", namespaces=nsmap)
            if len(measured_heights) > 0:
                properties["measured_height_uom"] = measured_heights[0].attrib["uom"]
                properties["measured_height"] = float(measured_heights[0].text)

            # bldg:address
            addresses = building.xpath(
                "bldg:address/core:Address/core:xalAddress/xAL:AddressDetails/xAL:Country/xAL:Locality/xAL:LocalityName",
                namespaces=nsmap,
            )
            if len(addresses) > 0:
                properties["address_type"] = addresses[0].attrib["Type"]
                properties["address"] = addresses[0].text

            # uro:buildingRoofEdgeArea
            building_roof_edge_area = building.xpath(
                "uro:buildingDetails/uro:BuildingDetails/uro:buildingRoofEdgeArea",
                namespaces=nsmap,
            )
            if len(building_roof_edge_area) > 0:
                properties["building_roof_edge_area_uom"] = building_roof_edge_area[0].attrib["uom"]
                properties["building_roof_edge_area"] = float(building_roof_edge_area[0].text)

            # uro:districtsAndZonesType
            districts_and_zones_type = building.xpath(
                "uro:buildingDetails/uro:BuildingDetails/uro:districtsAndZonesType",
                namespaces=nsmap,
            )
            if len(districts_and_zones_type) > 0:
                properties["districts_and_zones_type"] = districts_and_zones_type[0].text

            # uro:prefecture
            prefecture = building.xpath(
                "uro:buildingDetails/uro:BuildingDetails/uro:prefecture",
                namespaces=nsmap,
            )
            if len(prefecture) > 0:
                properties["prefecture"] = prefecture[0].text

            # uro:city
            city = building.xpath(
                "uro:buildingDetails/uro:BuildingDetails/uro:city",
                namespaces=nsmap,
            )
            if len(city) > 0:
                properties["city"] = city[0].text

            # uro:surveyYear
            survey_year = building.xpath(
                "uro:buildingDetails/uro:BuildingDetails/uro:surveyYear",
                namespaces=nsmap,
            )
            if len(survey_year) > 0:
                properties["survey_year"] = survey_year[0].text

        except lxml.etree.XPathEvalError as e:
            print(e)
            traceback.print_exc()

        return properties

    def get_textures(self):
        """テクスチャを取得する"""
        nsmap = self.root.nsmap
        tree = self.tree

        appearance_member = tree.xpath(
            "/core:CityModel/app:appearanceMember/app:Appearance/app:surfaceDataMember/app:ParameterizedTexture",
            namespaces=nsmap,
        )

        # 画像のURIを取得
        textures = []
        for appearance in appearance_member:
            texture = BuildingTexture()

            # 画像のURIを取得
            for image_url in appearance.xpath("app:imageURI", namespaces=nsmap):
                texture.set_image_uri(image_url.text)

            # テクスチャの情報を取得
            # テクスチャ1枚に対して、複数の面がある
            # targetは面のID
            for target in appearance.xpath("app:target", namespaces=nsmap):
                # 先頭の文字はリンク先を表す「#」なので除去
                poly_id = target.attrib["uri"][1:]

                # テクスチャのUV座標を取得
                # 文字列になっているので、floatに変換
                texture_coordinates = [
                    str2floats(coordinates).reshape((-1, 2))
                    for coordinates in target.xpath(
                        "app:TexCoordList/app:textureCoordinates",
                        namespaces=nsmap,
                    )
                ]

                # 要素数の最大値を取り出す
                maximum_of_elements = max(map(lambda x: x.shape[0], texture_coordinates))

                # 要素の数が最大値よりも多い時に要素を追加する
                for coordinate_index, coord in enumerate(texture_coordinates):
                    num = maximum_of_elements - coord.shape[0]

                    if num > 0:
                        texture_coordinates[coordinate_index] = np.append(
                            coord,
                            np.tile(coord[-1].reshape(-1, 2), (num, 1)),
                            axis=0,
                        )

                # テクスチャの座標とURIのペアを格納
                # 重複して同じ座標が2つ入っていることもあるので、除去
                texture.set_uv_coords(poly_id, np.unique(np.array(texture_coordinates), axis=0)[0])

            textures.append(texture)

        return textures

    def set_building_object(self, building, faces):
        """building objectを追加"""
        obj_building = Building(self.from_srid, self.to_srid, self.lonlat)

        # set properties
        properties = self.get_bldg_properties(building, self.root.nsmap)
        obj_building.set_properties(properties)

        # set textures
        textures = self.get_textures()
        obj_building.set_textures(textures)

        polygons = [str2floats(face_str).reshape((-1, 3)) for face_str in faces]
        # polygonのidを付与できるように、buildingからpolygonのidを取得
        # ない場合はNoneにしとく？
        if self.subset == Subset.PLY:
            obj_building.create_triangle_meshes(polygons)
        elif self.subset == Subset.GEOJSON:
            obj_building.create_vertices(polygons)
        else:
            raise Exception(f"ERROR: subset = {self.subset}")

        self.obj_buildings.append(obj_building)

    def lod0(self):
        nsmap = self.root.nsmap
        tree = self.tree
        self.lod = 0

        # 面リスト
        face_list = []

        # scan cityObjectMember
        buildings = tree.xpath("/core:CityModel/core:cityObjectMember/bldg:Building", namespaces=nsmap)
        for building in buildings:
            # bldg:lod0RoofEdge
            faces = building.xpath(
                "bldg:lod0RoofEdge/gml:MultiSurface/gml:surfaceMember/gml:Polygon/gml:exterior/gml:LinearRing/gml:posList",
                namespaces=nsmap,
            )

            # メッシュデータの建物を分割しない and subset ==　PLY
            if (not self.separate) and (self.subset == Subset.PLY):
                face_list.extend(faces)
            else:
                self.set_building_object(building, faces)

        # メッシュデータの全建物をまとめる？ and Subset.PLY ?
        if len(face_list):
            building = buildings[0]
            self.set_building_object(building, face_list)

    def lod1(self):
        nsmap = self.root.nsmap
        tree = self.tree
        self.lod = 1

        # 面リスト
        face_list = []

        # scan cityObjectMember
        buildings = tree.xpath("/core:CityModel/core:cityObjectMember/bldg:Building", namespaces=nsmap)
        for building in buildings:
            # bldg:lod1Solid
            faces = building.xpath(
                "bldg:lod1Solid/gml:Solid/gml:exterior/gml:CompositeSurface/gml:surfaceMember/gml:Polygon/gml:exterior/gml:LinearRing/gml:posList",
                namespaces=nsmap,
            )

            # メッシュデータの建物を分割しない and subset ==　PLY
            if (not self.separate) and (self.subset == Subset.PLY):
                face_list.extend(faces)
            else:
                self.set_building_object(building, faces)

        # メッシュデータの全建物をまとめる？ and Subset.PLY ?
        if len(face_list):
            building = buildings[0]
            self.set_building_object(building, face_list)

    def lod2(self):
        nsmap = self.root.nsmap
        tree = self.tree
        self.lod = 2

        # 面リスト
        face_list = []

        # scan cityObjectMember
        buildings = tree.xpath("/core:CityModel/core:cityObjectMember/bldg:Building", namespaces=nsmap)
        for building in buildings:
            # bldg:GroundSurface, bldg:RoofSurface, bldg:RoofSurface
            polygon_xpaths = [
                "bldg:boundedBy/bldg:GroundSurface/bldg:lod2MultiSurface/gml:MultiSurface/gml:surfaceMember/gml:Polygon",
                "bldg:boundedBy/bldg:RoofSurface/bldg:lod2MultiSurface/gml:MultiSurface/gml:surfaceMember/gml:Polygon",
                "bldg:boundedBy/bldg:WallSurface/bldg:lod2MultiSurface/gml:MultiSurface/gml:surfaceMember/gml:Polygon",
            ]
            faces = []
            poly_ids = []
            polys = []

            for polygon_xpath in polygon_xpaths:
                poslist_xpaths = building.xpath(polygon_xpath, namespaces=nsmap)
                for poslist_xpath in poslist_xpaths:
                    poly_id = poslist_xpath.attrib["{%s}id" % nsmap["gml"]]
                    poly_ids.append(poly_id)

                    vals = poslist_xpath.xpath("gml:exterior/gml:LinearRing/gml:posList", namespaces=nsmap)
                    faces.extend(vals)

                    # ポリゴンのオブジェクトを作成
                    poly = BuildingPolygon(vals, poly_id)
                    polys.append(poly)

            # メッシュデータの建物を分割しない and subset ==　PLY
            if (not self.separate) and (self.subset == Subset.PLY):
                face_list.extend(faces)
            else:
                self.set_building_object(building, faces)

        # メッシュデータの全建物をまとめる？ and Subset.PLY ?
        if len(face_list):
            building = buildings[0]
            self.set_building_object(building, face_list)

    def write_file(self, output_path):
        """ファイル作成"""
        if self.subset == Subset.PLY:
            self.write_ply(output_path)
        elif self.subset == Subset.GEOJSON:
            self.write_geojson(output_path)
        else:
            raise Exception(f"ERROR: subset = {self.subset}")

    def write_ply(self, output_path):
        """PLYファイル作成"""
        os.makedirs(output_path, exist_ok=True)
        if self.separate:  # メッシュデータの建物を分割する
            for index, obj_building in enumerate(self.obj_buildings):
                triangle_mesh = obj_building.get_triangle_mesh()
                pathname = os.path.join(
                    output_path,
                    f"{self.mesh_code}_{self.object_name}_{self.to_srid}_lod{self.lod}_{index:02}.ply",
                )
                o3d.io.write_triangle_mesh(pathname, triangle_mesh, write_ascii=True)
        else:  # メッシュデータの全建物をまとめる
            triangle_mesh = self.obj_buildings[0].get_triangle_mesh()
            pathname = os.path.join(
                output_path,
                f"{self.mesh_code}_{self.object_name}_{self.to_srid}_lod{self.lod}.ply",
            )
            o3d.io.write_triangle_mesh(pathname, triangle_mesh, write_ascii=True)

    def write_geojson(self, output_path):
        """GeoJSONファイル作成"""
        os.makedirs(output_path, exist_ok=True)
        buildings = []
        for index, obj_building in enumerate(self.obj_buildings):
            # create geometry
            polygons = [Polygon(row) for row in obj_building.get_vertices()]
            building_data = obj_building.get_properties()
            building_data["geometry"] = MultiPolygon(polygons)

            # add properties
            building_data["filename"] = os.path.basename(self.filename)
            building_data["mesh_code"] = self.mesh_code
            building_data["object"] = self.object_name

            if self.separate:  # 建物を分割する
                # save GeoJSON by geopandas
                gdf_data = gpd.GeoDataFrame([building_data], crs=f"EPSG:{self.to_srid}")
                pathname = os.path.join(
                    output_path, f"{self.mesh_code}_{self.object_name}_{self.to_srid}_lod{self.lod}_{index:02}.geojson"
                )
                gdf_data.to_file(pathname, driver="GeoJSON")
            else:  # 全建物をまとめる
                buildings.append(building_data)

        if not self.separate:  # 全建物をまとめる
            # save GeoJSON by geopandas
            gdf_data = gpd.GeoDataFrame(buildings, crs=f"EPSG:{self.to_srid}")
            pathname = os.path.join(
                output_path, f"{self.mesh_code}_{self.object_name}_{self.to_srid}_lod{self.lod}.geojson"
            )
            gdf_data.to_file(pathname, driver="GeoJSON")
