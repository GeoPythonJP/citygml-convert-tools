#!/usr/bin/env python
# coding: utf-8

import numpy as np
import open3d as o3d
import pyproj


class Building:
    """ bldg:Building"""

    def __init__(self, from_srid="6697", to_srid="6677"):
        # super().__init__()
        self.polygons = []
        self.vertices = []

        # pyproj.Transformer.from_crs(<変換元座標系>, <変換先座標系> [, always_xy])
        self.transformer = pyproj.Transformer.from_crs(f"epsg:{from_srid}", f"epsg:{to_srid}")

    def get_vertices(self):
        return self.vertices

    def transform_coordinate(self, latitude, longitude, height):
        xx, yy, zz = self.transformer.transform(latitude, longitude, height)
        return np.array([xx, yy, zz])

    def create_vertices(self, polygons):
        for plist in polygons:
            vertices = [self.transform_coordinate(*x) for x in plist]
            if len(vertices) > 0:
                self.vertices.extend(vertices)

        self.polygons = polygons
