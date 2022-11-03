#!/usr/bin/env python
# coding: utf-8

import os
import numpy as np
from lxml import etree
from pathlib import Path

from building import Building

import pandas as pd
import geopandas as gpd
# Shapely: https://shapely.readthedocs.io/en/latest/index.html
from shapely import wkt
from shapely.geometry import Polygon


def str2floats(x):
    return np.array([float(i) for i in x.text.split(' ')])


class CityGml:
    """ core:CityGml """

    def __init__(self, filename, to_srid="6677"):
        # filename
        self.filename = filename
        self.basename = os.path.basename(filename)

        # basename
        basenames = self.mesh_code = self.basename.split('_')
        # メッシュコード
        self.mesh_code = basenames[0]
        # 地物型 (bldg)
        self.object_name = basenames[1]
        # CRS 空間参照 ID (SRID)
        self.from_srid = basenames[2]
        self.to_srid = to_srid

        # 空間参照 ID (SRID)
        self.from_srid = basenames[2]
        self.to_srid = to_srid

        # xml tree
        tree = etree.parse(filename)
        root = tree.getroot()
        self.tree = tree
        self.root = root

        # buildings
        self.obj_buildings = []

    def lod0(self):
        nsmap = self.root.nsmap
        tree = self.tree

        # scan cityObjectMember
        buildings = tree.xpath('/core:CityModel/core:cityObjectMember/bldg:Building', namespaces=nsmap)
        for building in buildings:
            obj_building = Building(self.from_srid, self.to_srid)

            # bldg:lod0RoofEdge
            vals = building.xpath('bldg:lod0RoofEdge/gml:MultiSurface/gml:surfaceMember/gml:Polygon/gml:exterior/gml:LinearRing/gml:posList', namespaces=nsmap)
            polygons = [str2floats(v).reshape((-1, 3)) for v in vals]
            obj_building.create_vertices(polygons)
            self.obj_buildings.append(obj_building)

    def lod1(self):
        nsmap = self.root.nsmap
        tree = self.tree

        # scan cityObjectMember
        buildings = tree.xpath('/core:CityModel/core:cityObjectMember/bldg:Building', namespaces=nsmap)
        for building in buildings:
            obj_building = Building(self.from_srid, self.to_srid)

            # bldg:lod1Solid
            vals = building.xpath('bldg:lod1Solid/gml:Solid/gml:exterior/gml:CompositeSurface/gml:surfaceMember/gml:Polygon/gml:exterior/gml:LinearRing/gml:posList', namespaces=nsmap)
            polygons = [str2floats(v).reshape((-1, 3)) for v in vals]
            obj_building.create_vertices(polygons)
            self.obj_buildings.append(obj_building)

    def lod2(self):
        nsmap = self.root.nsmap
        tree = self.tree

        # scan cityObjectMember
        buildings = tree.xpath('/core:CityModel/core:cityObjectMember/bldg:Building', namespaces=nsmap)
        for building in buildings:
            obj_building = Building(self.from_srid, self.to_srid)

            # bldg:GroundSurface, bldg:RoofSurface, bldg:RoofSurface
            polygon_xpaths = ['bldg:boundedBy/bldg:GroundSurface/bldg:lod2MultiSurface/gml:MultiSurface/gml:surfaceMember/gml:Polygon',
                              'bldg:boundedBy/bldg:RoofSurface/bldg:lod2MultiSurface/gml:MultiSurface/gml:surfaceMember/gml:Polygon',
                              'bldg:boundedBy/bldg:WallSurface/bldg:lod2MultiSurface/gml:MultiSurface/gml:surfaceMember/gml:Polygon']
            polygons = []
            for polygon_xpath in polygon_xpaths:
                building_xpaths = building.xpath(polygon_xpath, namespaces=nsmap)
                for building_xpath in building_xpaths:
                    vals = building_xpath.xpath('gml:exterior/gml:LinearRing/gml:posList', namespaces=nsmap)
                    surface = [str2floats(v).reshape((-1, 3)) for v in vals][0]
                    polygons.append(surface)

            obj_building.create_vertices(polygons)
            self.obj_buildings.append(obj_building)

    def write_geojson(self, outputpath):
        basedir = Path(os.path.dirname(os.path.abspath(__file__)))
        for index, obj_building in enumerate(self.obj_buildings):
            vertices = obj_building.get_vertices()
            polygon = Polygon(vertices)

            data = {}
            data["geometry"] = polygon

            data_list = []
            data_list.append(data)

            df_data = pd.DataFrame(data_list)
            gdf_data = gpd.GeoDataFrame(df_data, crs=f"EPSG:{self.to_srid}")

            pathname = os.path.join(basedir, outputpath, f"{self.mesh_code}_{self.object_name}_{self.to_srid}_{index:02}.geojson")
            gdf_data.to_file(pathname, driver="GeoJSON")