#!/usr/bin/env python
# coding: utf-8

import os
import numpy as np
import lxml
from lxml import etree
from pathlib import Path
import traceback

from building import Building
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon


def str2floats(x):
    """ x y z -> [x, y, z] """
    return np.array([float(i) for i in x.text.split(' ')])


class CityGml:
    """ core:CityGml """

    def __init__(self, filename, to_srid="4326", lonlat_f=False):
        # filename
        self.filename = filename
        self.basename = os.path.basename(filename)

        # split from basename
        basenames = self.basename.split('_')
        # メッシュコード
        self.mesh_code = basenames[0]
        # 地物型 (bldg)
        self.object_name = basenames[1]
        # CRS 空間参照 ID (SRID)
        self.from_srid = basenames[2]
        self.to_srid = to_srid

        # xml tree
        tree = etree.parse(filename)
        root = tree.getroot()
        self.tree = tree
        self.root = root

        # buildings
        self.obj_buildings = []
        self.lonlat_f = lonlat_f

    def get_bldg_properties(self, building, nsmap):
        properties = dict()
        try:
            # bldg:Building attribute=>gml:id
            attrib_id = "{%s}id" % nsmap['gml']
            if attrib_id in building.attrib:
                properties["id"] = building.attrib[attrib_id]

            # gen:stringAttribute
            string_attributes = building.xpath('gen:stringAttribute', namespaces=nsmap)
            for string_attribute in string_attributes:
                properties[string_attribute.attrib['name']] = string_attribute.getchildren()[0].text

            # bldg:measuredHeight
            measured_heights = building.xpath('bldg:measuredHeight', namespaces=nsmap)
            if len(measured_heights) > 0:
                properties["measured_height_uom"] = measured_heights[0].attrib["uom"]
                properties["measured_height"] = float(measured_heights[0].text)

            # bldg:address
            addresses = building.xpath('bldg:address/core:Address/core:xalAddress/xAL:AddressDetails/xAL:Country/xAL:Locality/xAL:LocalityName', namespaces=nsmap)
            if len(addresses) > 0:
                properties["address_type"] = addresses[0].attrib["Type"]
                properties["address"] = addresses[0].text
            else:
                properties["address_type"] = ""
                properties["address"] = ""

        except lxml.etree.XPathEvalError as e:
            print(e)
            traceback.print_exc()

        return properties

    def lod0(self):
        nsmap = self.root.nsmap
        tree = self.tree

        # scan cityObjectMember
        buildings = tree.xpath('/core:CityModel/core:cityObjectMember/bldg:Building', namespaces=nsmap)
        for building in buildings:
            obj_building = Building(self.from_srid, self.to_srid, self.lonlat_f)

            # set properties
            properties = self.get_bldg_properties(building, nsmap)
            obj_building.set_properties(properties)

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
            obj_building = Building(self.from_srid, self.to_srid, self.lonlat_f)

            # set properties
            properties = self.get_bldg_properties(building, nsmap)
            obj_building.set_properties(properties)

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
            obj_building = Building(self.from_srid, self.to_srid, self.lonlat_f)

            # set properties
            properties = self.get_bldg_properties(building, nsmap)
            obj_building.set_properties(properties)

            # bldg:GroundSurface, bldg:RoofSurface, bldg:RoofSurface
            polygon_xpaths = ['bldg:boundedBy/bldg:GroundSurface/bldg:lod2MultiSurface/gml:MultiSurface/gml:surfaceMember/gml:Polygon',
                              'bldg:boundedBy/bldg:RoofSurface/bldg:lod2MultiSurface/gml:MultiSurface/gml:surfaceMember/gml:Polygon',
                              'bldg:boundedBy/bldg:WallSurface/bldg:lod2MultiSurface/gml:MultiSurface/gml:surfaceMember/gml:Polygon']
            vals_list = []
            for polygon_xpath in polygon_xpaths:
                poslist_xpaths = building.xpath(polygon_xpath, namespaces=nsmap)
                for poslist_xpath in poslist_xpaths:
                    vals = poslist_xpath.xpath('gml:exterior/gml:LinearRing/gml:posList', namespaces=nsmap)
                    vals_list.extend(vals)

            polygons = [str2floats(v).reshape((-1, 3)) for v in vals_list]
            obj_building.create_vertices(polygons)
            self.obj_buildings.append(obj_building)

    def write_geojson(self, output_path):
        buildings = []
        for obj_building in self.obj_buildings:
            # create geometry
            polygons = [Polygon(row) for row in obj_building.get_vertices()]
            building_data = obj_building.get_properties()
            building_data["geometry"] = MultiPolygon(polygons)

            # add properties
            building_data["filename"] = self.basename
            building_data["mesh_code"] = self.mesh_code
            building_data["object"] = self.object_name

            buildings.append(building_data)

        # save GeoJSON by geopandas
        gdf_data = gpd.GeoDataFrame(buildings, crs=f"EPSG:{self.to_srid}")
        basedir = Path(os.path.dirname(os.path.abspath(__file__)))
        pathname = os.path.join(basedir, output_path, f"{self.mesh_code}_{self.object_name}_{self.to_srid}.geojson")
        gdf_data.to_file(pathname, driver="GeoJSON")
