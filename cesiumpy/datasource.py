# Apache License 2.0

from __future__ import unicode_literals

import traitlets

from cesiumpy.base import _CesiumObject
import cesiumpy.entities.color
import cesiumpy.util.common as com
from cesiumpy.util.trait import MaybeTrait


class DataSource(_CesiumObject):
    _props = []

    def __init__(self, source_uri):
        self.source_uri = source_uri

    @property
    def script(self):
        props = com.to_jsobject(self._property_dict)
        props = "".join(props)
        if props != "":
            script = """{klass}.load("{source}", {props})"""
            script = script.format(
                klass=self._klass, source=self.source_uri, props="".join(props)
            )
        else:
            script = """{klass}.load("{source}")"""
            script = script.format(klass=self._klass, source=self.source_uri)
        return script

    def generate_script(self, widget=None) -> str:
        return self.script

    @classmethod
    def load(cls, source_uri, *args, **kwargs):
        return cls(source_uri, *args, **kwargs)


class CustomDataSource(DataSource):
    pass


class CzmlDataSource(DataSource):

    def __init__(self, source_uri):
        super(CzmlDataSource, self).__init__(source_uri=source_uri)


class GeoJsonDataSource(DataSource):
    """
    GeoJsonDataSource

    Parameters
    ----------

    source_uri : str
        Overrides the url to use for resolving relative links.
    describe : GeoJsonDataSource~describe, default GeoJsonDataSource.defaultDescribeProperty
        A function which returns a Property object (or just a string), which converts the properties into an html description.
    marker_size : int, default GeoJsonDataSource.marker_size
        The default size of the map pin created for each point, in pixels.
    marker_symbol : str, default GeoJsonDataSource.marker_symbol
        The default symbol of the map pin created for each point.
    marker_color : Color, default GeoJsonDataSource.marker_color
        The default color of the map pin created for each point.
    stroke : Color, default GeoJsonDataSource.stroke
        The default color of polylines and polygon outlines.
    stroke_width : int, GeoJsonDataSource.stroke_width
        The default width of polylines and polygon outlines.
    fill : Color, default GeoJsonDataSource.fill
        The default color for polygon interiors.
    """

    _props = [
        "describe",
        "marker_size",
        "marker_symbol",
        "marker_color",
        "stroke",
        "stroke_width",
        "fill",
    ]

    marker_size = traitlets.Float(allow_none=True)
    marker_symbol = traitlets.Unicode(allow_none=True)
    marker_color = MaybeTrait(klass=cesiumpy.color.Color, allow_none=True)
    stroke = MaybeTrait(klass=cesiumpy.color.Color, allow_none=True)
    stroke_width = traitlets.Float(allow_none=True)
    fill = MaybeTrait(klass=cesiumpy.color.Color, allow_none=True)

    def __init__(
        self,
        source_uri,
        describe=None,
        marker_size=None,
        marker_symbol=None,
        marker_color=None,
        stroke=None,
        stroke_width=None,
        fill=None,
    ):
        super(GeoJsonDataSource, self).__init__(source_uri=source_uri)

        self.describe = com.notimplemented(describe)

        self.marker_size = marker_size
        self.marker_symbol = marker_symbol
        self.marker_color = marker_color
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.fill = fill


class KmlDataSource(DataSource):
    """
    KmlDataSource

    Parameters
    ----------

    source_uri : str
        Overrides the url to use for resolving relative links and other KML network features.
    """

    pass
