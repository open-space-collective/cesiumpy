# Apache License 2.0

from __future__ import unicode_literals

import traitlets

import cesiumpy
from cesiumpy.base import _CesiumObject
import cesiumpy.entities.cartesian as cartesian
import cesiumpy.util.common as com
from cesiumpy.util.trait import MaybeTrait


class _CesiumProvider(_CesiumObject):
    _props = ["url"]

    def __repr__(self):
        if self.url is None:
            return super(_CesiumProvider, self).__repr__()
        else:
            rep = """{klass}(url="{url}")"""
            return rep.format(klass=self.__class__.__name__, url=self.url)

    @property
    def script(self):
        props = "".join(com.to_jsobject(self._property_dict))
        rep = """new {klass}({props})"""
        return rep.format(klass=self._klass, props=props)


# --------------------------------------------------
# Terrain Provider
# --------------------------------------------------


class TerrainProvider(_CesiumProvider):
    _props = ["url", "proxy", "ellipsoid", "credit"]

    url = traitlets.Unicode()
    credit = traitlets.Unicode(allow_none=True)

    def __init__(
        self, url=None, proxy=None, tiling_scheme=None, ellipsoid=None, credit=None
    ):
        self.url = url
        self.proxy = com.notimplemented(proxy)
        self.tiling_scheme = com.notimplemented(tiling_scheme)
        self.ellipsoid = com.notimplemented(ellipsoid)
        self.credit = credit


class ArcGisImageServerTerrainProvider(TerrainProvider):
    """
    ArcGisImageServerTerrainProvider

    Parameters
    ----------

    url : str
        The URL of the ArcGIS ImageServer service.
    token : str
        The authorization token to use to connect to the service.
    proxy : Proxy
        A proxy to use for requests. This object is expected to have a getURL function which returns the proxied URL, if needed.
    tiling_scheme : TilingScheme, default new GeographicTilingScheme()
        The tiling scheme specifying how the terrain is broken into tiles. If this parameter is not provided, a GeographicTilingScheme is used.
    ellipsoid : Ellipsoid
        The ellipsoid. If the tiling_scheme is specified, this parameter is ignored and the tiling scheme's ellipsoid is used instead. If neither parameter is specified, the WGS84 ellipsoid is used.
    credit : Credit or str
        The credit, which will is displayed on the canvas.
    """

    _props = ["url", "token", "proxy", "tiling_scheme", "ellipsoid", "credit"]

    token = traitlets.Unicode(allow_none=True)

    def __init__(
        self, url, token, proxy=None, tiling_scheme=None, ellipsoid=None, credit=None
    ):
        super(ArcGisImageServerTerrainProvider, self).__init__(
            url=url,
            proxy=proxy,
            tiling_scheme=tiling_scheme,
            ellipsoid=ellipsoid,
            credit=credit,
        )
        self.token = token


class CesiumTerrainProvider(TerrainProvider):
    """
    CesiumTerrainProvider

    Parameters
    ----------

    url : str
        The URL of the Cesium terrain server.
    proxy : Proxy
        A proxy to use for requests. This object is expected to have a getURL function which returns the proxied URL, if needed.
    request_vertex_normals : bool, default False
        Flag that indicates if the client should request additional lighting information from the server, in the form of per vertex normals if available.
    request_water_mask : bool, default False
        Flag that indicates if the client should request per tile water masks from the server, if available.
    ellipsoid : Ellipsoid
        The ellipsoid. If not specified, the WGS84 ellipsoid is used.
    credit : Credit or str
        A credit for the data source, which is displayed on the canvas.
    """

    _props = [
        "url",
        "proxy",
        "request_vertex_normals",
        "request_water_mask",
        "ellipsoid",
        "credit",
    ]

    request_vertex_normals = traitlets.Bool(allow_none=True)
    request_water_mask = traitlets.Bool(allow_none=True)

    def __init__(
        self,
        url,
        proxy=None,
        request_vertex_normals=None,
        request_water_mask=None,
        ellipsoid=None,
        credit=None,
    ):
        super(CesiumTerrainProvider, self).__init__(
            url=url, proxy=proxy, ellipsoid=ellipsoid, credit=credit
        )
        self.request_vertex_normals = request_vertex_normals
        self.request_water_mask = request_water_mask


class EllipsoidTerrainProvider(TerrainProvider):
    """
    EllipsoidTerrainProvider

    Parameters
    ----------

    tiling_scheme : TilingScheme, default new GeographicTilingScheme()
        The tiling scheme specifying how the ellipsoidal surface is broken into tiles. If this parameter is not provided, a GeographicTilingScheme is used.
    ellipsoid : Ellipsoid
        The ellipsoid. If the tiling_scheme is specified, this parameter is ignored and the tiling scheme's ellipsoid is used instead. If neither parameter is specified, the WGS84 ellipsoid is used.
    """

    url = traitlets.Unicode(allow_none=True)

    def __init__(self, tiling_scheme=None, ellipsoid=None):
        super(EllipsoidTerrainProvider, self).__init__(
            tiling_scheme=tiling_scheme, ellipsoid=ellipsoid
        )


class VRTheWorldTerrainProvider(TerrainProvider):
    """
    VRTheWorldTerrainProvider

    Parameters
    ----------
    url : str
        The URL of the VR-TheWorld TileMap.
    proxy : Proxy
        A proxy to use for requests. This object is expected to have a getURL function which returns the proxied URL, if needed.
    ellipsoid : Ellipsoid, default Ellipsoid.WGS84
        The ellipsoid. If this parameter is not specified, the WGS84 ellipsoid is used.
    credit : Credit or str
        A credit for the data source, which is displayed on the canvas.
    """

    def __init__(self, url, proxy=None, ellipsoid=None, credit=None):
        super(VRTheWorldTerrainProvider, self).__init__(
            url=url, proxy=proxy, ellipsoid=ellipsoid, credit=credit
        )


# --------------------------------------------------
# Imagery Provider
# --------------------------------------------------


class ImageryProvider(_CesiumProvider):
    _props = [
        "url",
        "file_extension",
        "rectangle",
        "tilling_scheme",
        "ellipsoid",
        "tile_width",
        "tile_height",
        "tile_discard_policy",
        "minimum_level",
        "maximum_level",
        "credit",
        "proxy",
        "subdomains",
    ]

    url = traitlets.Unicode(allow_none=True)
    file_extension = traitlets.Unicode(allow_none=True)
    rectangle = MaybeTrait(klass=cartesian.Rectangle, allow_none=True)

    tile_width = traitlets.Float(allow_none=True)
    tile_height = traitlets.Float(allow_none=True)

    minimum_level = traitlets.Float(allow_none=True)
    maximum_level = traitlets.Float(allow_none=True)

    credit = traitlets.Unicode(allow_none=True)

    def __init__(
        self,
        url=None,
        file_extension=None,
        rectangle=None,
        tilling_scheme=None,
        ellipsoid=None,
        tile_width=None,
        tile_height=None,
        tile_discard_policy=None,
        minimum_level=None,
        maximum_level=None,
        credit=None,
        proxy=None,
        subdomains=None,
    ):
        self.url = url
        self.file_extension = file_extension
        self.rectangle = rectangle

        self.tilling_scheme = com.notimplemented(tilling_scheme)
        self.ellipsoid = com.notimplemented(ellipsoid)

        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tile_discard_policy = com.notimplemented(tile_discard_policy)

        self.minimum_level = minimum_level
        self.maximum_level = maximum_level

        self.credit = credit

        self.proxy = com.notimplemented(proxy)
        self.subdomains = com.notimplemented(subdomains)


class ArcGisMapServerImageryProvider(ImageryProvider):
    """
    ArcGisImageServerTerrainProvider

    Parameters
    ----------

    url : str
        The URL of the ArcGIS MapServer service.
    token : str
        The ArcGIS token used to authenticate with the ArcGIS MapServer service.
    usePreCachedTilesIfAvailable : bool, default True
        If true, the server's pre-cached tiles are used if they are available. If false, any pre-cached tiles are ignored and the 'export' service is used.
    layers : str
        A comma-separated list of the layers to show, or undefined if all layers should be shown.
    enablePickFeatures : bool, default True
        If true, ArcGisMapServerImageryProvider#pickFeatures will invoke the Identify service on the MapServer and return the features included in the response. If false, ArcGisMapServerImageryProvider#pickFeatures will immediately return undefined (indicating no pickable features) without communicating with the server. Set this property to false if you don't want this provider's features to be pickable.
    rectangle : Rectangle, default Rectangle.MAX_VALUE
        The rectangle of the layer. This parameter is ignored when accessing a tiled layer.
    tiling_scheme : TilingScheme, default new GeographicTilingScheme()
        The tiling scheme to use to divide the world into tiles. This parameter is ignored when accessing a tiled server.
    ellipsoid : Ellipsoid
        The ellipsoid. If the tiling_scheme is specified and used, this parameter is ignored and the tiling scheme's ellipsoid is used instead. If neither parameter is specified, the WGS84 ellipsoid is used.
    tile_width : int, default 256
        The width of each tile in pixels. This parameter is ignored when accessing a tiled server.
    tile_height : int, default 256
        The height of each tile in pixels. This parameter is ignored when accessing a tiled server.
    tile_discard_policy : TileDiscardPolicy
        The policy that determines if a tile is invalid and should be discarded. If this value is not specified, a default DiscardMissingTileImagePolicy is used for tiled map servers, and a NeverTileDiscardPolicy is used for non-tiled map servers. In the former case, we request tile 0,0 at the maximum tile level and check pixels (0,0), (200,20), (20,200), (80,110), and (160, 130). If all of these pixels are transparent, the discard check is disabled and no tiles are discarded. If any of them have a non-transparent color, any tile that has the same values in these pixel locations is discarded. The end result of these defaults should be correct tile discarding for a standard ArcGIS Server. To ensure that no tiles are discarded, construct and pass a NeverTileDiscardPolicy for this parameter.
    maximum_level : int
        The maximum tile level to request, or undefined if there is no maximum. This parameter is ignored when accessing a tiled server.
    proxy : Proxy
        A proxy to use for requests. This object is expected to have a getURL function which returns the proxied URL, if needed.
    """

    _props = [
        "url",
        "token",
        "usePreCachedTilesIfAvailable",
        "layers",
        "enablePickFeatures",
        "rectangle",
        "tilling_scheme",
        "ellipsoid",
        "tile_width",
        "tile_height",
        "tile_discard_policy",
        "minimum_level",
        "proxy",
    ]

    token = traitlets.Unicode(allow_none=True)
    usePreCachedTilesIfAvailable = traitlets.Bool(allow_none=True)
    layers = traitlets.Unicode(allow_none=True)
    enablePickFeatures = traitlets.Bool(allow_none=True)

    def __init__(
        self,
        url,
        token=None,
        usePreCachedTilesIfAvailable=None,
        layers=None,
        enablePickFeatures=None,
        rectangle=None,
        tilling_scheme=None,
        ellipsoid=None,
        tile_width=None,
        tile_height=None,
        tile_discard_policy=None,
        minimum_level=None,
        proxy=None,
    ):
        super(ArcGisMapServerImageryProvider, self).__init__(
            url=url,
            rectangle=rectangle,
            tilling_scheme=tilling_scheme,
            ellipsoid=ellipsoid,
            tile_width=tile_width,
            tile_height=tile_height,
            tile_discard_policy=tile_discard_policy,
            minimum_level=minimum_level,
            proxy=proxy,
        )

        self.token = token
        self.usePreCachedTilesIfAvailable = usePreCachedTilesIfAvailable
        self.layers = layers
        self.enablePickFeatures = enablePickFeatures


class BingMapsImageryProvider(ImageryProvider):
    """
    BingMapsImageryProvider

    Parameters
    ----------

    url : str
        The url of the Bing Maps server hosting the imagery.
    key : str
        The Bing Maps key for your application, which can be created at https://www.bingmapsportal.com/. If this parameter is not provided, BingMapsApi.defaultKey is used. If BingMapsApi.defaultKey is undefined as well, a message is written to the console reminding you that you must create and supply a Bing Maps key as soon as possible. Please do not deploy an application that uses Bing Maps imagery without creating a separate key for your application.
    tileProtocol : str
        The protocol to use when loading tiles, e.g. 'http:' or 'https:'. By default, tiles are loaded using the same protocol as the page.
    mapStyle : str, default BingMapsStyle.AERIAL
        The type of Bing Maps imagery to load.
    culture : str, default ''
        The culture to use when requesting Bing Maps imagery. Not all cultures are supported. See http://msdn.microsoft.com/en-us/library/hh441729.aspx for information on the supported cultures.
    ellipsoid : Ellipsoid
        The ellipsoid. If not specified, the WGS84 ellipsoid is used.
    tile_discard_policy : TileDiscardPolicy
        The policy that determines if a tile is invalid and should be discarded. If this value is not specified, a default DiscardMissingTileImagePolicy is used which requests tile 0,0 at the maximum tile level and checks pixels (0,0), (120,140), (130,160), (200,50), and (200,200). If all of these pixels are transparent, the discard check is disabled and no tiles are discarded. If any of them have a non-transparent color, any tile that has the same values in these pixel locations is discarded. The end result of these defaults should be correct tile discarding for a standard Bing Maps server. To ensure that no tiles are discarded, construct and pass a NeverTileDiscardPolicy for this parameter.
    proxy : Proxy
        A proxy to use for requests. This object is expected to have a getURL function which returns the proxied URL, if needed.
    """

    _props = [
        "url",
        "key",
        "tileProtocol",
        "mapStyle",
        "culture",
        "ellipsoid",
        "tile_discard_policy",
        "proxy",
    ]

    key = traitlets.Unicode()
    tileProtocol = traitlets.Unicode()
    mapStyle = traitlets.Unicode(allow_none=True)
    culture = traitlets.Unicode(allow_none=True)

    def __init__(
        self,
        url,
        key,
        tileProtocol,
        mapStyle=None,
        culture=None,
        ellipsoid=None,
        tile_discard_policy=None,
        proxy=None,
    ):
        super(BingMapsImageryProvider, self).__init__(
            url=url,
            ellipsoid=ellipsoid,
            tile_discard_policy=tile_discard_policy,
            proxy=proxy,
        )

        self.key = key
        self.tileProtocol = key
        self.mapStyle = mapStyle
        self.culture = culture


class GoogleEarthImageryProvider(ImageryProvider):
    """
    GoogleEarthImageryProvider

    Parameters
    ----------

    url : str
        The url of the Google Earth server hosting the imagery.
    channel : int
        The channel (id) to be used when requesting data from the server. The channel number can be found by looking at the json file located at: earth.localdomain/default_map/query?request=Json&vars=geeServerDefs The /default_map path may differ depending on your Google Earth Enterprise server configuration. Look for the "id" that is associated with a "ImageryMaps" requestType. There may be more than one id available. Example: { layers: [ { id: 1002, requestType: "ImageryMaps" }, { id: 1007, requestType: "VectorMapsRaster" } ] }
    path : str, default "/default_map"
        The path of the Google Earth server hosting the imagery.
    ellipsoid : Ellipsoid
        The ellipsoid. If not specified, the WGS84 ellipsoid is used.
    tile_discard_policy : TileDiscardPolicy
        The policy that determines if a tile is invalid and should be discarded. To ensure that no tiles are discarded, construct and pass a NeverTileDiscardPolicy for this parameter.
    maximum_level : int
        The maximum level-of-detail supported by the Google Earth Enterprise server, or undefined if there is no limit.
    proxy : Proxy
        A proxy to use for requests. This object is expected to have a getURL function which returns the proxied URL, if needed.
    """

    _props = [
        "url",
        "channel",
        "path",
        "ellipsoid",
        "tile_discard_policy",
        "maximum_level",
        "proxy",
    ]

    channel = traitlets.Float()
    path = traitlets.Unicode(allow_none=True)

    def __init__(
        self,
        url,
        channel,
        path=None,
        ellipsoid=None,
        tile_discard_policy=None,
        maximum_level=None,
        proxy=None,
    ):
        super(GoogleEarthImageryProvider, self).__init__(
            url=url,
            ellipsoid=ellipsoid,
            tile_discard_policy=tile_discard_policy,
            maximum_level=maximum_level,
            proxy=proxy,
        )

        self.channel = channel
        self.path = path


class GridImageryProvider(ImageryProvider):
    def __init__(self):
        # this accepts other kw than options
        raise NotImplementedError


class MapboxImageryProvider(ImageryProvider):
    """
    MapboxImageryProvider

    Parameters
    ----------

    url : str, default '//api.mapbox.com/v4/'
        The Mapbox server url.
    mapId : str
        The Mapbox Map ID.
    accessToken : str
        The public access token for the imagery.
    format : str, default 'png'
        The format of the image request.
    rectangle : Rectangle, default Rectangle.MAX_VALUE
        The rectangle, in radians, covered by the image.
    ellipsoid : Ellipsoid
        The ellipsoid. If not specified, the WGS84 ellipsoid is used.
    minimum_level : int, default 0
        The minimum level-of-detail supported by the imagery provider. Take care when specifying this that the number of tiles at the minimum level is small, such as four or less. A larger number is likely to result in rendering problems.
    maximum_level : int, default 0
        The maximum level-of-detail supported by the imagery provider, or undefined if there is no limit.
    credit : Credit or str
        A credit for the data source, which is displayed on the canvas.
    proxy : Proxy
        A proxy to use for requests. This object is expected to have a getURL function which returns the proxied URL.
    """

    _props = [
        "url",
        "mapId",
        "accessToken",
        "format",
        "rectangle",
        "ellipsoid",
        "minimum_level",
        "maximum_level",
        "credit",
        "proxy",
    ]

    url = traitlets.Unicode()
    mapId = traitlets.Unicode()
    accessToken = traitlets.Unicode()
    format = traitlets.Unicode(allow_none=True)

    def __init__(
        self,
        url,
        mapId,
        accessToken,
        format=None,
        rectangle=None,
        ellipsoid=None,
        minimum_level=None,
        maximum_level=None,
        credit=None,
        proxy=None,
    ):
        super(MapboxImageryProvider, self).__init__(
            url=url,
            rectangle=rectangle,
            ellipsoid=ellipsoid,
            minimum_level=minimum_level,
            maximum_level=maximum_level,
            credit=credit,
            proxy=proxy,
        )

        self.mapId = mapId
        self.accessToken = accessToken
        self.format = format


class OpenStreetMapImageryProvider(ImageryProvider):
    """
    OpenStreetMapImageryProvider

    Parameters
    ----------

    url : str, default '//a.tile.openstreetmap.org'
        The OpenStreetMap server url.
    file_extension : str, default 'png'
        The file extension for images on the server.
    rectangle : Rectangle, default Rectangle.MAX_VALUE
        The rectangle of the layer.
    ellipsoid : Ellipsoid
        The ellipsoid. If not specified, the WGS84 ellipsoid is used.
    minimum_level : int, default 0
        The minimum level-of-detail supported by the imagery provider.
    maximum_level : int
        The maximum level-of-detail supported by the imagery provider, or undefined if there is no limit.
    credit : Credit or str, default 'MapQuest, Open Street Map and contributors, CC-BY-SA'
        A credit for the data source, which is displayed on the canvas.
    proxy : Proxy
        A proxy to use for requests. This object is expected to have a getURL function which returns the proxied URL.
    """

    def __init__(
        self,
        url=None,
        file_extension=None,
        rectangle=None,
        ellipsoid=None,
        minimum_level=None,
        maximum_level=None,
        credit=None,
        proxy=None,
    ):
        super(OpenStreetMapImageryProvider, self).__init__(
            url=url,
            file_extension=file_extension,
            rectangle=rectangle,
            ellipsoid=ellipsoid,
            minimum_level=minimum_level,
            maximum_level=maximum_level,
            credit=credit,
            proxy=proxy,
        )


class SingleTileImageryProvider(ImageryProvider):
    """
    SingleTileImageryProvider

    Parameters
    ----------

    url : str
        The url for the tile.
    rectangle : Rectangle, default Rectangle.MAX_VALUE
        The rectangle, in radians, covered by the image.
    ellipsoid : Ellipsoid
        The ellipsoid. If not specified, the WGS84 ellipsoid is used.
    credit : Credit or str
        A credit for the data source, which is displayed on the canvas.
    proxy : Proxy
        A proxy to use for requests. This object is expected to have a getURL function which returns the proxied URL, if needed.
    """

    def __init__(self, url, rectangle=None, ellipsoid=None, credit=None, proxy=None):
        from cesiumpy.entities.material import TemporaryImage

        if isinstance(url, TemporaryImage):
            url = url.script

        super(SingleTileImageryProvider, self).__init__(
            url=url,
            rectangle=rectangle,
            ellipsoid=ellipsoid,
            credit=credit,
            proxy=proxy,
        )


class TileCoordinatesImageryProvider(ImageryProvider):
    """
    TileCoordinatesImageryProvider

    Parameters
    ----------

    color : cesiumpy.color.Color, default YELLOW
        The color to draw the tile box and label.
    tiling_scheme : TilingScheme, default new GeographicTilingScheme()
        The tiling scheme for which to draw tiles.
    ellipsoid : Ellipsoid
        The ellipsoid. If the tiling_scheme is specified, this parameter is ignored and the tiling scheme's ellipsoid is used instead. If neither parameter is specified, the WGS84 ellipsoid is used.
    tile_width : int, default 256
        The width of the tile for level-of-detail selection purposes.
    tile_height : int, default 256
        The height of the tile for level-of-detail selection purposes.
    """

    _props = ["color", "tilling_scheme", "ellipsoid", "tile_width", "tile_height"]

    def __init__(
        self,
        color=None,
        tilling_scheme=None,
        ellipsoid=None,
        tile_width=None,
        tile_height=None,
    ):
        super(TileCoordinatesImageryProvider, self).__init__(
            tilling_scheme=tilling_scheme,
            ellipsoid=ellipsoid,
            tile_width=tile_width,
            tile_height=tile_height,
        )

        if color is not None:
            color = cesiumpy.color._maybe_color(color)
            if not isinstance(color, cesiumpy.color.Color):
                msg = "color must be a Color instance: {0}"
                raise ValueError(msg.format(type(color)))
        self.color = color


class TileMapServiceImageryProvider(ImageryProvider):
    """
    TileMapServiceImageryProvider

    Parameters
    ----------

    url : str, default '.'
        Path to image tiles on server.
    file_extension : default 'png'
        The file extension for images on the server.
    rectangle : Rectangle, default Rectangle.MAX_VALUE
        The rectangle, in radians, covered by the image.
    tiling_scheme : TilingScheme, default new GeographicTilingScheme()
        The tiling scheme specifying how the ellipsoidal surface is broken into tiles. If this parameter is not provided, a WebMercatorTilingScheme is used.
    ellipsoid : Ellipsoid
        The ellipsoid. If the tiling_scheme is specified, this parameter is ignored and the tiling scheme's ellipsoid is used instead. If neither parameter is specified, the WGS84 ellipsoid is used.
    tile_width : int, default 256
        Pixel width of image tiles.
    tile_height : int, default 256
        Pixel height of image tiles.
    minimum_level : int, default 0
        The minimum level-of-detail supported by the imagery provider. Take care when specifying this that the number of tiles at the minimum level is small, such as four or less. A larger number is likely to result in rendering problems.
    maximum_level : int
        The maximum level-of-detail supported by the imagery provider, or undefined if there is no limit.
    credit : Credit or str, default ''
        A credit for the data source, which is displayed on the canvas.
    proxy : Proxy
        A proxy to use for requests. This object is expected to have a getURL function which returns the proxied URL.
    """

    def __init__(
        self,
        url=None,
        file_extension=None,
        rectangle=None,
        tilling_scheme=None,
        ellipsoid=None,
        tile_width=None,
        tile_height=None,
        minimum_level=None,
        maximum_level=None,
        credit=None,
        proxy=None,
    ):
        super(TileMapServiceImageryProvider, self).__init__(
            url=url,
            file_extension=file_extension,
            rectangle=rectangle,
            tilling_scheme=tilling_scheme,
            ellipsoid=ellipsoid,
            tile_width=tile_width,
            tile_height=tile_height,
            minimum_level=minimum_level,
            maximum_level=maximum_level,
            credit=credit,
            proxy=proxy,
        )


class UrlTemplateImageryProvider(ImageryProvider):
    def __init__(self):
        raise NotImplementedError


class WebMapServiceImageryProvider(ImageryProvider):
    """
    WebMapServiceImageryProvider

    Parameters
    ----------

    url : str
        The URL of the WMS service. The URL supports the same keywords as the UrlTemplateImageryProvider.
    layers : str
        The layers to include, separated by commas.
    parameters : Object, default WebMapServiceImageryProvider.DefaultParameters
        Additional parameters to pass to the WMS server in the GetMap URL.
    getFeatureInfoParameters : Object, default WebMapServiceImageryProvider.GetFeatureInfoDefaultParameters
        Additional parameters to pass to the WMS server in the GetFeatureInfo URL.
    enablePickFeatures : bool, default True
        If true, WebMapServiceImageryProvider#pickFeatures will invoke the GetFeatureInfo operation on the WMS server and return the features included in the response. If false, WebMapServiceImageryProvider#pickFeatures will immediately return undefined (indicating no pickable features) without communicating with the server. Set this property to false if you know your WMS server does not support GetFeatureInfo or if you don't want this provider's features to be pickable.
    getFeatureInfoFormats : list of GetFeatureInfoFormat, default WebMapServiceImageryProvider.DefaultGetFeatureInfoFormats
        The formats in which to try WMS GetFeatureInfo requests.
    rectangle : Rectangle, default Rectangle.MAX_VALUE
        The rectangle of the layer.
    tiling_scheme : TilingScheme, default new GeographicTilingScheme()
        The tiling scheme to use to divide the world into tiles.
    ellipsoid : Ellipsoid
        The ellipsoid. If the tiling_scheme is specified, this parameter is ignored and the tiling scheme's ellipsoid is used instead. If neither parameter is specified, the WGS84 ellipsoid is used.
    tile_width : int, default 256
        The width of each tile in pixels.
    tile_height : int, default 256
        The height of each tile in pixels.
    minimum_level : int, default 0
        The minimum level-of-detail supported by the imagery provider. Take care when specifying this that the number of tiles at the minimum level is small, such as four or less. A larger number is likely to result in rendering problems.
    maximum_level : int
        The maximum level-of-detail supported by the imagery provider, or undefined if there is no limit. If not specified, there is no limit.
    credit : Credit or str
        A credit for the data source, which is displayed on the canvas.
    proxy : Proxy
        A proxy to use for requests. This object is expected to have a getURL function which returns the proxied URL, if needed.
    subdomains : str or list of str, default 'abc'
    """

    _props = [
        "url",
        "layers",
        "parameters",
        "getFeatureInfoParameters",
        "enablePickFeatures",
        "getFeatureInfoFormats",
        "rectangle",
        "tilling_scheme",
        "ellipsoid",
        "tile_width",
        "tile_height",
        "tile_discard_policy",
        "minimum_level",
        "maximum_level",
        "credit",
        "proxy",
        "subdomains",
    ]

    layers = traitlets.Unicode()
    enablePickFeatures = traitlets.Bool(allow_none=True)

    def __init__(
        self,
        url,
        layers,
        parameters=None,
        getFeatureInfoParameters=None,
        enablePickFeatures=None,
        getFeatureInfoFormats=None,
        rectangle=None,
        tilling_scheme=None,
        ellipsoid=None,
        tile_width=None,
        tile_height=None,
        tile_discard_policy=None,
        minimum_level=None,
        maximum_level=None,
        credit=None,
        proxy=None,
        subdomains=None,
    ):
        super(WebMapServiceImageryProvider, self).__init__(
            url=url,
            rectangle=rectangle,
            tilling_scheme=tilling_scheme,
            ellipsoid=ellipsoid,
            tile_width=tile_width,
            tile_height=tile_height,
            tile_discard_policy=tile_discard_policy,
            minimum_level=minimum_level,
            maximum_level=maximum_level,
            credit=credit,
            proxy=proxy,
            subdomains=subdomains,
        )

        self.layers = layers

        self.parameters = com.notimplemented(parameters)
        self.getFeatureInfoParameters = com.notimplemented(getFeatureInfoParameters)

        self.enablePickFeatures = enablePickFeatures

        self.getFeatureInfoFormats = com.notimplemented(getFeatureInfoFormats)


class WebMapTileServiceImageryProvider(ImageryProvider):
    """
    WebMapTileServiceImageryProvider

    Parameters
    ----------

    url : str
        The base URL for the WMTS GetTile operation (for KVP-encoded requests) or the tile-URL template (for RESTful requests). The tile-URL template should contain the following variables: {style}, {TileMatrixSet}, {TileMatrix}, {TileRow}, {TileCol}. The first two are optional if actual values are hardcoded or not required by the server. The {s} keyword may be used to specify subdomains.
    layer : str
        The layer name for WMTS requests.
    style : str
        The style name for WMTS requests.
    format : str, default 'image/jpeg'
        The MIME type for images to retrieve from the server.
    tile_matrix_set_id : str
        The identifier of the TileMatrixSet to use for WMTS requests.
    tile_matrix_labels : list
        optional A list of identifiers in the TileMatrix to use for WMTS requests, one per TileMatrix level.
    rectangle : Rectangle, default Rectangle.MAX_VALUE
        The rectangle covered by the layer.
    tiling_scheme : TilingScheme, default new GeographicTilingScheme()
        The tiling scheme corresponding to the organization of the tiles in the TileMatrixSet.
    ellipsoid : Ellipsoid
        The ellipsoid. If not specified, the WGS84 ellipsoid is used.
    tile_width : int, default 256
        optional The tile width in pixels.
    tile_height : int, default 256
        The tile height in pixels.
    minimum_level : int, default 0
        The minimum level-of-detail supported by the imagery provider.
    maximum_level : int
        The maximum level-of-detail supported by the imagery provider, or undefined if there is no limit.
    credit : Credit or str
        A credit for the data source, which is displayed on the canvas.
    proxy : Proxy
        A proxy to use for requests. This object is expected to have a getURL function which returns the proxied URL.
    subdomains : str or list of str, default 'abc'
        The subdomains to use for the {s} placeholder in the URL template. If this parameter is a single string, each character in the string is a subdomain. If it is an array, each element in the array is a subdomain.
    """

    _props = [
        "url",
        "layer",
        "style",
        "format",
        "tile_matrix_labels",
        "tile_matrix_labels",
        "rectangle",
        "tilling_scheme",
        "ellipsoid",
        "tile_width",
        "tile_height",
        "tile_discard_policy",
        "minimum_level",
        "maximum_level",
        "credit",
        "proxy",
        "subdomains",
    ]

    layer = traitlets.Unicode()
    style = traitlets.Unicode()
    format = traitlets.Unicode(allow_none=True)
    tile_matrix_set_id = traitlets.Unicode(allow_none=True)

    def __init__(
        self,
        url,
        layer,
        style,
        format=None,
        tile_matrix_set_id=None,
        tile_matrix_labels=None,
        rectangle=None,
        tilling_scheme=None,
        ellipsoid=None,
        tile_width=None,
        tile_height=None,
        tile_discard_policy=None,
        minimum_level=None,
        maximum_level=None,
        credit=None,
        proxy=None,
        subdomains=None,
    ):
        super(WebMapTileServiceImageryProvider, self).__init__(
            url=url,
            rectangle=rectangle,
            tilling_scheme=tilling_scheme,
            ellipsoid=ellipsoid,
            tile_width=tile_width,
            tile_height=tile_height,
            tile_discard_policy=tile_discard_policy,
            minimum_level=minimum_level,
            maximum_level=maximum_level,
            credit=credit,
            proxy=proxy,
            subdomains=subdomains,
        )
        self.layer = layer
        self.style = style
        self.format = format
        self.tile_matrix_set_id = tile_matrix_set_id

        self.tile_matrix_labels = com.notimplemented(tile_matrix_labels)
