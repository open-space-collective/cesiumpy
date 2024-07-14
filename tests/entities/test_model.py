# Apache License 2.0

import pytest

import cesiumpy


class TestModel:
    @pytest.mark.skip(reason="script not implemented")
    def test_basic_model(self):
        m = cesiumpy.Model("xxx.gltf", model_matrix=(-100, 40, 0), scale=200)
        assert repr(m) == """Model("xxx.gltf")"""
        exp = """Cesium.Model.fromGltf({url : "xxx.gltf", modelMatrix : Cesium.Transforms.eastNorthUpToFixedFrame(Cesium.Cartesian3.fromDegrees(-100.0, 40.0, 0.0)), scale : 200.0})"""
        assert m.script == exp
