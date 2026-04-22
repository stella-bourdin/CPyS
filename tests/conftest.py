from pathlib import Path

import huracanpy
import pandas as pd
import pytest
import xarray as xr


here = Path(__file__).parent
demo_path = here / "../demo/"


@pytest.fixture()
def tracks():
    return huracanpy.load(str(demo_path / "Dale.csv"))


@pytest.fixture()
def geopt():
    return xr.open_dataset(demo_path / "Dale.nc").snap_zg


@pytest.fixture()
def results():
    return pd.read_csv(here / "results.csv")
