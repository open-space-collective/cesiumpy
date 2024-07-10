######################################################################################################################################################

# @project        CesiumPy
# @file           cesiumpy/position.py
# @license        Apache 2.0

######################################################################################################################################################

from __future__ import annotations

from typing import Optional

import traitlets

from cesiumpy.base import _CesiumObject

######################################################################################################################################################


class Spherical(_CesiumObject):

    """
    A set of curvilinear 3-dimensional coordinates.

    https://cesium.com/learn/cesiumjs/ref-doc/Spherical.html
    """

    # Definitions

    _props = [
        "clock",
        "cone",
        "magnitude",
    ]

    clock = traitlets.Float(allow_none=True)
    cone = traitlets.Float(allow_none=True)
    magnitude = traitlets.Float(allow_none=True)

    # Constructor

    def __init__(
        self,
        clock: Optional[float] = None,
        cone: Optional[float] = None,
        magnitude: Optional[float] = None,
    ) -> None:
        self.clock: Optional[float] = clock
        self.cone: Optional[float] = cone
        self.magnitude: Optional[float] = magnitude


######################################################################################################################################################
