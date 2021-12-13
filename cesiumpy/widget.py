#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

from cesiumpy.base import _CesiumBase


class CesiumWidget(_CesiumBase):

    '''
    CesiumWidget

    Parameters
    ----------

    id: str
        id string used in div tag
    width: str
        width of div tag, should be provided as css format like "100%" or "100px"
    height: str
        height of div tag, should be provided as css format like "100%" or "100px"
    clock_view_model: ClockViewModel, new ClockViewModel(clock)
        The clock view model to use to control current time.
    imagery_provider: ImageryProvider, default new BingMapsImageryProvider()
        The imagery provider to serve as the base layer. If set to false, no imagery provider will be added.
    terrain_provider: TerrainProvider, default new EllipsoidTerrainProvider()
        The terrain provider.
    sky_box: SkyBox
        The skybox used to render the stars. When undefined, the default stars are used. If set to false, no skyBox, Sun, or Moon will be added.
    sky_atmosphere: SkyAtmosphere
        Blue sky, and the glow around the Earth's limb. Set to false to turn it off.
    scene_mode: SceneMode, default SceneMode.SCENE3D
        The initial scene mode.
    scene3d_only: bool, default False
        When true, each geometry instance will only be rendered in 3D to save GPU memory.
    order_independent_translucency: bool, default True
        If true and the configuration supports it, use order independent translucency.
    map_projection: MapProjection, default new GeographicProjection()
        The map projection to use in 2D and Columbus View modesself.
    globe: Globe, default new Globe(mapProjection.ellipsoid)
        The globe to use in the scene. If set to false, no globe will be added.
    use_default_render_loop: bool, default True
        True if this widget should control the render loop, false otherwise.
    target_frame_rate: int
        The target frame rate when using the default render loop.
    show_render_loop_errors: bool, default True
        If true, this widget will automatically display an HTML panel to the user containing the error, if a render loop error occurs.
    context_options: Object
        Context and WebGL creation properties corresponding to options passed to Scene.
    credit_container: Element or str
        The DOM element or ID that will contain the CreditDisplay. If not specified, the credits are added to the bottom of the widget itself.
    terrain_exaggeration: float, default 1.
        A scalar used to exaggerate the terrain. Note that terrain exaggeration will not modify any other primitive as they are positioned relative to the ellipsoid.
    '''
    ...
