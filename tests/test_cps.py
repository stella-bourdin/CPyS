import numpy as np

from CPyS.CPS import compute_CPS_parameters


def test_cps_parameters(tracks, geopt, results):
    df = compute_CPS_parameters(tracks, geopt)

    for var in ["B", "VTL", "VTU"]:
        np.testing.assert_allclose(df[var], results[var])
