import numpy as np
import pytest

from cpys import _hart


def test_b_non_vector(tracks, geopt, results):
    geopt = geopt.isel(snapshot=0)
    z900 = geopt.sel(level=90000)
    z600 = geopt.sel(level=60000)
    result = _hart.b(results.theta[0], z900, z600, tracks.lat)

    np.testing.assert_allclose(result, results.B[0])


def test_b_vector(tracks, geopt, results):
    z900 = geopt.sel(level=90000)
    z600 = geopt.sel(level=60000)
    result = _hart.b(results.theta, z900, z600, tracks.lat)

    np.testing.assert_allclose(result, results.B)


def test_right_left_vector(geopt, results):
    right, left = _hart.right_left(geopt.isel(level=-1, snapshot=slice(0, 2)), results.theta[:2])

    assert right.mean() == pytest.approx(21.023, abs=0.001)
    assert left.mean() == pytest.approx(12.955, abs=0.001)

    # 800 NaNs
    # snapshot: 2, r: 50, az: 16
    # 8 / 16 azimuths are masked
    # 2 * 50 * 8 = 800
    assert np.isnan(right).sum() == 800
    assert np.isnan(left).sum() == 800


def test_vt(geopt, results):
    geopt = geopt.rename(level="plev").sortby("plev", ascending=False)
    vtl, vtu = _hart.vt(geopt)

    np.testing.assert_allclose(vtl, results.VTL)
    np.testing.assert_allclose(vtu, results.VTU)
