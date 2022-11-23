// Cesium ionのアクセストークン
Cesium.Ion.defaultAccessToken = 'your_access_token';

// GeoJSONファイル表示
var promise = Cesium.GeoJsonDataSource.load('53392633_bldg_4326_lod2_05.geojson'); 
    promise.then(function(datasource){
    var viewer = new Cesium.Viewer('map', {
      animation : false,
      baseLayerPicker: false,
      fullscreenButton: false,
      geocoder: false,
      homeButton: false,
      navigationHelpButton: false,
      sceneModePicker: false,
      scene3DOnly: true,
      timeline: false,
      imageryProvider: new Cesium.OpenStreetMapImageryProvider({
        // 地理院タイル 色別標高図 https://maps.gsi.go.jp/development/ichiran.html
        url: '//cyberjapandata.gsi.go.jp/xyz/relief/'
      }),
      terrainProvider: Cesium.createWorldTerrain(),
    });

    var layers = viewer.scene.imageryLayers;
    var osm = layers.addImageryProvider(
      new Cesium.OpenStreetMapImageryProvider()
    );
    osm.alpha = 0.6;

    viewer.dataSources.add(datasource);
    viewer.zoomTo(datasource);
  });
