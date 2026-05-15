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
    z900 : xarray.DataArray
        The z900 field for each point
    z600 : xarray.DataArray
        The z600 field for each point
    lat :
        The latitude of each point

    Returns
    -------
    numpy.ndarray
        The Hart phase space parameter for symetry.
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
    """Calculate the Hart thermal wind parameter

    Parameters
    ----------
    geopt : xarray.DataArray
        The geopotential snapshots

    Returns
    -------
    numpy.ndarray
        The Hart Phase Space parameter for thermal wind
    """
    if p_bottom is not None and p_top is not None:
        if geopt.plev[0] > geopt.plev[-1]:
            geopt = geopt.sel(plev=slice(p_bottom, p_top))
        else:
            geopt = geopt.sel(plev=slice(p_top, p_bottom))

    # Maximum of Z at each level for each snapshot
    z_max = geopt.max(["az", "r"])
    # Minimum of ...
    z_min = geopt.min(["az", "r"])
    # Function of snapshot & plev
    dz = z_max - z_min

    x = np.log(dz.plev)

    return linregress(x, dz, axis=1).slope
