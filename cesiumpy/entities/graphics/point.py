# Apache License 2.0

from __future__ import unicode_literals

import traitlets

import cesiumpy
from cesiumpy.entities.entity import _CesiumEntity


class Point(_CesiumEntity):
    """
    PointGraphics

    Parameters
    ----------

    position: Cartesian3
        A Property specifying the Cartesian3 positions.
    color: Color, default WHITE
        A Property specifying the Color of the point.
    pixel_size: int, default 10
        A numeric Property specifying the size in pixels.
    outline_color: Color, default BLACK
        A Property specifying the Color of the outline.
    outline_width: int, default 0
        A numeric Property specifying the the outline width in pixels.
    show: bool, default True
        A boolean Property specifying the visibility of the point.
    scale_by_distance:
        A NearFarScalar Property used to scale the point based on distance.
    translucency_by_distance:
        A NearFarScalar Property used to set translucency based on distance from the camera.
    """

    # Definitions

    _klass = "point"

    _props = [
        "pixel_size",
    ]

    pixel_size = traitlets.Float(allow_none=True)

    # Constructor

    def __init__(
        self,
        position,
        color=None,
        pixel_size=None,
        outline_color=None,
        outline_width=None,
        show=None,
        scale_by_distance=None,
        translucency_by_distance=None,
        name=None,
        **kwargs,
    ) -> None:
        super().__init__(
            show=show,
            color=color or cesiumpy.color.WHITE,
            outline_color=outline_color,
            outline_width=outline_width,
            scale_by_distance=scale_by_distance,
            translucency_by_distance=translucency_by_distance,
            position=position,
            name=name,
            **kwargs,
        )

        self.pixel_size = pixel_size if pixel_size is not None else 10
