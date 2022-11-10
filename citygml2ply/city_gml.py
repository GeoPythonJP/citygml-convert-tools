#!/usr/bin/env python
# coding: utf-8

import os
import numpy as np
from lxml import etree
import open3d as o3d
from pathlib import Path

from building import Building


def str2floats(x):
    """ x y z -> [x, y, z] """
    return np.array([float(i) for i in x.text.split(' ')])


class CityGml:
    """ core:CityGml """

    def __init__(self, filename, to_srid="6677"):
        # filename
        self.filename = filename
        self.basename = os.path.splitext(os.path.basename(filename))[0]

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

    def lod0(self):
        nsmap = self.root.nsmap
        tree = self.tree

        # scan cityObjectMember
        buildings = tree.xpath('/core:CityModel/core:cityObjectMember/bldg:Building', namespaces=nsmap)
        for building in buildings:
            obj_building = Building(self.from_srid, self.to_srid)

            # bldg:lod0RoofEdge
            faces = building.xpath('bldg:lod0RoofEdge/gml:MultiSurface/gml:surfaceMember/gml:Polygon/gml:exterior/gml:LinearRing/gml:posList', namespaces=nsmap)
            polygons = [str2floats(face_str).reshape((-1, 3)) for face_str in faces]
            obj_building.create_triangle_meshes(polygons)
            self.obj_buildings.append(obj_building)

    def lod1(self):
        nsmap = self.root.nsmap
        tree = self.tree

        # scan cityObjectMember
        buildings = tree.xpath('/core:CityModel/core:cityObjectMember/bldg:Building', namespaces=nsmap)
        for building in buildings:
            obj_building = Building(self.from_srid, self.to_srid)

            # bldg:lod1Solid
            faces = building.xpath('bldg:lod1Solid/gml:Solid/gml:exterior/gml:CompositeSurface/gml:surfaceMember/gml:Polygon/gml:exterior/gml:LinearRing/gml:posList', namespaces=nsmap)
            polygons = [str2floats(face_str).reshape((-1, 3)) for face_str in faces]
            obj_building.create_triangle_meshes(polygons)
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
            vals_list = []
            for polygon_xpath in polygon_xpaths:
                poslist_xpaths = building.xpath(polygon_xpath, namespaces=nsmap)
                for poslist_xpath in poslist_xpaths:
                    vals = poslist_xpath.xpath('gml:exterior/gml:LinearRing/gml:posList', namespaces=nsmap)
                    vals_list.extend(vals)

            polygons = [str2floats(v).reshape((-1, 3)) for v in vals_list]
            obj_building.create_triangle_meshes(polygons)
            self.obj_buildings.append(obj_building)

    def write_ply(self, output_path):
        basedir = Path(os.path.dirname(os.path.abspath(__file__)))
        for index, obj_building in enumerate(self.obj_buildings):
            triangle_mesh = obj_building.get_triangle_mesh()
            pathname = os.path.join(basedir, output_path, f"{self.mesh_code}_{self.object_name}_{self.to_srid}_{index:02}.ply")
            o3d.io.write_triangle_mesh(pathname, triangle_mesh, write_ascii=True)
