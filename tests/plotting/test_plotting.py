# Apache License 2.0

import pytest

import cesiumpy

import pandas as pd

import numpy as np


class TestScatter:
    def test_scatter_xy(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.scatter([130, 140, 150], [30, 40, 50])
        assert isinstance(v, cesiumpy.Viewer)

        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), point: {color: Cesium.Color.WHITE}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), point: {color: Cesium.Color.WHITE}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), point: {color: Cesium.Color.WHITE}});"""
        assert exp in v.to_html()

    def test_scatter_xyz(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.scatter([130, 140, 150], [30, 40, 50], [1e05, 2e05, 3e05])
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 100000.0), point: {color: Cesium.Color.WHITE}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 200000.0), point: {color: Cesium.Color.WHITE}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 300000.0), point: {color: Cesium.Color.WHITE}});"""
        assert exp in v.to_html()

    def test_scatter_xy_color_scalar(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.scatter([130, 140, 150], [30, 40, 50], color=cesiumpy.color.BLUE)
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), point: {color: Cesium.Color.BLUE}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), point: {color: Cesium.Color.BLUE}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), point: {color: Cesium.Color.BLUE}});"""
        assert exp in v.to_html()

    def test_scatter_xy_color_list(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.scatter(
            [130, 140, 150],
            [30, 40, 50],
            color=[cesiumpy.color.BLUE, cesiumpy.color.RED, cesiumpy.color.GREEN],
        )
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), point: {color: Cesium.Color.BLUE}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), point: {color: Cesium.Color.RED}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), point: {color: Cesium.Color.GREEN}});"""
        assert exp in v.to_html()

    def test_scatter_xy_size_scalar(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.scatter([130, 140, 150], [30, 40, 50], size=50)
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), point: {pixelSize: 50.0, color: Cesium.Color.WHITE}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), point: {pixelSize: 50.0, color: Cesium.Color.WHITE}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), point: {pixelSize: 50.0, color: Cesium.Color.WHITE}});"""
        assert exp in v.to_html()

    def test_scatter_xy_size_list(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.scatter([130, 140, 150], [30, 40, 50], size=[20, 30, 40])
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), point: {pixelSize: 20.0, color: Cesium.Color.WHITE}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), point: {pixelSize: 30.0, color: Cesium.Color.WHITE}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), point: {pixelSize: 40.0, color: Cesium.Color.WHITE}});"""
        assert exp in v.to_html()

    def test_scatter_errors(self):
        v = cesiumpy.Viewer(id="viewertest")

        msg = "y must be list-likes: 0"
        with pytest.raises(ValueError, match=msg):
            v.plot.scatter([130, 140, 150], 0)

        msg = "y length must be 3: "
        with pytest.raises(ValueError, match=msg):
            v.plot.scatter([130, 140, 150], [30, 40])

        msg = "size length must be 3: "
        with pytest.raises(ValueError, match=msg):
            v.plot.scatter([130, 140, 150], [30, 40, 50], size=[1, 2])

    def test_scatter_pandas(self):
        try:
            import pandas as pd
        except:
            return

        df = pd.DataFrame(
            {
                "lon": [130, 140, 150],
                "lat": [50, 60, 70],
                "r": [10, 20, 30],
                "c": ["r", "g", "b"],
            }
        )
        # we can't use size column
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.scatter(x=df.lon, y=df.lat, size=df.r)
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 50.0, 0.0), point: {pixelSize: 10.0, color: Cesium.Color.WHITE}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 60.0, 0.0), point: {pixelSize: 20.0, color: Cesium.Color.WHITE}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 70.0, 0.0), point: {pixelSize: 30.0, color: Cesium.Color.WHITE}});"""
        assert exp in v.to_html()

        v = cesiumpy.Viewer(id="viewertest")
        v.plot.scatter(x=df.lon, y=df.lat, size=df.r, color=df.c)
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 50.0, 0.0), point: {pixelSize: 10.0, color: Cesium.Color.RED}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 60.0, 0.0), point: {pixelSize: 20.0, color: Cesium.Color.GREEN}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 70.0, 0.0), point: {pixelSize: 30.0, color: Cesium.Color.BLUE}});"""
        assert exp in v.to_html()


class TestBar:
    def test_bar_xyz(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.bar([130, 140, 150], [30, 40, 50], [10e5, 20e5, 30e5])
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 500000.0), cylinder: {length: 1000000.0, topRadius: 10000.0, bottomRadius: 10000.0}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 1000000.0), cylinder: {length: 2000000.0, topRadius: 10000.0, bottomRadius: 10000.0}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 1500000.0), cylinder: {length: 3000000.0, topRadius: 10000.0, bottomRadius: 10000.0}});
    """
        assert exp in v.to_html()

    def test_bar_color_scalar(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.bar(
            [130, 140, 150], [30, 40, 50], [10e5, 20e5, 30e5], color=cesiumpy.color.BLUE
        )
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 500000.0), cylinder: {length: 1000000.0, topRadius: 10000.0, bottomRadius: 10000.0, material: Cesium.Color.BLUE}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 1000000.0), cylinder: {length: 2000000.0, topRadius: 10000.0, bottomRadius: 10000.0, material: Cesium.Color.BLUE}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 1500000.0), cylinder: {length: 3000000.0, topRadius: 10000.0, bottomRadius: 10000.0, material: Cesium.Color.BLUE}});"""
        assert exp in v.to_html()

    def test_bar_color_list(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.bar(
            [130, 140, 150],
            [30, 40, 50],
            [10e5, 20e5, 30e5],
            color=[cesiumpy.color.BLUE, cesiumpy.color.RED, cesiumpy.color.GREEN],
        )
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 500000.0), cylinder: {length: 1000000.0, topRadius: 10000.0, bottomRadius: 10000.0, material: Cesium.Color.BLUE}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 1000000.0), cylinder: {length: 2000000.0, topRadius: 10000.0, bottomRadius: 10000.0, material: Cesium.Color.RED}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 1500000.0), cylinder: {length: 3000000.0, topRadius: 10000.0, bottomRadius: 10000.0, material: Cesium.Color.GREEN}});"""
        assert exp in v.to_html()

    def test_bar_size_scalar(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.bar([130, 140, 150], [30, 40, 50], [10e5, 20e5, 30e5], size=1e5)
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 500000.0), cylinder: {length: 1000000.0, topRadius: 100000.0, bottomRadius: 100000.0}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 1000000.0), cylinder: {length: 2000000.0, topRadius: 100000.0, bottomRadius: 100000.0}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 1500000.0), cylinder: {length: 3000000.0, topRadius: 100000.0, bottomRadius: 100000.0}});"""
        assert exp in v.to_html()

    def test_bar_size_list(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.bar(
            [130, 140, 150], [30, 40, 50], [10e5, 20e5, 30e5], size=[1e3, 1e4, 1e5]
        )
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 500000.0), cylinder: {length: 1000000.0, topRadius: 1000.0, bottomRadius: 1000.0}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 1000000.0), cylinder: {length: 2000000.0, topRadius: 10000.0, bottomRadius: 10000.0}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 1500000.0), cylinder: {length: 3000000.0, topRadius: 100000.0, bottomRadius: 100000.0}});"""
        assert exp in v.to_html()

    def test_bar_bottom(self):
        v = cesiumpy.Viewer("viewertest")
        v.plot.bar(
            [130, 140, 150], [30, 40, 50], [10e5, 20e5, 30e5], color=cesiumpy.color.RED
        )
        v.plot.bar(
            [130, 140, 150],
            [30, 40, 50],
            [30e5, 20e5, 10e5],
            color=cesiumpy.color.BLUE,
            bottom=[10e5, 20e5, 30e5],
        )
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 500000.0), cylinder: {length: 1000000.0, topRadius: 10000.0, bottomRadius: 10000.0, material: Cesium.Color.RED}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 1000000.0), cylinder: {length: 2000000.0, topRadius: 10000.0, bottomRadius: 10000.0, material: Cesium.Color.RED}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 1500000.0), cylinder: {length: 3000000.0, topRadius: 10000.0, bottomRadius: 10000.0, material: Cesium.Color.RED}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 2500000.0), cylinder: {length: 3000000.0, topRadius: 10000.0, bottomRadius: 10000.0, material: Cesium.Color.BLUE}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 3000000.0), cylinder: {length: 2000000.0, topRadius: 10000.0, bottomRadius: 10000.0, material: Cesium.Color.BLUE}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 3500000.0), cylinder: {length: 1000000.0, topRadius: 10000.0, bottomRadius: 10000.0, material: Cesium.Color.BLUE}});"""
        assert exp in v.to_html()

    def test_bar_pandas(self):
        try:
            import pandas as pd
        except:
            return

        df = pd.DataFrame(
            {
                "lon": [130, 140, 150],
                "lat": [50, 60, 70],
                "h": [1e5, 2e5, 3e5],
                "c": ["r", "g", "b"],
            }
        )
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.bar(x=df.lon, y=df.lat, z=df.h, color=df.c)
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 50.0, 50000.0), cylinder: {length: 100000.0, topRadius: 10000.0, bottomRadius: 10000.0, material: Cesium.Color.RED}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 60.0, 100000.0), cylinder: {length: 200000.0, topRadius: 10000.0, bottomRadius: 10000.0, material: Cesium.Color.GREEN}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 70.0, 150000.0), cylinder: {length: 300000.0, topRadius: 10000.0, bottomRadius: 10000.0, material: Cesium.Color.BLUE}});"""
        assert exp in v.to_html()


class TestLabel:
    def test_label_xy(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.label(["A", "B", "C"], [130, 140, 150], [30, 40, 50])
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), label: {text: "A"}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), label: {text: "B"}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), label: {text: "C"}});"""
        assert exp in v.to_html()

    def test_label_xyz(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.label(["A", "B", "C"], [130, 140, 150], [30, 40, 50], 10e5)
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 1000000.0), label: {text: "A"}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 1000000.0), label: {text: "B"}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 1000000.0), label: {text: "C"}});"""
        assert exp in v.to_html()

    def test_label_xyz_list(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.label(["A", "B", "C"], [130, 140, 150], [30, 40, 50], [10e4, 10e5, 10e4])
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 100000.0), label: {text: "A"}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 1000000.0), label: {text: "B"}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 100000.0), label: {text: "C"}});"""
        assert exp in v.to_html()

    def test_label_color_scalar(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.label(
            ["A", "B", "C"], [130, 140, 150], [30, 40, 50], color=cesiumpy.color.GREEN
        )
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), label: {text: "A", fillColor: Cesium.Color.GREEN}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), label: {text: "B", fillColor: Cesium.Color.GREEN}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), label: {text: "C", fillColor: Cesium.Color.GREEN}});"""
        assert exp in v.to_html()

    def test_label_color_list(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.label(
            ["A", "B", "C"],
            [130, 140, 150],
            [30, 40, 50],
            color=[cesiumpy.color.BLUE, cesiumpy.color.RED, cesiumpy.color.GREEN],
        )
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), label: {text: "A", fillColor: Cesium.Color.BLUE}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), label: {text: "B", fillColor: Cesium.Color.RED}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), label: {text: "C", fillColor: Cesium.Color.GREEN}});"""
        assert exp in v.to_html()

    def test_label_size_scalar(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.label(["A", "B", "C"], [130, 140, 150], [30, 40, 50], size=2)
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), label: {text: "A", scale: 2.0}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), label: {text: "B", scale: 2.0}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), label: {text: "C", scale: 2.0}});"""
        assert exp in v.to_html()

    def test_label_size_list(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.label(["A", "B", "C"], [130, 140, 150], [30, 40, 50], size=[2, 3, 0.5])
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), label: {text: "A", scale: 2.0}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), label: {text: "B", scale: 3.0}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), label: {text: "C", scale: 0.5}});"""
        assert exp in v.to_html()

    def test_label_pandas(self):
        try:
            import pandas as pd
        except:
            return

        df = pd.DataFrame(
            {
                "lon": [130, 140, 150],
                "lat": [50, 60, 70],
                "s": [1, 2, 3],
                "label": ["a", "b", "c"],
                "c": ["r", "g", "b"],
            }
        )
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.label(df.label, x=df.lon, y=df.lat, size=df.s, color=df.c)
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 50.0, 0.0), label: {text: "a", fillColor: Cesium.Color.RED, scale: 1.0}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 60.0, 0.0), label: {text: "b", fillColor: Cesium.Color.GREEN, scale: 2.0}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 70.0, 0.0), label: {text: "c", fillColor: Cesium.Color.BLUE, scale: 3.0}});"""
        assert exp in v.to_html()


@pytest.mark.skip(reason="script property not imeplemented")
class TestPin:
    def test_pin_xy(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.pin([130, 140, 150], [30, 40, 50])
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), billboard: {image: new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0)}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), billboard: {image: new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0)}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), billboard: {image: new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0)}});"""
        assert exp in v.to_html()

    def test_pin_xyz(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.pin([130, 140, 150], [30, 40, 50], z=1e6)
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 1000000.0), billboard: {image: new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0)}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 1000000.0), billboard: {image: new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0)}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 1000000.0), billboard: {image: new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0)}});"""
        assert exp in v.to_html()

    def test_pin_xyz_list(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.pin([130, 140, 150], [30, 40, 50], [10e4, 10e5, 10e4])
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 100000.0), billboard: {image: new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0)}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 1000000.0), billboard: {image: new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0)}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 100000.0), billboard: {image: new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0)}});"""
        assert exp in v.to_html()

    def test_pin_color_scalar(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.pin([130, 140, 150], [30, 40, 50], color=cesiumpy.color.GREEN)
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), billboard: {image: new Cesium.PinBuilder().fromColor(Cesium.Color.GREEN, 48.0)}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), billboard: {image: new Cesium.PinBuilder().fromColor(Cesium.Color.GREEN, 48.0)}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), billboard: {image: new Cesium.PinBuilder().fromColor(Cesium.Color.GREEN, 48.0)}});"""
        assert exp in v.to_html()

    def test_pin_color_list(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.pin(
            [130, 140, 150],
            [30, 40, 50],
            color=[cesiumpy.color.BLUE, cesiumpy.color.RED, cesiumpy.color.GREEN],
        )
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), billboard: {image: new Cesium.PinBuilder().fromColor(Cesium.Color.BLUE, 48.0)}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), billboard: {image: new Cesium.PinBuilder().fromColor(Cesium.Color.RED, 48.0)}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), billboard: {image: new Cesium.PinBuilder().fromColor(Cesium.Color.GREEN, 48.0)}});"""
        assert exp in v.to_html()

    def test_pin_size_scalar(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.pin([130, 140, 150], [30, 40, 50], size=24)
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), billboard: {image: new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 24.0)}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), billboard: {image: new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 24.0)}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), billboard: {image: new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 24.0)}});"""
        assert exp in v.to_html()

    def test_pin_size_list(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.pin([130, 140, 150], [30, 40, 50], size=[12, 24, 48])
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), billboard: {image: new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 12.0)}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), billboard: {image: new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 24.0)}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), billboard: {image: new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0)}});"""
        assert exp in v.to_html()

    def test_pin_label_scalar(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.pin([130, 140, 150], [30, 40, 50], text="!")
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), billboard: {image: new Cesium.PinBuilder().fromText("!", Cesium.Color.ROYALBLUE, 48.0)}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), billboard: {image: new Cesium.PinBuilder().fromText("!", Cesium.Color.ROYALBLUE, 48.0)}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), billboard: {image: new Cesium.PinBuilder().fromText("!", Cesium.Color.ROYALBLUE, 48.0)}});"""
        assert exp in v.to_html()

    def test_pin_label_list(self):
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.pin([130, 140, 150], [30, 40, 50], text=["!", "?", "XXX"])
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), billboard: {image: new Cesium.PinBuilder().fromText("!", Cesium.Color.ROYALBLUE, 48.0)}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), billboard: {image: new Cesium.PinBuilder().fromText("?", Cesium.Color.ROYALBLUE, 48.0)}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), billboard: {image: new Cesium.PinBuilder().fromText("XXX", Cesium.Color.ROYALBLUE, 48.0)}});"""
        assert exp in v.to_html()


class TestNumpyLike:
    def test_scatter_xy(self):
        try:
            import numpy as np
        except:
            return

        v = cesiumpy.Viewer(id="viewertest")
        res = v.plot.scatter(np.array([130, 140, 150]), np.array([30, 40, 50]))
        assert isinstance(v, cesiumpy.Viewer)

        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), point: {color: Cesium.Color.WHITE}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), point: {color: Cesium.Color.WHITE}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), point: {color: Cesium.Color.WHITE}});"""
        # entities must be added to original instance
        assert exp in v.to_html()

    def test_scatter_array_interface(self):
        try:
            import numpy as np
        except:
            return

        class ExtendedArray(object):
            def __init__(self, values):
                self.values = values

            def __array__(self):
                return np.array(self.values)

        v = cesiumpy.Viewer(id="viewertest")
        res = v.plot.scatter(
            ExtendedArray([130, 140, 150]), ExtendedArray([30, 40, 50])
        )
        assert isinstance(v, cesiumpy.Viewer)

        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), point: {color: Cesium.Color.WHITE}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), point: {color: Cesium.Color.WHITE}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), point: {color: Cesium.Color.WHITE}});"""
        assert exp in v.to_html()


class TestContour:
    def test_contour_xyz(self):
        try:
            import numpy as np
            import matplotlib.mlab as mlab
        except:
            return

        delta = 0.025
        x = np.arange(-3.0, 3.0, delta)
        y = np.arange(-2.0, 2.0, delta)
        X, Y = np.meshgrid(x, y)
        Z1 = mlab.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
        Z2 = mlab.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
        # difference of Gaussians
        Z = 10.0 * (Z2 - Z1)

        viewer = cesiumpy.Viewer()
        viewer.plot.contour(X, Y, Z)
        assert len(viewer.entities) == 7
        assert all(isinstance(x, cesiumpy.Polyline) for x in viewer.entities)
        assert viewer.entities[0].material == cesiumpy.color.Color(0.0, 0.0, 0.5, 1.0)

    @pytest.mark.skip(reason="Pin script not implemented")
    def test_pin_pandas(self):
        df = pd.DataFrame(
            {
                "lon": [130, 140, 150],
                "lat": [50, 60, 70],
                "s": [10, 20, 30],
                "label": ["a", "b", "c"],
                "c": ["r", "g", "b"],
            }
        )
        v = cesiumpy.Viewer(id="viewertest")
        v.plot.pin(x=df.lon, y=df.lat, size=df.s, color=df.c, text=df.label)
        exp = """    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(130.0, 50.0, 0.0), billboard: {image: new Cesium.PinBuilder().fromText("a", Cesium.Color.RED, 10.0)}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(140.0, 60.0, 0.0), billboard: {image: new Cesium.PinBuilder().fromText("b", Cesium.Color.GREEN, 20.0)}});
    widget.entities.add({position: Cesium.Cartesian3.fromDegrees(150.0, 70.0, 0.0), billboard: {image: new Cesium.PinBuilder().fromText("c", Cesium.Color.BLUE, 30.0)}});"""
        assert exp in v.to_html()
