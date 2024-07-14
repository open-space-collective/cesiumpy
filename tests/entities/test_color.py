# Apache License 2.0

import pytest

import traitlets

import cesiumpy


class TestColor:
    def test_maybe_color(self):
        blue = cesiumpy.color.Color.maybe("blue")
        assert repr(blue) == "Color.BLUE"
        assert blue.script == "Cesium.Color.BLUE"

        red = cesiumpy.color.Color.maybe("RED")
        assert repr(red) == "Color.RED"
        assert red.script == "Cesium.Color.RED"

        msg = "Unable to convert to Color instance: "
        with pytest.raises(ValueError, match=msg):
            cesiumpy.color.Color.maybe("NamedColor")

        msg = "Unable to convert to Color instance: "
        with pytest.raises(ValueError, match=msg):
            cesiumpy.color.Color.maybe("x")

        msg = "Unable to convert to Color instance: "
        with pytest.raises(ValueError, match=msg):
            cesiumpy.color.Color.maybe(1)

    def test_maybe_color_listlike(self):
        # tuple
        c = cesiumpy.color.Color.maybe((0.5, 0.3, 0.5))
        assert repr(c) == "Color(0.5, 0.3, 0.5)"
        assert c.script == "Cesium.Color(0.5, 0.3, 0.5)"

        c = cesiumpy.color.Color.maybe((0.5, 0.3, 0.5, 0.2))
        assert repr(c) == "Color(0.5, 0.3, 0.5, 0.2)"
        assert c.script == "Cesium.Color(0.5, 0.3, 0.5, 0.2)"

        # do not convert
        msg = "Unable to convert to Color instance: "
        with pytest.raises(ValueError, match=msg):
            cesiumpy.color.Color.maybe((0.5, 0.3))

        msg = "Unable to convert to Color instance: "
        with pytest.raises(ValueError, match=msg):
            cesiumpy.color.Color.maybe((0.5, 0.3, 0.2, 0.1, 0.5))

    def test_named_colors(self):
        aqua = cesiumpy.color.AQUA
        exp = "Color.AQUA"
        assert repr(aqua) == exp
        assert aqua.name == "AQUA"
        exp = "Cesium.Color.AQUA"
        assert aqua.script == exp

        aqua = aqua.set_alpha(0.5)
        exp = "Color.AQUA.withAlpha(0.5)"
        assert repr(aqua) == exp
        assert aqua.name == "AQUA"
        exp = "Cesium.Color.AQUA.withAlpha(0.5)"
        assert aqua.script == exp

        # confirm set_alpha modifies the constant
        aqua = cesiumpy.color.AQUA
        exp = "Color.AQUA"
        assert repr(aqua) == exp
        assert aqua.name == "AQUA"
        exp = "Cesium.Color.AQUA"
        assert aqua.script == exp

        blue = cesiumpy.color.BLUE
        exp = "Color.BLUE"
        assert repr(blue) == exp
        assert blue.name == "BLUE"
        exp = "Cesium.Color.BLUE"
        assert blue.script == exp

    def test_single_char_color(self):
        _m = cesiumpy.color.Color.maybe
        assert _m("b") == cesiumpy.color.BLUE
        assert _m("g") == cesiumpy.color.GREEN
        assert _m("r") == cesiumpy.color.RED
        assert _m("c") == cesiumpy.color.CYAN
        assert _m("m") == cesiumpy.color.MAGENTA
        assert _m("y") == cesiumpy.color.YELLOW
        assert _m("k") == cesiumpy.color.BLACK
        assert _m("w") == cesiumpy.color.WHITE

        assert _m("B") == cesiumpy.color.BLUE
        assert _m("G") == cesiumpy.color.GREEN
        assert _m("R") == cesiumpy.color.RED
        assert _m("C") == cesiumpy.color.CYAN
        assert _m("M") == cesiumpy.color.MAGENTA
        assert _m("Y") == cesiumpy.color.YELLOW
        assert _m("K") == cesiumpy.color.BLACK
        assert _m("W") == cesiumpy.color.WHITE

    def test_alpha(self):
        aqua = cesiumpy.color.AQUA

        res = aqua.set_alpha(0.3)
        exp = "Cesium.Color.AQUA.withAlpha(0.3)"
        assert res.script == exp

        res = aqua.with_alpha(0.3)
        exp = "Cesium.Color.AQUA.withAlpha(0.3)"
        assert res.script == exp

        res = aqua.with_alpha(1.0)
        exp = "Cesium.Color.AQUA.withAlpha(1.0)"
        assert res.script == exp

        res = aqua.with_alpha(0.0)
        exp = "Cesium.Color.AQUA.withAlpha(0.0)"
        assert res.script == exp

        msg = "The value of the 'alpha' trait of a ColorConstant instance should"
        with pytest.raises(traitlets.TraitError, match=msg):
            aqua.with_alpha(1.1)

    def test_rgb(self):
        c = cesiumpy.color.Color(1, 0, 0)
        exp = "Cesium.Color(1.0, 0.0, 0.0)"
        assert c.script == exp

        c = cesiumpy.color.Color(1, 0, 0, 0.5)
        exp = "Cesium.Color(1.0, 0.0, 0.0, 0.5)"
        assert c.script == exp

        c = cesiumpy.color.Color.from_bytes(255, 0, 255)
        exp = "Cesium.Color(1.0, 0.0, 1.0)"
        assert c.script == exp

        c = cesiumpy.color.Color.from_bytes(255, 0, 255, 255)
        exp = "Cesium.Color(1.0, 0.0, 1.0, 1.0)"
        assert c.script == exp

    def test_color_string(self):
        c = cesiumpy.color.Color.from_string("#FF0000")
        exp = """Cesium.Color.fromCSSColorString("#FF0000")"""
        assert c.script == exp

    def test_random(self):
        c = cesiumpy.color.choice()
        assert isinstance(c, cesiumpy.color.Color)

        colors = cesiumpy.color.sample(5)
        assert isinstance(colors, list)
        assert len(colors) == 5
        assert all(isinstance(c, cesiumpy.color.Color) for c in colors)

    def test_cmap(self):
        try:
            import matplotlib.pyplot as plt
        except:
            return

        mpl_cmap = plt.get_cmap("winter")
        cmap = cesiumpy.color.get_cmap("winter")

        exp = """ColorMap("winter")"""
        assert repr(cmap) == exp

        res = cmap(3)
        exp = mpl_cmap(3)
        assert res.red == exp[0]
        assert res.green == exp[1]
        assert res.blue == exp[2]
        assert res.alpha == exp[3]

        res = cmap([2, 4])
        exp = mpl_cmap([2, 4])
        for r, e in zip(res, exp):
            assert r.red == e[0]
            assert r.green == e[1]
            assert r.blue == e[2]
            assert r.alpha == e[3]
