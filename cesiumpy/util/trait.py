# Apache License 2.0

from __future__ import unicode_literals

import collections
from enum import Enum
import datetime
from typing import Optional

import traitlets

import cesiumpy.util.common as com
import cesiumpy.util.html as html


class MaybeTrait(traitlets.Instance):
    def validate(self, obj, value):
        if self.allow_none is True and value is None:
            return super(MaybeTrait, self).validate(obj, value)

        try:
            value = self.klass.maybe(value)
        except ValueError:
            self.error(obj, value)
        return super(MaybeTrait, self).validate(obj, value)


class URITrait(traitlets.Unicode):
    def validate(self, obj, value):
        if self.allow_none is True and value is None:
            return super(URITrait, self).validate(obj, value)

        if not html._check_uri(value):
            self.error(obj, value)
        return super(URITrait, self).validate(obj, value)


class CZMLTrait(traitlets.TraitType):
    info_text = "a CZML"

    def validate(self, obj, value):
        data = []
        if isinstance(value, list):
            data = value

        if isinstance(value, dict):
            data = [value]

        if len(data) == 0:
            raise ValueError("CZML is empty.")

        if data[0]["id"] != "document":
            raise ValueError("CZML must start with a document object.")

        return value


class DateTimeTrait(traitlets.TraitType):
    info_text = "a datetime"

    def validate(self, obj, value):
        if isinstance(value, datetime.datetime):
            return value
        self.error(obj, value)

    def from_string(self, s):
        return datetime.datetime.fromisoformat(s)


# --------------------------------------------------
# Container
# --------------------------------------------------


class _HTMLObject(traitlets.HasTraits):
    # Properties

    @property
    def script(self):
        raise NotImplementedError

    # Methods

    def generate_script(self, widget=None):
        return self.script

    def __eq__(self, other):
        # conmpare with script
        if isinstance(other, _HTMLObject):
            return self.script == other.script
        return False


class _JavaScriptObject(_HTMLObject):
    """
    Base class for JavaScript instances, which can be converted to
    JavaScript instance
    """

    # Properties

    @property
    def _klass(self):
        raise NotImplementedError("Must be overriden in child classes.")

    @property
    def _props(self):
        raise NotImplementedError("Must be overriden in child classes.")

    @property
    def _property_dict(self) -> collections.OrderedDict:
        props = collections.OrderedDict()
        for p in self._props:
            props[p] = getattr(self, p)
        return props

    # Methods

    def generate_script(self, widget=None) -> str:
        return "".join(com.to_jsobject(self._property_dict, widget=widget))


class _JavaScriptEnum(Enum):
    # Properties

    @property
    def script(self) -> str:
        return self.generate_script()

    # Methods

    def generate_script(self, widget=None) -> str:
        return self.value


class _DIV(_HTMLObject):
    # Definitions

    id = traitlets.Unicode()
    width = traitlets.Unicode()
    height = traitlets.Unicode()

    # Constructor

    def __init__(
        self,
        id: Optional[str] = None,
        width: str = "100%",
        height: str = "100%",
    ) -> None:
        super().__init__()

        self.id = id or "cesiumContainer"
        self.width = width
        self.height = height

    # Properties

    @property
    def script(self) -> str:
        return '<div id="{id}" style="width:{width}; height:{height};"><div>'.format(
            id=self.id, width=self.width, height=self.height
        )
