######################################################################################################################################################

# @project        CesiumPy
# @file           cesiumpy/sensor.py
# @license        Apache 2.0

######################################################################################################################################################

from __future__ import annotations

import traitlets

import cesiumpy
from cesiumpy.base import _CesiumObject

######################################################################################################################################################


class Quaternion(_CesiumObject):

    """
    var orientationProperty = new Cesium.SampledProperty(Cesium.Quaternion);

    var heading = Cesium.Math.toRadians(90+i);
    var pitch = Cesium.Math.toRadians(20);
    var roll = Cesium.Math.toRadians(0);
    var hpRoll = new Cesium.HeadingPitchRoll(heading,pitch,roll);
    var orientation = Cesium.Transforms.headingPitchRollQuaternion(position,hpRoll);
    orientationProperty.addSample(time, orientation);
    """

    # Definitions

    _props = ["x", "y", "z", "w"]

    x = traitlets.Float(allow_none=False)
    y = traitlets.Float(allow_none=False)
    z = traitlets.Float(allow_none=False)
    w = traitlets.Float(allow_none=False)

    # Constructor

    def __init__(
        self,
        x: float,
        y: float,
        z: float,
        w: float,
    ) -> None:

        self.x: float = x
        self.y: float = y
        self.z: float = z
        self.w: float = w

    # Methods

    def generate_script(self, widget=None) -> str:
        return f"new Cesium.Quaternion({self.x}, {self.y}, {self.z}, {self.w})"

    def __mul__(self, quaternion: Quaternion) -> Quaternion:
        return _QuaternionFromProduct(
            quaternion_1=self,
            quaternion_2=quaternion,
        )

    def __repr__(self) -> str:
        return f"Cesium.Quaternion({self.x}, {self.y}, {self.z}, {self.w})"

    # Static methods

    @staticmethod
    def unit() -> Quaternion:

        return Quaternion(
            x=0.0,
            y=0.0,
            z=0.0,
            w=1.0,
        )

    @staticmethod
    def from_axis_angle(
        axis: cesiumpy.Cartesian3,
        angle: float,
    ) -> Quaternion:

        return _QuaternionFromAxisAngle(
            axis=axis,
            angle=angle,
        )

    @staticmethod
    def from_heading_pitch_roll(
        heading_pitch_roll: HeadingPitchRoll,
    ) -> Quaternion:

        return _QuaternionFromHeadingPitchRoll(
            heading_pitch_roll=heading_pitch_roll,
        )


######################################################################################################################################################


class HeadingPitchRoll(_CesiumObject):

    """
    A rotation expressed as a heading, pitch, and roll.

    Heading is the rotation about the negative z axis.
    Pitch is the rotation about the negative y axis.
    Roll is the rotation about the positive x axis.
    """

    # Definitions

    _props = ["heading", "pitch", "roll"]

    heading = traitlets.Float(allow_none=False)
    pitch = traitlets.Float(allow_none=False)
    roll = traitlets.Float(allow_none=False)

    # Constructor

    def __init__(
        self,
        heading: float,
        pitch: float,
        roll: float,
    ) -> None:

        self.heading: float = heading
        self.pitch: float = pitch
        self.roll: float = roll

    # Methods

    def generate_script(self, widget=None) -> str:
        return f"new Cesium.HeadingPitchRoll({self.heading}, {self.pitch}, {self.roll})"

    # Static methods

    @staticmethod
    def from_degrees(
        heading: float,
        pitch: float,
        roll: float,
    ) -> HeadingPitchRoll:

        return _HeadingPitchRollFromDegrees(
            heading=heading,
            pitch=pitch,
            roll=roll,
        )

    @staticmethod
    def from_quaternion(
        quaternion: Quaternion,
    ) -> HeadingPitchRoll:

        return _HeadingPitchRollFromQuaternion(
            quaternion=quaternion,
        )


######################################################################################################################################################


class _QuaternionFromProduct(Quaternion):

    # Constructor

    def __init__(
        self,
        quaternion_1: Quaternion,
        quaternion_2: Quaternion,
    ) -> None:

        super().__init__(
            x=0.0,
            y=0.0,
            z=0.0,
            w=0.0,
        )

        self.quaternion_1: Quaternion = quaternion_1
        self.quaternion_2: Quaternion = quaternion_2

    # Methods

    def generate_script(self, widget=None) -> str:
        return f"Cesium.Quaternion.multiply({self.quaternion_2.generate_script(widget=widget)}, {self.quaternion_1.generate_script(widget=widget)}, {Quaternion.unit().generate_script(widget=widget)})"


######################################################################################################################################################


class _QuaternionFromAxisAngle(Quaternion):

    # Constructor

    def __init__(
        self,
        axis: cesiumpy.Cartesian3,
        angle: float,
    ) -> None:

        super().__init__(
            x=0.0,
            y=0.0,
            z=0.0,
            w=0.0,
        )

        self.axis = axis
        self.angle = angle

    # Methods

    def generate_script(self, widget=None) -> str:
        return f"Cesium.Quaternion.fromAxisAngle({self.axis.generate_script(widget=widget)}, {self.angle})"


######################################################################################################################################################


class _QuaternionFromHeadingPitchRoll(Quaternion):

    # Constructor

    def __init__(
        self,
        heading_pitch_roll: HeadingPitchRoll,
    ) -> None:

        super().__init__(
            x=0.0,
            y=0.0,
            z=0.0,
            w=0.0,
        )

        self.heading_pitch_roll: HeadingPitchRoll = heading_pitch_roll

    # Methods

    def generate_script(self, widget=None) -> str:
        return f"Cesium.Quaternion.fromHeadingPitchRoll({self.heading_pitch_roll.generate_script(widget=widget)})"


######################################################################################################################################################


class _HeadingPitchRollFromDegrees(HeadingPitchRoll):

    # Constructor

    def __init__(
        self,
        heading: float,
        pitch: float,
        roll: float,
    ) -> None:

        super().__init__(
            heading=heading,
            pitch=pitch,
            roll=roll,
        )

    # Methods

    def generate_script(self, widget=None) -> str:
        return f"Cesium.HeadingPitchRoll.fromDegrees({self.heading}, {self.pitch}, {self.roll})"


######################################################################################################################################################


class _HeadingPitchRollFromQuaternion(HeadingPitchRoll):

    # Constructor

    def __init__(
        self,
        quaternion: Quaternion,
    ) -> None:

        super().__init__(
            heading=0.0,
            pitch=0.0,
            roll=0.0,
        )

        self.quaternion: Quaternion = quaternion

    # Methods

    def generate_script(self, widget=None) -> str:
        return f"Cesium.HeadingPitchRoll.fromQuaternion({self.quaternion.generate_script(widget=widget)})"


######################################################################################################################################################
