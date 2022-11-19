import os
from pathlib import Path

import numpy as np

from py_plateau.city_gml import CityGml, Subset

DATA = "data"
OUTPUT = "output"
ANSWER = "answer"


def test_get_textures():
    # ベースディレクトリ
    basedir = Path(os.path.dirname(os.path.abspath(__file__)))
    pathname = os.path.join(basedir, DATA, "53392633_bldg_6697_2_op.gml")

    # 実行
    obj_city_gml = CityGml(pathname, Subset.PLY, "6677")
    textures = obj_city_gml.get_textures()

    # テクスチャ画像の数を確認
    num_of_images = len(textures)
    assert num_of_images == 10

    # 先頭の要素の画像のファイルパス・id・UV座標を確認
    first_image_uri = "53392633_bldg_6697_appearance/hnap0668.jpg"
    first_poly_id = "poly_HNAP0668_p4761_3"
    first_uv_coords = [
        [0.3808012, 0.3736107],
        [0.3808012, 0.5503924],
        [0.2627451, 0.5503924],
        [0.2627451, 0.3736107],
        [0.3808012, 0.3736107],
    ]

    first_texture = textures[0]

    assert first_texture.image_uri == first_image_uri
    assert list(first_texture.uv_coords.keys())[0] == first_poly_id
    assert np.allclose(first_texture.uv_coords[first_poly_id], first_uv_coords)

    # 最後の要素の画像のファイルパス・id・UV座標を確認
    last_image_uri = "53392633_bldg_6697_appearance/hnap0697.jpg"
    last_poly_id = "poly_HNAP0697_p4760_1"
    last_uv_coords = [
        [0.7234043, 0.6249189],
        [0.9878542, 0.6249189],
        [0.9878542, 1],
        [0.7234043, 1],
        [0.7234043, 0.6249189],
    ]

    last_texture = textures[-1]

    assert last_texture.image_uri == last_image_uri
    assert list(last_texture.uv_coords.keys())[-1] == last_poly_id
    assert np.allclose(last_texture.uv_coords[last_poly_id], last_uv_coords)
