# Apache License 2.0

from __future__ import unicode_literals

import traitlets

import cesiumpy
import cesiumpy.constants as constants
from cesiumpy.entities.entity import _CesiumEntity
from cesiumpy.entities.material import Material
import cesiumpy.entities.cartesian as cartesian
from cesiumpy.util.trait import MaybeTrait


class Polyline(_CesiumEntity):
    """
    PolylineGraphics

    Parameters
    ----------

    positions : Cartesian3
        A Property specifying the array of Cartesian3 positions that define the line strip.
    follow_surface : bool, default True
        A boolean Property specifying whether the line segments should be great arcs or linearly connected.
    width : float, default 1.
        A numeric Property specifying the width in pixels.
    show : bool, default True
        A boolean Property specifying the visibility of the polyline.
    material : cesiumpy.cesiumpy.color.Color, default WHITE
        A Property specifying the material used to draw the polyline.
    granularity : float, default cesiumpy.math.RADIANS_PER_DEGREE
        A numeric Property specifying the angular distance between each latitude and longitude if follow_surface is true.
    """

    # Definitions

    _klass = "polyline"

    _props = [
        "positions",
        "arc_type",
        "follow_surface",
    ]

    positions = traitlets.Instance(klass=cartesian.Cartesian3Array)
    arc_type = traitlets.Instance(klass=constants.ArcType, allow_none=True)
    follow_surface = traitlets.Bool(allow_none=True)

    # Constructor

    def __init__(
        self,
        positions,
        arc_type=None,
        follow_surface=None,
        width=None,
        show=None,
        material=None,
        granularity=None,
        name=None,
    ) -> None:
        super().__init__(
            width=width,
            show=show,
            material=material,
            granularity=granularity,
            name=name,
        )

        if not isinstance(positions, cartesian.Cartesian3Array):
            self.positions = cartesian.Cartesian3.fromDegreesArray(positions)
        else:
            self.positions = positions

        self.arc_type = arc_type
        self.follow_surface = follow_surface


class PolylineArrowMaterialProperty(Material):
    # Definitions

    _props = [
        "color",
    ]

    color = MaybeTrait(klass=cesiumpy.color.Color, allow_none=True)

    # Constructor

    def __init__(self, color=None) -> None:
        super().__init__()

        self.color = color

    # Methods

    def generate_script(self, widget=None) -> str:
        return f"new {self._klass}({self.color.generate_script(widget = widget)})"
