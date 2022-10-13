#!/usr/bin/env python
# coding: utf-8

from __future__ import annotations
from __future__ import unicode_literals

from datetime import datetime
from typing import List, Optional

import traitlets

from cesiumpy.base import _CesiumObject
from cesiumpy.util.trait import DateTimeTrait


class TimeInterval(_CesiumObject):

    # Definitions

    _props = [
        "start",
        "stop",
        "is_start_included",
        "is_stop_included",
        "data",
    ]

    start = DateTimeTrait(allow_none=True)
    stop = DateTimeTrait(allow_none=True)
    is_start_included = traitlets.Bool(allow_none=True)
    is_stop_included = traitlets.Bool(allow_none=True)
    data = traitlets.Dict(allow_none=True)

    # Constructor

    def __init__(
        self,
        start: Optional[datetime] = None,
        stop: Optional[datetime] = None,
        is_start_included: Optional[bool] = None,
        is_stop_included: Optional[bool] = None,
        data: Optional[dict] = None,
    ) -> None:

        """
        start: The start time of the interval.
        stop: The stop time of the interval.
        isStartIncluded: True if options.start is included in the interval, false otherwise.
        isStopIncluded: True if options.stop is included in the interval, false otherwise.
        data: Arbitrary data associated with this interval.
        """

        self.start = start
        self.stop = stop
        self.is_start_included = is_start_included
        self.is_stop_included = is_stop_included
        self.data = data

    # Properties

    def generate_script(self, widget=None) -> str:

        return f"new {self._klass}({super().generate_script(widget = widget)})"


class TimeIntervalCollection(_CesiumObject):

    # Definitions

    _props = [
        "intervals",
    ]

    # An array of intervals to add to the collection.
    intervals = traitlets.List(allow_none=False)

    # Constructor

    def __init__(
        self,
        intervals: List[TimeInterval],
    ) -> None:

        self.intervals: List[TimeInterval] = intervals

    # Properties

    def generate_script(self, widget=None) -> str:

        return f"new {self._klass}({super().generate_script(widget = widget)})"
