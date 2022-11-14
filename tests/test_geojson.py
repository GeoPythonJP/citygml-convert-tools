#!/usr/bin/env python
# coding: utf-8

import filecmp
import glob
import os
from pathlib import Path

import pytest

from py_plateau.city_gml import CityGml, Subset

DATA = "data"
OUTPUT = "output"
ANSWER = "answer"


def test_geojson_lod0():
    """GeoJSON LOD0"""
    # ベースディレクトリ
    basedir = Path(os.path.dirname(os.path.abspath(__file__)))
    pathname = os.path.join(basedir, DATA, "53392633_bldg_6697_2_op.gml")
    output_path_name = os.path.join(basedir, OUTPUT)

    # 実行
    obj_city_gml = CityGml(pathname, Subset.GEOJSON, "4326", lonlat=True)
    obj_city_gml.lod0()
    obj_city_gml.write_file(output_path_name)

    # ファイル比較
    output_answer_file = os.path.join(os.path.join(basedir, ANSWER), "53392633_bldg_4326_lod0.geojson")
    output_file = os.path.join(output_path_name, "53392633_bldg_4326_lod0.geojson")
    assert filecmp.cmp(output_answer_file, output_file)


def test_geojson_separate_lod0():
    """GeoJSON LOD0 (separate)"""
    # ベースディレクトリ
    basedir = Path(os.path.dirname(os.path.abspath(__file__)))
    pathname = os.path.join(basedir, DATA, "53392633_bldg_6697_2_op.gml")
    output_path_name = os.path.join(basedir, OUTPUT)

    # 実行
    obj_city_gml = CityGml(pathname, Subset.GEOJSON, "4326", separate=True, lonlat=True)
    obj_city_gml.lod0()
    obj_city_gml.write_file(output_path_name)

    # 出力ファイル数
    target_path = os.path.join(basedir, OUTPUT, "53392633_bldg_4326_lod0_*.geojson")
    files = glob.glob(target_path, recursive=True)
    length = len(files)
    assert length == 10

    # ファイル比較
    for index in range(length):
        output_answer_file = os.path.join(os.path.join(basedir, ANSWER), f"53392633_bldg_4326_lod0_{index:02}.geojson")
        output_file = os.path.join(output_path_name, f"53392633_bldg_4326_lod0_{index:02}.geojson")
        assert filecmp.cmp(output_answer_file, output_file)


def test_geojson_lod1():
    """GeoJSON LOD1"""
    # ベースディレクトリ
    basedir = Path(os.path.dirname(os.path.abspath(__file__)))
    pathname = os.path.join(basedir, DATA, "53392633_bldg_6697_2_op.gml")
    output_path_name = os.path.join(basedir, OUTPUT)

    # 実行
    obj_city_gml = CityGml(pathname, Subset.GEOJSON, "4326", lonlat=True)
    obj_city_gml.lod1()
    obj_city_gml.write_file(output_path_name)

    # ファイル比較
    output_answer_file = os.path.join(os.path.join(basedir, ANSWER), "53392633_bldg_4326_lod1.geojson")
    output_file = os.path.join(output_path_name, "53392633_bldg_4326_lod1.geojson")
    assert filecmp.cmp(output_answer_file, output_file)


def test_geojson_separate_lod1():
    """GeoJSON LOD1 (separate)"""
    # ベースディレクトリ
    basedir = Path(os.path.dirname(os.path.abspath(__file__)))
    pathname = os.path.join(basedir, DATA, "53392633_bldg_6697_2_op.gml")
    output_path_name = os.path.join(basedir, OUTPUT)

    # 実行
    obj_city_gml = CityGml(pathname, Subset.GEOJSON, "4326", separate=True, lonlat=True)
    obj_city_gml.lod1()
    obj_city_gml.write_file(output_path_name)

    # 出力ファイル数
    target_path = os.path.join(basedir, OUTPUT, "53392633_bldg_4326_lod1_*.geojson")
    files = glob.glob(target_path, recursive=True)
    length = len(files)
    assert length == 10

    # ファイル比較
    for index in range(length):
        output_answer_file = os.path.join(os.path.join(basedir, ANSWER), f"53392633_bldg_4326_lod1_{index:02}.geojson")
        output_file = os.path.join(output_path_name, f"53392633_bldg_4326_lod1_{index:02}.geojson")
        assert filecmp.cmp(output_answer_file, output_file)


def test_geojson_lod2():
    """GeoJSON LOD2"""
    # ベースディレクトリ
    basedir = Path(os.path.dirname(os.path.abspath(__file__)))
    pathname = os.path.join(basedir, DATA, "53392633_bldg_6697_2_op.gml")
    output_path_name = os.path.join(basedir, OUTPUT)

    # 実行
    obj_city_gml = CityGml(pathname, Subset.GEOJSON, "4326", lonlat=True)
    obj_city_gml.lod2()
    obj_city_gml.write_file(output_path_name)

    # ファイル比較
    output_answer_file = os.path.join(os.path.join(basedir, ANSWER), "53392633_bldg_4326_lod2.geojson")
    output_file = os.path.join(output_path_name, "53392633_bldg_4326_lod2.geojson")
    assert filecmp.cmp(output_answer_file, output_file)


def test_geojson_separate_lod2():
    """GeoJSON LOD2 (separate)"""
    # ベースディレクトリ
    basedir = Path(os.path.dirname(os.path.abspath(__file__)))
    pathname = os.path.join(basedir, DATA, "53392633_bldg_6697_2_op.gml")
    output_path_name = os.path.join(basedir, OUTPUT)

    # 実行
    obj_city_gml = CityGml(pathname, Subset.GEOJSON, "4326", separate=True, lonlat=True)
    obj_city_gml.lod2()
    obj_city_gml.write_file(output_path_name)

    # 出力ファイル数
    target_path = os.path.join(basedir, OUTPUT, "53392633_bldg_4326_lod2_*.geojson")
    files = glob.glob(target_path, recursive=True)
    length = len(files)
    assert length == 10

    # ファイル比較
    for index in range(length):
        output_answer_file = os.path.join(os.path.join(basedir, ANSWER), f"53392633_bldg_4326_lod2_{index:02}.geojson")
        output_file = os.path.join(output_path_name, f"53392633_bldg_4326_lod2_{index:02}.geojson")
        assert filecmp.cmp(output_answer_file, output_file)
