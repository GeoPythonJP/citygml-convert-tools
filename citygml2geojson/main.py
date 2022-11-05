#!/usr/bin/env python
# coding: utf-8

import traceback
import os
import argparse

from city_gml import CityGml


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='CityGML to GeoJSON convert')

        parser.add_argument('filename', help='input CityGML filename')
        parser.add_argument('-output', '--output', default="output", help='output path name')
        parser.add_argument('-to_srid', '--to_srid', default="4326", help='SRID(EPSG)')
        parser.add_argument('-lod', '--lod', default=2, type=int, help='output lod type 0:lod0 1:lod1 2:lod2')
        parser.add_argument('-lonlat', '--lonlat', default=True, action='store_true', help='swap longitude,latitude order')

        args = parser.parse_args()

        filename = args.filename   # e.g. 53392633_bldg_6697_2_op
        output_path = args.output  # default = 'output'
        to_srid = args.to_srid     # defalt = '4326'
        lod = args.lod             # defalt = 2
        lonlat_f = args.lonlat     # defalt = True

        obj_city_gml = CityGml(filename, to_srid, lonlat_f)
        if lod == 0:
            obj_city_gml.lod0()
        elif lod == 1:
            obj_city_gml.lod1()
        elif lod == 2:
            obj_city_gml.lod2()
        else:
            raise Exception(f'ERROR: lod number = {lod}')

        os.makedirs(output_path, exist_ok=True)
        obj_city_gml.write_geojson(output_path)

    except Exception as e:
        print(e)
        traceback.print_exc()
