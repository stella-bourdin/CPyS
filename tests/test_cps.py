import numpy as np

from cpys.cps import compute_cps_parameters


def test_cps_parameters(tracks, geopt, results):
    df = compute_cps_parameters(tracks, geopt)

    for var in ["B", "VTL", "VTU"]:
        np.testing.assert_allclose(df[var], results[var])
