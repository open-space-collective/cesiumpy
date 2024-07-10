# Apache License 2.0

from typing import Optional

import cesiumpy


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
                cesiumpy.ConicSensor(
                    direction=cesiumpy.Cartesian3(+1.0, 0.0, 0.0),
                    half_angle=cesiumpy.math.to_radians(1.0),
                    length=100.0,
                    material=cesiumpy.color.RED,
                ),
                cesiumpy.ConicSensor(
                    direction=cesiumpy.Cartesian3(0.0, +1.0, 0.0),
                    half_angle=cesiumpy.math.to_radians(1.0),
                    length=100.0,
                    material=cesiumpy.color.BLUE,
                ),
                cesiumpy.ConicSensor(
                    direction=cesiumpy.Cartesian3(0.0, 0.0, +1.0),
                    half_angle=cesiumpy.math.to_radians(1.0),
                    length=100.0,
                    material=cesiumpy.color.GREEN,
                ),
                # cesiumpy.ConicSensor(
                #     direction=cesiumpy.Cartesian3(0.0, +1.0, 0.0),
                #     half_angle=cesiumpy.math.to_radians(15.0),
                #     length=100.0,
                #     material=cesiumpy.color.YELLOW.with_alpha(0.3),
                # ),
                # cesiumpy.CustomPatternSensor(
                #     direction=cesiumpy.Cartesian3(+1.0, 0.0, 0.0),
                #     radius=100.0,
                #     directions=[
                #         cesiumpy.Spherical(
                #             cesiumpy.math.to_radians(45.0 * 0),
                #             cesiumpy.math.to_radians(5.0),
                #         ),
                #         cesiumpy.Spherical(
                #             cesiumpy.math.to_radians(45.0 * 1),
                #             cesiumpy.math.to_radians(15.0),
                #         ),
                #         cesiumpy.Spherical(
                #             cesiumpy.math.to_radians(45.0 * 2),
                #             cesiumpy.math.to_radians(20.0),
                #         ),
                #         cesiumpy.Spherical(
                #             cesiumpy.math.to_radians(45.0 * 3),
                #             cesiumpy.math.to_radians(25.0),
                #         ),
                #         cesiumpy.Spherical(
                #             cesiumpy.math.to_radians(45.0 * 4),
                #             cesiumpy.math.to_radians(15.0),
                #         ),
                #         cesiumpy.Spherical(
                #             cesiumpy.math.to_radians(45.0 * 5),
                #             cesiumpy.math.to_radians(10.0),
                #         ),
                #         cesiumpy.Spherical(
                #             cesiumpy.math.to_radians(45.0 * 6),
                #             cesiumpy.math.to_radians(60.0),
                #         ),
                #         cesiumpy.Spherical(
                #             cesiumpy.math.to_radians(45.0 * 7),
                #             cesiumpy.math.to_radians(25.0),
                #         ),
                #     ],
                #     material=cesiumpy.color.ORANGE.with_alpha(0.3),
                # ),
                cesiumpy.RectangularSensor(
                    direction=cesiumpy.Cartesian3(+1.0, 0.0, 0.0),
                    radius=600e3,
                    x_half_angle=cesiumpy.math.to_radians(20.0),
                    y_half_angle=cesiumpy.math.to_radians(20.0),
                    material=cesiumpy.color.ORANGE.with_alpha(0.3),
                ),
            ],
        )

        satellite.render(viewer)

        with open("viewer.html", "w") as f:
            f.write(viewer.to_html())

    def test_viewer_czml_datasource_success(self):
        ds = cesiumpy.CzmlDataSource(sourceUri="data/simple.czml")
        viewer = cesiumpy.Viewer(data_sources=[ds])
        assert (
            'widget.dataSources.add(Cesium.CzmlDataSource.load("data/simple.czml")'
            in viewer.to_html()
        )
