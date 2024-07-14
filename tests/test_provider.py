# Apache License 2.0

import pytest

import re
import traitlets

import cesiumpy
import cesiumpy.testing as tm


class TestTerrainProvider:
    def test_provider_klass(self):
        url = "x"

        assert cesiumpy.TerrainProvider(url=url)._klass == "Cesium.TerrainProvider"
        assert (
            cesiumpy.ArcGisImageServerTerrainProvider(url=url, token="DUMMY")._klass
            == "Cesium.ArcGisImageServerTerrainProvider"
        )
        assert (
            cesiumpy.CesiumTerrainProvider(url=url)._klass
            == "Cesium.CesiumTerrainProvider"
        )
        assert (
            cesiumpy.EllipsoidTerrainProvider()._klass
            == "Cesium.EllipsoidTerrainProvider"
        )
        assert (
            cesiumpy.VRTheWorldTerrainProvider(url=url)._klass
            == "Cesium.VRTheWorldTerrainProvider"
        )

    def test_viewer(self):
        url = "http://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer"
        imagery_provider = cesiumpy.ArcGisMapServerImageryProvider(url=url)
        v = cesiumpy.Viewer(id="viewertest", imagery_provider=imagery_provider)
        result = v.to_html()

        exp = """<meta charset="utf-8">
<script src="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Cesium.js"></script>
<script src="https://storage.googleapis.com/loft-orbital-public/cesium-sensor-volumes.js"></script>
<link href="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  async function init() {
    var widget = new Cesium.Viewer("viewertest", {baseLayerPicker: false, imageryProvider: {url: "http://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer"}});
  }
  init();
</script>"""
        assert result == exp

    def test_CesiumTerrainProvider(self):
        url = "//assets.agi.com/stk-terrain/world"
        terrainProvider = cesiumpy.CesiumTerrainProvider(url=url)
        result = terrainProvider.script
        exp = """new Cesium.CesiumTerrainProvider({url: "//assets.agi.com/stk-terrain/world"})"""
        assert result == exp

        terrainProvider = cesiumpy.CesiumTerrainProvider(
            url=url, request_water_mask=True
        )
        result = terrainProvider.script
        exp = """new Cesium.CesiumTerrainProvider({url: "//assets.agi.com/stk-terrain/world", requestWaterMask: true})"""
        assert result == exp

        terrainProvider = cesiumpy.CesiumTerrainProvider(
            url=url, request_water_mask=True, request_vertex_normals=True
        )
        result = terrainProvider.script
        exp = """new Cesium.CesiumTerrainProvider({url: "//assets.agi.com/stk-terrain/world", requestVertexNormals: true, requestWaterMask: true})"""
        assert result == exp

        with pytest.raises(traitlets.TraitError):
            cesiumpy.CesiumTerrainProvider(url=1)

    def test_EllipsoidTerrainProvider(self):
        terrainProvider = cesiumpy.EllipsoidTerrainProvider()
        result = terrainProvider.script
        exp = """new Cesium.EllipsoidTerrainProvider()"""
        assert result == exp

    def test_EllipsoidTerrainProvider_repr(self):
        terrainProvider = cesiumpy.EllipsoidTerrainProvider()
        exp = """<cesiumpy.provider.EllipsoidTerrainProvider"""
        assert repr(terrainProvider).startswith(exp)

    def test_VRTheWorldTerrainProvider(self):
        url = "//www.vr-theworld.com/vr-theworld/tiles1.0.0/73/"
        credit = "Terrain data courtesy VT MAK"

        terrainProvider = cesiumpy.VRTheWorldTerrainProvider(url=url, credit=credit)
        result = terrainProvider.script
        exp = """new Cesium.VRTheWorldTerrainProvider({url: "//www.vr-theworld.com/vr-theworld/tiles1.0.0/73/", credit: "Terrain data courtesy VT MAK"})"""
        assert result == exp


class TestImageProvider:
    def test_provider_klass(self):
        url = "x"

        assert cesiumpy.ImageryProvider(url=url)._klass == "Cesium.ImageryProvider"

        assert (
            cesiumpy.ArcGisMapServerImageryProvider(url=url)._klass
            == "Cesium.ArcGisMapServerImageryProvider"
        )
        assert (
            cesiumpy.BingMapsImageryProvider(
                url=url, key="xx", tileProtocol="xx"
            )._klass
            == "Cesium.BingMapsImageryProvider"
        )
        assert (
            cesiumpy.GoogleEarthImageryProvider(url=url, channel=1)._klass
            == "Cesium.GoogleEarthImageryProvider"
        )
        # Not Implemented
        # self.assertEqual(cesiumpy.GridImageryProvider(url=url)._klass,
        #                  "Cesium.GridImageryProvider")
        assert (
            cesiumpy.MapboxImageryProvider(url=url, mapId="xx", accessToken="xx")._klass
            == "Cesium.MapboxImageryProvider"
        )
        assert (
            cesiumpy.OpenStreetMapImageryProvider(url=url)._klass
            == "Cesium.OpenStreetMapImageryProvider"
        )
        assert (
            cesiumpy.SingleTileImageryProvider(url=url)._klass
            == "Cesium.SingleTileImageryProvider"
        )
        assert (
            cesiumpy.TileCoordinatesImageryProvider()._klass
            == "Cesium.TileCoordinatesImageryProvider"
        )
        assert (
            cesiumpy.TileMapServiceImageryProvider(url=url)._klass
            == "Cesium.TileMapServiceImageryProvider"
        )
        # Not Implemented
        # self.assertEqual(cesiumpy.UrlTemplateImageryProvider(url=url)._klass,
        #                  "Cesium.UrlTemplateImageryProvider")
        assert (
            cesiumpy.WebMapServiceImageryProvider(url=url, layers="xx")._klass
            == "Cesium.WebMapServiceImageryProvider"
        )
        assert (
            cesiumpy.WebMapTileServiceImageryProvider(
                url=url, layer="xx", style="xx"
            )._klass
            == "Cesium.WebMapTileServiceImageryProvider"
        )

    def test_viewer(self):
        url = "//assets.agi.com/stk-terrain/world"
        terrain_provider = cesiumpy.CesiumTerrainProvider(
            url=url, request_water_mask=True
        )
        v = cesiumpy.Viewer(id="viewertest", terrain_provider=terrain_provider)
        result = v.to_html()

        exp = """<meta charset="utf-8">
<script src="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Cesium.js"></script>
<script src="https://storage.googleapis.com/loft-orbital-public/cesium-sensor-volumes.js"></script>
<link href="https://cesium.com/downloads/cesiumjs/releases/1.86/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  async function init() {
    var widget = new Cesium.Viewer("viewertest", {baseLayerPicker: false, terrainProvider: {url: "//assets.agi.com/stk-terrain/world", requestWaterMask: true}});
  }
  init();
</script>"""
        assert result == exp

    def test_ArcGisMapServerImageryProvider(self):
        url = "http://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer"
        imageryProvider = cesiumpy.ArcGisMapServerImageryProvider(url=url)
        result = imageryProvider.script
        exp = """new Cesium.ArcGisMapServerImageryProvider({url: "http://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer"})"""
        assert result == exp

        url = (
            "//server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer"
        )
        imageryProvider = cesiumpy.ArcGisMapServerImageryProvider(url=url)
        result = imageryProvider.script
        exp = """new Cesium.ArcGisMapServerImageryProvider({url: "//server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer"})"""
        assert result == exp

    def test_TileMapServiceImageryProvider(self):
        url = "//cesiumjs.org/tilesets/imagery/blackmarble"
        credit = "Black Marble imagery courtesy NASA Earth Observatory"
        imageryProvider = cesiumpy.TileMapServiceImageryProvider(
            url=url, maximum_level=8, credit=credit
        )
        result = imageryProvider.script
        exp = """new Cesium.TileMapServiceImageryProvider({url: "//cesiumjs.org/tilesets/imagery/blackmarble", maximumLevel: 8.0, credit: "Black Marble imagery courtesy NASA Earth Observatory"})"""
        assert result == exp

        # ToDo:
        """
        'Natural Earth II (local)',
        new Cesium.TileMapServiceImageryProvider({
            url: require.toUrl('Assets/Textures/NaturalEarthII')
        }));
        """

        url = "../images/cesium_maptiler/Cesium_Logo_Color"
        imageryProvider = cesiumpy.TileMapServiceImageryProvider(url=url)
        result = imageryProvider.script
        exp = """new Cesium.TileMapServiceImageryProvider({url: "../images/cesium_maptiler/Cesium_Logo_Color"})"""
        assert result == exp

    def test_SingleTileImageryProvider(self):
        url = "../images/Cesium_Logo_overlay.png"
        rectangle = cesiumpy.entities.cartesian.Rectangle.fromDegrees(
            -75.0, 28.0, -67.0, 29.75
        )
        imageryProvider = cesiumpy.SingleTileImageryProvider(
            url=url, rectangle=rectangle
        )
        result = imageryProvider.script
        exp = """new Cesium.SingleTileImageryProvider({url: "../images/Cesium_Logo_overlay.png", rectangle: Cesium.Rectangle.fromDegrees(-75.0, 28.0, -67.0, 29.75)})"""
        assert result == exp

        url = "../images/Cesium_Logo_overlay.png"
        rectangle = cesiumpy.entities.cartesian.Rectangle.fromDegrees(
            -115.0, 38.0, -107, 39.75
        )
        imageryProvider = cesiumpy.SingleTileImageryProvider(
            url=url, rectangle=rectangle
        )
        result = imageryProvider.script
        exp = """new Cesium.SingleTileImageryProvider({url: "../images/Cesium_Logo_overlay.png", rectangle: Cesium.Rectangle.fromDegrees(-115.0, 38.0, -107.0, 39.75)})"""
        assert result == exp

    # def test_SingleTimeImageryProvider_tempfile(self):
    #     import numpy as np
    #     import matplotlib.pyplot as plt

    #     img = np.random.randint(0, 255, (100, 100, 3))
    #     ax = plt.imshow(img)
    #     img = cesiumpy.entities.material.TemporaryImage(ax.figure)
    #     m = cesiumpy.SingleTileImageryProvider(img, rectangle=(-120.0, 40.0, -100, 60))
    #     self.assertTrue(
    #         re.match(
    #             """new Cesium\\.SingleTileImageryProvider\\(\\{url: "\w+\\.png", rectangle: Cesium\\.Rectangle\\.fromDegrees\\(-120\\.0, 40\\.0, -100\\.0, 60\\.0\\)\\}\\)""",
    #             m.script,
    #         )
    #     )
    #     plt.close()

    def test_BingMapsImageryProvider(self):
        """
        new Cesium.BingMapsImageryProvider({
            url: '//dev.virtualearth.net',
            mapStyle: Cesium.BingMapsStyle.ROAD
        }));
        # ToDo: NotImplemented
        """

    def test_OpenStreetMapImageryProvider(self):
        imageryProvider = cesiumpy.OpenStreetMapImageryProvider()
        result = imageryProvider.script
        exp = """new Cesium.OpenStreetMapImageryProvider()"""
        assert result == exp

        url = "//otile1-s.mqcdn.com/tiles/1.0.0/osm/"
        imageryProvider = cesiumpy.OpenStreetMapImageryProvider(url=url)
        result = imageryProvider.script
        exp = """new Cesium.OpenStreetMapImageryProvider({url: "//otile1-s.mqcdn.com/tiles/1.0.0/osm/"})"""
        assert result == exp

        url = "//stamen-tiles.a.ssl.fastly.net/watercolor/"
        credit = "Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under CC BY SA."
        imageryProvider = cesiumpy.OpenStreetMapImageryProvider(url=url, credit=credit)
        result = imageryProvider.script
        exp = """new Cesium.OpenStreetMapImageryProvider({url: "//stamen-tiles.a.ssl.fastly.net/watercolor/", credit: "Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under CC BY SA."})"""
        assert result == exp

        imageryProvider = cesiumpy.OpenStreetMapImageryProvider(
            url=url, file_extension="jpg", credit=credit
        )
        result = imageryProvider.script
        exp = """new Cesium.OpenStreetMapImageryProvider({url: "//stamen-tiles.a.ssl.fastly.net/watercolor/", fileExtension: "jpg", credit: "Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under CC BY SA."})"""
        assert result == exp

    def test_OpenStreetMapImageryProvider_repr(self):
        imageryProvider = cesiumpy.OpenStreetMapImageryProvider()
        exp = """<cesiumpy.provider.OpenStreetMapImageryProvider"""
        assert repr(imageryProvider).startswith(exp)

        url = "//otile1-s.mqcdn.com/tiles/1.0.0/osm/"
        imageryProvider = cesiumpy.OpenStreetMapImageryProvider(url=url)
        exp = """OpenStreetMapImageryProvider(url="//otile1-s.mqcdn.com/tiles/1.0.0/osm/")"""
        assert repr(imageryProvider) == exp

    def test_WebMapServiceImageryProvider(self):
        pass

        # Not Implemented
        """
        new Cesium.WebMapServiceImageryProvider({
                url : '//mesonet.agron.iastate.edu/cgi-bin/wms/goes/conus_ir.cgi?',
                layers : 'goes_conus_ir',
                credit : 'Infrared data courtesy Iowa Environmental Mesonet',
                parameters : {
                    transparent : 'true',
                    format : 'image/png'
                },
                proxy : new Cesium.DefaultProxy('/proxy/')
            })

        new Cesium.WebMapServiceImageryProvider({
                url : '//mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi?',
                layers : 'nexrad-n0r',
                credit : 'Radar data courtesy Iowa Environmental Mesonet',
                parameters : {
                    transparent : 'true',
                    format : 'image/png'
                },
                proxy : new Cesium.DefaultProxy('/proxy/')
            })
        """

    def test_WebMapTileServiceImageryProvider(self):
        url = "http://basemap.nationalmap.gov/arcgis/rest/services/USGSShadedReliefOnly/MapServer/WMTS"
        imageryProvider = cesiumpy.WebMapTileServiceImageryProvider(
            url=url,
            layer="USGSShadedReliefOnly",
            style="default",
            format="image/jpeg",
            tile_matrix_set_id="default028mm",
            maximum_level=19,
            credit="U. S. Geological Survey",
        )
        result = imageryProvider.script
        exp = """new Cesium.WebMapTileServiceImageryProvider({url: "http://basemap.nationalmap.gov/arcgis/rest/services/USGSShadedReliefOnly/MapServer/WMTS", layer: "USGSShadedReliefOnly", style: "default", format: "image/jpeg", maximumLevel: 19.0, credit: "U. S. Geological Survey"})"""
        assert result == exp

    def test_GridImageryProvider(self):
        # Not Implemented
        # imageryProvider = cesiumpy.GridImageryProvider()
        # result = imageryProvider.script
        # exp = """new Cesium.TileCoordinatesImageryProvider()"""
        # assert result == exp
        pass

    def test_TileCoordinatesImageryProvider(self):
        imageryProvider = cesiumpy.TileCoordinatesImageryProvider()
        result = imageryProvider.script
        exp = """new Cesium.TileCoordinatesImageryProvider()"""
        assert result == exp
