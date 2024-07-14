# Apache License 2.0

import numpy as np

import cesiumpy.util.common as com


class TestChecker:
    def test_islistlike(self):
        assert com.is_listlike([10])
        assert com.is_listlike((1.5, 2))

        assert not com.is_listlike(None)
        assert not com.is_listlike("1.5")

    def test_islistlike_numpy(self):

        assert com.is_listlike(np.ndarray([10]))
        assert com.is_listlike(np.array([1.5, 2]))

        assert not com.is_listlike(np.int64(2))
        assert not com.is_listlike(np.array(1))

    def test_isnumeric(self):
        assert com.is_numeric(10)
        assert com.is_numeric(1.5)

        assert not com.is_numeric(None)
        assert not com.is_numeric("1.5")
        assert not com.is_numeric([1.5])

    def test_lon_lat(self):
        assert com.is_longitude(10)
        assert com.is_longitude(-180)
        assert com.is_longitude(180)
        assert com.is_longitude(10.0)

        assert com.is_latitude(10)
        assert com.is_latitude(-90)
        assert com.is_latitude(90)
        assert com.is_latitude(10.0)

        assert not com.is_longitude(-181)
        assert not com.is_latitude(-91)
        assert not com.is_longitude(181)
        assert not com.is_latitude(91)

        assert not com.is_longitude("x")
        assert not com.is_latitude("x")
        assert not com.is_longitude([1])
        assert not com.is_latitude([1])
        assert not com.is_longitude((1, 2))
        assert not com.is_latitude((1, 2))


class TestConverter:
    def test_to_jsscalar(self):
        assert '"x"' == com.to_jsscalar("x")
        assert "true" == com.to_jsscalar(True)
        assert "false" == com.to_jsscalar(False)
        assert "[false, true]" == com.to_jsscalar([False, True])
