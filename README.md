citygml-convert-tools
===

### インストール
```
$ git clone --recursive git@github.com:GeoPythonJP/citygml-convert-tools.git
$ poetry install
$ poetry shell
```

### CityGML 変換ツール
* citygml2ply
  - CityGML -> PLYファイル変換

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
$ python main.py data/53392633_bldg_6697_2_op.gml --to_srid=6677
```

出力ディレクトリ: citygml2ply/output


### ライブラリ

#### 単調多角形を三角形分割する手法(耳刈り取り法)
```
$ git submodule add https://github.com/joshuaskelly/earcut-python.git citygml2ply/contrib/earcutpython
```

### 参考コード
* [AcculusSasao/plateaupy](https://github.com/AcculusSasao/plateaupy)
* [ksasao/PlateauCityGmlSharp](https://github.com/ksasao/PlateauCityGmlSharp/)

### CitGMLビューワー
* Windows版
    * [FZKViewer](https://www.iai.kit.edu/1302.php)
        * [FZKViewer のインストール（Windows 上）](https://www.kkaneko.jp/tools/win/fzkviewer.html)
* Mac版
    * [azul](https://github.com/tudelft3d/azul)

### 座標系

#### CityGMLの座標系　緯度/経度:6697-6668
* 日本測地系2011における経緯度座標系と東京湾平均海面を基準とする標高の複合座標参照系 6697
* 日本測地系2011における経緯度座標系 6668

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
