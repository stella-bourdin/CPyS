import numpy as np

import cpys


def test_rot(ds_croad, results_croad):
    result = cpys.rot(ds_croad.snap_vo, ds_croad.snap_geopt / 9.81)

    np.testing.assert_allclose(result, results_croad.Ro_T)
