#!/usr/bin/env python
# coding: utf-8

import math
import pdb
from typing import Any, List

import numpy as np
import open3d as o3d
import pyproj

from .earcut import earcut


class BuildingTexture:
    """Building texture"""

    def __init__(self):
        self.image_uri = ""
        self.uv_coords = dict()

    def set_image_uri(self, image_uri):
        """Set image URI"""
        self.image_uri = image_uri

    def set_uv_coords(self, poly_id, uv_coords):
        """Set UV coordinates"""
        self.uv_coords[poly_id] = uv_coords

    def search_uv_coords(self, poly_id):
        """Search UV coordinates"""
        if poly_id in self.uv_coords:
            return self.uv_coords[poly_id]
        return None


class BuildingPolygon:
    """gml:Polygon"""

    def __init__(self, vertices, poly_id):
        # self.verticesはlxml.etree._Elementの要素
        self.vertices: Any = vertices
        self.poly_id: str = poly_id

    def _str2floats(self):
        """x y z -> [x, y, z]"""
        return np.array([float(i) for i in self.vertices.text.split(" ")])

    def get_coords(self):
        return self._str2floats().reshape((-1, 3))

    def check_poly_id(self, poly_id):
        """Check poly_id"""
        return self.poly_id == poly_id


class Building:
    """bldg:Building"""

    def __init__(self, from_srid="6697", to_srid="6677", lonlat=False):
        # super().__init__()
        self.polygons = []
        self.properties = None

        self.vertices = []
        self.triangles = []
        self.triangle_meshes = []
        self.textures = []

        self.lonlat = lonlat

        # pyproj.Transformer.from_crs(<変換元座標系>, <変換先座標系> [, always_xy])
        self.transformer = pyproj.Transformer.from_crs(f"epsg:{from_srid}", f"epsg:{to_srid}")

    def get_properties(self):
        return self.properties

    def set_properties(self, properties):
        self.properties = properties

    def set_textures(self, textures):
        self.textures = textures

    def get_vertices(self):
        return self.vertices

    def get_triangle_mesh(self):
        return self.triangle_meshes

    def transform_coordinate(self, latitude, longitude, height):
        xx, yy, zz = self.transformer.transform(latitude, longitude, height)
        if self.lonlat:
            return np.array([yy, xx, zz])
        else:
            return np.array([xx, yy, zz])

    def create_vertices(self, polygons):
        self.polygons = polygons
        self.vertices = []

        for plist in polygons:
            vertices = [self.transform_coordinate(*x) for x in plist.get_coords()]
            if len(vertices) > 0:
                self.vertices.append(vertices)

    def find_uv_coords(self, poly_id):
        """Find UV coordinates"""
        if self.textures:
            for texture in self.textures:
                uv_coords = texture.search_uv_coords(poly_id)
                if uv_coords:
                    return uv_coords
        return None

    def create_triangle_meshes(self, polygons: List[BuildingPolygon]):
        for poly in polygons:
            transformed_polygon = [self.transform_coordinate(*x) for x in poly.get_coords()]
            # CityGMLと法線計算時の頂点の取扱順序が異なるため、反転させる
            transformed_polygon = transformed_polygon[::-1]
            transformed_polygon = np.array(transformed_polygon)

            normal = self.get_normal(transformed_polygon)[0]
            poly_2d = np.zeros((transformed_polygon.shape[0], 2))
            for i, vertex in enumerate(transformed_polygon):
                xy = self.to_2d(vertex, normal)
                poly_2d[i] = xy

            vertices_earcut = earcut(np.array(poly_2d, dtype=np.int64).flatten(), dim=2)

            if len(vertices_earcut) > 0:
                vertices_length = len(self.vertices)
                self.vertices.extend(transformed_polygon)
                triangles = np.array(vertices_earcut).reshape((-1, 3))
                triangles_offset = triangles + vertices_length
                self.triangles.extend(triangles_offset)

            poly_id = poly.poly_id
            # 面に対応するUV座標があるかどうか探す
            uv_coords = self.find_uv_coords(poly_id)

        # create triangle mesh by Open3D
        triangle_meshes = o3d.geometry.TriangleMesh()
        triangle_meshes.vertices = o3d.utility.Vector3dVector(self.vertices)
        triangle_meshes.triangles = o3d.utility.Vector3iVector(self.triangles)

        # 法線の取得
        triangle_meshes.compute_vertex_normals()

        self.triangle_meshes = triangle_meshes
        self.polygons = polygons

    # 3つ以上の点を渡して、ポリゴンの法線を求める
    @staticmethod
    def get_normal(poly):
        normal = np.array([0.0, 0.0, 0.0], dtype=np.float64)

        for i, _ in enumerate(poly):
            next_index = i + 1

            if next_index == len(poly):
                next_index = 0

            point_1 = poly[i]
            point_1_x = point_1[0]
            point_1_y = point_1[1]
            point_1_z = point_1[2]

            point_2 = poly[next_index]
            point_2_x = point_2[0]
            point_2_y = point_2[1]
            point_2_z = point_2[2]

            normal[0] += (point_1_y - point_2_y) * (point_1_z + point_2_z)
            normal[1] += (point_1_z - point_2_z) * (point_1_x + point_2_x)
            normal[2] += (point_1_x - point_2_x) * (point_1_y + point_2_y)

        if (normal == np.array([0.0, 0.0, 0.0])).all():
            return (normal, False)

        normal = normal / math.sqrt(normal[0] * normal[0] + normal[1] * normal[1] + normal[2] * normal[2])
        return (normal, True)

    # 面と法線を渡して、2次元の座標に変換する
    @staticmethod
    def to_2d(p, n):
        x3 = np.array([1.1, 1.1, 1.1])

        if (n == x3).all():
            x3 += np.array([1, 2, 3])
        x3 = x3 - np.dot(x3, n) * n
        x3 /= math.sqrt((x3**2).sum())
        y3 = np.cross(n, x3)
        return (np.dot(p, x3), np.dot(p, y3))
