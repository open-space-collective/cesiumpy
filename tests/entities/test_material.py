# Apache License 2.0

import pytest

import re

import cesiumpy


class TestImageMaterial:
    @pytest.mark.skip(reason="script not implemented")
    def test_imagematerial(self):
        m = cesiumpy.entities.material.ImageMaterialProperty("xxx.png")
        assert repr(m) == "ImageMaterialProperty(xxx.png)"
        assert m.script == """new Cesium.ImageMaterialProperty({image : "xxx.png"})"""


class TestTempImageMaterial:
    def test_matplotlibimage(self):

        try:
            import numpy as np
            import matplotlib.pyplot as plt
        except:
            return

        img = np.random.randint(0, 255, (100, 100, 3))
        ax = plt.imshow(img)
        img = cesiumpy.entities.material.TemporaryImage(ax.figure)
        m = cesiumpy.entities.material.ImageMaterialProperty(img)
        assert re.match(
            """new Cesium\\.ImageMaterialProperty\\({image : "\w+\\.png"}\\)""",
            m.script,
        )

        img = cesiumpy.entities.material.TemporaryImage(ax)
        m = cesiumpy.entities.material.ImageMaterialProperty(img)
        assert re.match(
            """new Cesium\\.ImageMaterialProperty\\({image : "\w+\\.png"}\\)""",
            m.script,
        )
        plt.close()

        fig, axes = plt.subplots(2, 2)
        msg = "Unable to trim a Figure contains multiple Axes"
        with pytest.raises(ValueError, match=msg):
            img = cesiumpy.entities.material.TemporaryImage(fig)
            cesiumpy.entities.material.ImageMaterialProperty(img)
        plt.close()
