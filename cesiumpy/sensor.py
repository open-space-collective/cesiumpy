# Apache License 2.0

import abc
import math
from typing import Optional

import cesiumpy
from cesiumpy.util.name import generate_name

DEFAULT_LENGTH: int = 1
DEFAULT_SLICES: int = 10
DEFAULT_COLOR: cesiumpy.entities.color.Color = cesiumpy.entities.color.Color(
    red=1, green=0, blue=0, alpha=0.2
)
DEFAULT_INTERSECTION_COLOR: cesiumpy.entities.color.Color = cesiumpy.color.WHITE


class Sensor(abc.ABC):
    """
    Sensor.
    """

    # Constructor

    def __init__(
        self,
        direction: cesiumpy.Cartesian3,
        material: Optional[cesiumpy.entities.color.Color] = None,
        show_intersection: Optional[bool] = None,
        intersection_color: Optional[cesiumpy.color.Color] = None,
        name: Optional[str] = None,
        show: Optional[bool] = None,
    ) -> None:
        self._direction: cesiumpy.Cartesian3 = direction
        self._material: cesiumpy.entities.color.Color = material or DEFAULT_COLOR

        self._show_intersection: bool = (
            show_intersection if (show_intersection is not None) else True
        )
        self._intersection_color: cesiumpy.color.Color = (
            intersection_color or DEFAULT_INTERSECTION_COLOR
        )

        self._name: str = name or generate_name()
        self._show: bool = show if (show is not None) else True

    # Properties

    @property
    def direction(self) -> cesiumpy.Cartesian3:
        return self._direction

    @property
    def material(self) -> cesiumpy.entities.color.Color:
        return self._material

    @property
    def show_intersection(self) -> bool:
        return self._show_intersection

    @property
    def intersection_color(self) -> cesiumpy.color.Color:
        return self._intersection_color

    @property
    def name(self) -> str:
        return self._name

    @property
    def show(self) -> bool:
        return self._show

    # Methods

    @abc.abstractmethod
    def render(
        self,
        viewer: cesiumpy.Viewer,
        satellite: cesiumpy.Satellite,
    ) -> None:
        raise NotImplementedError

    # Private methods

    def _generate_position(
        self,
        satellite: cesiumpy.Satellite,
    ) -> cesiumpy.SampledPositionProperty:
        sampled_position = cesiumpy.SampledPositionProperty(
            name=f"{self.name}_position",
        )

        for time, lla_B, _ in satellite.position.samples:
            lla_S = lla_B  # TBI

            sampled_position.add_sample(
                time=time,
                position=lla_S,
            )

        return sampled_position

    def _generate_orientation(
        self,
        satellite: cesiumpy.Satellite,
    ) -> cesiumpy.SampledProperty:
        sampled_orientation = cesiumpy.SampledProperty(
            type=cesiumpy.Quaternion,
            name=f"{self.name}_orientation",
        )

        x_direction: cesiumpy.Cartesian3 = cesiumpy.Cartesian3(0.0, 0.0, 1.0)

        q_S_B: Optional[cesiumpy.Quaternion] = None

        if self.direction.dot(x_direction) != 1.0:
            if self.direction.dot(x_direction) != -1.0:
                q_S_B = cesiumpy.Quaternion.from_axis_angle(
                    axis=x_direction.cross(self.direction).normalized(),
                    angle=self.direction.angle_with(x_direction),
                )

            else:
                q_S_B = cesiumpy.Quaternion.from_axis_angle(
                    axis=cesiumpy.Cartesian3(1.0, 0.0, 0.0),
                    angle=cesiumpy.math.to_radians(180.0),
                )

        for time, q_B_ECEF, _ in satellite.orientation.samples:
            if q_S_B is not None:
                q_S_ECEF = q_S_B * q_B_ECEF

            else:
                q_S_ECEF = q_B_ECEF

            sampled_orientation.add_sample(
                time=time,
                value=q_S_ECEF,
            )

        return sampled_orientation


class CustomPatternSensor(Sensor):
    """
    Custom Pattern Sensor.
    """

    # Constructor

    def __init__(
        self,
        direction: cesiumpy.Cartesian3,
        radius: float,
        directions: list[cesiumpy.Spherical],
        material: Optional[cesiumpy.entities.color.Color] = None,
        show_intersection: Optional[bool] = None,
        intersection_color: Optional[cesiumpy.color.Color] = None,
        name: Optional[str] = None,
        show: Optional[bool] = None,
    ) -> None:
        super().__init__(
            direction=direction,
            material=material,
            show_intersection=show_intersection,
            intersection_color=intersection_color,
            name=name,
            show=show,
        )

        self._radius: float = radius
        self._directions: list[cesiumpy.Spherical] = directions

    # Properties

    @property
    def radius(self) -> float:
        return self._radius

    @property
    def directions(self) -> list[cesiumpy.Spherical]:
        return self._directions

    # Methods

    def render(
        self,
        viewer: cesiumpy.Viewer,
        satellite: cesiumpy.Satellite,
    ) -> None:
        from cesiumpy.entities.sensors.custom_pattern_sensor import (
            CustomPatternSensor as CustomPatternSensorEntity,
        )

        viewer.entities.add(
            CustomPatternSensorEntity(
                position=self._generate_position(satellite),
                orientation=self._generate_orientation(satellite),
                availability=satellite.availability,
                radius=self.radius,
                directions=self.directions,
                lateral_surface_material=self.material,
                show_intersection=self.show_intersection,
                intersection_color=self.intersection_color,
                intersection_width=1,
                show=self.show,
            )
        )


class RectangularSensor(CustomPatternSensor):
    """
    Rectangular Sensor.
    """

    # Constructor

    def __init__(
        self,
        direction: cesiumpy.Cartesian3,
        radius: float,
        x_half_angle: float,
        y_half_angle: float,
        material: Optional[cesiumpy.entities.color.Color] = None,
        name: Optional[str] = None,
        show_intersection: Optional[bool] = None,
        intersection_color: Optional[cesiumpy.color.Color] = None,
        show: Optional[bool] = None,
    ) -> None:
        super().__init__(
            direction=direction,
            radius=radius,
            directions=RectangularSensor.generate_directions(
                x_half_angle, y_half_angle
            ),
            material=material,
            show_intersection=show_intersection,
            intersection_color=intersection_color,
            name=name,
            show=show,
        )

        self._x_half_angle: float = x_half_angle
        self._y_half_angle: float = y_half_angle

    # Properties

    @property
    def x_half_angle(self) -> float:
        return self._x_half_angle

    @property
    def y_half_angle(self) -> float:
        return self._y_half_angle

    # Static methods

    @staticmethod
    def generate_directions(
        x_half_angle: float,
        y_half_angle: float,
    ) -> list[cesiumpy.Spherical]:
        tan_x: float = math.tan(min(x_half_angle, cesiumpy.math.to_radians(89.0)))
        tan_y: float = math.tan(min(y_half_angle, cesiumpy.math.to_radians(89.0)))
        theta: float = math.atan(tan_x / tan_y)
        cone: float = math.atan(math.sqrt((tan_x * tan_x) + (tan_y * tan_y)))

        return [
            cesiumpy.Spherical(theta, cone),
            cesiumpy.Spherical(cesiumpy.math.to_radians(180.0) - theta, cone),
            cesiumpy.Spherical(cesiumpy.math.to_radians(180.0) + theta, cone),
            cesiumpy.Spherical(-theta, cone),
        ]


class CylindricalSensor(Sensor):
    """
    Cylindrical Sensor.
    """

    # Constructor

    def __init__(
        self,
        direction: cesiumpy.Cartesian3,
        top_radius: int,
        bottom_radius: int,
        length: int,
        slices: Optional[int] = None,
        material: Optional[cesiumpy.entities.color.Color] = None,
        name: Optional[str] = None,
        show_intersection: Optional[bool] = None,
        intersection_color: Optional[cesiumpy.color.Color] = None,
        show: Optional[bool] = None,
    ) -> None:
        super().__init__(
            direction=direction,
            material=material,
            show_intersection=show_intersection,
            intersection_color=intersection_color,
            name=name,
            show=show,
        )

        self._top_radius: int = top_radius
        self._bottom_radius: int = bottom_radius
        self._length: int = length
        self._slices: int = slices or DEFAULT_SLICES

    # Properties

    @property
    def top_radius(self) -> int:
        return self._top_radius

    @property
    def bottom_radius(self) -> int:
        return self._bottom_radius

    @property
    def length(self) -> int:
        return self._length

    @property
    def slices(self) -> int:
        return self._slices

    # Methods

    def render(
        self,
        viewer: cesiumpy.Viewer,
        satellite: cesiumpy.Satellite,
    ) -> None:
        viewer.entities.add(
            cesiumpy.Cylinder(
                position=self._generate_position(satellite),
                orientation=self._generate_orientation(satellite),
                availability=satellite.availability,
                length=self.length,
                top_radius=self.top_radius,
                bottom_radius=self.bottom_radius,
                slices=self.slices,
                material=self.material,
            )
        )


class ConicSensor(CylindricalSensor):
    """
    Conic Sensor.
    """

    # Constructor

    def __init__(
        self,
        direction: cesiumpy.Cartesian3,
        half_angle: float,
        length: Optional[int] = None,
        slices: Optional[int] = None,
        material: Optional[cesiumpy.entities.color.Color] = None,
        name: Optional[str] = None,
        show_intersection: Optional[bool] = None,
        intersection_color: Optional[cesiumpy.color.Color] = None,
        show: Optional[bool] = None,
    ) -> None:
        length = length or DEFAULT_LENGTH

        super().__init__(
            direction=direction,
            top_radius=length * math.tan(half_angle),
            bottom_radius=0,
            length=length,
            slices=slices,
            material=material,
            name=name,
            show_intersection=show_intersection,
            intersection_color=intersection_color,
            show=show,
        )

        self._half_angle: float = half_angle

    # Properties

    @property
    def half_angle(self) -> float:
        return self._half_angle

    # Methods

    def render(
        self,
        viewer: cesiumpy.Viewer,
        satellite: cesiumpy.Satellite,
    ) -> None:
        from cesiumpy.entities.sensors.conic_sensor import (
            ConicSensor as ConicSensorEntity,
        )

        viewer.entities.add(
            ConicSensorEntity(
                position=self._generate_position(satellite),
                orientation=self._generate_orientation(satellite),
                availability=satellite.availability,
                radius=self.length,
                inner_half_angle=self.half_angle,
                outer_half_angle=self.half_angle,
                lateral_surface_material=self.material,
                show_intersection=self.show_intersection,
                intersection_color=self.intersection_color,
                intersection_width=1,
                show=self.show,
            )
        )
