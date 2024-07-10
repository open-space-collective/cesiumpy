# Apache License 2.0

import cesiumpy


class TestDataSource:
    def test_czmldatasource(self):
        ds = cesiumpy.CzmlDataSource("xxx.czml")
        exp = 'Cesium.CzmlDataSource.load("xxx.czml")'
        assert ds.script == exp
        ds = cesiumpy.CzmlDataSource.load("xxx.czml")
        assert ds.script == exp

    def test_geojsondatasource(self):
        ds = cesiumpy.GeoJsonDataSource("xxx.geojson")

        exp = 'Cesium.GeoJsonDataSource.load("xxx.geojson")'
        assert ds.script == exp
        ds = cesiumpy.GeoJsonDataSource.load("xxx.geojson")
        assert ds.script == exp

        ds = cesiumpy.GeoJsonDataSource(
            "xxx.geojson",
            markerColor=cesiumpy.color.RED,
            stroke=cesiumpy.color.BLUE,
            fill=cesiumpy.color.GREEN,
        )
        exp = 'Cesium.GeoJsonDataSource.load("xxx.geojson", {markerColor: Cesium.Color.RED, stroke: Cesium.Color.BLUE, fill: Cesium.Color.GREEN})'
        assert ds.script == exp
        ds = cesiumpy.GeoJsonDataSource.load(
            "xxx.geojson",
            markerColor=cesiumpy.color.RED,
            stroke=cesiumpy.color.BLUE,
            fill=cesiumpy.color.GREEN,
        )
        assert ds.script == exp

        ds = cesiumpy.GeoJsonDataSource(
            "xxx.geojson", markerColor="red", stroke="blue", fill="green"
        )
        assert ds.script == exp
        ds = cesiumpy.GeoJsonDataSource.load(
            "xxx.geojson", markerColor="red", stroke="blue", fill="green"
        )
        assert ds.script == exp

    def test_kmldatasource(self):
        ds = cesiumpy.KmlDataSource("xxx.kml")

        exp = 'Cesium.KmlDataSource.load("xxx.kml")'
        assert ds.script == exp
        ds = cesiumpy.KmlDataSource.load("xxx.kml")
        assert ds.script == exp

    def test_czml_viewer(self):
        v = cesiumpy.Viewer(id="viewertest")
        d = cesiumpy.CzmlDataSource("data/simple.czml")
        v.data_sources.add(d)
        result = v.to_html()
        exp = """<meta charset="utf-8">
<script src="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Cesium.js"></script>
<script src="https://storage.googleapis.com/loft-orbital-public/cesium-sensor-volumes.js"></script>
<link href="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  async function init() {
    var widget = new Cesium.Viewer("viewertest");
    widget.dataSources.add(Cesium.CzmlDataSource.load("data/simple.czml"));
  }
  init();
</script>"""
        assert result == exp

    def test_geojson_viewer(self):
        ds = cesiumpy.GeoJsonDataSource("./test.geojson", markerSymbol="?")
        viewer = cesiumpy.Viewer(id="viewertest")
        viewer.data_sources.add(ds)
        viewer.camera.flyTo((-105.01621, 39.57422, 1000))
        result = viewer.to_html()

        exp = """<meta charset="utf-8">
<script src="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Cesium.js"></script>
<script src="https://storage.googleapis.com/loft-orbital-public/cesium-sensor-volumes.js"></script>
<link href="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  async function init() {
    var widget = new Cesium.Viewer("viewertest");
    widget.dataSources.add(Cesium.GeoJsonDataSource.load("./test.geojson", {markerSymbol: "?"}));
    widget.camera.flyTo({destination: Cesium.Cartesian3.fromDegrees(-105.01621, 39.57422, 1000.0)});
  }
  init();
</script>"""

        assert result == exp
