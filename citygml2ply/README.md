[![Python 3](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/) 

citygml2ply
---
CityGMLYファイル → PLYファイル変換 

### Features
- CityGMLファイル -> PLYファイル変換
- 建物(bldg)のみ対応
- LOD0, LOD1, LOD2対応
- テクスチャは非対応

※1 LOD2のテクスチャは対応は、次バージョンで対応予定

### Usage
```
$ cd citygml2ply
$ python main.py -h

usage: main.py [-h] [-output OUTPUT] -to_srid TO_SRID [-lod LOD] filename

CityGML to PLY convert

positional arguments:
  filename              input CityGML filename

optional arguments:
  -h, --help            show this help message and exit
  -output OUTPUT, --output OUTPUT
                        output path name
  -to_srid TO_SRID, --to_srid TO_SRID
                        SRID(EPSG)
  -lod LOD, --lod LOD   output lod type 0:lod0 1:lod1 2:lod2
```

### Examples
```
$ python main.py 53392633_bldg_6697_2_op.gml --lod=2 --to_srid=6677
```

出力ディレクトリ: ./output


### Tests
[3D都市モデル（Project PLATEAU）東京都23区](https://www.geospatial.jp/ckan/dataset/plateau-tokyo23ku)のCityGMLの東京都大田区羽田空港三丁目データ ”53392633_bldg_6697_2_op.gml” のみで動作確認

### Modules
下記のモジュールを参考、使用しています。
各々のライセンスに従ってください。

