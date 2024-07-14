# Apache License 2.0

import cesiumpy


class TestMath:
    def test_constant(self):
        # check constant can be loaded from root namespace
        pi = cesiumpy.Math.PI
        assert pi.script == "Cesium.Math.PI"

        rad = cesiumpy.Math.RADIANS_PER_DEGREE
        assert rad.script == "Cesium.Math.RADIANS_PER_DEGREE"
