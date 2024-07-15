# CesiumPy

Lightweight Python wrapper for [Cesium.js](http://cesiumjs.org/). Mainly intended to be used with `Jupyter Notebook`.

## Installation

Use `pip`:

```py
pip install cesiumpy
```

## Example

Running following script on Jupyter Notebook will show an embedded interactive 3D map:

```py
import cesiumpy

v = cesiumpy.Viewer()
v.entities.add(
  cesiumpy.Box(
    dimensions=(40e4, 30e4, 50e4),
    material=cesiumpy.color.RED,
    position=(-120, 40, 0),
)
v
```

![viewer01.png]([/assets/images/tux.png](https://raw.githubusercontent.com/sinhrks/cesiumpy/master/doc/source/_static/viewer01.png))

## Documentation

- http://cesiumpy.readthedocs.org/en/latest/

## Bundled Datasets

- World countries: https://github.com/mledoze/countries (ODbL)

## Dependencies

- `geopy`, `traitlets`
- (Optional) `scipy` and `shapely`
