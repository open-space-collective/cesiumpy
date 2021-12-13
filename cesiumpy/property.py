#!/usr/bin/env python
# coding: utf-8

from __future__ import annotations

from datetime import datetime
from typing import Tuple, List, Any, Type, Optional

from cesiumpy.base import _CesiumEnum
from cesiumpy.base import _CesiumObject


class ReferenceFrame(_CesiumEnum):

    FIXED = 'Cesium.ReferenceFrame.FIXED'  # The fixed frame.
    INERTIAL = 'Cesium.ReferenceFrame.INERTIAL'  # The inertial frame.


class Property(_CesiumObject):

    # Methods

    def get_value(self, time: datetime) -> Any:
        raise NotImplementedError


class SampledProperty(Property):

    # Constructor

    def __init__(
        self,
        property_name: str,
        type: Type[Property],
        derivative_types = None,  # TBI
    ) -> None:

        super().__init__()

        self._property_name: str = property_name
        self._type = type
        self._derivative_types = derivative_types

        assert self._derivative_types is None, NotImplementedError  # TBI

        self._samples: List[Tuple[datetime, Any, Optional[List[Any]]]] = []

    # Methods

    def add_sample(
        self,
        time: datetime,
        value: Any,
        derivatives: Optional[List[Any]] = None,
    ) -> None:

        self._samples.append((time, value, derivatives))

    def generate_script(self, widget = None):

        # TBI: derivatives not supported

        assert widget is not None

        property_scripts: List[str] = []

        property_scripts.append(
            '{widget}.{property_name} = new Cesium.SampledProperty({type_name});'.format(
                widget = widget._varname,
                property_name = self._property_name,
                type_name = self._type._static_klass(),
            )
        )

        for (time, value, _) in self._samples:

            pre_script: str = '{widget}.{property_name}.addSample({time}, {value});'.format(
                widget = widget._varname,
                property_name = self._property_name,
                time = f'"{time.isoformat()}"',
                value = value.generate_script(widget = widget),
            )

            property_scripts.append(pre_script)

        widget.register_property(self._property_name, property_scripts)

        return f'{widget._varname}.{self._property_name}'
