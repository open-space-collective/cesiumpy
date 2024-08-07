# Apache License 2.0

from __future__ import unicode_literals

import collections
import importlib
import itertools
import datetime

from cesiumpy.util import case

# --------------------------------------------------
# Misc
# --------------------------------------------------


def _check_package(package_name):
    try:
        return importlib.import_module(package_name)
    except ImportError:
        msg = "{pkg} is required to use this functionality"
        raise ImportError(msg.format(pkg=package_name))


# --------------------------------------------------
# Validators
# --------------------------------------------------


def notimplemented(x):
    if x is not None:
        raise NotImplementedError
    return x


def validate_numeric(x, key):
    """validate whether x is int, long or float"""
    if not is_numeric(x):
        raise ValueError("{key} must be numeric: {x}".format(key=key, x=x))
    return x


def validate_numeric_or_none(x, key):
    """validate whether x is int, long, float or None"""
    if x is None:
        return x
    return validate_numeric(x, key=key)


def validate_longitude(x, key):
    """validate whether x is numeric, and between -180 and 180"""
    if not is_longitude(x):
        raise ValueError(
            "{key} must be longitude, between -180 to 180: {x}".format(key=key, x=x)
        )
    return True


def validate_latitude(x, key):
    """validate whether x is numeric, and between -90 and 90"""
    if not is_latitude(x):
        raise ValueError(
            "{key} must be latitude, between -90 to 90: {x}".format(key=key, x=x)
        )
    return True


def validate_listlike(x, key):
    """validate whether x is list-likes"""
    if not is_listlike(x):
        raise ValueError("{key} must be list-likes: {x}".format(key=key, x=x))
    if hasattr(x, "__array__"):
        # array interface, 0 dimensional array raises ValueError in
        # previous block
        x = x.__array__()
        # convert to python list as traitlets doesn't handle numpy scalar
        x = x.tolist()
    return x


def validate_listlike_even(x, key):
    """validate whether x is list-likes which length is even-number"""
    x = validate_listlike(x, key)
    if len(x) % 2 != 0:
        raise ValueError(
            "{key} length must be an even number: {x}".format(key=key, x=x)
        )
    return x


def validate_listlike_lonlat(x, key):
    """validate whether x is list-likes consists from lon, lat pairs"""
    x = validate_listlike_even(x, key)
    try:
        all(validate_longitude(e, key=key) for e in x[::2])
        all(validate_latitude(e, key=key) for e in x[1::2])
        # validation will raise ValueError immediately
    except ValueError:
        msg = "{key} must be a list consists from longitude and latitude: {x}"
        raise ValueError(msg.format(key=key, x=x))

    return x


def validate_listlike_lonlatalt(x, key):
    """validate whether x is list-likes consists from lon, lat, alt tuples"""
    try:
        assert len(x) % 3 == 0
        all(validate_longitude(e, key=key) for e in x[::3])
        all(validate_latitude(e, key=key) for e in x[1::3])
        # validation will raise ValueError immediately
    except ValueError:
        msg = "{key} must be a list consists from longitude and latitude: {x}"
        raise ValueError(msg.format(key=key, x=x))

    return x


# --------------------------------------------------
# Check Functions
# --------------------------------------------------

# There is not is_bool and is_str, because these are single expression


def is_numeric(x):
    return isinstance(x, (int, float))


def is_longitude(x):
    if is_numeric(x):
        return -180 <= x <= 180
    return False


def is_latitude(x):
    if is_numeric(x):
        return -90 <= x <= 90
    return False


try:
    import numpy as np

    listlike_types = (list, tuple, np.ndarray)
except ImportError:
    listlike_types = (list, tuple)


def is_listlike(x):
    """whether the input can be regarded as list"""
    if hasattr(x, "__array__"):
        # array interface
        x = x.__array__()
        if x.ndim == 0:
            # 0 dimensional array
            return False
    return isinstance(x, listlike_types)


def is_listlike_2elem(x):
    if is_listlike(x):
        if all(is_listlike(e) and len(e) == 2 for e in x):
            return True
    return False


def is_listlike_3elem(x):
    if is_listlike(x):
        if all(is_listlike(e) and len(e) == 3 for e in x):
            return True
    return False


# --------------------------------------------------
# Converter Functions
# --------------------------------------------------


def to_jsscalar(x, widget=None):
    """convert x to JavaScript representation"""

    from cesiumpy.base import _CesiumObject, _CesiumEnum

    if isinstance(x, (_CesiumObject, _CesiumEnum)):
        return x.generate_script(widget=widget)

    if isinstance(x, bool):
        # convert to JavaScript repr
        x = "true" if x else "false"
    elif isinstance(x, str):
        x = f'"{x}"'
    elif isinstance(x, datetime.datetime):
        x = f'Cesium.JulianDate.fromIso8601("{x.isoformat()}")'
    elif isinstance(x, dict):
        x = "".join(to_jsobject(x, widget=widget))
    elif isinstance(x, list):
        x = [str(to_jsscalar(e, widget=widget)) for e in x]
        x = "[{0}]".format(", ".join(x))
    return x


def to_jsobject(x, widget=None):
    """convert x to JavaScript Object"""

    results = ["{"]

    # filter None
    dic = collections.OrderedDict()
    # do not use dict comprehension to keep property order
    for k, v in x.items():
        if v is not None:
            dic[k] = v
    x = dic
    if len(x) == 0:
        return [""]

    for key, val in x.items():
        results.append(
            f"{case.snake_case_to_camel_case(key)}: {to_jsscalar(val, widget = widget)}, "
        )
    results[-1] = results[-1][:-2]  # remove final comma
    results.append("}")
    return results


def flatten_list_of_listlike(x):
    return list(itertools.chain(*x))
