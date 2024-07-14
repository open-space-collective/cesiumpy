# Apache License 2.0

import shapely.geometry
import cesiumpy
import cesiumpy.entities.cartesian as cartesian


class TestShapelyCartesian:
    def test_point_to_cartesian(self):

        p = shapely.geometry.Point(0, 1)
        res = cartesian.Cartesian2.maybe(p)
        exp = cesiumpy.Cartesian2(0.0, 1.0)
        assert isinstance(res, cartesian.Cartesian2)
        assert res.generate_script() == exp.generate_script()

        p = shapely.geometry.Point(0, 1, 3)
        res = cartesian.Cartesian3.maybe(p)
        exp = cesiumpy.Cartesian3(0.0, 1.0, 3.0)
        assert isinstance(res, cartesian.Cartesian3)
        assert res.generate_script() == exp.generate_script()

        # ToDo: Point doesn't support more than 4 elem?
        # p = shapely.geometry.Point(0, 1, 3, 5)
        # res = cartesian.Cartesian4.maybe(p, key='x')
        # exp = cesiumpy.Cartesian4(0., 1., 3., 5.)
        # assert isinstance(res, cartesian.Cartesian4)
        # assert res.generate_script() == exp.generate_script()

    def test_point_to_cartesian_degrees(self):

        p = shapely.geometry.Point(0, 1)
        res = cartesian.Cartesian2.maybe(p, degrees=True)
        exp = cesiumpy.Cartesian2.fromDegrees(0.0, 1.0)
        assert isinstance(res, cartesian.Cartesian2)
        assert res.generate_script() == exp.generate_script()

        # do not convert
        res = cartesian.Cartesian3.maybe(p)
        assert res == [0.0, 1.0]

        p = shapely.geometry.Point(0, 1, 3)
        res = cartesian.Cartesian3.maybe(p, degrees=True)
        exp = cesiumpy.Cartesian3.fromDegrees(0.0, 1.0, 3.0)
        assert isinstance(res, cartesian.Cartesian3)
        assert res.generate_script() == exp.generate_script()

        # do not convert
        res = cartesian.Cartesian2.maybe(p)
        assert res == [0.0, 1.0, 3.0]

    def test_line_to_cartesian_array(self):

        p = shapely.geometry.LineString([(0, 1), (2, 3)])
        res = cartesian.Cartesian3.fromDegreesArray(p)
        exp = cartesian.Cartesian3.fromDegreesArray([0.0, 1.0, 0.0, 2.0, 3.0, 0.0])
        assert isinstance(res, cartesian.Cartesian3Array)
        assert res.generate_script() == exp.generate_script()

        p = shapely.geometry.LinearRing([(0, 1), (2, 3), (1, 3)])
        res = cartesian.Cartesian3.fromDegreesArray(p)
        # last element is being added
        exp = cartesian.Cartesian3.fromDegreesArray(
            [0.0, 1.0, 0.0, 2.0, 3.0, 0.0, 1.0, 3.0, 0.0, 0.0, 1.0, 0.0]
        )
        assert isinstance(res, cartesian.Cartesian3Array)
        assert res.generate_script() == exp.generate_script()

    def test_polygon_to_cartesian_array(self):

        p = shapely.geometry.Polygon([[1, 1], [1, 2], [2, 2], [2, 1]])
        res = cartesian.Cartesian3.fromDegreesArray(p)
        exp = cartesian.Cartesian3.fromDegreesArray(
            [1.0, 1.0, 0.0, 1.0, 2.0, 0.0, 2.0, 2.0, 0.0, 2.0, 1.0, 0.0, 1.0, 1.0, 0.0]
        )
        assert isinstance(res, cartesian.Cartesian3Array)
        assert res.generate_script() == exp.generate_script()


class TestShapelyEntity:
    def test_point_to_entity(self):

        p = shapely.geometry.Point(0, 1)
        res = cesiumpy.extension.shapefile.to_entity(p)
        exp = """{position: Cesium.Cartesian3.fromDegrees(0.0, 1.0, 0.0), point: {pixelSize: 10.0, color: Cesium.Color.WHITE}}"""
        assert res.generate_script() == exp

        p = shapely.geometry.Point(0, 1, 3)
        res = cesiumpy.extension.shapefile.to_entity(p)
        exp = """{position: Cesium.Cartesian3.fromDegrees(0.0, 1.0, 3.0), point: {pixelSize: 10.0, color: Cesium.Color.WHITE}}"""
        assert res.generate_script() == exp

        # multipoint
        p = shapely.geometry.MultiPoint([[1, 1], [1, 2], [2, 2], [2, 1]])
        res = cesiumpy.extension.shapefile.to_entity(p)
        assert isinstance(res, list)
        assert len(res) == 4

        exp = [
            "{position: Cesium.Cartesian3.fromDegrees(1.0, 1.0, 0.0), point: {pixelSize: 10.0, color: Cesium.Color.WHITE}}",
            "{position: Cesium.Cartesian3.fromDegrees(1.0, 2.0, 0.0), point: {pixelSize: 10.0, color: Cesium.Color.WHITE}}",
            "{position: Cesium.Cartesian3.fromDegrees(2.0, 2.0, 0.0), point: {pixelSize: 10.0, color: Cesium.Color.WHITE}}",
            "{position: Cesium.Cartesian3.fromDegrees(2.0, 1.0, 0.0), point: {pixelSize: 10.0, color: Cesium.Color.WHITE}}",
        ]
        assert [e.generate_script() for e in res] == exp

    def test_line_to_entity(self):

        p = shapely.geometry.LineString([(0, 1), (2, 3)])
        res = cesiumpy.extension.shapefile.to_entity(p)
        exp = """{polyline: {positions: Cesium.Cartesian3.fromDegreesArrayHeights([0.0, 1.0, 0.0, 2.0, 3.0, 0.0])}}"""
        assert res.generate_script() == exp

        p = shapely.geometry.LinearRing([(0, 1), (2, 3), (1, 3)])
        res = cesiumpy.extension.shapefile.to_entity(p)
        # last element is being added
        exp = """{polyline: {positions: Cesium.Cartesian3.fromDegreesArrayHeights([0.0, 1.0, 0.0, 2.0, 3.0, 0.0, 1.0, 3.0, 0.0, 0.0, 1.0, 0.0])}}"""
        assert res.generate_script() == exp

        # multilinestring
        p = shapely.geometry.MultiLineString([[[1, 1], [1, 2]], [[2, 2], [2, 1]]])
        res = cesiumpy.extension.shapefile.to_entity(p)
        assert isinstance(res, list)
        assert len(res) == 2

        exp = [
            "{polyline: {positions: Cesium.Cartesian3.fromDegreesArrayHeights([1.0, 1.0, 0.0, 1.0, 2.0, 0.0])}}",
            "{polyline: {positions: Cesium.Cartesian3.fromDegreesArrayHeights([2.0, 2.0, 0.0, 2.0, 1.0, 0.0])}}",
        ]
        assert [e.generate_script() for e in res] == exp

    def test_polygon_to_entity(self):

        p = shapely.geometry.Polygon([[1, 1], [1, 2], [2, 2], [2, 1]])
        res = cesiumpy.extension.shapefile.to_entity(p)
        exp = """{polygon: {hierarchy: Cesium.Cartesian3.fromDegreesArrayHeights([1.0, 1.0, 0.0, 1.0, 2.0, 0.0, 2.0, 2.0, 0.0, 2.0, 1.0, 0.0, 1.0, 1.0, 0.0])}}"""
        assert res.generate_script() == exp

        # multipolygon
        p1 = shapely.geometry.Polygon([[1, 1], [1, 2], [2, 2], [2, 1]])
        p2 = shapely.geometry.Polygon([[3, 3], [3, 4], [4, 4], [4, 3]])
        p = shapely.geometry.MultiPolygon([p1, p2])
        res = cesiumpy.extension.shapefile.to_entity(p)
        assert isinstance(res, list)
        assert len(res) == 2

        exp = [
            "{polygon: {hierarchy: Cesium.Cartesian3.fromDegreesArrayHeights([1.0, 1.0, 0.0, 1.0, 2.0, 0.0, 2.0, 2.0, 0.0, 2.0, 1.0, 0.0, 1.0, 1.0, 0.0])}}",
            "{polygon: {hierarchy: Cesium.Cartesian3.fromDegreesArrayHeights([3.0, 3.0, 0.0, 3.0, 4.0, 0.0, 4.0, 4.0, 0.0, 4.0, 3.0, 0.0, 3.0, 3.0, 0.0])}}",
        ]
        assert [e.generate_script() for e in res] == exp
