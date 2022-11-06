Geo関連情報のメモ
---
周辺のGeo関連情報のメモ

### 平面直角座標系変換

#### 市区町村名・緯度経度から平面直角座標系を取得するCLIツール
* [市区町村名・緯度経度から平面直角座標系の系番号を取得するツールを作成した！](https://qiita.com/nokonoko_1203/items/f8925081665cab3f36f0)
  * [MIERUNE/create_city_feather](https://github.com/MIERUNE/create_gpkg_for_city_boundaries)
  * [MIERUNE/search_zone_number](https://github.com/MIERUNE/search_zone_number)


### ファイルフォーマット
* [ESRI Shaplefile](https://www.esri.com/content/dam/esrisites/sitecore-archive/Files/Pdfs/library/whitepapers/pdfs/shapefile.pdf)
  * [Shaplefile](https://www.loc.gov/preservation/digital/formats/fdd/fdd000280.shtml)
* [GeoJSON - GeoJSON · GIS実習オープン教材](https://gis-oer.github.io/gitbook/book/materials/web_gis/GeoJSON/GeoJSON.html)
* [GeoPackage](https://www.geopackage.org/)
  * [opengeospatial/geopackage](https://github.com/opengeospatial/geopackage)
* [mapbox/geobuf](https://github.com/mapbox/geobuf
* [flatgeobuf / flatgeobuf](https://github.com/flatgeobuf/flatgeobuf)
* [GeoParquet](https://github.com/opengeospatial/geoparquet)
* [GeoTIFF](https://www.loc.gov/preservation/digital/formats/fdd/fdd000279.shtml)

#### 参考
* [GeoPandasをやるならFlatGeobufより10倍早いGeoParquetを使おう！](https://qiita.com/nokonoko_1203/items/a01168096c2d4c2d6914)
* [GeoJSONをバイナリ化して圧縮するFlatGeobuf](https://gunmagisgeek.com/blog/data/7222)

### 全国地方公共団体コード 
* [全国地方公共団体コード](https://www.soumu.go.jp/denshijiti/code.html)
  - [JIS X 0401 都道府県コード, （旧 JIS C 6260, ISO3166-2:JP](https://www.jisc.go.jp/app/jis/general/GnrJISNumberNameSearchList?show&jisStdNo=X0401)
  - [JIS X 0402 市区町村コード](https://www.jisc.go.jp/app/jis/general/GnrJISNumberNameSearchList?show&jisStdNo=X0402)
    - [JIS X 0402:2020]2020年版というように更新版がある。市町村は名前変更、合併などで[改正](https://webdesk.jsa.or.jp/books/W11M0090/index/?bunsyo_id=JIS+X+0402%3A2020)がある
* [日本の標準地域メッシュを生成するツール](https://github.com/MIERUNE/japan-mesh-tool)

### 地域メッシュコード
[地域メッシュコード]https://ja.wikipedia.org/wiki/地域メッシュ)は、に、緯度・経度で網の目（メッシュ）に分けたもの。
メッシュの大きさで、第1次メッシュ -> 第2次メッシュ -> 第3次メッシュとメッシュのサイズが異なる

第1次メッシュ: 1辺の長さは約80km  
第2次メッシュ: 1辺の長さは約10km  
第3次メッシュ: 1辺の長さは約1km  

* [JIS X 0410:2002地域メッシュコー](https://www.jisc.go.jp/app/jis/general/GnrJISNumberNameSearchList?show&jisStdNo=X0410)
  * [JIS X 0410:2002「地域メッシュコード」（日本産業標準調査会、経済産業省）](https://www.jisc.go.jp/app/jis/general/GnrJISNumberNameSearchList?show&jisStdNo=X0410)

### ジオコーディング
* [CSVアドレス マッチング サービス(CSIS)](https://geocode.csis.u-tokyo.ac.jp/home/csv-admatch/)
* [GeoNLP](https://geonlp.ex.nii.ac.jp/)
* [IMIコンポーネントツール](https://info.gbiz.go.jp/tools/imi_tools/)
  - [IMI](https://imi.go.jp/)
  - [GitHub](https://github.com/IMI-Tool-Project)
* [Community Geocoder](https://community-geocoder.geolonia.com/)
  - [オープンソースのジオコーディング API ](https://github.com/geolonia/community-geocoder)
  - [Geolonia 住所データ](https://github.com/geolonia/japanese-addresses)
  - [オープンソースの住所正規化ライブラリです。](https://github.com/geolonia/normalize-japanese-addresses)
* [ExcelGeo (ITDART)](http://excelgeo.itdart.org/)

#### 参考
* [地番と住居表示の違いは何か](https://登記簿図書館.com/cpu/column/theme01/column03.html)
* [ジオコーディングと住所データ](https://qiita.com/nyampire/items/d74dcde6e57f793ab0c1)

### その他
* [位置参照情報(国土交通省)](https://nlftp.mlit.go.jp/isj/)
* [GeoNames.jp](https://geonames.jp/)
* [GeoNLP](http://agora.ex.nii.ac.jp/GeoNLP/)
* [電子国土基本図（地名情報）「住居表示住所」](https://www.gsi.go.jp/kihonjohochousa/jukyo_jusho.html)
* [地名集日本（GAZETTEER OF JAPAN)](https://www.gsi.go.jp/kihonjohochousa/gazetteer.html)
* [OpenAddressess(海外)](https://openaddresses.io/)


----

### リンク集

#### GIS学習サイト
* [GIS実習オープン教材](https://gis-oer.github.io/gitbook/book/)
* [オンラインGIS教材](https://sites.google.com/view/gis-online-learning/)
* [地理教材共有サイト](https://sites.google.com/view/geoclass2020/)

#### 雑多なメモ
* [Pythonではじめる地理空間情報(α版) HackMD](https://hackmd.io/@geopythonjp/HkppxtRP5/%2FBBL9R2NVRAaagfWNHHIHhQ)
  * [Pythonではじめる地理空間情報 (PyConJP2022版)](https://speakerdeck.com/homata/pythondehazimerudi-li-kong-jian-qing-bao)
