#!/usr/bin/env python
# coding: utf-8

import traceback
import os
import argparse

from city_gml import CityGml


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='citygml-convert-tools')

        parser.add_argument('filename', help='input CityGML filename')
        parser.add_argument('-to_srid', '--to_srid', default="6677", required=True, help='to SRID')
        parser.add_argument('-lod', '--lod', default=2, type=int, help='output lod type 0:lod0 1:lod1 2:lod2')

        args = parser.parse_args()

        filename = args.filename   # 'data/53392633_bldg_6697_2_op.gml'
        to_srid = args.to_srid     # '6677'
        lod = args.lod             # 2

        obj_city_gml = CityGml(filename, to_srid)
        if lod == 0:
            obj_city_gml.lod0()
        elif lod == 1:
            obj_city_gml.lod1()
        elif lod == 2:
            obj_city_gml.lod2()
        else:
            raise Exception(f'ERROR: lod number = {lod}')

        outpath = "output"
        os.makedirs(outpath, exist_ok=True)
        obj_city_gml.write_geojson(outpath)

    except Exception as e:
        print(e)
        traceback.print_exc()
