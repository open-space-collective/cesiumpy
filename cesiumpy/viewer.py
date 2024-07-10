#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import traitlets

from cesiumpy.base import _CesiumBase
import cesiumpy.util.common as com


class Viewer(_CesiumBase):
    """
    Viewer

    Parameters
    ----------

    id: str
        id string used in div tag
    width: str
        width of div tag, should be provided as css format like "100%" or "100px"
    height: str
        height of div tag, should be provided as css format like "100%" or "100px"
    animation: bool, default True
        If set to false, the Animation widget will not be created.
    base_layer_picker: bool, default True
        If set to false, the BaseLayerPicker widget will not be created.
    fullscreen_button: bool, default True
        If set to false, the FullscreenButton widget will not be created.
    geocoder: bool, default True
        If set to false, the Geocoder widget will not be created.
    home_button: bool, default True
        If set to false, the HomeButton widget will not be created.
    info_box: bool, default True
        If set to false, the InfoBox widget will not be created.
    scene_mode_picker: bool, default True
        If set to false, the SceneModePicker widget will not be created.
    selection_indicator: bool, default True
        If set to false, the SelectionIndicator widget will not be created.
    timeline: bool, default True
        If set to false, the Timeline widget will not be created.
    navigation_help_button: bool, default True
        If set to the false, the navigation help button will not be created.
    navigation_instructions_initially_visible: bool, defaut True
        True if the navigation instructions should initially be visible, or false if the should not be shown until the user explicitly clicks the button.
    scene3d_only: bool, default False
        When true, each geometry instance will only be rendered in 3D to save GPU memory.
    clock_view_model: ClockViewModel, new ClockViewModel(clock)
        The clock view model to use to control current time.
    selected_imagery_provider_view_model: ProviderViewModel
        The view model for the current base imagery layer, if not supplied the first available base layer is used. This value is only valid if options.baseLayerPicker is set to true.
    imagery_provider_view_models: list of ProviderViewModel, default createDefaultImageryProviderViewModels()
        The list of ProviderViewModels to be selectable from the BaseLayerPicker. This value is only valid if options.baseLayerPicker is set to true.
    selected_terrain_provider_view_model: ProviderViewModel
        The view model for the current base terrain layer, if not supplied the first available base layer is used. This value is only valid if options.baseLayerPicker is set to true.
    terrain_provider_view_models: list of ProviderViewModel, default createDefaultTerrainProviderViewModels()
        The list of ProviderViewModels to be selectable from the BaseLayerPicker. This value is only valid if options.baseLayerPicker is set to true.
    imagery_provider: ImageryProvider, default new BingMapsImageryProvider()
        The imagery provider to use. This value is only valid if options.baseLayerPicker is set to false.
    terrain_provider: TerrainProvider, default new EllipsoidTerrainProvider()
        The terrain provider to use
    sky_box: SkyBox
        The skybox used to render the stars. When undefined, the default stars are used.
    sky_atmosphere: SkyAtmosphere
        Blue sky, and the glow around the Earth's limb. Set to false to turn it off.
    fullscreen_element: Element or str, default document.body
        The element or id to be placed into fullscreen mode when the full screen button is pressed.
    use_default_render_loop: bool, default True
        True if this widget should control the render loop, false otherwise.
    target_frame_rate: float
        The target frame rate when using the default render loop.
    show_render_loop_errors: bool, default True
        If true, this widget will automatically display an HTML panel to the user containing the error, if a render loop error occurs.
    automatically_track_data_source_clocks: bool, default True
        If true, this widget will automatically track the clock settings of newly added DataSources, updating if the DataSource's clock changes. Set this to false if you want to configure the clock independently.
    context_options: Object
        Context and WebGL creation properties corresponding to options passed to Scene.
    scene_mode: SceneMode, default SceneMode.SCENE3D
        The initial scene mode.
    map_projection: MapProjection, default new GeographicProjection()
        The map projection to use in 2D and Columbus View modes.
    globe: Globe, default new Globe(mapProjection.ellipsoid)
        The globe to use in the scene. If set to false, no globe will be added.
    order_independent_translucency: bool, default True
        If true and the configuration supports it, use order independent translucency.
    credit_container: Element or str
        The DOM element or ID that will contain the CreditDisplay. If not specified, the credits are added to the bottom of the widget itself.
    data_sources: list of DataSource
        The collection of data sources visualized by the widget. If this parameter is provided, the instance is assumed to be owned by the caller and will not be destroyed when the viewer is destroyed.
    terrain_exaggeration: float, default 1.
        A scalar used to exaggerate the terrain. Note that terrain exaggeration will not modify any other primitive as they are positioned relative to the ellipsoid.
    """

    # Definitions

    # data_sources should be excluded from init, as it is handled separately
    _props = [
        "animation",
        "base_layer_picker",
        "fullscreen_button",
        "geocoder",
        "home_button",
        "info_box",
        "scene_mode_picker",
        "selection_indicator",
        "timeline",
        "navigation_help_button",
        "navigation_instructions_initially_visible",
        "scene3d_only",
        "clock_view_model",
        "selected_imagery_provider_view_model",
        "imagery_provider_view_models",
        "selected_terrain_provider_view_model",
        "terrain_provider_view_models",
        "imagery_provider",
        "terrain_provider",
        "sky_box",
        "sky_atmosphere",
        "fullscreen_element",
        "use_default_render_loop",
        "target_frame_rate",
        "show_render_loop_errors",
        "automatically_track_data_source_clocks",
        "context_options",
        "scene_mode",
        "map_projection",
        "globe",
        "order_independent_translucency",
        "credit_container",
        "terrain_exaggeration",
    ]

    animation = traitlets.Bool(allow_none=True)
    base_layer_picker = traitlets.Bool(allow_none=True)
    fullscreen_button = traitlets.Bool(allow_none=True)
    geocoder = traitlets.Bool(allow_none=True)
    home_button = traitlets.Bool(allow_none=True)
    info_box = traitlets.Bool(allow_none=True)
    scene_mode_picker = traitlets.Bool(allow_none=True)
    selection_indicator = traitlets.Bool(allow_none=True)
    timeline = traitlets.Bool(allow_none=True)
    navigation_help_button = traitlets.Bool(allow_none=True)
    navigation_instructions_initially_visible = traitlets.Bool(allow_none=True)
    automatically_track_data_source_clocks = traitlets.Bool(allow_none=True)

    # Constructor

    def __init__(
        self,
        id=None,
        width="100%",
        height="100%",
        animation=None,
        base_layer_picker=None,
        fullscreen_button=None,
        geocoder=None,
        home_button=None,
        info_box=None,
        scene_mode_picker=None,
        selection_indicator=None,
        timeline=None,
        navigation_help_button=None,
        navigation_instructions_initially_visible=None,
        scene3d_only=None,
        clock_view_model=None,
        selected_imagery_provider_view_model=None,
        imagery_provider_view_models=None,
        selected_terrain_provider_view_model=None,
        terrain_provider_view_models=None,
        imagery_provider=None,
        terrain_provider=None,
        sky_box=None,
        sky_atmosphere=None,
        fullscreen_element=None,
        use_default_render_loop=None,
        target_frame_rate=None,
        show_render_loop_errors=None,
        automatically_track_data_source_clocks=None,
        context_options=None,
        scene_mode=None,
        map_projection=None,
        globe=None,
        order_independent_translucency=None,
        credit_container=None,
        data_sources=None,
        terrain_exaggeration=None,
        zoom_to_entity=None,
        track_entity=None,
        **kwargs,
    ) -> None:
        super().__init__(
            id=id,
            width=width,
            height=height,
            scene3d_only=scene3d_only,
            clock_view_model=clock_view_model,
            imagery_provider=imagery_provider,
            terrain_provider=terrain_provider,
            sky_box=sky_box,
            sky_atmosphere=sky_atmosphere,
            scene_mode=scene_mode,
            order_independent_translucency=order_independent_translucency,
            map_projection=map_projection,
            globe=globe,
            use_default_render_loop=use_default_render_loop,
            target_frame_rate=target_frame_rate,
            show_render_loop_errors=show_render_loop_errors,
            context_options=context_options,
            credit_container=credit_container,
            terrain_exaggeration=terrain_exaggeration,
            zoom_to_entity=zoom_to_entity,
            track_entity=track_entity,
            **kwargs,
        )

        self.animation = animation

        if (self.imagery_provider is not None) or (self.terrain_provider is not None):
            # disable baseLayerPicker explicitly when any provider is specified
            if base_layer_picker is None:
                base_layer_picker = False

        self.base_layer_picker = base_layer_picker
        self.fullscreen_button = fullscreen_button
        self.geocoder = geocoder
        self.home_button = home_button
        self.info_box = info_box
        self.scene_mode_picker = scene_mode_picker
        self.selection_indicator = selection_indicator
        self.timeline = timeline
        self.navigation_help_button = navigation_help_button
        self.navigation_instructions_initially_visible = (
            navigation_instructions_initially_visible
        )

        self.selected_imagery_provider_view_model = com.notimplemented(
            selected_imagery_provider_view_model
        )
        self.imagery_provider_view_models = com.notimplemented(
            imagery_provider_view_models
        )
        self.selected_terrain_provider_view_model = com.notimplemented(
            selected_terrain_provider_view_model
        )
        self.terrain_provider_view_models = com.notimplemented(
            terrain_provider_view_models
        )
        self.fullscreen_element = com.notimplemented(fullscreen_element)

        self.automatically_track_data_source_clocks = (
            automatically_track_data_source_clocks
        )

        # ToDo: API to disable all flags to False

        if data_sources is not None:
            data_sources = com.validate_listlike(data_sources, key="dataSources")
            for ds in data_sources:
                self._data_sources.add(ds)

    # Properties

    @property
    def plot(self):
        from cesiumpy.plotting.plot import PlottingAccessor

        return PlottingAccessor(self)
