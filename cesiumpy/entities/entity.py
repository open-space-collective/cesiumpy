# Apache License 2.0

from __future__ import unicode_literals

import collections
import traitlets

import cesiumpy
from cesiumpy.base import _CesiumObject
import cesiumpy.entities.cartesian as cartesian
import cesiumpy.constants as constants
import cesiumpy.time as time
import cesiumpy.position as position
from cesiumpy.path_graphics import PathGraphics
import cesiumpy.util.common as com
from cesiumpy.util.trait import MaybeTrait


class _CesiumEntity(_CesiumObject):
    # name and position should not be included,
    # because these are handled separetedly in _properties_dict
    _common_props = [
        "width",
        "height",
        "extruded_height",
        "show",
        "fill",
        "material",
        "color",
        "outline",
        "outline_color",
        "outline_width",
        "number_of_vertical_lines",
        "rotation",
        "st_rotation",
        "granularity",
        "scale_by_distance",
        "translucency_by_distance",
        "scale",
        "horizontal_origin",
        "vertical_origin",
        "eye_offset",
        "pixel_offset",
        "pixel_offset_scale_by_distance",
        "availability",
        "path",
    ]

    width = traitlets.Float(allow_none=True)
    height = traitlets.Float(allow_none=True)
    extruded_height = traitlets.Float(allow_none=True)
    show = traitlets.Bool(allow_none=True)
    fill = traitlets.Bool(allow_none=True)

    material = MaybeTrait(klass=cesiumpy.entities.material.Material, allow_none=True)
    color = MaybeTrait(klass=cesiumpy.color.Color, allow_none=True)
    outline = traitlets.Bool(allow_none=True)
    outline_color = MaybeTrait(klass=cesiumpy.color.Color, allow_none=True)

    outline_width = traitlets.Float(allow_none=True)
    number_of_vertical_lines = traitlets.Float(allow_none=True)
    rotation = traitlets.Float(allow_none=True)
    st_rotation = traitlets.Float(allow_none=True)

    scale = traitlets.Float(allow_none=True)

    horizontal_origin = traitlets.Instance(
        klass=constants.HorizontalOrigin, allow_none=True
    )
    vertical_origin = traitlets.Instance(
        klass=constants.VerticalOrigin, allow_none=True
    )

    eye_offset = MaybeTrait(klass=cartesian.Cartesian3, allow_none=True)
    pixel_offset = MaybeTrait(klass=cartesian.Cartesian2, allow_none=True)

    availability = traitlets.Instance(
        klass=time.TimeIntervalCollection, allow_none=True
    )
    path = traitlets.Instance(klass=PathGraphics, allow_none=True)

    position = traitlets.Union(
        trait_types=[
            traitlets.Instance(klass=cartesian.Cartesian3),
            traitlets.Instance(klass=position.PositionProperty),
        ],
        allow_none=True,
    )

    # Constructor

    def __init__(
        self,
        width=None,
        height=None,
        extruded_height=None,
        show=None,
        fill=None,
        material=None,
        color=None,
        outline=None,
        outline_color=None,
        outline_width=None,
        number_of_vertical_lines=None,
        rotation=None,
        st_rotation=None,
        granularity=None,
        scale_by_distance=None,
        translucency_by_distance=None,
        scale=None,
        vertical_origin=None,
        horizontal_origin=None,
        eye_offset=None,
        pixel_offset=None,
        pixel_offset_scale_by_distance=None,
        position=None,
        orientation=None,
        name=None,
        availability=None,
        path=None,
    ) -> None:
        self.width = width
        self.height = height
        self.extruded_height = extruded_height
        self.show = show
        self.fill = fill

        # color, validated in setter
        self.material = material
        self.color = color

        self.outline = outline

        # color, validated in setter
        self.outline_color = outline_color

        self.outline_width = outline_width
        self.number_of_vertical_lines = number_of_vertical_lines
        self.rotation = rotation
        self.st_rotation = st_rotation

        self.granularity = com.notimplemented(granularity)
        self.scale_by_distance = com.notimplemented(scale_by_distance)
        self.translucency_by_distance = com.notimplemented(translucency_by_distance)

        self.scale = scale

        self.horizontal_origin = horizontal_origin
        self.vertical_origin = vertical_origin

        self.eye_offset = eye_offset
        self.pixel_offset = pixel_offset

        self.availability = availability
        self.path = path

        self.pixel_offset_scale_by_distance = com.notimplemented(
            pixel_offset_scale_by_distance
        )

        if position is not None:
            position = cartesian.Cartesian3.maybe(position, degrees=True)
        self.position = position
        self.orientation = orientation

        self.name = name

    # Properties

    @property
    def _property_dict(self):
        props = collections.OrderedDict()
        props["name"] = self.name
        props["position"] = self.position
        props["orientation"] = self.orientation

        # properties are handled in _CesiumInstance
        childs = super(_CesiumEntity, self)._property_dict
        for p in self._common_props:
            childs[p] = getattr(self, p)
        props[self._klass] = childs
        return props

    # Methods

    def copy(self):
        kwds = {}
        for key in (
            self._props
            + self._common_props
            + [
                "name",
                "position",
                "orientation",
            ]
        ):
            val = getattr(self, key)
            if val is not None:
                kwds[key] = val
        return self.__class__(**kwds)

    def __repr__(self):
        if self.position is not None:
            if isinstance(self.position, cartesian.Cartesian3):
                return "{klass}({x}, {y}, {z})".format(
                    klass=self.__class__.__name__,
                    x=self.position.x,
                    y=self.position.y,
                    z=self.position.z,
                )

            else:
                return "{klass}".format(
                    klass=self.__class__.__name__,
                )

        elif self.positions is not None:
            return "{klass}({x})".format(
                klass=self.__class__.__name__, x=self.positions.x
            )
        else:
            # should be defined in each classes
            raise NotImplementedError
