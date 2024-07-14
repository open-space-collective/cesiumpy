# Apache License 2.0

import pytest
import traitlets

import cesiumpy


class TestCamera:
    def test_camera_basics(self):
        widget = cesiumpy.CesiumWidget(id="cesiumwidget")

        c = cesiumpy.Camera(widget)
        assert c.script == ""

        c.flyTo((1, 2, 3))
        exp = "{destination: Cesium.Cartesian3.fromDegrees(1.0, 2.0, 3.0)}"
        assert c.script == exp

        c.flyTo((4, 5, 6))
        exp = "{destination: Cesium.Cartesian3.fromDegrees(4.0, 5.0, 6.0)}"
        assert c.script == exp

        c.flyTo((4, 5, 6, 7))
        exp = "{destination: Cesium.Rectangle.fromDegrees(4.0, 5.0, 6.0, 7.0)}"
        assert c.script == exp

        msg = "x must be longitude, between -180 to 180"
        with pytest.raises(ValueError, match=msg):
            c.flyTo((200, 2, 3))

        msg = "y must be latitude, between -90 to 90"
        with pytest.raises(ValueError, match=msg):
            c.flyTo((1, 200, 3))

        msg = (
            "The 'destination' trait of a Camera instance must be a _Cartesian or None"
        )
        with pytest.raises(traitlets.TraitError):
            c.flyTo(1)

    def test_camera_repr(self):
        widget = cesiumpy.CesiumWidget(id="cesiumwidget")

        c = cesiumpy.Camera(widget)
        assert repr(c) == "Camera(destination=default)"

        c.flyTo((-130, 40, 10000))

        assert (
            repr(c)
            == "Camera(destination=Cartesian3.fromDegrees(-130.0, 40.0, 10000.0))"
        )

    def test_widget(self):
        widget = cesiumpy.CesiumWidget(id="cesiumwidget")
        widget.camera.flyTo((-117.16, 32.71, 15000.0))
        result = widget.to_html()

        exp = """<meta charset="utf-8">
<script src="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Cesium.js"></script>
<script src="https://storage.googleapis.com/loft-orbital-public/cesium-sensor-volumes.js"></script>
<link href="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
<div id="cesiumwidget" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  async function init() {
    var widget = new Cesium.CesiumWidget("cesiumwidget");
    widget.camera.flyTo({destination: Cesium.Cartesian3.fromDegrees(-117.16, 32.71, 15000.0)});
  }
  init();
</script>"""
        assert result == exp

    def test_viewer(self):
        viewer = cesiumpy.Viewer(id="viewertest")
        viewer.camera.flyTo((135, 30, 145, 45))
        result = viewer.to_html()

        exp = """<meta charset="utf-8">
<script src="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Cesium.js"></script>
<script src="https://storage.googleapis.com/loft-orbital-public/cesium-sensor-volumes.js"></script>
<link href="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  async function init() {
    var widget = new Cesium.Viewer("viewertest");
    widget.camera.flyTo({destination: Cesium.Rectangle.fromDegrees(135.0, 30.0, 145.0, 45.0)});
  }
  init();
</script>"""
        assert result == exp

        # add entity (doesn't change camera position)
        cyl = cesiumpy.Cylinder(
            position=(120, 35, 5000),
            length=10000,
            top_radius=10000,
            bottom_radius=20000,
            material="red",
        )
        viewer.entities.add(cyl)
        result = viewer.to_html()

        exp = """<meta charset="utf-8">
<script src="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Cesium.js"></script>
<script src="https://storage.googleapis.com/loft-orbital-public/cesium-sensor-volumes.js"></script>
<link href="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  async function init() {
    var widget = new Cesium.Viewer("viewertest");
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(120.0, 35.0, 5000.0), cylinder: {length: 10000.0, topRadius: 10000.0, bottomRadius: 20000.0, material: Cesium.Color.RED}});
    widget.camera.flyTo({destination: Cesium.Rectangle.fromDegrees(135.0, 30.0, 145.0, 45.0)});
    widget.zoomTo(widget.entities);
  }
  init();
</script>"""
        assert result == exp

        # we can pass entity with position to camera
        viewer.camera.flyTo(cyl)
        result = viewer.to_html()

        exp = """<meta charset="utf-8">
<script src="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Cesium.js"></script>
<script src="https://storage.googleapis.com/loft-orbital-public/cesium-sensor-volumes.js"></script>
<link href="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  async function init() {
    var widget = new Cesium.Viewer("viewertest");
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(120.0, 35.0, 5000.0), cylinder: {length: 10000.0, topRadius: 10000.0, bottomRadius: 20000.0, material: Cesium.Color.RED}});
    widget.camera.flyTo({destination: Cesium.Cartesian3.fromDegrees(120.0, 35.0, 5000.0)});
    widget.zoomTo(widget.entities);
  }
  init();
</script>"""
        assert result == exp

    def test_geocode_defaultheight(self):
        import geopy

        try:
            viewer = cesiumpy.Viewer(id="viewertest")
            viewer.camera.flyTo("Los Angeles")
            result = viewer.to_html()

            exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="https://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.camera.flyTo({destination: Cesium.Cartesian3.fromDegrees(-118.2436849, 34.0522342, 100000.0)});
</script>"""
            assert result == exp
        except (geopy.exc.GeocoderQuotaExceeded, geopy.exc.GeocoderServiceError):
            pass
