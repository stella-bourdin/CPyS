import numpy as np
import pytest

import cpys
from cpys import _asymmetry


def test_b_non_vector(tracks, geopt, results):
    geopt = geopt.isel(snapshot=0)
    z900 = geopt.sel(level=90000)
    z600 = geopt.sel(level=60000)
    result = cpys.b(z600 - z900, tracks.lat[0], results.theta[0])

    np.testing.assert_allclose(result, results.B[0])


def test_b_vector(tracks, geopt, results):
    z900 = geopt.sel(level=90000)
    z600 = geopt.sel(level=60000)
    result = cpys.b(z600 - z900, tracks.lat, results.theta)

    np.testing.assert_allclose(result, results.B)


def test_b_croad(ds_croad, results_croad):
    result = cpys.b(
        ds_croad.snap_theta.sel(level=slice(70000, 92500)).mean(dim="level"),
        ds_croad.snap_lat,
        method="Croad",
    )

    np.testing.assert_allclose(result, results_croad.B)


def test_right_left_vector(geopt, results):
    right, left = _asymmetry.right_left(
        geopt.isel(level=-1, snapshot=slice(0, 2)), results.theta[:2]
    )

    assert right.mean() == pytest.approx(21.023, abs=0.001)
    assert left.mean() == pytest.approx(12.955, abs=0.001)

    # 800 NaNs
    # snapshot: 2, r: 50, az: 16
    # 8 / 16 azimuths are masked
    # 2 * 50 * 8 = 800
    assert np.isnan(right).sum() == 800
    assert np.isnan(left).sum() == 800
