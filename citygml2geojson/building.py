#!/usr/bin/env python
# coding: utf-8

import pyproj


class Building:
    """ bldg:Building"""

    def __init__(self, from_srid="6697", to_srid="4326", lonlat_f=False):
        # super().__init__()
        self.polygons = []
        self.vertices = []

        # pyproj.Transformer.from_crs(<変換元座標系>, <変換先座標系> [, always_xy])
        self.transformer = pyproj.Transformer.from_crs(f"epsg:{from_srid}", f"epsg:{to_srid}")
        self.lonlat_f = lonlat_f

        self.properties = None

    def get_properties(self):
        return self.properties

    def set_properties(self, properties):
        self.properties = properties

    def get_vertices(self):
        return self.vertices

    def transform_coordinate(self, latitude, longitude, height):
        xx, yy, zz = self.transformer.transform(latitude, longitude, height)
        if self.lonlat_f:
            return [yy, xx, zz]
        else:
            return [xx, yy, zz]

    def create_vertices(self, polygons):
        self.polygons = polygons
        self.vertices = []

        for plist in polygons:
            vertices = [self.transform_coordinate(*x) for x in plist]
            if len(vertices) > 0:
                self.vertices.append(vertices)
