import pandas as pd
import xarray as xr

from CPyS.CPS import compute_CPS_parameters


def test_cps_parameters():
    tracks = pd.read_csv("tests/Dale.csv", index_col=False)
    geopt = xr.open_dataset("tests/Dale.nc")

    df = compute_CPS_parameters(tracks, geopt)
