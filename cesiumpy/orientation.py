#!/usr/bin/env python
# coding: utf-8

from __future__ import annotations

import traitlets

from cesiumpy.base import _CesiumObject


"""
var orientationProperty = new Cesium.SampledProperty(Cesium.Quaternion);

var heading = Cesium.Math.toRadians(90+i);
var pitch = Cesium.Math.toRadians(20);
var roll = Cesium.Math.toRadians(0);
var hpRoll = new Cesium.HeadingPitchRoll(heading,pitch,roll);
var orientation = Cesium.Transforms.headingPitchRollQuaternion(position,hpRoll);
orientationProperty.addSample(time, orientation);
"""


class Quaternion(_CesiumObject):

    # Definitions

    _props = ["x", "y", "z", "w"]

    x = traitlets.Float(allow_none=False)
    y = traitlets.Float(allow_none=False)
    z = traitlets.Float(allow_none=False)
    w = traitlets.Float(allow_none=False)

    # Constructor

    def __init__(self, x: float, y: float, z: float, w: float) -> None:

        self.x = x
        self.y = y
        self.z = z
        self.w = w

    # Methods

    def generate_script(self, widget=None) -> str:
        return f"new Cesium.Quaternion({self.x}, {self.y}, {self.z}, {self.w})"

    def __repr__(self) -> str:
        return f"Cesium.Quaternion({self.x}, {self.y}, {self.z}, {self.w})"
