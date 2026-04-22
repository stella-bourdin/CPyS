import numpy as np
import xarray as xr

import cpys


def test_theta():
    for (x0, x1, y0, y1), expected in [
        ((0, 1, 0, 0), 0),  # Eastward
        ((0, 0, 0, 1), 90), # Northward
        ((0, -1, 0, 0), 180),  # Westward
        ((0, 0, 0, -1), 270)  # Southward
    ]:
        tracks = xr.Dataset(data_vars=dict(
            lon=("record", [x0, x1]),
            lat=("record", [y0, y1]),
            track_id=("record", [0, 0]),
        ))
        assert cpys.theta(tracks)[0] == expected


def test_theta_track():
    lon = np.array([0, 1, 1, 0, 0])
    lat = np.array([0, 0, 1, 1, 0])
    tracks = xr.Dataset(data_vars=dict(
        lon=("record", lon),
        lat=("record", lat),
        track_id=("record", [0]*5),
    ))
    t = cpys.theta(tracks)
    assert len(t) == len(lon)
    np.testing.assert_allclose(t, [0, 90, 180, 270, 270], atol=0.01)


def test_theta_multitrack(tracks, results):
    result = cpys.theta(tracks)
    np.testing.assert_allclose(result, results.theta)
