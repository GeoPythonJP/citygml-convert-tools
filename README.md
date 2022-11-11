[![Python 3](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/) 

CityGML変換ツール (citygml-convert-tools)
===

[CityGML](https://www.mlit.go.jp/plateau/learning/)は、地理空間データのため標準データフォーマットです。
XMLベースで定義されているCityGMLは、中間データフォーマットと言われているように利用サイドが使いやすい形式に変換して利用することを想定されている。
手軽にCityGMLファイルを変換できるツールを作成した

コードは出来るだけシンプルにしたかったので、サンプルコードとしてバッサリとコードは簡潔にしてます。  
エラー処理やテスト等も省略している部分があります。何かの参考にしていただければ幸いです  

## Tools
* [citygml2ply](./citygml2ply/README.md) : CityGMLYファイル → PLYファイル変換 
* [citygml2geojson](./citygml2geojson/README.md): CityGMLYファイル → GeoJSONファイル変換

## Changelog
see the [changelog](./CHANGELOG.md).

Installation
---
Pythonと[poetry](https://python-poetry.org/)を利用します。

```
$ git clone --recursive git@github.com:GeoPythonJP/citygml-convert-tools.git
$ poetry install
$ poetry shell
```

License
---
MIT
See the[license](./LICENSE) document for the full text.

Modules
---
下記のモジュールを参考、使用しています。
各々のライセンスに従ってください。
* [earcut-python](https://github.com/joshuaskelly/earcut-python)
* [AcculusSasao/plateaupy](https://github.com/AcculusSasao/plateaupy)
* [ksasao/PlateauCityGmlSharp](https://github.com/ksasao/PlateauCityGmlSharp/)
* [cityjson/cjio](https://github.com/cityjson/cjio)


Contributors
---
| GitHub                                          | Twitter                                           | 
|-------------------------------------------------|---------------------------------------------------| 
| [homata](http://github.com/homata)              | [@homata](https://twitter.com/homata)             |
| [nokonoko1203](https://github.com/nokonoko1203) | [@nokonoko_1203](https://qiita.com/nokonoko_1203) |

CityGMLビューワー
---
CityGMLファイルを表示させる下記のツールがあります。

* Windows版
    * [FZKViewer](https://www.iai.kit.edu/1302.php)
        * [FZKViewer のインストール（Windows 上）](https://www.kkaneko.jp/tools/win/fzkviewer.html)
* Mac版
    * [azul](https://github.com/tudelft3d/azul)

座標系のメモ
---
座標系の変換等をする場合の参考情報を記述します

#### CityGMLの座標系
* 日本測地系2011における経緯度座標系と東京湾平均海面を基準とする標高の複合座標参照系: 6697
* 日本測地系2011における経緯度座標系: 6668

#### 日本の測地系
* [日本の測地系](https://www.gsi.go.jp/sokuchikijun/datum-main.html)
* [わかりやすい平面直角座標系](https://www.gsi.go.jp/sokuchikijun/jpc.html)

#### EPSG:6697
EPSG:6697というのは「JGD2011 + JGD2011 (vertical) height」という座標参照系でEPSG:6668（JGD2011）とEPSG:6695（JGD2011 (vertical) height）からなる座標系である

* [EPSG:6697](https://epsg.io/6697): JGD2011 + JGD2011 (vertical) height　緯度、経度、標高 (EPSG:6668+6695)
  * [EPSG:6668](https://epsg.io/6668): JGD2011　緯度、経度
  * [EPSG:6695](https://epsg.io/6695): JGD2011 (vertical) height　標高単位：m
* [EPSG:6666](https://epsg.io/6666):  JGD2011 地心直交座標系 (X, Y, Z) 地球中心のXYZ 単位：m

#### 日本測地系2011　平面直角座標系:6669-6687
```
系	EPSG (JGD2011)	区域
1	6669	長崎県、鹿児島県の一部
2	6670	福岡県、佐賀県、熊本県、大分県、宮崎県、鹿児島県の一部
3	6671	山口県、島根県、広島県
4	6672	香川県、愛媛県、徳島県、高知県
5	6673	兵庫県、鳥取県、岡山県
6	6674	京都府、大阪府、福井県、滋賀県、三重県、奈良県、和歌山県
7	6675	石川県、富山県、岐阜県、愛知県
8	6676	新潟県、長野県、山梨県、静岡県
9	6677	東京都の一部、福島県、栃木県、茨城県、埼玉県、千葉県、群馬県、神祭川県
10	6678	青森県、秋田県、山形県、岩手県、宮城県
11	6679	北海道の一部
12	6680	北海道の一部
13	6681	北海道の一部
14	6682	東京都の一部
15	6683	沖縄県の一部
16	6684	沖縄県の一部
17	6685	沖縄県の一部
18	6686	東京都の一部
19	6687	東京都の一部
```


PLATEAU関連情報
---
PLATEAU関連情報のメモ

* [Project PLATEAU](https://www.mlit.go.jp/plateau/)
    * [3D都市モデル標準製品仕様書（第2.3版）](https://www.mlit.go.jp/plateau/file/libraries/doc/plateau_doc_0001_ver02.pdf)
    * [3D都市モデル標準製品仕様書（第2.3版）(HTML)](https://www.mlit.go.jp/plateaudocument/)
    * [3D都市モデル整備のためのBIM活用マニュアル（第1.0版）](https://www.mlit.go.jp/plateau/file/libraries/doc/plateau_doc_0003_ver01.pdf)
    * [3D都市モデルのデータ変換マニュアル](https://www.mlit.go.jp/plateau/file/libraries/doc/plateau_doc_0007_ver01.pdf)
        * [3D都市モデルのデータ変換マニュアル](https://github.com/Project-PLATEAU/Data-Conversion-Manual-for-3D-City-Model)
    * [G空間情報センター](https://www.geospatial.jp/ckan/dataset/plateau)
    * [GitHub](https://github.com/Project-PLATEAU)
* [i－都市再生技術仕様（案）／i-UR Technical Materials](https://www.chisou.go.jp/tiiki/toshisaisei/itoshisaisei/iur/index.html)
* [東京都デジタルツイン実現プロジェクト](https://info.tokyo-digitaltwin.metro.tokyo.lg.jp/)
    * [CityJSONに変換するcitygml-toolsの日本語マニュアル](https://github.com/tokyo-digitaltwin/citygml-tools)
* [国土交通データプラットフォーム](https://www.mlit-data.jp/platform/)
* [スマートシティ官民連携プラットフォーム](https://www.mlit.go.jp/scpf/)

### 仕様と変換ツール類
* [CityGML](https://www.ogc.org/standards/citygml)
* [CityJSON](https://www.cityjson.org/)
* [FME](https://www.safe.com/fme/)
* [3dcitydb/3dcitydb](https://github.com/3dcitydb/3dcitydb)

### CityGML
* [CityGML 3.0のGML仕様のドラフト](https://www.ogc.org/standards/requests/257)

### i-UR
* i-UR1.4は名前空間及びXMLSchemaファイルの所在が変更されたことに伴い、i-UR1.5に改定されている (https://www.chisou.go.jp/tiiki/toshisaisei/itoshisaisei/iur)

### 3dcitydb
TBD

### CityJSON
TBD

### OpenStreetMap
* [JA:MLIT PLATEAU/imports outline](https://wiki.openstreetmap.org/wiki/JA:MLIT_PLATEAU/imports_outline)
  * [議論：JA talk:MLIT PLATEAU/imports outline](https://wiki.openstreetmap.org/wiki/JA_talk:MLIT_PLATEAU/imports_outline#既存データを編集していたマッパーへの、OSMメッセージ連絡の要否)
* [JA talk:MLIT PLATEAU](https://wiki.openstreetmap.org/wiki/JA_talk:MLIT_PLATEAU)
  * [citygml-osm](https://github.com/yuuhayashi/citygml-osm)
    * [citygml-osm wiki](https://github.com/yuuhayashi/citygml-osm/wiki/Transformation)
* [Plateau建物データ: OpenStreetMapへのインポート手順（ドラフト）](https://qiita.com/nyampire/items/1c10afdd36750c87154d)

### 便利なツール
* [CloudCompare](https://cloudcompare.org/)
* [Meshlab](https://www.meshlab.net/)
* [Blender.jp](https://blender.jp/)
* [Cesium](https://cesium.com/)
* [QGIS](https://qgis.org/)

### その他

関連情報のメモ
* [Geo関連情報のメモ](./GEOMEMO.md)

