# Apache License 2.0


from cesiumpy.util.trait import _DIV


class TestTrait:
    def test_div(self):
        div1 = _DIV()
        div2 = _DIV()
        assert div1 == div2

        div1 = _DIV(id="xxx")
        div2 = _DIV(id="xxx")
        assert div1 == div2

        assert div1.script == """<div id="xxx" style="width:100%; height:100%;"><div>"""

        div = _DIV(id="xxx", width="90%", height="60%")
        assert div.script == """<div id="xxx" style="width:90%; height:60%;"><div>"""
