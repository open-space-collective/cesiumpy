######################################################################################################################################################

# @project        CesiumPy
# @file           cesiumpy/satellite.py
# @license        Apache 2.0

######################################################################################################################################################

import cesiumpy

from typing import Optional

from cesiumpy.util.name import generate_name

######################################################################################################################################################


class Satellite:

    """
    Satellite.
    """

    # Constructor

    def __init__(
        self,
        position: cesiumpy.SampledPositionProperty,
        orientation: Optional[cesiumpy.SampledProperty] = None,
        availability: Optional[cesiumpy.TimeIntervalCollection] = None,
        model: Optional[cesiumpy.IonResource] = None,
        sensors: Optional[list["cesiumpy.Sensor"]] = None,
        name: Optional[str] = None,
    ) -> None:

        self._name: str = name or generate_name()
        self._position: cesiumpy.SampledPositionProperty = position
        self._orientation: Optional[cesiumpy.SampledProperty] = orientation
        self._availability: Optional[cesiumpy.TimeIntervalCollection] = availability
        self._model: Optional[cesiumpy.IonResource] = model
        self._sensors: list["cesiumpy.Sensor"] = sensors or []

    # Properties

    @property
    def name(self) -> str:
        return self._name

    @property
    def position(self) -> cesiumpy.SampledPositionProperty:
        return self._position

    @property
    def orientation(self) -> Optional[cesiumpy.SampledProperty]:
        return self._orientation

    @property
    def availability(self) -> Optional[cesiumpy.TimeIntervalCollection]:
        return self._availability

    @property
    def model(self) -> Optional[cesiumpy.IonResource]:
        return self._model

    @property
    def sensors(self) -> list["cesiumpy.Sensor"]:
        return self._sensors

    # Methods

    def add_sensor(self, sensor: "cesiumpy.Sensor") -> None:
        self._sensors.append(sensor)

    def render(self, viewer: cesiumpy.Viewer) -> None:

        # Add orbital track
        # viewer.entities.add(
        #     cesiumpy.Polyline(
        #         positions=cesiumpy.entities.cartesian.Cartesian3Array(
        #             functools.reduce(
        #                 operator.iconcat,
        #                 [
        #                     [
        #                         state["position"]["longitude"],
        #                         state["position"]["latitude"],
        #                         state["position"]["altitude"],
        #                     ]
        #                     for state in states
        #                 ],
        #                 [],
        #             )
        #         ),
        #         width=1,
        #     )
        # )

        # Add satellite model
        viewer.entities.add(
            cesiumpy.Model(
                position=self.position,
                orientation=self.orientation,
                availability=self.availability,
                uri=self.model,
            )
        )

        for sensor in self.sensors:
            sensor.render(
                viewer=viewer,
                satellite=self,
            )


#######################################################################################################################################
