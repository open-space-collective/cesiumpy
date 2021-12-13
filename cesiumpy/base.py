#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import functools
import operator
from typing import List, Dict, Optional

import six
import traitlets

import cesiumpy.util.common as com
import cesiumpy.util.html as html
from cesiumpy.util.trait import _JavaScriptObject, _JavaScriptEnum, _DIV


CESIUM_VERSION: str = '1.86'


class _CesiumObject(_JavaScriptObject):

    @property
    def _klass(self) -> str:
        return self._static_klass()

    @classmethod
    def _static_klass(cls) -> str:
        return f'Cesium.{cls.__name__}'


class _CesiumEnum(_JavaScriptEnum):
    ...


DEFAULT_ZOOM_TO_ENTITY: bool = True
DEFAULT_TRACK_ENTITY: bool = False


class _CesiumBase(_CesiumObject):

    '''
    Base class for Cesium Widget / Viewer.
    '''

    # Definitions

    _varname = 'widget'

    _props = [
        'clock_view_model',
        'imagery_provider',
        'terrain_provider',
        'sky_box',
        'sky_atmosphere',
        'scene_mode',
        'scene3d_only',
        'order_independent_translucency',
        'map_projection',
        'globe',
        'use_default_render_loop',
        'target_frame_rate',
        'show_render_loop_errors',
        'context_options',
        'credit_container',
        'terrain_exaggeration',
    ]

    width = traitlets.Unicode()
    height = traitlets.Unicode()
    scene3d_only = traitlets.Bool(allow_none = True)
    order_independent_translucency = traitlets.Bool(allow_none = True)
    use_default_render_loop = traitlets.Bool(allow_none = True)
    target_frame_rate = traitlets.Float(allow_none = True)
    show_render_loop_errors = traitlets.Bool(allow_none = True)
    terrain_exaggeration = traitlets.Float(allow_none = True)

    # Constructor

    def __init__(
        self,
        id = None,
        width = '100%',
        height = '100%',
        clock_view_model = None,
        imagery_provider = None,
        terrain_provider = None,
        sky_box = None,
        sky_atmosphere = None,
        scene_mode = None,
        scene3d_only = None,
        order_independent_translucency = None,
        map_projection = None,
        globe = None,
        use_default_render_loop = None,
        target_frame_rate = None,
        show_render_loop_errors = None,
        context_options = None,
        credit_container = None,
        terrain_exaggeration = None,
        zoom_to_entity = None,
        track_entity = None,
        default_access_token: Optional[str] = None,
    ) -> None:

        self.div = _DIV(
            id = id,
            width = width,
            height = height,
        )

        self.clock_view_model = clock_view_model

        self.imagery_provider = imagery_provider
        self.terrain_provider = terrain_provider

        self.sky_box = com.notimplemented(sky_box)
        self.sky_atmosphere = com.notimplemented(sky_atmosphere)
        self.scene_mode = com.notimplemented(scene_mode)

        self.scene3d_only = scene3d_only
        self.order_independent_translucency = order_independent_translucency

        self.map_projection = com.notimplemented(map_projection)
        self.globe = com.notimplemented(globe)

        self.use_default_render_loop = use_default_render_loop
        self.target_frame_rate = target_frame_rate
        self.show_render_loop_errors = show_render_loop_errors

        self.context_options = com.notimplemented(context_options)
        self.credit_container = com.notimplemented(credit_container)

        self.terrain_exaggeration = terrain_exaggeration

        self.zoom_to_entity: bool = zoom_to_entity if (zoom_to_entity is not None) else DEFAULT_ZOOM_TO_ENTITY
        self.track_entity: bool = track_entity if (track_entity is not None) else DEFAULT_TRACK_ENTITY

        self._default_access_token: Optional[str] = default_access_token

        from cesiumpy.camera import Camera
        self._camera = Camera(self)

        from cesiumpy.scene import Scene
        self._scene = Scene(self)

        from cesiumpy.entities.entity import _CesiumEntity
        self._entities = RestrictedList(
            self,
            allowed = _CesiumEntity,
            propertyname = 'entities',
        )

        from cesiumpy.datasource import DataSource
        self._data_sources = RestrictedList(
            self,
            allowed = DataSource,
            propertyname='data_sources',
        )

        self._scripts = RestrictedList(
            self,
            allowed = six.string_types,
            propertyname = 'script',
        )

        self._property_map: Dict[str, List[str]] = {}

    # Properties

    @property
    def container(self):
        return self.div.script

    @property
    def script(self):

        self._property_map = {}

        entities_scripts = self._entities.generate_script(widget = self)
        data_sources_scripts = self._data_sources.generate_script(widget = self)
        scene_scripts = self._scene.generate_script(widget = self)

        return (
            self._setup_scripts
            + self._widget_scripts
            + self._property_scripts
            + entities_scripts
            + data_sources_scripts
            + self._camera_scripts
            + scene_scripts
            + self.scripts._items
        )

    @property
    def camera(self):
        return self._camera

    # Methods

    def register_property(self, property: str, scripts: List[str]) -> None:
        self._property_map[property] = scripts

    # Private properties

    @property
    def _load_scripts(self) -> List[str]:

        meta: str = '<meta charset="utf-8">'
        js: str = f'<script src="https://cesium.com/downloads/cesiumjs/releases/{CESIUM_VERSION}/Build/Cesium/Cesium.js"></script>'
        css: str = f'<link href="https://cesium.com/downloads/cesiumjs/releases/{CESIUM_VERSION}/Build/Cesium/Widgets/widgets.css" rel="stylesheet">'

        return [meta, js, css]

    @property
    def _setup_scripts(self) -> List[str]:

        setup_scripts: List[str] = []

        if self._default_access_token:
            setup_scripts.append(f'Cesium.Ion.defaultAccessToken = "{self._default_access_token}";')

        return setup_scripts

    @property
    def _widget_scripts(self) -> List[str]:
        props = com.to_jsobject(self._property_dict, widget=self)
        props = ''.join(props)
        if props != '':
            script = """var {varname} = new {klass}("{id}", {props});"""
            script = script.format(varname=self._varname, klass=self._klass,
                                   id=self.div.id, props=''.join(props))
        else:
            script = """var {varname} = new {klass}("{id}");"""
            script = script.format(varname=self._varname, klass=self._klass,
                                   id=self.div.id)
        return [script]

    @property
    def _camera_scripts(self) -> List[str]:

        camera_scripts: List[str] = []

        camera = self.camera.generate_script(widget = self)

        if camera != '':
            camera_scripts.append(f'{self._varname}.camera.flyTo({camera});')

        if self.zoom_to_entity and (len(self.entities) > 0):  # Zoom to added entities
            camera_scripts.append(f'{self._varname}.zoomTo({self._varname}.entities);')

        if self.track_entity and (len(self.entities) > 0):
            camera_scripts.append(f'{self._varname}.trackedEntity = {self._varname}.entities.values[{self._varname}.entities.values.length - 1];')

        return camera_scripts

    @property
    def entities(self):
        return self._entities

    @property
    def data_sources(self):
        return self._data_sources

    @property
    def scene(self):
        return self._scene

    @property
    def scripts(self):
        return self._scripts

    @property
    def _property_scripts(self) -> List[str]:
        return functools.reduce(operator.iconcat, self._property_map.values(), [])

    # Methods

    def to_html(self) -> str:
        headers = self._load_scripts
        container = self.container
        scripts = html._wrap_scripts(self.script)

        return html._build_html(
            headers,
            container,
            scripts
        )

    # Private methods

    def _repr_html_(self) -> str:
        return self.to_html()


class RestrictedList(_CesiumObject):

    widget = traitlets.Instance(klass=_CesiumBase)

    def __init__(self, widget, allowed, propertyname):
        self.widget = widget

        self._items = []
        self._allowed = allowed
        self._propertyname = propertyname

    def add(self, item, **kwargs):
        if com.is_listlike(item):
            for i in item:
                self.add(i, **kwargs)
        elif isinstance(item, self._allowed):
            for key, value in six.iteritems(kwargs):
                setattr(item, key, value)
            self._items.append(item)
        else:
            msg = 'item must be {allowed} instance: {item}'

            if isinstance(self._allowed, tuple):
                allowed = ', '.join([a.__name__ for a in self._allowed])
            else:
                allowed = self._allowed

            raise ValueError(msg.format(allowed=allowed, item=item))

    def clear(self):
        self._items = []

    def __len__(self):
        return len(self._items)

    def __getitem__(self, item):
        return self._items[item]

    def generate_script(self, widget = None):

        '''
        Return list of scripts built from entities
        each script may be a list of commands also
        '''

        results = []
        for item in self._items:
            script = '{varname}.{propertyname}.add({item});'.format(
                varname = (widget or self.widget)._varname,
                propertyname = self._propertyname,
                item = item.generate_script(widget = (widget or self.widget))
            )
            results.append(script)
        return results
