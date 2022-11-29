// Cesium Ionの読み込みアクセストークンを設定
Cesium.Ion.defaultAccessToken = 'your_access_token';

// 地形モデルのTerrainデータの指定
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
      url : 'https://a.tile.openstreetmap.org/'
    }),
    terrainProvider: Cesium.createWorldTerrain()
});

// 航空写真オルソ画像タイルデータ(PLATEAU-Ortho)の指定
/*
var imageProvider = new Cesium.UrlTemplateImageryProvider({ url: 'https://gic-plateau.s3.ap-northeast-1.amazonaws.com/2020/ortho/tiles/{z}/{x}/{y}.png', maximumLevel : 19});
var current_image = viewer.scene.imageryLayers.addImageryProvider(imageProvider); 
*/

// 建築物モデル等の3DTilesデータ(東京都千代田区の建物データ)の指定
var your_3d_tiles = viewer.scene.primitives.add(new Cesium.Cesium3DTileset({
    // テクスチャなし
	// url : 'https://plateau.geospatial.jp/main/data/3d-tiles/bldg/13100_tokyo/13101_chiyoda-ku/notexture/tileset.json'
    // テクスチャ付き
    // url : 'https://plateau.geospatial.jp/main/data/3d-tiles/bldg/13100_tokyo/13101_chiyoda-ku/texture/tileset.json'
    // テクスチャ付き（低解像度）
	url : 'https://plateau.geospatial.jp/main/data/3d-tiles/bldg/13100_tokyo/13101_chiyoda-ku/low_resolution/tileset.json'
}));

// カメラの初期位置の指定
viewer.camera.setView({
    destination : Cesium.Cartesian3.fromDegrees(139.74887, 35.65692, 800.0),
    orientation: {
        heading : Cesium.Math.toRadians(0.0),  // east, default value is 0.0 (north)
        pitch : Cesium.Math.toRadians(-10),    // default value (looking down)
        roll : 0.0                             // default value
    }
});

// マウスクリックで緯度経度を表示
/*
viewer.canvas.addEventListener('click', function(e) {
    var mousePosition = new Cesium.Cartesian2(e.clientX, e.clientY);
    var ellipsoid = viewer.scene.globe.ellipsoid;
    var cartesian = viewer.camera.pickEllipsoid(mousePosition, ellipsoid);
    if (cartesian) {
        var cartographic = ellipsoid.cartesianToCartographic(cartesian);
        var lon = Cesium.Math.toDegrees(cartographic.longitude).toFixed(5);
        var lat = Cesium.Math.toDegrees(cartographic.latitude).toFixed(5);
        alert(lon + ', ' + lat);
    } else {
        alert('Globe was not picked');
    }
}, false);
*/