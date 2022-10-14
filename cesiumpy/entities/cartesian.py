######################################################################################################################################################

# @project        CesiumPy
# @file           cesiumpy/entities/cartesian.py
# @license        Apache 2.0

######################################################################################################################################################

from __future__ import annotations
from __future__ import unicode_literals

import math
import traitlets

from cesiumpy.base import _CesiumObject
import cesiumpy.extension.geocode as geocode
import cesiumpy.extension.shapefile as shapefile
import cesiumpy.util.common as com

######################################################################################################################################################


class _Cartesian(_CesiumObject):

    _is_degrees = traitlets.Bool()

    # class property
    _is_array = False

    def __init__(self):
        raise NotImplementedError

    def generate_script(self, widget=None) -> str:
        if self._is_array or self._is_degrees:
            return f"Cesium.{self}"
        return f"new Cesium.{self}"


def _maybe_cartesian2_list(x, key):
    """
    Convert list or tuple to list of Cartesian2 instances. Used by PolylineVolume
    """
    if com.is_listlike(x):
        if all(isinstance(e, Cartesian2) for e in x):
            return x
        elif all(isinstance(e, _Cartesian) for e in x):
            # for better error message
            msg = "{key} must be a listlike of Cartesian2: {x}"
            raise ValueError(msg.format(key=key, x=x))

        if com.is_listlike_2elem(x):
            x = com._flatten_list_of_listlike(x)

    x = com.validate_listlike_even(x, key=key)
    x = [Cartesian2(i, j) for (i, j) in zip(x[::2], x[1::2])]
    return x


######################################################################################################################################################


class Cartesian2(_Cartesian):

    # Definitions

    x = traitlets.Float()
    y = traitlets.Float()

    # Constructor

    def __init__(
        self,
        x: float,
        y: float,
        degrees: bool = False,
    ) -> None:

        self.x: float = x
        self.y: float = y

        self._is_degrees: bool = degrees

        if degrees:
            com.validate_longitude(x, key="x")
            com.validate_latitude(y, key="y")

    # Methods

    def __len__(self) -> int:
        return len(self.x)

    def __repr__(self) -> str:
        if self._is_degrees:
            rep = """Cartesian2.fromDegrees({x}, {y})"""
            return rep.format(x=self.x, y=self.y)

        rep = """Cartesian2({x}, {y})"""
        return rep.format(x=self.x, y=self.y)

    # Class methods

    @classmethod
    def fromDegrees(cls, x, y):
        return Cartesian2(x, y, degrees=True)

    @classmethod
    def maybe(cls, x, degrees=False):
        """Convert list or tuple to Cartesian2"""
        if isinstance(x, Cartesian2):
            return x

        x = shapefile._maybe_shapely_point(x)
        if com.is_listlike(x) and len(x) == 2:
            return Cartesian2(*x, degrees=degrees)
        return x


######################################################################################################################################################


class Cartesian3(_Cartesian):

    # Definitions

    x = traitlets.Float()
    y = traitlets.Float()
    z = traitlets.Float()

    # Constructor

    def __init__(
        self,
        x: float,
        y: float,
        z: float,
        degrees: bool = False,
    ) -> None:

        self.x: float = x
        self.y: float = y
        self.z: float = z

        self._is_degrees: bool = degrees

        if degrees:
            com.validate_longitude(x, key="x")
            com.validate_latitude(y, key="y")

    # Methods

    def __eq__(self, other: Cartesian3) -> bool:

        """
        Return True if two vectors are equal.
        """

        return self.x == other.x and self.y == other.y and self.z == other.z

    def __mul__(self, scalar: float) -> Cartesian3:

        """
        Return vector multiplied by scalar.
        """

        return Cartesian3(
            x=self.x * scalar,
            y=self.y * scalar,
            z=self.z * scalar,
        )

    def __truediv__(self, scalar: float) -> Cartesian3:

        """
        Return vector divided by scalar.
        """

        return Cartesian3(
            x=self.x / scalar,
            y=self.y / scalar,
            z=self.z / scalar,
        )

    def angle_with(self, other: Cartesian3) -> float:

        """
        Return angle between two vectors in radians.
        """

        return math.acos(self.dot(other) / (self.magnitude() * other.magnitude()))

    def magnitude(self) -> float:

        """
        Return magnitude of vector.
        """

        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def normalized(self) -> Cartesian3:

        """
        Return normalized vector.
        """

        return self / self.magnitude()

    def dot(self, other: Cartesian3) -> float:

        """
        Return dot product of two vectors.
        """

        assert not self._is_degrees
        assert not other._is_degrees

        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Cartesian3) -> Cartesian3:

        """
        Return cross product of two vectors.
        """

        assert not self._is_degrees
        assert not other._is_degrees

        return Cartesian3(
            x=self.y * other.z - self.z * other.y,
            y=self.z * other.x - self.x * other.z,
            z=self.x * other.y - self.y * other.x,
        )

    def __repr__(self) -> str:

        """
        Return string representation of Cartesian3.
        """

        if self._is_degrees:
            return f"Cartesian3.fromDegrees({self.x}, {self.y}, {self.z})"

        return f"Cartesian3({self.x}, {self.y}, {self.z})"

    # Class methods

    @classmethod
    def fromDegrees(cls, x, y, z) -> Cartesian3:
        return Cartesian3(x, y, z, degrees=True)

    @classmethod
    def fromDegreesArray(cls, x) -> Cartesian3Array:
        # convert shaply.Polygon to coordinateslist
        x = shapefile._maybe_shapely_polygon(x)
        x = shapefile._maybe_shapely_line(x)
        x = geocode._maybe_geocode(x, height=0)

        if com.is_listlike_2elem(x):
            x = com._flatten_list_of_listlike(x)
        elif com.is_listlike_3elem(x):
            raise NotImplementedError

        return Cartesian3Array(x)

    @classmethod
    def maybe(cls, x, degrees=False):
        """Convert list or tuple to Cartesian3"""
        if isinstance(x, Cartesian3):
            return x

        x = shapefile._maybe_shapely_point(x)

        # currently, only Cartesian3 tries to geocode passed loc
        x = geocode._maybe_geocode(x, height=0)
        if com.is_listlike(x):
            if len(x) == 3:
                return Cartesian3(*x, degrees=degrees)
            elif len(x) == 2 and degrees:
                # if degrees is True, z can filled by 0
                # otherwise raise (non-degrees Cartesian is used in Box)
                return Cartesian3(x=x[0], y=x[1], z=0, degrees=degrees)
        return x


######################################################################################################################################################


class Cartesian3Array(_Cartesian):

    _is_array = True

    def __init__(self, x):
        if isinstance(x, Cartesian3Array):
            x = x.x

        self.x = com.validate_listlike_lonlatalt(x, "x")
        # currently, array always be degrees
        self._is_degrees = True

    def __len__(self):
        return len(self.x)

    def __repr__(self):
        rep = """Cartesian3.fromDegreesArrayHeights({x})"""
        return rep.format(x=self.x)


######################################################################################################################################################


class Cartesian4(_Cartesian):

    x = traitlets.Float()
    y = traitlets.Float()
    z = traitlets.Float()
    w = traitlets.Float()

    def __init__(self, x, y, z, w, degrees=False):

        self.x = x
        self.y = y
        self.z = z
        self.w = w

        self._is_degrees = degrees

        if degrees:
            com.validate_longitude(x, key="x")
            com.validate_latitude(y, key="y")

    @classmethod
    def fromDegrees(cls, x, y, z, w):
        return Cartesian4(x, y, z, w, degrees=True)

    def __repr__(self):
        if self._is_degrees:
            rep = """Cartesian4.fromDegrees({x}, {y}, {z}, {w})"""
            return rep.format(x=self.x, y=self.y, z=self.z, w=self.w)
        else:
            rep = """Cartesian4({x}, {y}, {z}, {w})"""
            return rep.format(x=self.x, y=self.y, z=self.z, w=self.w)

    @classmethod
    def maybe(cls, x, degrees=False):
        """Convert list or tuple to Cartesian4"""
        if isinstance(x, Cartesian4):
            return x

        x = shapefile._maybe_shapely_point(x)

        if com.is_listlike(x) and len(x) == 4:
            return Cartesian4(*x, degrees=degrees)
        return x


######################################################################################################################################################


class Rectangle(_Cartesian):

    west = traitlets.Float()
    south = traitlets.Float()
    east = traitlets.Float()
    north = traitlets.Float()

    def __init__(self, west, south, east, north, degrees=False):

        self.west = west
        self.south = south
        self.east = east
        self.north = north

        self._is_degrees = degrees

        if degrees:
            self.west = com.validate_longitude(west, key="west")
            self.south = com.validate_latitude(south, key="south")
            self.east = com.validate_longitude(east, key="east")
            self.north = com.validate_latitude(north, key="north")

    @classmethod
    def fromDegrees(cls, west, south, east, north):
        return Rectangle(west, south, east, north, degrees=True)

    @property
    def _inner_repr(self):
        rep = "west={west}, south={south}, east={east}, north={north}"
        return rep.format(
            west=self.west, south=self.south, east=self.east, north=self.north
        )

    def __repr__(self):
        # show more detailed repr, as arg order is not easy to remember
        if self._is_degrees:
            return "Rectangle.fromDegrees({rep})".format(rep=self._inner_repr)
        else:
            return "Rectangle({rep})".format(rep=self._inner_repr)

    @property
    def script(self):
        # we can't use repr as it is like other Cartesian
        if self._is_degrees:
            rep = """Cesium.Rectangle.fromDegrees({west}, {south}, {east}, {north})"""
            return rep.format(
                west=self.west, south=self.south, east=self.east, north=self.north
            )
        else:
            rep = """new Cesium.Rectangle({west}, {south}, {east}, {north})"""
            return rep.format(
                west=self.west, south=self.south, east=self.east, north=self.north
            )

    @classmethod
    def maybe(cls, x):
        if isinstance(x, Rectangle):
            return x

        if com.is_listlike_2elem(x):
            x = com._flatten_list_of_listlike(x)
        if com.is_listlike(x) and len(x) == 4:
            return Rectangle.fromDegrees(*x)
        return x


######################################################################################################################################################
