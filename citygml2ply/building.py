#!/usr/bin/env python
# coding: utf-8

import numpy as np
import open3d as o3d
import pyproj

from contrib.earcutpython.earcut.earcut import earcut


class Building:
    """ bldg:Building"""

    def __init__(self, from_srid="6697", to_srid="6677"):
        # super().__init__()
        self.polygons = []

        self.vertices = []
        self.triangles = []
        self.triangle_meshes = []

        # pyproj.Transformer.from_crs(<変換元座標系>, <変換先座標系> [, always_xy])
        self.transformer = pyproj.Transformer.from_crs(f"epsg:{from_srid}", f"epsg:{to_srid}")

    def get_triangle_mesh(self):
        return self.triangle_meshes

    def transform_coordinate(self, latitude, longitude, height):
        xx, yy, zz = self.transformer.transform(latitude, longitude, height)
        return np.array([xx, yy, zz])

    def create_triangle_meshes(self, polygons):
        for plist in polygons:
            vertices = [self.transform_coordinate(*x) for x in plist]
            vertices_earcut = earcut(np.array(vertices).flatten(), dim=3)
            if len(vertices_earcut) > 0:
                vertices_length = len(self.vertices)
                self.vertices.extend(vertices)
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
