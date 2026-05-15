import numpy as np
from scipy.stats import linregress


def right_left(z, theta):
    """
    Separate geopotential field into left and right of the th line.

    Parameters
    ----------
    z: xarray.DataArray
        The geopotential field
    theta :
        The direction (in degrees)

    Returns
    -------
    left, right (2 xr.DataArray): The left and right side of the z. field.
    """
    # matrix of az x r
    az = np.broadcast_to(z.az, [len(z.r), len(z.az)])

    angle = -np.subtract.outer(np.asarray(theta), az) % 360

    # Mask in 3D (az, r, snapshot)
    mask_right = angle > 180

    return z.where(mask_right), z.where(~mask_right)


def b(th_vec, z900, z600, lat):
    """
    Computes the B parameter for a vector of points, with the corresponding snapshot of
    geopt at 600hPa and 900hPa

    Parameters
    ----------
    th_vec :
        The theta parameter for each point
    z900 :
        The z900 field for each point
    z600 :
        The z600 field for each point
    lat :
        The latitude of each point

    Returns
    -------
    B, the Hart phase space parameter for symetry.
    """
    dz = z600 - z900
    dz_r, dz_l = right_left(dz, th_vec)
    h = np.where(lat < 0, -1, 1)
    return (
        h
        * (
            dz_r.weighted(dz.r).mean(["az", "r"])
            - dz_l.weighted(dz.r).mean(["az", "r"])
        ).values
    )


def vt(geopt, p_bottom=None, p_top=None):
    """
    Parameters
    ----------
    geopt : xarray.DataArray
        The Geopotential snapshots DataArray. plev must be decreasing

    Returns
    -------
    numpy.ndarray
        The Hart Phase Space parameter for thermal wind
    """
    # Maximum of Z at each level for each snapshot
    z_max = geopt.max(["az", "r"])
    # Minimum of ...
    z_min = geopt.min(["az", "r"])
    # Function of snapshot & plev
    dz = z_max - z_min

    x = np.log(dz.plev).values.reshape(-1, 1).flatten()

    return linregress(x, dz, axis=1).slope
