# Apache License 2.0

from __future__ import unicode_literals

import os
import warnings
from typing import List, Union


def build_html(*args):
    results = []
    for a in args:
        if isinstance(a, list):
            results.extend(a)
        elif isinstance(a, str):
            results.append(a)
        else:
            raise ValueError(type(a))
    return os.linesep.join(results)


def check_uri(sourceUri):
    if not os.path.exists(sourceUri):
        msg = "Unable to read specified path, be sure to the output HTML can read the path: {0}"
        warnings.warn(msg.format(sourceUri))
    return True


def wrap_uri(sourceUri):
    if sourceUri.endswith(".js"):
        return '<script src="{0}"></script>'.format(sourceUri)
    elif sourceUri.endswith(".css"):
        return '<link rel="stylesheet" href="{0}" type="text/css">'.format(sourceUri)
    else:
        raise ValueError(sourceUri)


def wrap_scripts(scripts: Union[List[str], str]) -> List[str]:
    if isinstance(scripts, str):
        scripts = [scripts]

    # filter None and empty str
    scripts = [s for s in scripts if ((s is not None) and len(s) > 0)]

    before: List[str] = [
        '<script type="text/javascript">',
    ]

    after: List[str] = [
        "</script>",
    ]

    return before + _add_indent(_wrap_async_init(scripts)) + after


def _wrap_async_init(scripts: List[str]) -> List[str]:
    before: List[str] = [
        "async function init() {",
    ]

    after: List[str] = [
        "}",
        "init();",
    ]

    return before + _add_indent(scripts) + after


def _add_indent(script, indent=2):
    """Indent list of script with specfied number of spaces"""
    if not isinstance(script, list):
        script = [script]

    indent = " " * indent
    return [indent + s for s in script]
