#!/usr/bin/env python
# coding: utf-8

import os

import pytest
from pathlib import Path

from py_plateau.city_gml import CityGml, Subset

import filecmp

DATA = "data"
OUTPUT = "output"
ANSWER = "answer"


def test_geojson_lod0():
    """ GeoJSON LOD0 """
    # ベースディレクトリ
    basedir = Path(os.path.dirname(os.path.abspath(__file__)))
    pathname = os.path.join(basedir, DATA, "53392633_bldg_6697_2_op.gml")
    output_path_name = os.path.join(basedir, OUTPUT)

    obj_city_gml = CityGml(pathname, Subset.GEOJSON, "4326", True)
    obj_city_gml.lod0()
    obj_city_gml.write_file(output_path_name)

    output_answer_file = os.path.join(os.path.join(basedir, ANSWER), "53392633_bldg_4326_lod0.geojson")
    output_file = os.path.join(output_path_name, "53392633_bldg_4326_lod0.geojson")

    assert filecmp.cmp(output_answer_file, output_file)


def test_geojson_lod1():
    """ GeoJSON LOD1 """
    # ベースディレクトリ
    basedir = Path(os.path.dirname(os.path.abspath(__file__)))
    pathname = os.path.join(basedir, DATA, "53392633_bldg_6697_2_op.gml")
    output_path_name = os.path.join(basedir, OUTPUT)

    obj_city_gml = CityGml(pathname, Subset.GEOJSON, "4326", True)
    obj_city_gml.lod1()
    obj_city_gml.write_file(output_path_name)

    output_answer_file = os.path.join(os.path.join(basedir, ANSWER), "53392633_bldg_4326_lod1.geojson")
    output_file = os.path.join(output_path_name, "53392633_bldg_4326_lod1.geojson")

    assert filecmp.cmp(output_answer_file, output_file)


def test_geojson_lod2():
    """ GeoJSON LOD1 """
    # ベースディレクトリ
    basedir = Path(os.path.dirname(os.path.abspath(__file__)))
    pathname = os.path.join(basedir, DATA, "53392633_bldg_6697_2_op.gml")
    output_path_name = os.path.join(basedir, OUTPUT)

    obj_city_gml = CityGml(pathname, Subset.GEOJSON, "4326", True)
    obj_city_gml.lod2()
    obj_city_gml.write_file(output_path_name)

    output_answer_file = os.path.join(os.path.join(basedir, ANSWER), "53392633_bldg_4326_lod2.geojson")
    output_file = os.path.join(output_path_name, "53392633_bldg_4326_lod2.geojson")

    assert filecmp.cmp(output_answer_file, output_file)