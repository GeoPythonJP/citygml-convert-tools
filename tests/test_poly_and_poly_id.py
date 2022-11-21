import os
from pathlib import Path

from py_plateau.city_gml import CityGml, Subset

DATA = "data"
OUTPUT = "output"
ANSWER = "answer"


def _make_city_gml_instance():
    """Make CityGml instance"""
    basedir = Path(os.path.dirname(os.path.abspath(__file__)))
    pathname = os.path.join(basedir, DATA, "53392633_bldg_6697_2_op.gml")
    obj_city_gml = CityGml(pathname, Subset.PLY, "6677")
    return obj_city_gml


def test_compare_polygon_and_id_from_first_element():
    """Whether polygon/id pairs are correct or not"""
    # CityGmlのインスタンスを生成
    obj_city_gml = _make_city_gml_instance()
    obj_city_gml.lod2()

    # 最初の要素を取得
    buildings = obj_city_gml.obj_buildings
    target = buildings[0]
    first_poly = target.polygons[0]
    first_poly_id = first_poly.poly_id
    first_vertices = first_poly.vertices.text

    test_vertices = "35.533096948566886 139.7963519674318 3.66410811 35.53309215110142 139.79634196185296 3.66408749 35.53312183726169 139.79632067879015 3.6635608 35.53312663453339 139.79633068408438 3.66358141 35.53314158466162 139.79631996558618 3.66331703 35.533175221159944 139.7963901364649 3.66346657 35.533160279972336 139.79640085582636 3.66373085 35.53316408451471 139.7964087906811 3.66374829 35.53313440429897 139.79643008508884 3.66427499 35.533130599460456 139.79642214971136 3.66425755 35.533115953337905 139.79643265736863 3.6645183 35.5330823072676 139.7963624645014 3.66436872 35.533096948566886 139.7963519674318 3.66410811"

    # ポリゴンのidが想定されるものかどうか比較
    assert first_poly_id == "poly_HNAP0664_b_0"
    # verticesが一致するか比較
    assert first_vertices == test_vertices
