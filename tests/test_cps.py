import numpy as np

import cpys


def test_cps_parameters(tracks, geopt, results):
    df = cpys.compute_cps_parameters(tracks, geopt)

    for var in ["B", "VTL", "VTU"]:
        np.testing.assert_allclose(df[var].values, results[var].values)
