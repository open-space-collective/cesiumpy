#!/usr/bin/env python
# coding: utf-8

import nose
import unittest

import cesiumpy
from cesiumpy.testing import _skip_if_no_scipy, _skip_if_no_shapely


class TestVoronoi(unittest.TestCase):

    def test_voronoi(self):

        _skip_if_no_scipy()
        _skip_if_no_shapely()

        import numpy as np
        import scipy.spatial

        np.random.seed(1234)
        points = np.random.rand(15, 2) * 5 + np.array([130, 40])

        vor = cesiumpy.spatial.Voronoi(points)
        polygons = vor.get_polygons()

        expected = [[129.53037742006228, 44.33471494590681, 131.40476793036768,
                     43.448996661779695, 131.39784031783313, 43.270076795621065,
                     130.99199913910985, 42.328426095963245, 129.53037742006228,
                     42.99862087958684, 129.53037742006228, 44.33471494590681],
                    [132.5231502900114, 45.90344076159844, 132.97793597508354,
                     44.336889661521575, 132.64956736534268, 43.22629856885517,
                     132.04973345010688, 43.48337280292282, 132.25107509065992,
                     45.90344076159844, 132.5231502900114, 45.90344076159844],
                    [133.77311875584925, 40.110955821295555, 132.56020732493596,
                     41.408540471782935, 133.05978915987998, 42.33192230184925,
                     133.81747880349292, 42.498078263756426, 135.4154315003338,
                     41.85193612810953, 135.4154315003338, 40.110955821295555,
                     133.77311875584925, 40.110955821295555],
                    [131.89390865691786, 45.90344076159844, 131.63882963366206,
                     43.55998220705691, 131.40476793036768, 43.448996661779695,
                     129.53037742006228, 44.33471494590681, 129.53037742006228,
                     45.90344076159844, 131.89390865691786, 45.90344076159844],
                    [135.4154315003338, 43.741768534167036, 134.30817767731628,
                     43.86503713071969, 134.38197047363133, 45.90344076159844,
                     135.4154315003338, 45.90344076159844, 135.4154315003338,
                     43.741768534167036],
                    [131.03585127801438, 42.275291825551136, 131.69926550801236,
                     42.680449017412236, 133.0090748373699, 42.409930619839045,
                     133.05978915987998, 42.33192230184925, 132.56020732493596,
                     41.408540471782935, 131.57844318202783, 41.115828979808505,
                     131.03585127801438, 42.275291825551136],
                    [132.64956736534268, 43.22629856885517, 132.97793597508354,
                     44.336889661521575, 134.12142452823772, 43.73557828446551,
                     133.81747880349292, 42.498078263756426, 133.05978915987998,
                     42.33192230184925, 133.0090748373699, 42.409930619839045,
                     132.7101884373397, 43.027826672381536, 132.64956736534268,
                     43.22629856885517],
                    [131.7316387448889, 42.93096881919415, 132.7101884373397,
                     43.027826672381536, 133.0090748373699, 42.409930619839045,
                     131.69926550801236, 42.680449017412236, 131.7316387448889,
                     42.93096881919415],
                    [130.7442505383254, 40.110955821295555, 131.57844318202783,
                     41.115828979808505, 132.56020732493596, 41.408540471782935,
                     133.77311875584925, 40.110955821295555, 130.7442505383254,
                     40.110955821295555],
                    [134.38197047363133, 45.90344076159844, 134.30817767731628,
                     43.86503713071969, 134.12142452823772, 43.73557828446551,
                     132.97793597508354, 44.336889661521575, 132.5231502900114,
                     45.90344076159844, 134.38197047363133, 45.90344076159844],
                    [132.04973345010688, 43.48337280292282, 132.64956736534268,
                     43.22629856885517, 132.7101884373397, 43.027826672381536,
                     131.7316387448889, 42.93096881919415, 131.39784031783313,
                     43.270076795621065, 131.40476793036768, 43.448996661779695,
                     131.63882963366206, 43.55998220705691, 132.04973345010688,
                     43.48337280292282],
                    [129.53037742006228, 42.99862087958684, 130.99199913910985,
                     42.328426095963245, 131.03585127801438, 42.275291825551136,
                     131.57844318202783, 41.115828979808505, 130.7442505383254,
                     40.110955821295555, 129.53037742006228, 40.110955821295555,
                     129.53037742006228, 42.99862087958684],
                    [135.4154315003338, 41.85193612810953, 133.81747880349292,
                     42.498078263756426, 134.12142452823772, 43.73557828446551,
                     134.30817767731628, 43.86503713071969, 135.4154315003338,
                     43.741768534167036, 135.4154315003338, 41.85193612810953],
                    [132.25107509065992, 45.90344076159844, 132.04973345010688,
                     43.48337280292282, 131.63882963366206, 43.55998220705691,
                     131.89390865691786, 45.90344076159844, 132.25107509065992,
                     45.90344076159844],
                    [131.39784031783313, 43.270076795621065, 131.7316387448889,
                     42.93096881919415, 131.69926550801236, 42.680449017412236,
                     131.03585127801438, 42.275291825551136, 130.99199913910985,
                     42.328426095963245, 131.39784031783313, 43.270076795621065]]

        for polygon, exp in zip(polygons, expected):
            self.assertEqual(polygon.hierarchy.x, exp)

        # testing scipy.spatial.Voronoi instance
        vor = scipy.spatial.Voronoi(points)
        vor = cesiumpy.spatial.Voronoi(vor)
        polygons = vor.get_polygons()
        for polygon, exp in zip(polygons, expected):
            self.assertEqual(polygon.hierarchy.x, exp)



class TestConvex(unittest.TestCase):

    def test_convexhull(self):

        _skip_if_no_scipy()
        _skip_if_no_shapely()

        import numpy as np
        import scipy.spatial

        np.random.seed(1234)
        points = np.random.rand(15, 2) * 5 + np.array([130, 40])

        hull = cesiumpy.spatial.ConvexHull(points)
        polyline = hull.get_polyline()

        expected = [130.37690620821488, 41.844120030009876,
                    132.51541582653905, 40.06884224795341,
                    133.89987904059402, 41.36296302641321,
                    134.6657005099126, 43.25689071613289,
                    134.7906967684185, 44.379663173710476,
                    133.86413310806188, 44.41320595318058,
                    131.38232127571547, 44.00936088767509,
                    130.95759725189447, 43.11054385519916,
                    130.37690620821488, 41.844120030009876]

        self.assertEqual(polyline.positions.x, expected)

        hull = scipy.spatial.ConvexHull(points)
        hull = cesiumpy.spatial.ConvexHull(hull)
        polyline = hull.get_polyline()
        self.assertEqual(polyline.positions.x, expected)



if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
