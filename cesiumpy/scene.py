#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import traitlets

import cesiumpy
from cesiumpy.base import _CesiumObject, _CesiumBase, RestrictedList


class Scene(_CesiumObject):
    widget = traitlets.Instance(klass=_CesiumBase)

    def __init__(self, widget):
        self.widget = widget
        self._primitives = RestrictedList(
            self.widget, allowed=cesiumpy.ModelGraphic, propertyname="scene.primitives"
        )

    @property
    def primitives(self):
        return self._primitives

    def generate_script(self, widget=None):
        return self._primitives.generate_script(widget=widget)
