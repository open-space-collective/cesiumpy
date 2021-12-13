#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import traitlets

from cesiumpy import constants
from cesiumpy.entities.entity import _CesiumEntity


class Cylinder(_CesiumEntity):

    '''
    CylinderGraphics

    Parameters
    ----------

    position: Cartesian3
        A Property specifying the Cartesian3 positions.
    length: float
        A numeric Property specifying the length of the cylinder.
    top_radius: float
        A numeric Property specifying the radius of the top of the cylinder.
    bottom_radius: float
        A numeric Property specifying the radius of the bottom of the cylinder.
    height_reference: TBI
    show: bool, default True
        A boolean Property specifying the visibility of the cylinder.
    fill: bool, default True
        A boolean Property specifying whether the cylinder is filled with the provided material.
    material: cesiumpy.cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the cylinder.
    outline: bool, default False
        A boolean Property specifying whether the cylinder is outlined.
    outline_color: cesiumpy.cesiumpy.color.Color, default BLACK
        A Property specifying the Color of the outline.
    outline_width: float, default 1.
        A numeric Property specifying the width of the outline.
    number_of_vertical_lines: int, default 16
        A numeric Property specifying the number of vertical lines to draw along the perimeter for the outline.
    slices: int, default 128
        The number of edges around perimeter of the cylinder.
    '''

    # Definitons

    _klass = 'cylinder'

    _props = [
        'length',
        'top_radius',
        'bottom_radius',
        'height_reference',
        'slices',
    ]

    length = traitlets.Float()
    top_radius = traitlets.Float()
    bottom_radius = traitlets.Float()
    height_reference = traitlets.Instance(klass = constants.HeightReference, allow_none = True)
    slices = traitlets.Float(allow_none = True)

    # Constructor

    def __init__(
        self,
        position,
        length,
        top_radius,
        bottom_radius,
        height_reference = None,
        orientation = None,
        show = None,
        fill = None,
        material = None,
        outline = None,
        outline_color = None,
        outline_width = None,
        number_of_vertical_lines = None,
        slices = None,
        name = None,
        **kwargs,
    ) -> None:

        super().__init__(
            show = show,
            fill = fill,
            material = material,
            outline = outline,
            outline_color = outline_color,
            outline_width = outline_width,
            number_of_vertical_lines = number_of_vertical_lines,
            position = position,
            orientation = orientation,
            name = name,
            **kwargs,
        )

        self.length = length
        self.top_radius = top_radius
        self.bottom_radius = bottom_radius
        self.height_reference = height_reference
        self.slices = slices
