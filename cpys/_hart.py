import numpy as np
from scipy.stats import linregress


def right_left(z, theta):
    """
    Separate geopotential field into left and right of the th line.

    Parameters
    ----------
    z (xr.DataArray): The geopotential field
    th: The direction (in degrees)

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
    th_vec : The theta parameter for each point
    z900 : The z900 field for each point
    z600 : The z600 field for each point
    lat : The latitude of each point

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


def vt(geopt):
    """
    Parameters
    ----------
    geopt (xr.DataArray) : The Geopotential snapshots DataArray.
        plev must be decreasing
    name (str) : Name of the geopotential snapshots variable.

    Returns
    -------
    VTL, VTU : The Hart Phase Space parameters for upper and lower thermal wind respectively.
    """
    # from sklearn.linear_model import LinearRegression
    z_max = geopt.max(["az", "r"])  # Maximum of Z at each level for each snapshot
    z_min = geopt.min(["az", "r"])  # Minimum of ...
    ΔZ = z_max - z_min  # Fonction of snapshot & plev
    ΔZ_bottom = ΔZ.sel(plev=slice(950e2, 600e2))  # Lower troposphere
    ΔZ_top = ΔZ.sel(plev=slice(600e2, 250e2))  # Upper tropo
    X = np.log(ΔZ_bottom.plev).values.reshape(-1, 1).flatten()
    # VTL = [LinearRegression().fit(X, y).coef_[0] if not np.isnan(y).any() else np.nan for y in ΔZ_bottom.values]
    VTL = [
        linregress(X, y).slope if not np.isnan(y).any() else np.nan
        for y in ΔZ_bottom.values
    ]
    X = np.log(ΔZ_top.plev).values.reshape(-1, 1).flatten()
    # VTU = [LinearRegression().fit(X, y).coef_[0] for y in ΔZ_top.values]
    VTU = [linregress(X, y).slope for y in ΔZ_top.values]
    return VTL, VTU
