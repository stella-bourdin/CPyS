import numpy as np

import cpys


def test_vt(geopt, results):
    geopt = geopt.rename(level="plev").sortby("plev", ascending=False)
    vtl = cpys.vt(geopt.sel(plev=slice(950e2, 600e2)))
    vtu = cpys.vt(geopt.sel(plev=slice(600e2, 250e2)))

    np.testing.assert_allclose(vtl, results.VTL)
    np.testing.assert_allclose(vtu, results.VTU)
