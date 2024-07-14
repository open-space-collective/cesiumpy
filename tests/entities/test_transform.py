# Apache License 2.0

import cesiumpy


class TestTransform:
    def test_transform(self):
        c = cesiumpy.Cartesian3(1, 1, 1)
        res = cesiumpy.Transforms.eastNorthUpToFixedFrame(c)
        exp = """Cesium.Transforms.eastNorthUpToFixedFrame(Cesium.Cartesian3(1.0, 1.0, 1.0))"""
        assert res.script == exp

        res = cesiumpy.Transforms.northEastDownToFixedFrame(c)
        exp = """Cesium.Transforms.northEastDownToFixedFrame(Cesium.Cartesian3(1.0, 1.0, 1.0))"""
        assert res.script == exp

        res = cesiumpy.Transforms.northUpEastToFixedFrame(c)
        exp = """Cesium.Transforms.northUpEastToFixedFrame(Cesium.Cartesian3(1.0, 1.0, 1.0))"""
        assert res.script == exp
