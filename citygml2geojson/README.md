[![Python 3](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/) 

citygml2geojson 
---
CityGMLファイル -> GeoJSONファイル変換

### Features
- 建物(bldg)のみ対応
- LOD0, LOD1, LOD2対応
- [緯度経度]、[経度緯度]の変換対応

※1 2D座標系に変換する場合も3D座標で[longitude, latitude, height]に変換します  

### Usage
```
$ cd citygml2geojson
$ python main.py -h

usage: main.py [-h] [-output OUTPUT] [-to_srid TO_SRID] [-lod LOD] [-lonlat] filename

CityGML to GeoJSON convert

positional arguments:
  filename              input CityGML filename

optional arguments:
  -h, --help            show this help message and exit
  -output OUTPUT, --output OUTPUT
                        output path name
  -to_srid TO_SRID, --to_srid TO_SRID
                        SRID(EPSG)
  -lod LOD, --lod LOD   output lod type 0:lod0 1:lod1 2:lod2
  -lonlat, --lonlat     swap longitude,latitude order
```

### Examples
```
$ python main.py 53392633_bldg_6697_2_op.gml
```

### Tests
[3D都市モデル（Project PLATEAU）東京都23区](https://www.geospatial.jp/ckan/dataset/plateau-tokyo23ku)のCityGMLの東京都大田区羽田空港三丁目データ ”53392633_bldg_6697_2_op.gml” のみで動作確認

### Modules
下記のモジュールを参考、使用しています。
各々のライセンスに従ってください。
