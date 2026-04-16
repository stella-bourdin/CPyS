import numpy as np
import pandas as pd
import pytest

from CPyS import theta


def test_theta():
    x0, x1, y0, y1 = 0, 1, 0, 0  # Eastward
    assert theta.theta(x0, x1, y0, y1) == 0
    x0, x1, y0, y1 = 0, 0, 0, 1  # Northward
    assert theta.theta(x0, x1, y0, y1) == 90
    x0, x1, y0, y1 = 0, -1, 0, 0  # Westward
    assert theta.theta(x0, x1, y0, y1) == 180
    x0, x1, y0, y1 = 0, 0, 0, -1  # Southward
    assert theta.theta(x0, x1, y0, y1) == 270


def test_theta_track():
    lon = [0, 1, 1, 0, 0]
    lat = [0, 0, 1, 1, 0]
    t = theta.theta_track(lon, lat)
    assert len(t) == len(lon)
    assert t == pytest.approx([0, 90, 180, 270, 270], 0.01)


def test_theta_multitrack():
    tracks = pd.read_csv("tests/1996.csv", index_col=False)
    assert type(theta.theta_multitrack(tracks)) == np.ndarray
    assert theta.theta_multitrack(tracks)[1] == 90.0

    print("All good")
