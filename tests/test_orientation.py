# Apache License 2.0

from cesiumpy import Cartesian3
from cesiumpy import Quaternion
from cesiumpy import HeadingPitchRoll


class TestQuaternion:
    def test_constructor_success(self):
        assert (
            Quaternion(0.0, 0.0, 0.0, 1.0).generate_script()
            == "new Cesium.Quaternion(0.0, 0.0, 0.0, 1.0)"
        )

    def test_multiply_success(self):
        assert (
            Quaternion(0.0, 0.0, 0.0, 1.0) * Quaternion(0.0, 1.0, 0.0, 0.0)
        ).generate_script() == "Cesium.Quaternion.multiply(new Cesium.Quaternion(0.0, 1.0, 0.0, 0.0), new Cesium.Quaternion(0.0, 0.0, 0.0, 1.0), new Cesium.Quaternion(0.0, 0.0, 0.0, 1.0))"

    def test_from_axis_angle_success(self):
        assert (
            Quaternion.from_axis_angle(Cartesian3(0.0, 0.0, 1.0), 1.2).generate_script()
            == "Cesium.Quaternion.fromAxisAngle(new Cesium.Cartesian3(0.0, 0.0, 1.0), 1.2)"
        )

    def test_from_heading_pitch_roll_success(self):
        assert (
            Quaternion.from_heading_pitch_roll(
                HeadingPitchRoll(1.0, 2.0, 3.0)
            ).generate_script()
            == "Cesium.Quaternion.fromHeadingPitchRoll(new Cesium.HeadingPitchRoll(1.0, 2.0, 3.0))"
        )


class TestHeadingPitchRoll:
    def test_constructor_success(self):
        assert (
            HeadingPitchRoll(1.0, 2.0, 3.0).generate_script()
            == "new Cesium.HeadingPitchRoll(1.0, 2.0, 3.0)"
        )

    def test_from_degrees_success(self):
        assert (
            HeadingPitchRoll.from_degrees(1.0, 2.0, 3.0).generate_script()
            == "Cesium.HeadingPitchRoll.fromDegrees(1.0, 2.0, 3.0)"
        )

    def test_from_quaternion_success(self):
        assert (
            HeadingPitchRoll.from_quaternion(
                Quaternion(0.0, 0.0, 0.0, 1.0)
            ).generate_script()
            == "Cesium.HeadingPitchRoll.fromQuaternion(new Cesium.Quaternion(0.0, 0.0, 0.0, 1.0))"
        )
