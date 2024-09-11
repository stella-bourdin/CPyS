import pytest

from CPyS.theta import theta, theta_track

def test_theta():
    x0, x1, y0, y1 = 0, 1, 0, 0 # Eastward
    assert theta(x0,x1,y0,y1) == 0
    x0, x1, y0, y1 = 0, 0, 0, 1 # Northward
    assert theta(x0,x1,y0,y1) == 90
    x0, x1, y0, y1 = 0, -1, 0, 0 # Westward
    assert theta(x0,x1,y0,y1) == 180
    x0, x1, y0, y1 = 0, 0, 0, -1 # Southward
    assert theta(x0,x1,y0,y1) == 270
    
def test_theta_track():
    lon = [0,1,1,0,0]
    lat = [0,0,1,1,0]
    t = theta_track(lon, lat)
    assert len(t) == len(lon)
    assert t == pytest.approx([0, 90, 180, 270, 270], 0.01)
    