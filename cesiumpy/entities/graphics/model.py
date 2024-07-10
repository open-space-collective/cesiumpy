#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals
from __future__ import annotations

import traitlets

from cesiumpy.base import _CesiumObject
from cesiumpy.entities.entity import _CesiumEntity


class IonResource(_CesiumObject):
    # Definitions

    _props = [
        "asset_id",
    ]

    asset_id = traitlets.Int()

    # Constructor

    def __init__(
        self,
        asset_id: int,
    ) -> None:
        super().__init__()

        self.asset_id = asset_id

    # Methods

    def generate_script(self, widget=None) -> str:
        return f"await Cesium.IonResource.fromAssetId({self.asset_id})"


class Model(_CesiumEntity):
    """
    ModelGraphic

    Parameters
    ----------


    """

    # Definitions

    _klass = "model"

    _props = [
        "uri",
    ]

    uri = traitlets.Instance(klass=IonResource)

    # Constructor

    def __init__(
        self,
        uri,
        **kwargs,
    ) -> None:
        super().__init__(
            **kwargs,
        )

        self.uri = uri
