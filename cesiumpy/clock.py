#!/usr/bin/env python
# coding: utf-8

from __future__ import annotations

from datetime import datetime
from typing import Optional

import traitlets

from cesiumpy.base import _CesiumObject
from cesiumpy.base import _CesiumEnum
from cesiumpy.util.trait import DateTimeTrait


class Clock(_CesiumObject):

    # Definitions

    class Step(_CesiumEnum):

        TICK_DEPENDENT = "Cesium.ClockStep.TICK_DEPENDENT"  # Tick advances the current time by a fixed step, which is the number of seconds specified by Clock#multiplier.
        SYSTEM_CLOCK_MULTIPLIER = "Cesium.ClockStep.SYSTEM_CLOCK_MULTIPLIER"  # Tick advances the current time by the amount of system time elapsed since the previous call multiplied by Clock#multiplier.
        SYSTEM_CLOCK = "Cesium.ClockStep.SYSTEM_CLOCK"  # Tick sets the clock to the current system time; ignoring all other settings.

    class Range(_CesiumEnum):

        UNBOUNDED = "Cesium.ClockRange.UNBOUNDED"  # Tick will always advances the clock in its current direction.
        CLAMPED = "Cesium.ClockRange.CLAMPED"  # When Clock#startTime or Clock#stopTime is reached, Clock#tick will not advance Clock#currentTime any further.
        LOOP_STOP = "Cesium.ClockRange.LOOP_STOP"  # When Clock#stopTime is reached, Clock#tick will advance Clock#currentTime to the opposite end of the interval. When time is moving backwards, Clock#tick will not advance past Clock#startTime

    _props = [
        "start_time",
        "stop_time",
        "current_time",
        "multiplier",
        "clock_step",
        "clock_range",
        "can_animate",
        "should_animate",
    ]

    start_time = DateTimeTrait(allow_none=True)
    stop_time = DateTimeTrait(allow_none=True)
    current_time = DateTimeTrait(allow_none=True)
    multiplier = traitlets.Float(allow_none=True)
    clock_step = traitlets.Instance(klass=Step, allow_none=True)
    clock_range = traitlets.Instance(klass=Range, allow_none=True)
    can_animate = traitlets.Bool(allow_none=True)
    should_animate = traitlets.Bool(allow_none=True)

    # Constructor

    def __init__(
        self,
        start_time: Optional[datetime] = None,
        stop_time: Optional[datetime] = None,
        current_time: Optional[datetime] = None,
        multiplier: Optional[float] = None,
        clock_step: Optional[Clock.Step] = None,
        clock_range: Optional[Clock.Range] = None,
        can_animate: Optional[bool] = None,
        should_animate: Optional[bool] = None,
    ) -> None:

        """
        start_time: The start time of the clock.
        stop_time: The stop time of the clock.
        current_time: The current time.
        multiplier: Determines how much time advances when Clock#tick is called, negative values allow for advancing backwards.
        clock_step: Determines if calls to Clock#tick are frame dependent or system clock dependent.
        clock_range: Determines how the clock should behave when Clock#startTime or Clock#stopTime is reached.
        can_animate: Indicates whether Clock#tick can advance time. This could be false if data is being buffered, for example. The clock will only tick when both Clock#canAnimate and Clock#shouldAnimate are true.
        should_animate: Indicates whether Clock#tick should attempt to advance time. The clock will only tick when both Clock#canAnimate and Clock#shouldAnimate are true.
        """

        self.start_time = start_time
        self.stop_time = stop_time
        self.current_time = current_time
        self.multiplier = multiplier
        self.clock_step = clock_step
        self.clock_range = clock_range
        self.can_animate = can_animate
        self.should_animate = should_animate

    # Properties

    def generate_script(self, widget=None) -> str:
        return f"new {self._klass}({super().generate_script(widget = widget)})"


class ClockViewModel(_CesiumObject):

    # Definitions

    _props = [
        "clock",
    ]

    clock = traitlets.Instance(klass=Clock, allow_none=False)

    # Constructor

    def __init__(
        self,
        clock: Clock,
    ) -> None:

        self.clock: Clock = clock

    # Properties

    def generate_script(self, widget=None) -> str:
        return f"new {self._klass}({self.clock.generate_script(widget = widget)})"
