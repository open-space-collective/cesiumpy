# Apache License 2.0

from __future__ import unicode_literals

import six
import traitlets

import cesiumpy
from cesiumpy.base import _CesiumEnum
from cesiumpy.entities.entity import _CesiumEntity
from cesiumpy.entities.pinbuilder import Pin
import cesiumpy.entities.cartesian as cartesian
import cesiumpy.constants as constants
import cesiumpy.util.common as com
from cesiumpy.util.trait import MaybeTrait


class Label(_CesiumEntity):
    """
    LabelGraphics

    Parameters
    ----------

    position : Cartesian3
        A Property specifying the Cartesian3 positions.
    text : str
        A Property specifying the text.
    font : str, default '10px sans-serif'
        A Property specifying the CSS font.
    style : LabeStyle, default LabelStyle.FILL
        A Property specifying the LabelStyle.
    fill_color : Color, default Color.WHITE
        A Property specifying the fill Color.
    outline_color : Color, default, Color.BLACK
        A Property specifying the outline Color.
    outline_width : float, default 1.
        A numeric Property specifying the outline width.
    show : bool, default True
        A boolean Property specifying the visibility of the label.
    scale : float, default 1.
        A numeric Property specifying the scale to apply to the text.
    horizontal_origin : horizontal_origin, default horizontal_origin.CENTER
        A Property specifying the horizontal_origin.
    vertical_origin : vertical_origin, default vertical_origin.CENTER
        A Property specifying the vertical_origin.
    eye_offset : Cartesian3, default Cartesian3.ZERO
        A Cartesian3 Property specifying the eye offset.
    pixel_offset : Cartesian2, default Cartesian2.ZERO
        A Cartesian2 Property specifying the pixel offset.
    translucency_by_distance :
        A NearFarScalar Property used to set translucency based on distance from the camera.
    pixel_offset_scale_by_distance :
        A NearFarScalar Property used to set pixel_offset based on distance from the camera.
    """

    _klass = "label"
    _props = ["text", "style", "fill_color"]

    text = traitlets.Unicode()
    fill_color = MaybeTrait(klass=cesiumpy.color.Color, allow_none=True)

    def __init__(
        self,
        position,
        text,
        style=None,
        fill_color=None,
        outline_color=None,
        outline_width=None,
        show=None,
        scale=None,
        horizontal_origin=None,
        vertical_origin=None,
        eye_offset=None,
        pixel_offset=None,
        translucency_by_distance=None,
        pixel_offset_scale_by_distance=None,
        name=None,
    ):
        super(Label, self).__init__(
            show=show,
            outline_color=outline_color,
            outline_width=outline_width,
            translucency_by_distance=translucency_by_distance,
            scale=scale,
            horizontal_origin=horizontal_origin,
            vertical_origin=vertical_origin,
            eye_offset=eye_offset,
            pixel_offset=pixel_offset,
            pixel_offset_scale_by_distance=pixel_offset_scale_by_distance,
            position=position,
            name=name,
        )

        self.text = text
        self.style = com.notimplemented(style)
        self.fill_color = fill_color


class Billboard(_CesiumEntity):
    """
    PointGraphics

    Parameters
    ----------

    position : Cartesian3
        A Property specifying the Cartesian3 positions.
    image : str or Pin, default Pin()
        A Property specifying the Image, URI, or Canvas to use for the billboard.
    show : bool, default True
        A boolean Property specifying the visibility of the billboard.
    scale : float, default 1.
        A numeric Property specifying the scale to apply to the image size.
    horizontal_origin : horizontal_origin, default horizontal_origin.CENTER
        A Property specifying the horizontal_origin.
    vertical_origin : vertical_origin, default vertical_origin.CENTER
        A Property specifying the vertical_origin.
    eye_offset : Cartesian3, default Cartesian3.ZERO
        A Cartesian3 Property specifying the eye offset.
    pixel_offset : Cartesian2, default Cartesian2.ZERO
        A Cartesian2 Property specifying the pixel offset.
    rotation : float, default 0.
        A numeric Property specifying the rotation about the aligned_axis.
    aligned_axis : Cartesian3, default Cartesian3.ZERO
        A Cartesian3 Property specifying the axis of rotation.
    width : float
        A numeric Property specifying the width of the billboard in pixels, overriding the native size.
    height : float
        A numeric Property specifying the height of the billboard in pixels, overriding the native size.
    color : Color, default Color.WHITE
        A Property specifying the tint Color of the image.
    scale_by_distance :
        A NearFarScalar Property used to scale the point based on distance from the camera.
    translucency_by_distance :
        optional A NearFarScalar Property used to set translucency based on distance from the camera.
    pixel_offset_scale_by_distance :
        optional A NearFarScalar Property used to set pixel_offset based on distance from the camera.
    image_sub_region :
        A Property specifying a BoundingRectangle that defines a sub-region of the image to use for the billboard, rather than the entire image.
    size_in_meters : bool
        A boolean Property specifying whether this billboard's size should be measured in meters.
    """

    _klass = "billboard"
    _props = ["image", "aligned_axis", "image_sub_region", "size_in_meters"]

    image = traitlets.Instance(klass=cesiumpy.entities.pinbuilder._BillboardContents)

    def __init__(
        self,
        position,
        image=None,
        show=None,
        scale=None,
        horizontal_origin=None,
        vertical_origin=None,
        eye_offset=None,
        pixel_offset=None,
        rotation=None,
        aligned_axis=None,
        width=None,
        height=None,
        color=None,
        scale_by_distance=None,
        translucency_by_distance=None,
        pixel_offset_scale_by_distance=None,
        image_sub_region=None,
        size_in_meters=None,
        name=None,
    ):
        super(Billboard, self).__init__(
            show=show,
            scale=scale,
            color=color,
            horizontal_origin=horizontal_origin,
            vertical_origin=vertical_origin,
            eye_offset=eye_offset,
            pixel_offset=pixel_offset,
            rotation=rotation,
            width=width,
            height=height,
            scale_by_distance=scale_by_distance,
            translucency_by_distance=translucency_by_distance,
            pixel_offset_scale_by_distance=pixel_offset_scale_by_distance,
            position=position,
            name=name,
        )
        if image is None:
            image = Pin()

        if isinstance(image, six.string_types):
            image = cesiumpy.entities.pinbuilder.Icon(image)
        self.image = image

        self.aligned_axis = com.notimplemented(aligned_axis)
        self.image_sub_region = com.notimplemented(image_sub_region)
        self.size_in_meters = com.notimplemented(size_in_meters)


class Ellipse(_CesiumEntity):
    """
    EllipseGraphics

    Parameters
    ----------

    position : Cartesian3
        A Property specifying the Cartesian3 positions.
    semi_major_axis : float
        The numeric Property specifying the semi-major axis.
    semi_minor_axis : float
        The numeric Property specifying the semi-minor axis.
    height : float, default 0.
        A numeric Property specifying the altitude of the ellipse.
    extruded_height : float, default 0.
        A numeric Property specifying the altitude of the ellipse extrusion.
    show : bool, default True
        A boolean Property specifying the visibility of the ellipse.
    fill : bool, default True
        A boolean Property specifying whether the ellipse is filled with the provided material.
    material : cesiumpy.cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the ellipse.
    outline : bool, default False
        A boolean Property specifying whether the ellipse is outlined.
    outline_color : cesiumpy.cesiumpy.color.Color, default BLACK
        A Property specifying the Color of the outline.
    outline_width : float, default 1.
        A numeric Property specifying the width of the outline.
    number_of_vertical_lines : int, default 16
        Property specifying the number of vertical lines to draw along the perimeter for the outline.
    rotation : float, default 0.
        A numeric property specifying the rotation of the ellipse counter-clockwise from north.
    st_rotation : float, default 0.
        A numeric property specifying the rotation of the ellipse texture counter-clockwise from north.
    granularity : float, default cesiumpy.math.RADIANS_PER_DEGREE
        A numeric Property specifying the angular distance between points on the ellipse.
    """

    _klass = "ellipse"
    _props = ["semi_minor_axis", "semi_major_axis"]

    semi_minor_axis = traitlets.Float()
    semi_major_axis = traitlets.Float()

    def __init__(
        self,
        position,
        semi_minor_axis,
        semi_major_axis,
        height=None,
        extruded_height=None,
        show=None,
        fill=None,
        material=None,
        outline=None,
        outline_color=None,
        outline_width=None,
        number_of_vertical_lines=None,
        rotation=None,
        st_rotation=None,
        name=None,
    ):
        super(Ellipse, self).__init__(
            height=height,
            extruded_height=extruded_height,
            show=show,
            fill=fill,
            material=material,
            outline=outline,
            outline_color=outline_color,
            outline_width=outline_width,
            number_of_vertical_lines=number_of_vertical_lines,
            rotation=rotation,
            st_rotation=st_rotation,
            position=position,
            name=name,
        )

        self.semi_minor_axis = semi_minor_axis
        self.semi_major_axis = semi_major_axis


class Ellipsoid(_CesiumEntity):
    """
    EllipsoidGraphics

    Parameters
    ----------
    position : Cartesian3
        A Property specifying the Cartesian3 positions.
    radii : Cartesian3
        A Cartesian3 Property specifying the radii of the ellipsoid.
    show : bool, default True
        A boolean Property specifying the visibility of the ellipsoid.
    fill : bool, default True
        A boolean Property specifying whether the ellipsoid is filled with the provided material.
    material : cesiumpy.cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the ellipsoid.
    outline : bool, default False
        A boolean Property specifying whether the ellipsoid is outlined.
    outline_color : CeciumColor, BLACK
        A Property specifying the Color of the outline.
    outline_width : float, default 1.
        A numeric Property specifying the width of the outline.
    subdivisions : int, default 128
        A Property specifying the number of samples per outline ring, determining the granularity of the curvature.
    stackPartitions : int, default 64
        A Property specifying the number of stacks.
    slicePartitions : int, default 64
        A Property specifying the number of radial slices.
    """

    _klass = "ellipsoid"
    _props = ["radii", "subdivisions", "stackPartitions", "slicePartitions"]

    radii = MaybeTrait(klass=cartesian.Cartesian3)
    subdivisions = traitlets.Float(allow_none=True)
    stackPartitions = traitlets.Float(allow_none=True)
    slicePartitions = traitlets.Float(allow_none=True)

    def __init__(
        self,
        position,
        radii,
        show=None,
        fill=None,
        material=None,
        outline=None,
        outline_color=None,
        outline_width=None,
        subdivisions=None,
        stackPartitions=None,
        slicePartitions=None,
        name=None,
    ):
        super(Ellipsoid, self).__init__(
            show=show,
            fill=fill,
            material=material,
            outline=outline,
            outline_color=outline_color,
            outline_width=outline_width,
            position=position,
            name=name,
        )
        self.radii = radii
        self.subdivisions = subdivisions
        self.stackPartitions = stackPartitions
        self.slicePartitions = slicePartitions


class PolylineVolume(_CesiumEntity):
    """
    PolylineVolumeGraphics

    Parameters
    ----------

    positions : Cartesian3
        A Property specifying the array of Cartesian3 positions which define the line strip.
    shape : Cartesian2
        optional A Property specifying the array of Cartesian2 positions which define the shape to be extruded.
    cornerType : CornerType, default ROUNDED
        A CornerType Property specifying the style of the corners.
    show : bool, default True
        A boolean Property specifying the visibility of the volume.
    fill : bool, default True
        A boolean Property specifying whether the volume is filled with the provided material.
    material : cesiumpy.cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the volume.
    outline : bool, default False
        A boolean Property specifying whether the volume is outlined.
    outline_color : cesiumpy.cesiumpy.color.Color, default BLACK
        A Property specifying the Color of the outline.
    outline_width : float, default 1.
        A numeric Property specifying the width of the outline.
    granularity : float, default cesiumpy.math.RADIANS_PER_DEGREE
        A numeric Property specifying the angular distance between each latitude and longitude point.
    """

    _klass = "polylineVolume"
    _props = ["positions", "shape", "cornerType"]

    positions = traitlets.Instance(klass=cartesian.Cartesian3Array)
    shape = traitlets.List(minlen=2)
    cornerType = traitlets.Instance(klass=constants.CornerType, allow_none=True)

    def __init__(
        self,
        positions,
        shape,
        cornerType=None,
        show=None,
        fill=None,
        material=None,
        outline=None,
        outline_color=None,
        outline_width=None,
        granularity=None,
        name=None,
    ):
        # polylineVolume uses "positions", not "position"

        super(PolylineVolume, self).__init__(
            show=show,
            fill=fill,
            material=material,
            outline=outline,
            outline_color=outline_color,
            outline_width=outline_width,
            granularity=granularity,
            name=name,
        )

        self.positions = cartesian.Cartesian3.fromDegreesArray(positions)
        self.shape = cartesian._maybe_cartesian2_list(shape, key="shape")
        self.cornerType = cornerType


class Corridor(_CesiumEntity):
    """
    CorridorGraphics

    Parameters
    ----------

    positions : Cartesian3
        A Property specifying the array of Cartesian3 positions that define the centerline of the corridor.
    width : float
        A numeric Property specifying the distance between the edges of the corridor.
    cornerType : CornerType, default CornerType.ROUNDED
        A CornerType Property specifying the style of the corners.
    height : float, default 0.
        A numeric Property specifying the altitude of the corridor.
    extruded_height : float, default 0.
        A numeric Property specifying the altitude of the corridor extrusion.
    show : bool, default True
        A boolean Property specifying the visibility of the corridor.
    fill : bool, default True
        A boolean Property specifying whether the corridor is filled with the provided material.
    material : cesiumpy.cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the corridor.
    outline : bool, default False
        A boolean Property specifying whether the corridor is outlined.
    outline_color : cesiumpy.cesiumpy.color.Color, default BLACK
        A Property specifying the Color of the outline.
    outline_width : float, default 1.
        A numeric Property specifying the width of the outline.
    granularity : float, default cesiumpy.math.RADIANS_PER_DEGREE
        A numeric Property specifying the distance between each latitude and longitude.
    """

    _klass = "corridor"
    _props = ["positions", "cornerType"]

    positions = traitlets.Instance(klass=cartesian.Cartesian3Array)
    cornerType = traitlets.Instance(klass=constants.CornerType, allow_none=True)

    def __init__(
        self,
        positions,
        width,
        cornerType=None,
        height=None,
        extruded_height=None,
        show=None,
        fill=None,
        material=None,
        outline=None,
        outline_color=None,
        outline_width=None,
        granularity=None,
        name=None,
    ):
        # corridor uses "positions", not "position"

        super(Corridor, self).__init__(
            width=width,
            height=height,
            extruded_height=extruded_height,
            show=show,
            fill=fill,
            material=material,
            outline=outline,
            outline_color=outline_color,
            outline_width=outline_width,
            granularity=granularity,
            name=name,
        )

        self.positions = cartesian.Cartesian3.fromDegreesArray(positions)
        self.cornerType = cornerType


class Wall(_CesiumEntity):
    """
    WallGraphics

    Parameters
    ----------

    positions : Cartesian3
        A Property specifying the array of Cartesian3 positions which define the top of the wall.
    maximum_heights : float or its list
        A Property specifying an array of heights to be used for the top of the wall instead of the height of each position.
    minimum_heights : float or its list
        A Property specifying an array of heights to be used for the bottom of the wall instead of the globe surface.
    show : bool, default True
        A boolean Property specifying the visibility of the wall.
    fill : bool, default True
        A boolean Property specifying whether the wall is filled with the provided material.
    material : cesiumpy.cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the wall.
    outline : bool, default False
        A boolean Property specifying whether the wall is outlined.
    outline_color : cesiumpy.cesiumpy.color.Color, default BLACK
        A Property specifying the Color of the outline.
    outline_width : float, default 1.
        A numeric Property specifying the width of the outline.
    granularity : float, default cesiumpy.math.RADIANS_PER_DEGREE
        A numeric Property specifying the angular distance between each latitude and longitude point.
    """

    _klass = "wall"
    _props = ["positions", "maximum_heights", "minimum_heights"]

    positions = traitlets.Instance(klass=cartesian.Cartesian3Array)

    def __init__(
        self,
        positions,
        maximum_heights,
        minimum_heights,
        show=None,
        fill=None,
        material=None,
        outline=None,
        outline_color=None,
        outline_width=None,
        granularity=None,
        name=None,
    ):
        # Wall uses "positions", not "position"
        super(Wall, self).__init__(
            show=show,
            fill=fill,
            material=material,
            outline=outline,
            outline_color=outline_color,
            outline_width=outline_width,
            granularity=granularity,
            name=name,
        )

        # ToDo: Support fromDegreesArrayHeights
        self.positions = cartesian.Cartesian3.fromDegreesArray(positions)
        pos_len = len(self.positions) // 3

        def _init_heights(x, key):
            if not isinstance(x, list):
                com.validate_numeric(x, key=key)
                x = [x] * pos_len
            if len(x) != pos_len:
                msg = "{key} must has the half length ({pos_len}) of positions: {x}"
                raise ValueError(
                    msg.format(key=key, pos_len=pos_len, x=len(maximum_heights))
                )
            return x

        self.maximum_heights = _init_heights(maximum_heights, key="maximum_heights")
        self.minimum_heights = _init_heights(minimum_heights, key="minimum_heights")


class Rectangle(_CesiumEntity):
    """
    RectangleGraphics

    Parameters
    ----------

    coordinates : list of 4 floats, corresponding to west, south, east, north
        The Property specifying the Rectangle.
    height : float, default 0.
        A numeric Property specifying the altitude of the rectangle.
    extruded_height : float, default 0.
        A numeric Property specifying the altitude of the rectangle extrusion.
    close_top : bool, default True
        A boolean Property specifying whether the rectangle has a top cover when extruded
    close_bottom : bool, default True
        A boolean Property specifying whether the rectangle has a bottom cover when extruded.
    show : bool, default True
        A boolean Property specifying the visibility of the rectangle.
    fill : bool, default True
        A boolean Property specifying whether the rectangle is filled with the provided material.
    material : cesiumpy.cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the rectangle.
    outline : bool, default False
        A boolean Property specifying whether the rectangle is outlined.
    outline_color : cesiumpy.cesiumpy.color.Color, default BLACK
        A Property specifying the Color of the outline.
    outline_width : float, default 1.
        A numeric Property specifying the width of the outline.
    rotation : float, default 0.
        A numeric property specifying the rotation of the rectangle clockwise from north.
    st_rotation : float, default 0.
        A numeric property specifying the rotation of the rectangle texture counter-clockwise from north.
    granularity : float, default cesiumpy.math.RADIANS_PER_DEGREE
        A numeric Property specifying the angular distance between points on the rectangle.
    """

    _klass = "rectangle"
    _props = ["coordinates", "close_top", "close_bottom"]

    coordinates = MaybeTrait(klass=cartesian.Rectangle)
    close_top = traitlets.Bool(allow_none=True)
    close_bottom = traitlets.Bool(allow_none=True)

    def __init__(
        self,
        coordinates,
        height=None,
        extruded_height=None,
        close_top=None,
        close_bottom=None,
        show=None,
        fill=None,
        material=None,
        outline=None,
        outline_color=None,
        outline_width=None,
        st_rotation=None,
        granularity=None,
        name=None,
    ):
        super(Rectangle, self).__init__(
            height=height,
            extruded_height=extruded_height,
            show=show,
            fill=fill,
            material=material,
            outline=outline,
            outline_color=outline_color,
            outline_width=outline_width,
            st_rotation=st_rotation,
            granularity=granularity,
            name=name,
        )

        self.coordinates = coordinates
        self.close_top = close_top
        self.close_bottom = close_bottom

    def __repr__(self):
        rep = """{klass}({rep})""".format(
            klass=self.__class__.__name__, rep=self.coordinates._inner_repr
        )
        return rep


class ShadowMode(_CesiumEnum):
    DISABLED = (
        "Cesium.ShadowMode.DISABLED"  # The object does not cast or receive shadows.
    )
    ENABLED = "Cesium.ShadowMode.ENABLED"  # The object casts and receives shadows.
    CAST_ONLY = "Cesium.ShadowMode.CAST_ONLY"  # The object casts shadows only.
    RECEIVE_ONLY = "Cesium.ShadowMode.RECEIVE_ONLY"  # The object receives shadows only.


class Polygon(_CesiumEntity):
    """
    PolygonGraphics

    Parameters
    ----------

    hierarchy : Cartesian3
        A Property specifying the PolygonHierarchy.
    height : float, default 0.
        A numeric Property specifying the altitude of the polygon.
    extruded_height : float, default 0.
        A numeric Property specifying the altitude of the polygon extrusion.
    show : bool, default True
        A boolean Property specifying the visibility of the polygon.
    fill : bool, default True
        A boolean Property specifying whether the polygon is filled with the provided material.
    material : cesiumpy.cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the polygon.
    outline : bool, default False
        A boolean Property specifying whether the polygon is outlined.
    outline_color : cesiumpy.cesiumpy.color.Color, default cesiumpy.color.BLACK
        A Property specifying the Color of the outline.
    outline_width : float, default 1.
        A numeric Property specifying the width of the outline.
    st_rotation : float, default 0.
        A numeric property specifying the rotation of the polygon texture counter-clockwise from north.
    granularity : float, default cesiumpy.math.RADIANS_PER_DEGREE
        A numeric Property specifying the angular distance between each latitude and longitude point.
    per_position_height : bool, default False
        A boolean specifying whether or not the the height of each position is used.
    """

    _klass = "polygon"
    _props = ["hierarchy", "per_position_height"]

    per_position_height = traitlets.Bool(allow_none=True)

    def __init__(
        self,
        hierarchy,
        height=None,
        extruded_height=None,
        show=None,
        fill=None,
        material=None,
        outline=None,
        outline_color=None,
        outline_width=None,
        st_rotation=None,
        granularity=None,
        per_position_height=None,
        name=None,
    ):
        super(Polygon, self).__init__(
            height=height,
            extruded_height=extruded_height,
            show=show,
            fill=fill,
            material=material,
            outline=outline,
            outline_color=outline_color,
            outline_width=outline_width,
            st_rotation=st_rotation,
            granularity=granularity,
            name=name,
        )

        self.hierarchy = cartesian.Cartesian3.fromDegreesArray(hierarchy)
        self.per_position_height = per_position_height

    @property
    def positions(self):
        # for compat
        return self.hierarchy
