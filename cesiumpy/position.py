#!/usr/bin/env python
# coding: utf-8

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

import traitlets

from cesiumpy.base import _CesiumEnum
import cesiumpy.entities.cartesian as cartesian
from cesiumpy.property import Property, SampledProperty


class ReferenceFrame(_CesiumEnum):

    FIXED = 'Cesium.ReferenceFrame.FIXED'  # The fixed frame.
    INERTIAL = 'Cesium.ReferenceFrame.INERTIAL'  # The inertial frame.


class PositionProperty(Property):

    # Definitions

    _props = [
        'reference_frame',
    ]

    # The reference frame in which the position is defined.
    reference_frame = traitlets.Instance(klass = ReferenceFrame, allow_none = True)

    # Constructor

    def __init__(
        self,
        reference_frame: Optional[ReferenceFrame] = None,
    ) -> None:

        self.reference_frame = reference_frame


class SampledPositionProperty(PositionProperty, SampledProperty):

    # Definitions

    _props = [
        'number_of_derivatives',
    ]

    # The number of derivatives that accompany each position; i.e. velocity, acceleration, etc...
    number_of_derivatives = traitlets.Float(allow_none = True)

    # Constructor

    def __init__(
        self,
        property_name: str,
        reference_frame: Optional[ReferenceFrame] = None,
        number_of_derivatives: Optional[float] = None,
    ) -> None:

        PositionProperty.__init__(
            self = self,
            reference_frame = reference_frame,
        )

        SampledProperty.__init__(
            self = self,
            property_name = property_name,
            type = cartesian.Cartesian3,
        )

        self.number_of_derivatives = number_of_derivatives

    # Methods

    def add_sample(
        self,
        time: datetime,
        position: cartesian.Cartesian3,
        derivatives: Optional[List[cartesian.Cartesian3]] = None,
    ) -> None:

        super().add_sample(time, position, derivatives)
