# Apache License 2.0

import pytest

import cesiumpy
import cesiumpy.entities.cartesian as cartesian


class TestCartesian:
    def test_cartesian2(self):
        c = cesiumpy.Cartesian2(5, 10)
        exp = "Cesium.Cartesian2(5.0, 10.0)"
        assert c.script == exp

        c = cesiumpy.Cartesian2.fromDegrees(5, 10)
        exp = "Cesium.Cartesian2.fromDegrees(5.0, 10.0)"
        assert c.script == exp

        with pytest.raises(ValueError):
            cesiumpy.Cartesian2.fromDegrees(200, 10)

        with pytest.raises(ValueError):
            cesiumpy.Cartesian2.fromDegrees(50, 100)

    def test_cartesian2_repr(self):
        c = cesiumpy.Cartesian2(5, 10)
        exp = "Cartesian2(5.0, 10.0)"
        assert repr(c) == exp

        c = cesiumpy.Cartesian2.fromDegrees(5, 10)
        exp = "Cartesian2.fromDegrees(5.0, 10.0)"
        assert repr(c) == exp

    def test_cartesian3(self):
        c = cesiumpy.Cartesian3(5, 10, 20)
        exp = "Cesium.Cartesian3(5.0, 10.0, 20.0)"
        assert c.script == exp

        c = cesiumpy.Cartesian3.fromDegrees(5, 10, 20)
        exp = "Cesium.Cartesian3.fromDegrees(5.0, 10.0, 20.0)"
        assert c.script == exp

        msg = "x must be longitude, between -180 to 180"
        with pytest.raises(ValueError, match=msg):
            cesiumpy.Cartesian3.fromDegrees(200, 10, 20)

        msg = "y must be latitude, between -90 to 90"
        with pytest.raises(ValueError, match=msg):
            cesiumpy.Cartesian3.fromDegrees(50, 100, 20)

    def test_cartesian3_repr(self):
        c = cesiumpy.Cartesian3(5, 10, 20)
        exp = "Cartesian3(5.0, 10.0, 20.0)"
        assert repr(c) == exp

        c = cesiumpy.Cartesian3.fromDegrees(5, 10, 20)
        exp = "Cartesian3.fromDegrees(5.0, 10.0, 20.0)"
        assert repr(c) == exp

    def test_cartesian3_array(self):
        c = cesiumpy.Cartesian3.fromDegreesArray([1, 2, 3, 4, 5, 6])
        exp = "Cesium.Cartesian3.fromDegreesArrayHeights([1, 2, 3, 4, 5, 6])"
        assert c.script == exp

        # we can pass tuple
        c = cesiumpy.Cartesian3.fromDegreesArray([(1, 2, 3), (4, 5, 6)])
        assert c.script == exp

        msg = "x must be a list consists from longitude and latitude"
        with pytest.raises(ValueError, match=msg):
            cesiumpy.Cartesian3.fromDegreesArray([10, 20, 0.0, 200, 20, 0.0])

        with pytest.raises(ValueError, match=msg):
            cesiumpy.Cartesian3.fromDegreesArray([(10, 20, 0.0), (200, 20, 0.0)])

        try:
            import geopy

            # string causes geocode search
            with pytest.raises(ValueError):
                cesiumpy.Cartesian3.fromDegreesArray([("X", 20), (20, 20)])
        except (
            geopy.exc.GeocoderQuotaExceeded,
            geopy.exc.GeocoderUnavailable,
            geopy.exc.GeocoderServiceError,
        ):
            pass

        msg = "x must be a list consists from longitude and latitude"
        with pytest.raises(ValueError, match=msg):
            cesiumpy.Cartesian3.fromDegreesArray([10, 20, 0.0, 20, 91, 0.0])

    def test_cartesian4(self):
        c = cesiumpy.Cartesian4(5, 10, 20, 30)
        exp = "Cesium.Cartesian4(5.0, 10.0, 20.0, 30.0)"
        assert c.script == exp

        c = cesiumpy.Cartesian4.fromDegrees(5, 10, 20, 30)
        exp = "Cesium.Cartesian4.fromDegrees(5.0, 10.0, 20.0, 30.0)"
        assert c.script == exp

        msg = "x must be longitude, between -180 to 180"
        with pytest.raises(ValueError, match=msg):
            cesiumpy.Cartesian4.fromDegrees(200, 10, 20, 50)

        msg = "y must be latitude, between -90 to 90"
        with pytest.raises(ValueError, match=msg):
            cesiumpy.Cartesian4.fromDegrees(50, 100, 20, 50)

    def test_cartesian4_repr(self):
        c = cesiumpy.Cartesian4(5, 10, 20, 30)
        exp = "Cartesian4(5.0, 10.0, 20.0, 30.0)"
        assert repr(c) == exp

        c = cesiumpy.Cartesian4.fromDegrees(5, 10, 20, 30)
        exp = "Cartesian4.fromDegrees(5.0, 10.0, 20.0, 30.0)"
        assert repr(c) == exp

    def test_maybe_cartesian(self):
        c = cesiumpy.entities.cartesian.Cartesian2.maybe((0, 10))
        exp = "Cesium.Cartesian2(0.0, 10.0)"
        assert c.script == exp

        c = cesiumpy.entities.cartesian.Cartesian3.maybe((0, 10, 20))
        exp = "Cesium.Cartesian3(0.0, 10.0, 20.0)"
        assert c.script == exp

        c = cesiumpy.entities.cartesian.Cartesian4.maybe((0, 10, 20, 30))
        exp = "Cesium.Cartesian4(0.0, 10.0, 20.0, 30.0)"
        assert c.script == exp

        c = cesiumpy.entities.cartesian.Cartesian2.maybe([0, 10])
        exp = "Cesium.Cartesian2(0.0, 10.0)"
        assert c.script == exp

        c = cesiumpy.entities.cartesian.Cartesian3.maybe([0, 10, 20])
        exp = "Cesium.Cartesian3(0.0, 10.0, 20.0)"
        assert c.script == exp

        c = cesiumpy.entities.cartesian.Cartesian4.maybe([0, 10, 20, 30])
        exp = "Cesium.Cartesian4(0.0, 10.0, 20.0, 30.0)"
        assert c.script == exp

        # do not convert
        res = cartesian.Cartesian2.maybe(3)
        assert res == 3

        res = cartesian.Cartesian2.maybe((1, 2, 3, 5, 5))
        assert res, (1, 2, 3, 5 == 5)

    def test_maybe_cartesian_from_degrees(self):
        c = cesiumpy.entities.cartesian.Cartesian2.maybe((0, 10), degrees=True)
        exp = "Cesium.Cartesian2.fromDegrees(0.0, 10.0)"
        assert c.script == exp

        c = cesiumpy.entities.cartesian.Cartesian3.maybe((0, 10, 20), degrees=True)
        exp = "Cesium.Cartesian3.fromDegrees(0.0, 10.0, 20.0)"
        assert c.script == exp

        c = cesiumpy.entities.cartesian.Cartesian4.maybe((0, 10, 20, 30), degrees=True)
        exp = "Cesium.Cartesian4.fromDegrees(0.0, 10.0, 20.0, 30.0)"
        assert c.script == exp

        c = cesiumpy.entities.cartesian.Cartesian2.maybe([0, 10], degrees=True)
        exp = "Cesium.Cartesian2.fromDegrees(0.0, 10.0)"
        assert c.script == exp

        c = cesiumpy.entities.cartesian.Cartesian3.maybe([0, 10, 20], degrees=True)
        exp = "Cesium.Cartesian3.fromDegrees(0.0, 10.0, 20.0)"
        assert c.script == exp

        c = cesiumpy.entities.cartesian.Cartesian4.maybe([0, 10, 20, 30], degrees=True)
        exp = "Cesium.Cartesian4.fromDegrees(0.0, 10.0, 20.0, 30.0)"
        assert c.script == exp

        # do not convert
        res = cartesian.Cartesian3.maybe(3, degrees=True)
        assert res == 3

        res = cartesian.Cartesian3.maybe((1, 2, 3, 5, 5), degrees=True)
        assert res, [1, 2, 3, 5 == 5]

    def test_rectangle(self):
        c = cartesian.Rectangle(5, 10, 20, 30)
        exp = "new Cesium.Rectangle(5.0, 10.0, 20.0, 30.0)"
        assert c.script == exp

        c = cartesian.Rectangle.fromDegrees(5, 10, 20, 30)
        exp = "Cesium.Rectangle.fromDegrees(5.0, 10.0, 20.0, 30.0)"
        assert c.script == exp

        msg = "west must be longitude, between -180 to 180"
        with pytest.raises(ValueError, match=msg):
            cartesian.Rectangle.fromDegrees(200, 10, 20, 50)

        msg = "south must be latitude, between -90 to 90"
        with pytest.raises(ValueError, match=msg):
            cartesian.Rectangle.fromDegrees(50, 100, 20, 50)

        msg = "east must be longitude, between -180 to 180"
        with pytest.raises(ValueError, match=msg):
            cartesian.Rectangle.fromDegrees(10, 10, -190, 50)

        msg = "north must be latitude, between -90 to 90"
        with pytest.raises(ValueError, match=msg):
            cartesian.Rectangle.fromDegrees(50, 20, 20, -100)

    def test_rectangle_repr(self):
        c = cartesian.Rectangle(5, 10, 20, 30)
        exp = "Rectangle(west=5.0, south=10.0, east=20.0, north=30.0)"
        assert repr(c) == exp

        c = cartesian.Rectangle.fromDegrees(5, 10, 20, 30)
        exp = "Rectangle.fromDegrees(west=5.0, south=10.0, east=20.0, north=30.0)"
        assert repr(c) == exp
