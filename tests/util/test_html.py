# Apache License 2.0


import cesiumpy.util.html as html


class TestHTML:
    def testwrap_uri(self):
        res = html.wrap_uri("https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js")
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>"""
        assert res == exp

        res = html.wrap_uri(
            "http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css"
        )
        exp = """<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">"""
        assert res == exp

    def test_wrap_script(self):
        res = html.wrap_scripts("aaa")
        exp = [
            '<script type="text/javascript">',
            "  async function init() {",
            "    aaa",
            "  }",
            "  init();",
            "</script>",
        ]
        assert res == exp

        res = html.wrap_scripts(["aaa", "bbb"])
        exp = [
            '<script type="text/javascript">',
            "  async function init() {",
            "    aaa",
            "    bbb",
            "  }",
            "  init();",
            "</script>",
        ]
        assert res == exp

    def test_add_indent(self):
        res = html._add_indent("aaa")
        exp = ["  aaa"]
        assert res == exp

        res = html._add_indent(["aaa", "bbb"])
        exp = ["  aaa", "  bbb"]
        assert res == exp

        res = html._add_indent(["aaa", "bbb"], indent=3)
        exp = ["   aaa", "   bbb"]
        assert res == exp
