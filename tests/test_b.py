import numpy as np
import pytest

import CPyS.B


def test_b_vector(tracks, geopt, results):
    z900 = geopt.snap_zg.sel(level=90000)
    z600 = geopt.snap_zg.sel(level=60000)
    result = CPyS.B.B_vector(results.theta, z900, z600, tracks.lat)

    np.testing.assert_allclose(result, results.B)


def test_area_weights(geopt):
    result = CPyS.B.area_weights(geopt)

    np.testing.assert_allclose(result, np.arange(0.04, 4, 0.08))


def test_right_left_vector(geopt, results):
    right, left = CPyS.B.right_left_vector(
        geopt.snap_zg.isel(level=0, snapshot=slice(0, 2)), results.theta[:2]
    )

    assert right.mean() == pytest.approx(20.501, abs=0.001)
    assert left.mean() == pytest.approx(12.394, abs=0.001)

    # 900 NaNs
    # snapshot: 2, r: 50, az: 16
    # 9 / 16 azimuths are masked
    # 2 * 50 * 90 = 900
    assert np.isnan(right).sum() == 900
    assert np.isnan(left).sum() == 900
