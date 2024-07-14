# Apache License 2.0

from __future__ import unicode_literals

import traitlets

from cesiumpy.base import _CesiumObject
from cesiumpy.entities.transform import Transforms
import cesiumpy.util.common as com
from cesiumpy.util.trait import URITrait


class Model(_CesiumObject):
    """
    3D Model

    Parameters
    ----------

    url : str
        The object for the glTF JSON or an arraybuffer of Binary glTF defined by the KHR_binary_glTF extension.
    model_matrix : Matrix4, default Matrix4.IDENTITY
        The 4x4 transformation matrix that transforms the model from model to world coordinates.
    base_path : str, default ''
        The base path that paths in the glTF JSON are relative to.
    show : bool, default True
        Determines if the model primitive will be shown.
    scale : float, default 1.0
        A uniform scale applied to this model.
    minimum_pixel_size : float, default 0.0
        The approximate minimum pixel size of the model regardless of zoom.
    maximum_scale : float
        The maximum scale size of a model. An upper limit for minimum_pixel_size.
    id :
        A user-defined object to return when the model is picked with Scene#pick.
    allow_picking : bool, default True
        When true, each glTF mesh and primitive is pickable with Scene#pick.
    incrementally_load_textures : bool, default True
        Determine if textures may continue to stream in after the model is loaded.
    asynchronous : bool, default True
        Determines if model WebGL resource creation will be spread out over several frames or block until completion once all glTF files are loaded.
    debug_show_bounding_volume : bool, default False
        For debugging only. Draws the bounding sphere for each draw command in the model.
    debug_wireframe : bool, default False
        For debugging only. Draws the model in wireframe.
    """

    _props = [
        "url",
        "base_path",
        "show",
        "model_matrix",
        "scale",
        "minimum_pixel_size",
        "maximum_scale",
        "id",
        "allow_picking",
        "incrementally_load_textures",
        "asynchronous",
        "debug_show_bounding_volume",
        "debug_wireframe",
    ]

    url = URITrait()
    model_matrix = traitlets.Instance(klass=Transforms)

    base_path = traitlets.Unicode(allow_none=True)
    show = traitlets.Bool(allow_none=True)
    scale = traitlets.Float(allow_none=True)
    minimum_pixel_size = traitlets.Float(allow_none=True)
    maximum_scale = traitlets.Float(allow_none=True)

    allow_picking = traitlets.Bool(allow_none=True)
    incrementally_load_textures = traitlets.Bool(allow_none=True)
    asynchronous = traitlets.Bool(allow_none=True)
    debug_show_bounding_volume = traitlets.Bool(allow_none=True)
    debug_wireframe = traitlets.Bool(allow_none=True)

    def __init__(
        self,
        url,
        model_matrix,
        base_path=None,
        show=None,
        scale=None,
        minimum_pixel_size=None,
        maximum_scale=None,
        id=None,
        allow_picking=None,
        incrementally_load_textures=None,
        asynchronous=None,
        debug_show_bounding_volume=None,
        debug_wireframe=None,
    ):
        self.url = url

        self.model_matrix = Transforms.eastNorthUpToFixedFrame(model_matrix)

        self.base_path = base_path
        self.show = show
        self.scale = scale
        self.minimum_pixel_size = minimum_pixel_size
        self.maximum_scale = maximum_scale
        self.id = com.notimplemented(id)
        self.allow_picking = allow_picking
        self.incrementally_load_textures = incrementally_load_textures
        self.asynchronous = asynchronous
        self.debug_show_bounding_volume = debug_show_bounding_volume
        self.debug_wireframe = debug_wireframe

    def __repr__(self):
        rep = """{klass}("{url}")"""
        return rep.format(klass=self.__class__.__name__, url=self.url)

    @property
    def script(self):
        script = """Cesium.Model.fromGltf({script})"""
        return script.format(script=super(Model, self).script)
