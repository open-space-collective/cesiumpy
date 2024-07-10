######################################################################################################################################################

# @project        CesiumPy
# @file           tests/test_country.py
# @license        Apache 2.0

######################################################################################################################################################

import pytest

import sys

import cesiumpy

######################################################################################################################################################


class TestCountry:
    def test_country_getattr_error(self):
        msg = "Unable to load country data, file not found: 'X'"
        with pytest.raises(AttributeError, match=msg):
            cesiumpy.countries.X

        with pytest.raises(ValueError, match=msg):
            cesiumpy.countries.get("X")

    @pytest.mark.skipif(
        "shapely.geometry" not in sys.modules, reason="requires Shapely"
    )
    def test_country_jpn(self):
        jpn = cesiumpy.countries.jpn
        assert isinstance(jpn, list)
        assert all([isinstance(e, cesiumpy.Polygon) for e in jpn]) is True
        exp = """{polygon : {hierarchy : Cesium.Cartesian3.fromDegreesArray([153.958588, 24.295, 153.953308, 24.292774, 153.946625, 24.293331, 153.942749, 24.296944, 153.939697, 24.300831, 153.938873, 24.306942, 153.940247, 24.312496, 153.947754, 24.319443, 153.952759, 24.321384, 153.960236, 24.321663, 153.96579, 24.31361, 153.96579, 24.309441, 153.963013, 24.29833, 153.958588, 24.295])}}"""
        assert jpn[0].script == exp

        jpn = cesiumpy.countries.JPN
        assert isinstance(jpn, list)
        assert all([isinstance(e, cesiumpy.Polygon) for e in jpn]) is True
        assert jpn[0].script == exp

        # 2 character
        jpn = cesiumpy.countries.JP
        assert isinstance(jpn, list)
        assert all([isinstance(e, cesiumpy.Polygon) for e in jpn]) is True
        assert jpn[0].script == exp

        # official name
        jpn = cesiumpy.countries.JAPAN
        assert isinstance(jpn, list)
        assert all([isinstance(e, cesiumpy.Polygon) for e in jpn]) is True
        assert jpn[0].script == exp

    @pytest.mark.skipif(
        "shapely.geometry" not in sys.modules, reason="requires Shapely"
    )
    def test_country_get_jpn(self):
        jpn = cesiumpy.countries.get("jpn")
        assert isinstance(jpn, list)
        assert all([isinstance(e, cesiumpy.Polygon) for e in jpn]) is True
        exp = """{polygon : {hierarchy : Cesium.Cartesian3.fromDegreesArray([153.958588, 24.295, 153.953308, 24.292774, 153.946625, 24.293331, 153.942749, 24.296944, 153.939697, 24.300831, 153.938873, 24.306942, 153.940247, 24.312496, 153.947754, 24.319443, 153.952759, 24.321384, 153.960236, 24.321663, 153.96579, 24.31361, 153.96579, 24.309441, 153.963013, 24.29833, 153.958588, 24.295])}}"""
        assert jpn[0].script == exp

    @pytest.mark.skipif(
        "shapely.geometry" not in sys.modules, reason="requires Shapely"
    )
    def test_viewer(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.entities.add(cesiumpy.countries.abw)
        res = v.to_html()
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="https://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({polygon : {hierarchy : Cesium.Cartesian3.fromDegreesArray([-69.882233, 12.41111, -69.946945, 12.436666, -70.056122, 12.534443, -70.059448, 12.538055, -70.060287, 12.544167, -70.063339, 12.621666, -70.063065, 12.628611, -70.058899, 12.631109, -70.053345, 12.629721, -70.035278, 12.61972, -70.031113, 12.616943, -69.932236, 12.528055, -69.896957, 12.480833, -69.891403, 12.472221, -69.885559, 12.457777, -69.873901, 12.421944, -69.873337, 12.415833, -69.876114, 12.411665, -69.882233, 12.41111])}});
  widget.zoomTo(widget.entities);
</script>"""
        assert res == exp


######################################################################################################################################################
