######################################################################################################################################################

# @project        CesiumPy
# @file           tests/test_viewer.py
# @license        Apache 2.0

######################################################################################################################################################

from typing import Optional

import cesiumpy

######################################################################################################################################################


class TestViewer:
    def test_viewer_success(
        self,
        asset_id: int,
        time_interval: cesiumpy.TimeInterval,
        sampled_position: cesiumpy.SampledPositionProperty,
        sampled_orientation: cesiumpy.SampledProperty,
        cesium_token: Optional[str],
    ):

        viewer = cesiumpy.Viewer(
            width="1000px",
            height="600px",
            clock_view_model=cesiumpy.ClockViewModel(
                clock=cesiumpy.Clock(
                    start_time=time_interval.start,
                    stop_time=time_interval.stop,
                    clock_range=cesiumpy.Clock.Range.CLAMPED,
                    can_animate=True,
                    should_animate=False,
                )
            ),
            fullscreen_button=False,
            home_button=False,
            info_box=False,
            timeline=True,
            navigation_help_button=False,
            navigation_instructions_initially_visible=False,
            scene_mode_picker=False,
            selection_indicator=False,
            scene3d_only=True,
            zoom_to_entity=True,
            track_entity=True,
            default_access_token=cesium_token,
        )

        satellite = cesiumpy.Satellite(
            position=sampled_position,
            orientation=sampled_orientation,
            availability=cesiumpy.TimeIntervalCollection(
                intervals=[
                    time_interval,
                ]
            ),
            model=cesiumpy.IonResource(asset_id=asset_id),
            sensors=[
                cesiumpy.ConicalSensor(
                    direction=cesiumpy.Cartesian3(+1.0, 0.0, 0.0),
                    half_angle=cesiumpy.math.to_radians(1.0),
                    length=100.0,
                    material=cesiumpy.color.RED,
                ),
                cesiumpy.ConicalSensor(
                    direction=cesiumpy.Cartesian3(0.0, +1.0, 0.0),
                    half_angle=cesiumpy.math.to_radians(1.0),
                    length=100.0,
                    material=cesiumpy.color.BLUE,
                ),
                cesiumpy.ConicalSensor(
                    direction=cesiumpy.Cartesian3(0.0, 0.0, +1.0),
                    half_angle=cesiumpy.math.to_radians(1.0),
                    length=100.0,
                    material=cesiumpy.color.GREEN,
                ),
                cesiumpy.ConicalSensor(
                    direction=cesiumpy.Cartesian3(0.0, 0.0, -1.0),
                    half_angle=cesiumpy.math.to_radians(15.0),
                    length=1000e3,
                    material=cesiumpy.color.YELLOW.with_alpha(0.3),
                    intersection_color=cesiumpy.color.RED,
                    show=True,
                ),
            ],
        )

        satellite.render(viewer)

        with open("viewer.html", "w") as f:
            f.write(viewer.to_html())


######################################################################################################################################################
