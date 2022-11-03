citygml-convert-tools
===

CityGMLとは
---
"""
CityGML は、都市スケールの分析・シミュレーションに必要なセマンティクスを記述できる地理空間データのための唯一の標準データフォーマットである。諸外国では国家・都市レベルでのデータ整備が進められているが、日本における大規模なデータ整備は今回が初の試みである。

CityGML は、都市に存在する建物や街路、橋梁などのオブジェクトを地物として定義し、形状や名称、種類、建築年といったオブジェクトについての空間・時間・主題に係る全ての情報を地物の属性として定義している。この厳密性の高さにより、誰が作った3D都市モデルであっても、どの場所の3D都市モデルであっても、一貫性のあるデータ構造となる。
"""
https://www.mlit.go.jp/plateau/learning/

インストール
---
```
$ git clone --recursive git@github.com:GeoPythonJP/citygml-convert-tools.git
$ poetry install
$ poetry shell
```

CityGML 変換ツール
---
コードは出来るだけシンプルにしたかったので、サンプルとしてバッサリと簡潔にしてます。  
参考にしていただければ幸いです  
※ LOD2のテクスチャは対応は、次バージョンで対応予定

1. citygml2ply
  - CityGML -> PLYファイル変換
  - 建物(bldg)のみ対応
  - LOD0, LOD1, LOD2対応
  - テクスチャは非対応

2. citygml2geojson
  - CityGML -> GeoJSONファイル変換
  - 建物(bldg)のみ対応
  - LOD0, LOD1, LOD2対応
  - テクスチャは非対応

### usage 
```
$ cd citygml2ply
$ python main.py -h
usage: main.py [-h] -to_srid TO_SRID [-lod LOD] filename

citygml-convert-tools

positional arguments:
  filename              input CityGML filename

optional arguments:
  -h, --help            show this help message and exit
  -to_srid TO_SRID, --to_srid TO_SRID
                        to SRID
  -lod LOD, --lod LOD   output lod type 0:lod0 1:lod1 2:lod2
```

実行例
```
$ python main.py 53392633_bldg_6697_2_op.gml --lod=2 --to_srid=6677
```

出力ディレクトリ: ./output


### ライブラリ

#### 単調多角形を三角形分割する手法(耳刈り取り法)

```
$ git submodule add https://github.com/joshuaskelly/earcut-python.git citygml2ply/contrib/earcutpython
```

### ライセンス
下記のライセンスで公開をしてます。
* [MIT License](https://github.com/GeoPythonJP/citygml-convert-tools/blob/master/LICENSE)

下記のモジュールを参考、使用しています。
各々のライセンスに従ってください。

* [earcut-python](https://github.com/joshuaskelly/earcut-python)
* [AcculusSasao/plateaupy](https://github.com/AcculusSasao/plateaupy)
* [ksasao/PlateauCityGmlSharp](https://github.com/ksasao/PlateauCityGmlSharp/)

### CityGMLビューワー
* Windows版
    * [FZKViewer](https://www.iai.kit.edu/1302.php)
        * [FZKViewer のインストール（Windows 上）](https://www.kkaneko.jp/tools/win/fzkviewer.html)
* Mac版
    * [azul](https://github.com/tudelft3d/azul)

### 座標系のメモ

#### CityGMLの座標系
* 日本測地系2011における経緯度座標系と東京湾平均海面を基準とする標高の複合座標参照系: 6697
* 日本測地系2011における経緯度座標系: 6668

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

---

PLATEAU関連情報
---
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

仕様と変換ツール類
---
* [CityGML](https://www.ogc.org/standards/citygml)
* [CityJSON](https://www.cityjson.org/)
* [FME](https://www.safe.com/fme/)
* [3dcitydb/3dcitydb](https://github.com/3dcitydb/3dcitydb)

---

参考
---

#### OpenStreetMap
* [JA:MLIT PLATEAU/imports outline](https://wiki.openstreetmap.org/wiki/JA:MLIT_PLATEAU/imports_outline)
  * [議論：JA talk:MLIT PLATEAU/imports outline](https://wiki.openstreetmap.org/wiki/JA_talk:MLIT_PLATEAU/imports_outline#既存データを編集していたマッパーへの、OSMメッセージ連絡の要否)
* [JA talk:MLIT PLATEAU](https://wiki.openstreetmap.org/wiki/JA_talk:MLIT_PLATEAU)
  * [citygml-osm](https://github.com/yuuhayashi/citygml-osm)
    * [citygml-osm wiki](https://github.com/yuuhayashi/citygml-osm/wiki/Transformation)
* [Plateau建物データ: OpenStreetMapへのインポート手順（ドラフト）](https://qiita.com/nyampire/items/1c10afdd36750c87154d)

便利な編集ツール
---
* [CloudCompare](https://cloudcompare.org/)
* [Meshlab](https://www.meshlab.net/)
* [Blender.jp](https://blender.jp/)
