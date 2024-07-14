# Apache License 2.0

from __future__ import unicode_literals

from cesiumpy.entities.entity import _CesiumEntity
import cesiumpy.entities.cartesian as cartesian
from cesiumpy.util.trait import MaybeTrait


class Box(_CesiumEntity):
    """
    BoxGraphics

    Parameters
    ----------

    position: Cartesian3
        A Property specifying the Cartesian3 positions.
    dimensions: Cartesian3
        A Cartesian3 Property specifying the length, width, and height of the box.
    show: bool, default True
        A boolean Property specifying the visibility of the box.
    fill: bool, default True
        A boolean Property specifying whether the box is filled with the provided material.
    material: cesiumpy.cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the box.
    outline: bool, default False
        A boolean Property specifying whether the box is outlined.
    outline_color: cesiumpy.cesiumpy.color.Color, default BLACK
        A Property specifying the Color of the outline.
    outline_width: float, default 1.
        A numeric Property specifying the width of the outline.
    """

    # Definitions

    _klass = "box"

    _props = [
        "dimensions",
        "shadows",
    ]

    dimensions = MaybeTrait(klass=cartesian.Cartesian3)
    # shadows = MaybeTrait(klass = ShadowMode)

    # Constructor

    def __init__(
        self,
        position,
        dimensions,
        orientation=None,
        show=None,
        fill=None,
        material=None,
        outline=None,
        outline_color=None,
        outline_width=None,
        shadows=None,
        name=None,
        **kwargs,
    ) -> None:
        super().__init__(
            show=show,
            fill=fill,
            material=material,
            outline=outline,
            outline_color=outline_color,
            outline_width=outline_width,
            position=position,
            orientation=orientation,
            name=name,
            **kwargs,
        )

        self.dimensions = dimensions
        self.shadows = shadows
