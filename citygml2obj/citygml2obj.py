#!/usr/bin/env python
# coding: utf-8

import traceback

import xml.etree.ElementTree as ET

from city_model import CityModel


if __name__ == '__main__':
    try:
        # CityGML(XML)ファイルの読み込み
        tree = ET.parse('data/53392633_bldg_6697_2_op.gml')
        # ツリーを取得
        root_element = tree.getroot()
        # CityModelツリーを処理
        CityModel(root_element).execute()

    except Exception as e:
        print(e)
        traceback.print_exc()
