from pathlib import Path

import pandas as pd
import pytest
import xarray as xr


here = Path(__file__).parent
demo_path = here / "../demo/"


@pytest.fixture()
def tracks():
    return pd.read_csv(demo_path / "Dale.csv", index_col=False)


@pytest.fixture()
def geopt():
    return xr.open_dataset(demo_path / "Dale.nc")


@pytest.fixture()
def results():
    return pd.read_csv(here / "results.csv")
