# Apache License 2.0

from __future__ import annotations

from datetime import datetime
from typing import Any, Type, Optional

from cesiumpy.base import _CesiumEnum
from cesiumpy.base import _CesiumObject
from cesiumpy.util.name import generate_name


class ReferenceFrame(_CesiumEnum):
    FIXED = "Cesium.ReferenceFrame.FIXED"  # The fixed frame.
    INERTIAL = "Cesium.ReferenceFrame.INERTIAL"  # The inertial frame.


class Property(_CesiumObject):
    # Constructor

    def __init__(
        self,
        name: Optional[str] = None,
    ) -> None:
        super().__init__()

        self._name: str = name or generate_name()

    # Properties

    @property
    def name(self) -> str:
        return self._name

    # Methods

    def get_value(self, time: datetime) -> Any:
        raise NotImplementedError


class SampledProperty(Property):
    # Constructor

    def __init__(
        self,
        type: Type[Property],
        name: Optional[str] = None,
        samples: Optional[list[tuple[datetime, Any, Optional[list[Any]]]]] = None,
        derivative_types=None,  # TBI
    ) -> None:
        assert derivative_types is None, NotImplementedError  # TBI

        super().__init__(
            name=name,
        )

        self._type = type
        self._samples: list[tuple[datetime, Any, Optional[list[Any]]]] = samples or []
        self._derivative_types = derivative_types

    # Properties

    @property
    def samples(self) -> list[tuple[datetime, Any, Optional[list[Any]]]]:
        return self._samples

    # Methods

    def add_sample(
        self,
        time: datetime,
        value: Any,
        derivatives: Optional[list[Any]] = None,
    ) -> None:
        self._samples.append((time, value, derivatives))

    def generate_script(self, widget=None):
        # TBI: derivatives not supported

        assert widget is not None

        property_scripts: list[str] = []

        property_scripts.append(
            "{widget}.{name} = new Cesium.SampledProperty({type_name});".format(
                widget=widget._varname,
                name=self.name,
                type_name=self._type._static_klass(),
            )
        )

        for time, value, _ in self._samples:
            pre_script: str = "{widget}.{name}.addSample({time}, {value});".format(
                widget=widget._varname,
                name=self.name,
                time=f'"{time.isoformat()}"',
                value=value.generate_script(widget=widget),
            )

            property_scripts.append(pre_script)

        widget.register_property(self.name, property_scripts)

        return f"{widget._varname}.{self.name}"
