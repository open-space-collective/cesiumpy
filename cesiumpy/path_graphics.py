# Apache License 2.0

from __future__ import annotations

from typing import Optional

import traitlets

from cesiumpy.base import _CesiumObject


class PathGraphics(_CesiumObject):
    # Definitions

    _props = [
        "show",
        "lead_time",
        "trail_time",
        "width",
        "resolution",
    ]

    # A boolean Property specifying the visibility of the path.
    show = traitlets.Bool(allow_none=True)

    # A Property specifying the number of seconds in front the object to show.
    lead_time = traitlets.Float(allow_none=True)

    # A Property specifying the number of seconds behind of the object to show.
    trail_time = traitlets.Float(allow_none=True)

    # A numeric Property specifying the width in pixels.
    width = traitlets.Float(allow_none=True)

    # A numeric Property specifying the maximum number of seconds to step when sampling the position.
    resolution = traitlets.Float(allow_none=True)

    # Constructor

    def __init__(
        self,
        show: Optional[bool] = None,
        lead_time: Optional[float] = None,
        trail_time: Optional[float] = None,
        width: Optional[float] = None,
        resolution: Optional[float] = None,
        # material: Optional[Color] = None,
        # distance_display_condition: Optional[DistanceDisplayCondition] = None,
    ) -> None:
        self.show = show
        self.lead_time = lead_time
        self.trail_time = trail_time
        self.width = width
        self.resolution = resolution

    # Properties

    def generate_script(self, widget=None) -> str:
        return f"new {self._klass}({super().generate_script(widget = widget)})"
