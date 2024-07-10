# Apache License 2.0

import pytest

import cesiumpy


@pytest.fixture
def widget() -> cesiumpy.CesiumWidget:
    return cesiumpy.CesiumWidget(id="widgettest")


@pytest.fixture
def options() -> dict:
    return dict(
        animation=True,
        base_layer_picker=False,
        fullscreen_button=False,
        geocoder=False,
        home_button=False,
        info_box=False,
        scene_mode_picker=True,
        selection_indicator=False,
        navigation_help_button=False,
        timeline=False,
        navigation_instructions_initially_visible=False,
    )


@pytest.fixture
def viewer(options: dict) -> cesiumpy.Viewer:
    return cesiumpy.Viewer(id="viewertest", **options)


class TestWidget:
    def test_repr(self, widget: cesiumpy.CesiumWidget):
        # should not be to_html output
        result = repr(widget)
        assert result.startswith("<cesiumpy.widget.CesiumWidget object")

    def test_html(self, widget: cesiumpy.CesiumWidget):
        result = widget.to_html()
        exp = """<meta charset="utf-8">
<script src="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Cesium.js"></script>
<script src="https://storage.googleapis.com/loft-orbital-public/cesium-sensor-volumes.js"></script>
<link href="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
<div id="widgettest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  async function init() {
    var widget = new Cesium.CesiumWidget("widgettest");
  }
  init();
</script>"""
        assert result == exp

    def test_widget_props(self, widget: cesiumpy.CesiumWidget):
        widget = cesiumpy.CesiumWidget(id="namechange", height="50%", width="70%")
        result = widget.to_html()
        exp = """<meta charset="utf-8">
<script src="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Cesium.js"></script>
<script src="https://storage.googleapis.com/loft-orbital-public/cesium-sensor-volumes.js"></script>
<link href="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
<div id="namechange" style="width:70%; height:50%;"><div>
<script type="text/javascript">
  async function init() {
    var widget = new Cesium.CesiumWidget("namechange");
  }
  init();
</script>"""
        assert result == exp

    def test_repr_html(self, widget: cesiumpy.CesiumWidget):
        assert widget.to_html() == widget._repr_html_()


class TestViewer:

    def test_repr(self, viewer: cesiumpy.Viewer):
        # should not be to_html output
        result = repr(viewer)
        assert result.startswith("<cesiumpy.viewer.Viewer object")

    def test_html(self, viewer: cesiumpy.Viewer):
        result = viewer.to_html()
        exp = """<meta charset="utf-8">
<script src="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Cesium.js"></script>
<script src="https://storage.googleapis.com/loft-orbital-public/cesium-sensor-volumes.js"></script>
<link href="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  async function init() {
    var widget = new Cesium.Viewer("viewertest", {animation: true, baseLayerPicker: false, fullscreenButton: false, geocoder: false, homeButton: false, infoBox: false, sceneModePicker: true, selectionIndicator: false, timeline: false, navigationHelpButton: false, navigationInstructionsInitiallyVisible: false});
  }
  init();
</script>"""
        assert result == exp

    def test_add_cylinder(self, viewer: cesiumpy.Viewer):
        cyl = cesiumpy.Cylinder(
            position=(-110, 50, 2000000),
            length=4000000,
            top_radius=100000,
            bottom_radius=100000,
            material=cesiumpy.color.AQUA,
            name="x",
        )
        viewer.entities.add(cyl)
        result = viewer.to_html()

        # entity name must come first
        exp = """<meta charset="utf-8">
<script src="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Cesium.js"></script>
<script src="https://storage.googleapis.com/loft-orbital-public/cesium-sensor-volumes.js"></script>
<link href="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  async function init() {
    var widget = new Cesium.Viewer("viewertest", {animation: true, baseLayerPicker: false, fullscreenButton: false, geocoder: false, homeButton: false, infoBox: false, sceneModePicker: true, selectionIndicator: false, timeline: false, navigationHelpButton: false, navigationInstructionsInitiallyVisible: false});
    widget.entities.add({name: "x", position: Cesium.Cartesian3.fromDegrees(-110.0, 50.0, 2000000.0), cylinder: {length: 4000000.0, topRadius: 100000.0, bottomRadius: 100000.0, material: Cesium.Color.AQUA}});
    widget.zoomTo(widget.entities);
  }
  init();
</script>"""
        assert result == exp

    def test_entities_attribute(self, viewer: cesiumpy.Viewer):
        with pytest.raises(AttributeError):
            viewer.entities = None

    def test_add_polygon(self, viewer: cesiumpy.Viewer):
        pol = cesiumpy.Polygon(
            [
                -109.080842,
                45.002073,
                0.0,
                -105.91517,
                45.002073,
                0.0,
                -104.058488,
                44.996596,
                0.0,
                -104.053011,
                43.002989,
                0.0,
                -104.053011,
                41.003906,
                0.0,
                -105.728954,
                40.998429,
                0.0,
                -107.919731,
                41.003906,
                0.0,
                -109.04798,
                40.998429,
                0.0,
                -111.047063,
                40.998429,
                0.0,
                -111.047063,
                42.000709,
                0.0,
                -111.047063,
                44.476286,
                0.0,
                -111.05254,
                45.002073,
                0.0,
            ],
            material=cesiumpy.color.RED,
            name="x",
        )
        viewer.entities.add(pol)
        result = viewer.to_html()

        exp = """<meta charset="utf-8">
<script src="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Cesium.js"></script>
<script src="https://storage.googleapis.com/loft-orbital-public/cesium-sensor-volumes.js"></script>
<link href="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  async function init() {
    var widget = new Cesium.Viewer("viewertest", {animation: true, baseLayerPicker: false, fullscreenButton: false, geocoder: false, homeButton: false, infoBox: false, sceneModePicker: true, selectionIndicator: false, timeline: false, navigationHelpButton: false, navigationInstructionsInitiallyVisible: false});
    widget.entities.add({name: "x", polygon: {hierarchy: Cesium.Cartesian3.fromDegreesArrayHeights([-109.080842, 45.002073, 0.0, -105.91517, 45.002073, 0.0, -104.058488, 44.996596, 0.0, -104.053011, 43.002989, 0.0, -104.053011, 41.003906, 0.0, -105.728954, 40.998429, 0.0, -107.919731, 41.003906, 0.0, -109.04798, 40.998429, 0.0, -111.047063, 40.998429, 0.0, -111.047063, 42.000709, 0.0, -111.047063, 44.476286, 0.0, -111.05254, 45.002073, 0.0]), material: Cesium.Color.RED}});
    widget.zoomTo(widget.entities);
  }
  init();
</script>"""
        assert result == exp

    def test_add_entities(self, viewer: cesiumpy.Viewer):

        box = cesiumpy.Box(
            dimensions=(40e4, 30e4, 50e4),
            material=cesiumpy.color.RED,
            position=[-120, 40, 0],
        )
        viewer.entities.add(box)

        ellipse = cesiumpy.Ellipse(
            semi_minor_axis=25e4,
            semi_major_axis=40e4,
            material=cesiumpy.color.BLUE,
            position=[-110, 40, 0],
        )
        viewer.entities.add(ellipse)

        cyl = cesiumpy.Cylinder(
            position=[-100, 40, 50e4],
            length=100e4,
            top_radius=10e4,
            bottom_radius=10e4,
            material=cesiumpy.color.AQUA,
        )
        viewer.entities.add(cyl)

        pol = cesiumpy.Polygon(
            [-90, 40, 0, -95, 40, 0, -95, 45, 0, -90, 40, 0],
            material=cesiumpy.color.ORANGE,
        )
        viewer.entities.add(pol)

        rect = cesiumpy.Rectangle(
            coordinates=(-85, 40, -80, 45), material=cesiumpy.color.GREEN
        )
        viewer.entities.add(rect)

        ellipsoid = cesiumpy.Ellipsoid(
            position=(-70, 40, 0),
            radii=(20e4, 20e4, 30e4),
            material=cesiumpy.color.GREEN,
        )
        viewer.entities.add(ellipsoid)

        wall = cesiumpy.Wall(
            positions=[-60, 40, 0, -65, 40, 0, -65, 45, 0, -60, 45, 0],
            maximum_heights=[10e4] * 6,
            minimum_heights=[0] * 6,
            material=cesiumpy.color.RED,
        )
        viewer.entities.add(wall)

        corridor = cesiumpy.Corridor(
            positions=[-120, 30, 0, -90, 35, 0, -60, 30, 0],
            width=2e5,
            material=cesiumpy.color.RED,
        )
        viewer.entities.add(corridor)

        polyline = cesiumpy.Polyline(
            positions=[-120, 25, -90, 30, -60, 25],
            width=0.5,
            material=cesiumpy.color.BLUE,
        )
        viewer.entities.add(polyline)
        polylinevolume = cesiumpy.PolylineVolume(
            positions=[-120, 20, -90, 25, -60, 20],
            shape=[
                cesiumpy.Cartesian2(-50000, -50000),
                cesiumpy.Cartesian2(50000, -50000),
                cesiumpy.Cartesian2(50000, 50000),
                cesiumpy.Cartesian2(-50000, 50000),
            ],
            material=cesiumpy.color.GREEN,
        )
        viewer.entities.add(polylinevolume)
        result = viewer.to_html()

        exp = """<meta charset="utf-8">
<script src="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Cesium.js"></script>
<script src="https://storage.googleapis.com/loft-orbital-public/cesium-sensor-volumes.js"></script>
<link href="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  async function init() {
    var widget = new Cesium.Viewer("viewertest", {animation: true, baseLayerPicker: false, fullscreenButton: false, geocoder: false, homeButton: false, infoBox: false, sceneModePicker: true, selectionIndicator: false, timeline: false, navigationHelpButton: false, navigationInstructionsInitiallyVisible: false});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(-120.0, 40.0, 0.0), box: {dimensions: new Cesium.Cartesian3(400000.0, 300000.0, 500000.0), material: Cesium.Color.RED}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(-110.0, 40.0, 0.0), ellipse: {semiMinorAxis: 250000.0, semiMajorAxis: 400000.0, material: Cesium.Color.BLUE}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(-100.0, 40.0, 500000.0), cylinder: {length: 1000000.0, topRadius: 100000.0, bottomRadius: 100000.0, material: Cesium.Color.AQUA}});
    widget.entities.add({polygon: {hierarchy: Cesium.Cartesian3.fromDegreesArrayHeights([-90, 40, 0, -95, 40, 0, -95, 45, 0, -90, 40, 0]), material: Cesium.Color.ORANGE}});
    widget.entities.add({rectangle: {coordinates: Cesium.Rectangle.fromDegrees(west=-85.0, south=40.0, east=-80.0, north=45.0), material: Cesium.Color.GREEN}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(-70.0, 40.0, 0.0), ellipsoid: {radii: new Cesium.Cartesian3(200000.0, 200000.0, 300000.0), material: Cesium.Color.GREEN}});
    widget.entities.add({wall: {positions: Cesium.Cartesian3.fromDegreesArrayHeights([-60, 40, 0, -65, 40, 0, -65, 45, 0, -60, 45, 0]), maximumHeights: [100000.0, 100000.0, 100000.0, 100000.0, 100000.0, 100000.0], minimumHeights: [0, 0, 0, 0, 0, 0], material: Cesium.Color.RED}});
    widget.entities.add({corridor: {positions: Cesium.Cartesian3.fromDegreesArrayHeights([-120, 30, 0, -90, 35, 0, -60, 30, 0]), width: 200000.0, material: Cesium.Color.RED}});
    widget.entities.add({polyline: {positions: Cesium.Cartesian3.fromDegreesArrayHeights([-120, 25, -90, 30, -60, 25]), width: 0.5, material: Cesium.Color.BLUE}});
    widget.entities.add({polylineVolume: {positions: Cesium.Cartesian3.fromDegreesArrayHeights([-120, 20, -90, 25, -60, 20]), shape: [new Cesium.Cartesian2(-50000.0, -50000.0), new Cesium.Cartesian2(50000.0, -50000.0), new Cesium.Cartesian2(50000.0, 50000.0), new Cesium.Cartesian2(-50000.0, 50000.0)], material: Cesium.Color.GREEN}});
    widget.zoomTo(widget.entities);
  }
  init();
</script>"""
        assert result == exp

        # clear entities
        viewer.entities.clear()
        result = viewer.to_html()
        exp_clear = """<meta charset="utf-8">
<script src="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Cesium.js"></script>
<script src="https://storage.googleapis.com/loft-orbital-public/cesium-sensor-volumes.js"></script>
<link href="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  async function init() {
    var widget = new Cesium.Viewer("viewertest", {animation: true, baseLayerPicker: false, fullscreenButton: false, geocoder: false, homeButton: false, infoBox: false, sceneModePicker: true, selectionIndicator: false, timeline: false, navigationHelpButton: false, navigationInstructionsInitiallyVisible: false});
  }
  init();
</script>"""
        assert result == exp_clear

        # add multiple objects at once
        objs = [
            box,
            ellipse,
            cyl,
            pol,
            rect,
            ellipsoid,
            wall,
            corridor,
            polyline,
            polylinevolume,
        ]
        viewer.entities.add(objs)
        result = viewer.to_html()
        exp = """<meta charset="utf-8">
<script src="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Cesium.js"></script>
<script src="https://storage.googleapis.com/loft-orbital-public/cesium-sensor-volumes.js"></script>
<link href="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  async function init() {
    var widget = new Cesium.Viewer("viewertest", {animation: true, baseLayerPicker: false, fullscreenButton: false, geocoder: false, homeButton: false, infoBox: false, sceneModePicker: true, selectionIndicator: false, timeline: false, navigationHelpButton: false, navigationInstructionsInitiallyVisible: false});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(-120.0, 40.0, 0.0), box: {dimensions: new Cesium.Cartesian3(400000.0, 300000.0, 500000.0), material: Cesium.Color.RED}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(-110.0, 40.0, 0.0), ellipse: {semiMinorAxis: 250000.0, semiMajorAxis: 400000.0, material: Cesium.Color.BLUE}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(-100.0, 40.0, 500000.0), cylinder: {length: 1000000.0, topRadius: 100000.0, bottomRadius: 100000.0, material: Cesium.Color.AQUA}});
    widget.entities.add({polygon: {hierarchy: Cesium.Cartesian3.fromDegreesArrayHeights([-90, 40, 0, -95, 40, 0, -95, 45, 0, -90, 40, 0]), material: Cesium.Color.ORANGE}});
    widget.entities.add({rectangle: {coordinates: Cesium.Rectangle.fromDegrees(west=-85.0, south=40.0, east=-80.0, north=45.0), material: Cesium.Color.GREEN}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(-70.0, 40.0, 0.0), ellipsoid: {radii: new Cesium.Cartesian3(200000.0, 200000.0, 300000.0), material: Cesium.Color.GREEN}});
    widget.entities.add({wall: {positions: Cesium.Cartesian3.fromDegreesArrayHeights([-60, 40, 0, -65, 40, 0, -65, 45, 0, -60, 45, 0]), maximumHeights: [100000.0, 100000.0, 100000.0, 100000.0, 100000.0, 100000.0], minimumHeights: [0, 0, 0, 0, 0, 0], material: Cesium.Color.RED}});
    widget.entities.add({corridor: {positions: Cesium.Cartesian3.fromDegreesArrayHeights([-120, 30, 0, -90, 35, 0, -60, 30, 0]), width: 200000.0, material: Cesium.Color.RED}});
    widget.entities.add({polyline: {positions: Cesium.Cartesian3.fromDegreesArrayHeights([-120, 25, -90, 30, -60, 25]), width: 0.5, material: Cesium.Color.BLUE}});
    widget.entities.add({polylineVolume: {positions: Cesium.Cartesian3.fromDegreesArrayHeights([-120, 20, -90, 25, -60, 20]), shape: [new Cesium.Cartesian2(-50000.0, -50000.0), new Cesium.Cartesian2(50000.0, -50000.0), new Cesium.Cartesian2(50000.0, 50000.0), new Cesium.Cartesian2(-50000.0, 50000.0)], material: Cesium.Color.GREEN}});
    widget.zoomTo(widget.entities);
  }
  init();
</script>
"""
        for result_line, expected_line in zip(result.splitlines(), exp.splitlines()):
            assert result_line == expected_line

    def test_add_entities_with_properties(self):
        viewer = cesiumpy.Viewer(id="viewertest")
        box = cesiumpy.Box(dimensions=(40e4, 30e4, 50e4), position=[-120, 40, 0])
        viewer.entities.add(box, material=cesiumpy.color.RED)
        result = viewer.to_html()
        exp = """<meta charset="utf-8">
<script src="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Cesium.js"></script>
<script src="https://storage.googleapis.com/loft-orbital-public/cesium-sensor-volumes.js"></script>
<link href="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  async function init() {
    var widget = new Cesium.Viewer("viewertest");
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(-120.0, 40.0, 0.0), box: {dimensions: new Cesium.Cartesian3(400000.0, 300000.0, 500000.0), material: Cesium.Color.RED}});
    widget.zoomTo(widget.entities);
  }
  init();
</script>"""
        assert result == exp

        viewer = cesiumpy.Viewer(id="viewertest")
        box1 = cesiumpy.Box(dimensions=(40e4, 30e4, 50e4), position=[-120, 40, 0])
        box2 = cesiumpy.Box(dimensions=(50e4, 60e4, 70e4), position=[-100, 80, 0])
        viewer.entities.add([box1, box2], material=cesiumpy.color.RED)
        result = viewer.to_html()
        exp = """<meta charset="utf-8">
<script src="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Cesium.js"></script>
<script src="https://storage.googleapis.com/loft-orbital-public/cesium-sensor-volumes.js"></script>
<link href="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  async function init() {
    var widget = new Cesium.Viewer("viewertest");
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(-120.0, 40.0, 0.0), box: {dimensions: new Cesium.Cartesian3(400000.0, 300000.0, 500000.0), material: Cesium.Color.RED}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(-100.0, 80.0, 0.0), box: {dimensions: new Cesium.Cartesian3(500000.0, 600000.0, 700000.0), material: Cesium.Color.RED}});
    widget.zoomTo(widget.entities);
  }
  init();
</script>"""
        assert result == exp

    @pytest.mark.skip(reason="Not propertly implemented yet")
    def test_model(self):
        viewer = cesiumpy.Viewer(id="viewertest")
        m = cesiumpy.Model("xxx.gltf", model_matrix=(-100, 40, 0), scale=200)
        viewer.scene.primitives.add(m)
        result = viewer.to_html()
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="https://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.scene.primitives.add(Cesium.Model.fromGltf({url : "xxx.gltf", modelMatrix : Cesium.Transforms.eastNorthUpToFixedFrame(Cesium.Cartesian3.fromDegrees(-100.0, 40.0, 0.0)), scale : 200.0}));
</script>"""
        assert result == exp

    def test_add_scripts(self):
        viewer = cesiumpy.Viewer(id="viewertest")
        viewer.scripts.add('console.log("xxx");')
        result = viewer.to_html()
        exp = """<meta charset="utf-8">
<script src="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Cesium.js"></script>
<script src="https://storage.googleapis.com/loft-orbital-public/cesium-sensor-volumes.js"></script>
<link href="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  async function init() {
    var widget = new Cesium.Viewer("viewertest");
    console.log("xxx");
  }
  init();
</script>"""
        assert result == exp

        viewer = cesiumpy.Viewer(id="viewertest")
        viewer.scripts.add(['console.log("xxx");', 'console.log("yyy");'])
        result = viewer.to_html()
        exp = """<meta charset="utf-8">
<script src="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Cesium.js"></script>
<script src="https://storage.googleapis.com/loft-orbital-public/cesium-sensor-volumes.js"></script>
<link href="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  async function init() {
    var widget = new Cesium.Viewer("viewertest");
    console.log("xxx");
    console.log("yyy");
  }
  init();
</script>"""
        assert result == exp

        with pytest.raises(ValueError):
            viewer.scripts.add(1)
