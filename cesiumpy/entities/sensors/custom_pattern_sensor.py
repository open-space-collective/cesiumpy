# Apache License 2.0

from __future__ import unicode_literals

import collections
from typing import Optional

import traitlets

import cesiumpy
from cesiumpy.base import _CesiumObject
from cesiumpy.entities.entity import _CesiumEntity
from cesiumpy.util.trait import MaybeTrait


class CustomPatternSensor(_CesiumEntity):
    """
    CustomPattern Sensor.
    """

    # Definitons

    _klass = "custom_pattern_sensor"

    _props = [
        "radius",
        "directions",
        "lateral_surface_material",
        "show_intersection",
        "intersection_color",
        "intersection_width",
    ]

    radius = traitlets.Float()

    directions = traitlets.List()

    lateral_surface_material = MaybeTrait(klass=cesiumpy.color.Color, allow_none=True)

    show_intersection = traitlets.Bool(allow_none=True)
    intersection_color = MaybeTrait(klass=cesiumpy.color.Color, allow_none=True)
    intersection_width = traitlets.Float(allow_none=True)

    # Constructor

    def __init__(
        self,
        position,
        radius: float,
        directions: list[cesiumpy.Spherical],
        lateral_surface_material: Optional[cesiumpy.color.Color] = None,
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

        self.directions: list[cesiumpy.Spherical] = directions

        self.lateral_surface_material: Optional[cesiumpy.color.Color] = (
            lateral_surface_material
        )

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

        props[self._klass] = CustomPatternSensorGraphics(
            **{prop: getattr(self, prop) for prop in CustomPatternSensorGraphics._props}
        )

        return props


class CustomPatternSensorGraphics(_CesiumObject):
    # Definitions

    _props = [
        "radius",
        "directions",
        "lateral_surface_material",
        "show_intersection",
        "intersection_color",
        "intersection_width",
        "show",
    ]

    radius = traitlets.Float()

    directions = traitlets.List()

    lateral_surface_material = MaybeTrait(klass=cesiumpy.color.Color, allow_none=True)

    show_intersection = traitlets.Bool(allow_none=True)
    intersection_color = MaybeTrait(klass=cesiumpy.color.Color, allow_none=True)
    intersection_width = traitlets.Float(allow_none=True)

    show = traitlets.Bool(allow_none=True)

    # Constructor

    def __init__(
        self,
        radius: float,
        directions: list[cesiumpy.Spherical],
        lateral_surface_material: Optional[cesiumpy.color.Color] = None,
        show_intersection: Optional[bool] = None,
        intersection_color: Optional[cesiumpy.color.Color] = None,
        intersection_width: Optional[float] = None,
        show: Optional[bool] = None,
    ) -> None:
        self.radius: float = radius

        self.directions: list[cesiumpy.Spherical] = directions

        self.lateral_surface_material: Optional[cesiumpy.color.Color] = (
            lateral_surface_material
        )

        self.show_intersection: Optional[bool] = show_intersection
        self.intersection_color: Optional[cesiumpy.color.Color] = intersection_color
        self.intersection_width: Optional[float] = intersection_width

        self.show: Optional[bool] = show

    # Methods

    def generate_script(self, widget=None) -> str:
        return f"new CesiumSensorVolumes.CustomPatternSensorGraphics({super().generate_script(widget=widget)})"
