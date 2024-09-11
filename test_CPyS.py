from CPyS.theta import theta

def test_theta():
    x0, x1, y0, y1 = 0, 1, 0, 0 # Eastward
    assert theta(x0,x1,y0,y1) == 0
    x0, x1, y0, y1 = 0, 0, 0, 1 # Northward
    assert theta(x0,x1,y0,y1) == 90
    x0, x1, y0, y1 = 0, -1, 0, 0 # Westward
    assert theta(x0,x1,y0,y1) == 180
    x0, x1, y0, y1 = 0, 0, 0, -1 # Southward
    assert theta(x0,x1,y0,y1) == 270
    