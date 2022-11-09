#!/usr/bin/env python
# coding: utf-8

import math

import numpy as np
import open3d as o3d
import pyproj

from contrib.earcutpython.earcut.earcut import earcut


class Building:
    """bldg:Building"""

    def __init__(self, from_srid="6697", to_srid="6677"):
        # super().__init__()
        self.polygons = []

        self.vertices = []
        self.triangles = []
        self.triangle_meshes = []

        # pyproj.Transformer.from_crs(<変換元座標系>, <変換先座標系> [, always_xy])
        self.transformer = pyproj.Transformer.from_crs(
            f"epsg:{from_srid}", f"epsg:{to_srid}"
        )

    def get_triangle_mesh(self):
        return self.triangle_meshes

    def transform_coordinate(self, latitude, longitude, height):
        xx, yy, zz = self.transformer.transform(latitude, longitude, height)
        return np.array([xx, yy, zz])

    def create_triangle_meshes(self, polygons):
        for poly in polygons:
            transformed_polygon = [self.transform_coordinate(*x) for x in poly]
            transformed_polygon = np.array(transformed_polygon)

            normal = self.get_normal_newell(transformed_polygon)[0]
            poly_2d = np.zeros((transformed_polygon.shape[0], 2))
            for i, vertex in enumerate(transformed_polygon):
                xy = self.to_2d(vertex, normal)
                poly_2d[i] = xy

            vertices_earcut = earcut(np.array(poly_2d, dtype=np.int).flatten(), dim=2)

            if len(vertices_earcut) > 0:
                vertices_length = len(self.vertices)
                self.vertices.extend(transformed_polygon)
                triangles = np.array(vertices_earcut).reshape((-1, 3))
                triangles_offset = triangles + vertices_length
                self.triangles.extend(triangles_offset)

        # create triangle mesh by Open3D
        triangle_meshes = o3d.geometry.TriangleMesh()
        triangle_meshes.vertices = o3d.utility.Vector3dVector(self.vertices)
        triangle_meshes.triangles = o3d.utility.Vector3iVector(self.triangles)

        # 法線の取得
        triangle_meshes.compute_vertex_normals()

        self.triangle_meshes = triangle_meshes
        self.polygons = polygons

    # 3つ以上の点を渡して、ポリゴンの法線を求める
    def get_normal_newell(self, poly):
        n = np.array([0.0, 0.0, 0.0], dtype=np.float64)

        for i, p in enumerate(poly):
            ne = i + 1
            if ne == len(poly):
                ne = 0
            n[0] += (poly[i][1] - poly[ne][1]) * (poly[i][2] + poly[ne][2])
            n[1] += (poly[i][2] - poly[ne][2]) * (poly[i][0] + poly[ne][0])
            n[2] += (poly[i][0] - poly[ne][0]) * (poly[i][1] + poly[ne][1])

        if (n == np.array([0.0, 0.0, 0.0])).all():
            return (n, False)
        n = n / math.sqrt(n[0] * n[0] + n[1] * n[1] + n[2] * n[2])
        return (n, True)

    # 面と法線を渡して、2次元の座標に変換する
    def to_2d(self, p, n):
        x3 = np.array([1.1, 1.1, 1.1])
        if (n == x3).all():
            x3 += np.array([1, 2, 3])
        x3 = x3 - np.dot(x3, n) * n

        x3 /= math.sqrt((x3**2).sum())
        y3 = np.cross(n, x3)
        return (np.dot(p, x3), np.dot(p, y3))
