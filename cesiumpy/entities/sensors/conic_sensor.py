######################################################################################################################################################

# @project        CesiumPy
# @file           cesiumpy/entities/sensors/cylinder.py
# @license        Apache 2.0

######################################################################################################################################################

from __future__ import unicode_literals

import collections
from typing import Optional

import traitlets

import cesiumpy
from cesiumpy.base import _CesiumObject
from cesiumpy.entities.entity import _CesiumEntity
from cesiumpy.util.trait import MaybeTrait

######################################################################################################################################################


class ConicSensor(_CesiumEntity):

    """
    Conic Sensor.
    """

    # Definitons

    _klass = "conic_sensor"

    _props = [
        "radius",
        "inner_half_angle",
        "outer_half_angle",
        "lateral_surface_material",
        "minimum_clock_angle",
        "maximum_clock_angle",
        "show_intersection",
        "intersection_color",
        "intersection_width",
    ]

    radius = traitlets.Float()

    inner_half_angle = traitlets.Float()
    outer_half_angle = traitlets.Float()

    lateral_surface_material = MaybeTrait(klass=cesiumpy.color.Color, allow_none=True)

    minimum_clock_angle = traitlets.Float(allow_none=True)
    maximum_clock_angle = traitlets.Float(allow_none=True)

    show_intersection = traitlets.Bool(allow_none=True)
    intersection_color = MaybeTrait(klass=cesiumpy.color.Color, allow_none=True)
    intersection_width = traitlets.Float(allow_none=True)

    # Constructor

    def __init__(
        self,
        position,
        radius: float,
        inner_half_angle: float,
        outer_half_angle: float,
        lateral_surface_material: Optional[cesiumpy.color.Color] = None,
        minimum_clock_angle: Optional[float] = None,
        maximum_clock_angle: Optional[float] = None,
        show_intersection: Optional[bool] = None,
        intersection_color: Optional[cesiumpy.color.Color] = None,
        intersection_width: Optional[float] = None,
        orientation=None,
        show=None,
        fill=None,
        material=None,
        outline=None,
        outline_color=None,
        outline_width=None,
        number_of_vertical_lines=None,
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
            number_of_vertical_lines=number_of_vertical_lines,
            position=position,
            orientation=orientation,
            name=name,
            **kwargs,
        )

        self.radius: float = radius

        self.inner_half_angle: float = inner_half_angle
        self.outer_half_angle: float = outer_half_angle

        self.lateral_surface_material: Optional[
            cesiumpy.color.Color
        ] = lateral_surface_material

        self.minimum_clock_angle: Optional[float] = minimum_clock_angle
        self.maximum_clock_angle: Optional[float] = maximum_clock_angle

        self.show_intersection: Optional[bool] = show_intersection
        self.intersection_color: Optional[cesiumpy.color.Color] = intersection_color
        self.intersection_width: Optional[float] = intersection_width

    # Properties

    @property
    def _property_dict(self) -> dict:
        props = collections.OrderedDict()

        props["name"] = self.name
        props["position"] = self.position
        props["orientation"] = self.orientation

        props[self._klass] = ConicSensorGraphics(
            **{prop: getattr(self, prop) for prop in ConicSensorGraphics._props}
        )

        return props


######################################################################################################################################################


class ConicSensorGraphics(_CesiumObject):
    # Definitions

    _props = [
        "radius",
        "inner_half_angle",
        "outer_half_angle",
        "lateral_surface_material",
        "minimum_clock_angle",
        "maximum_clock_angle",
        "show_intersection",
        "intersection_color",
        "intersection_width",
        "show",
    ]

    radius = traitlets.Float()

    inner_half_angle = traitlets.Float()
    outer_half_angle = traitlets.Float()

    lateral_surface_material = MaybeTrait(klass=cesiumpy.color.Color, allow_none=True)

    minimum_clock_angle = traitlets.Float(allow_none=True)
    maximum_clock_angle = traitlets.Float(allow_none=True)

    show_intersection = traitlets.Bool(allow_none=True)
    intersection_color = MaybeTrait(klass=cesiumpy.color.Color, allow_none=True)
    intersection_width = traitlets.Float(allow_none=True)

    show = traitlets.Bool(allow_none=True)

    # Constructor

    def __init__(
        self,
        radius: float,
        inner_half_angle: float,
        outer_half_angle: float,
        lateral_surface_material: Optional[cesiumpy.color.Color] = None,
        minimum_clock_angle: Optional[float] = None,
        maximum_clock_angle: Optional[float] = None,
        show_intersection: Optional[bool] = None,
        intersection_color: Optional[cesiumpy.color.Color] = None,
        intersection_width: Optional[float] = None,
        show: Optional[bool] = None,
    ) -> None:
        self.radius: float = radius

        self.inner_half_angle: float = inner_half_angle
        self.outer_half_angle: float = outer_half_angle

        self.lateral_surface_material: Optional[
            cesiumpy.color.Color
        ] = lateral_surface_material

        self.minimum_clock_angle: Optional[float] = minimum_clock_angle
        self.maximum_clock_angle: Optional[float] = maximum_clock_angle

        self.show_intersection: Optional[bool] = show_intersection
        self.intersection_color: Optional[cesiumpy.color.Color] = intersection_color
        self.intersection_width: Optional[float] = intersection_width

        self.show: Optional[bool] = show

    # Methods

    def generate_script(self, widget=None) -> str:
        return f"new CesiumSensorVolumes.ConicSensorGraphics({super().generate_script(widget=widget)})"


######################################################################################################################################################
