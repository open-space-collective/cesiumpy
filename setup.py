# Apache License 2.0

import codecs
import os
import sys

from setuptools import setup, find_packages

PACKAGE = "cesiumpy"
README = "README.md"
REQUIREMENTS = "requirements.txt"

VERSION = "0.4.0.dev"


def read(fname):
    # file must be read as utf-8 in py3 to avoid to be bytes
    return codecs.open(
        os.path.join(os.path.dirname(__file__), fname), encoding="utf-8"
    ).read()


install_requires = list(read(REQUIREMENTS).splitlines())
if sys.version_info < (3, 4, 0):
    install_requires.append("enum34")

setup(
    name=PACKAGE,
    version=VERSION,
    description="python wrapper of cesium.js for 3D geospatial visualization",
    long_description=read(README),
    author="sinhrks",
    author_email="sinhrks@gmail.com",
    url="http://cesiumpy.readthedocs.org/en/stable",
    license="Apache 2.0",
    packages=find_packages(),
    package_data={
        "cesiumpy.data": [
            "countries/*.json",
            "countries/data/*.json",
            "countries/data/*.svg",
        ]
    },
    install_requires=install_requires,
)
