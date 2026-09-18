from pathlib import Path

import huracanpy
import metpy
import numpy as np
import pandas as pd
import pytest
import xarray as xr


here = Path(__file__).parent
demo_path = here / "../demo/"
cases_path = here / "../cases/"


snaps_levels = (
    np.concatenate(
        [
            [1, 2, 3, 5, 7],
            [10, 20, 30, 50, 70],
            np.arange(100, 250, 25),
            np.arange(250, 750, 50),
            np.arange(750, 1025, 25),
        ]
    )
    * 100
)


@pytest.fixture()
def tracks():
    return huracanpy.load(str(demo_path / "Dale.csv"))


@pytest.fixture()
def geopt():
    return xr.open_dataset(demo_path / "Dale.nc").snap_zg


@pytest.fixture()
def results():
    return pd.read_csv(here / "results.csv")


@pytest.fixture()
def tracks_croad():
    return huracanpy.load(str(cases_path / "tracks/CroadA_2020.csv"))


@pytest.fixture()
def ds_croad():
    ds = xr.open_dataset(cases_path / "snaps/CroadA_2020.nc").assign(level=snaps_levels)
    ds.snap_ta.attrs["units"] = "kelvin"
    ds.level.attrs["units"] = "Pa"
    theta = metpy.calc.potential_temperature(
        ds.level.broadcast_like(ds.snap_ta), ds.snap_ta
    )
    ds["snap_theta"] = theta

    return ds


@pytest.fixture()
def results_croad():
    return pd.read_csv(here / "results_croad.csv")
