#!/usr/bin/env python
# coding: utf-8

import os

import pytest
from pathlib import Path

from py_plateau.city_gml import CityGml, Subset

import filecmp
import glob

DATA = "data"
OUTPUT = "output"
ANSWER = "answer"


def test_ply_lod0():
    """ PLY LOD0 """
    # ベースディレクトリ
    basedir = Path(os.path.dirname(os.path.abspath(__file__)))
    pathname = os.path.join(basedir, DATA, "53392633_bldg_6697_2_op.gml")
    output_path_name = os.path.join(basedir, OUTPUT)

    # 実行
    obj_city_gml = CityGml(pathname, Subset.PLY, "6677")
    obj_city_gml.lod0()
    obj_city_gml.write_file(output_path_name)

    # 出力ファイル数
    target_path = os.path.join(basedir, OUTPUT, "53392633_bldg_6677_lod0_*.ply")
    files = glob.glob(target_path, recursive=True)
    length = len(files)
    assert length == 10

    # ファイル比較
    for index in range(length):
        output_answer_file = os.path.join(os.path.join(basedir, ANSWER), f"53392633_bldg_6677_lod0_{index:02}.ply")
        output_file = os.path.join(output_path_name, f"53392633_bldg_6677_lod0_{index:02}.ply")
        assert filecmp.cmp(output_answer_file, output_file)


def test_ply_lod1():
    """ PLY LOD1 """
    # ベースディレクトリ
    basedir = Path(os.path.dirname(os.path.abspath(__file__)))
    pathname = os.path.join(basedir, DATA, "53392633_bldg_6697_2_op.gml")
    output_path_name = os.path.join(basedir, OUTPUT)

    # 実行
    obj_city_gml = CityGml(pathname, Subset.PLY, "6677")
    obj_city_gml.lod1()
    obj_city_gml.write_file(output_path_name)

    # 出力ファイル数
    target_path = os.path.join(basedir, OUTPUT, "53392633_bldg_6677_lod1_*.ply")
    files = glob.glob(target_path, recursive=True)
    length = len(files)
    assert length == 10

    # ファイル比較
    for index in range(length):
        output_answer_file = os.path.join(os.path.join(basedir, ANSWER), f"53392633_bldg_6677_lod1_{index:02}.ply")
        output_file = os.path.join(output_path_name, f"53392633_bldg_6677_lod1_{index:02}.ply")
        assert filecmp.cmp(output_answer_file, output_file)


def test_ply_lod2():
    """ PLY LOD2 """
    # ベースディレクトリ
    basedir = Path(os.path.dirname(os.path.abspath(__file__)))
    pathname = os.path.join(basedir, DATA, "53392633_bldg_6697_2_op.gml")
    output_path_name = os.path.join(basedir, OUTPUT)

    # 実行
    obj_city_gml = CityGml(pathname, Subset.PLY, "6677")
    obj_city_gml.lod2()
    obj_city_gml.write_file(output_path_name)

    # 出力ファイル数
    target_path = os.path.join(basedir, OUTPUT, "53392633_bldg_6677_lod2_*.ply")
    files = glob.glob(target_path, recursive=True)
    length = len(files)
    assert length == 10

    # ファイル比較
    for index in range(length):
        output_answer_file = os.path.join(os.path.join(basedir, ANSWER), f"53392633_bldg_6677_lod2_{index:02}.ply")
        output_file = os.path.join(output_path_name, f"53392633_bldg_6677_lod2_{index:02}.ply")
        assert filecmp.cmp(output_answer_file, output_file)
