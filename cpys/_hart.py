import numpy as np
import pandas as pd
from scipy.stats import linregress


def right_left(field, th):
    """
    Separate geopotential field into left and right of the th line.

    Parameters
    ----------
    field (xr.DataArray): The geopotential field
    th: The direction (in degrees)

    Returns
    -------
    left, right (2 xr.DataArray): The left and right side of the geopt. field.
    """
    th = field.sel(
        az=157.44, method="nearest"
    ).az.values  # Select nearest available az to theta
    if th <= 180:
        return field.where((field.az <= th) | (field.az > 180 + th)), field.where(
            (field.az > th) & (field.az <= 180 + th)
        )
    else:
        return field.where((field.az <= th) & (field.az > th - 180)), field.where(
            (field.az > th) | (field.az <= th - 180)
        )


def right_left_vector(z, th):
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
    # Curate input
    if type(th) != np.ndarray:
        th = th.values

    th = z.az.sel(
        az=th, method="nearest"
    ).az.values  # Select nearest available az to theta
    A = pd.DataFrame([list(z.az.values)] * len(z.snapshot))  # matrix of az x snapshot
    A_shift = A.sub(th, axis=0) % 360
    mask_right = A_shift > 180  # Mask in 2D (az, snapshot)
    mask_left = (A_shift > 0) & (A_shift < 180)
    mask_right, mask_left = (
        np.array([mask_right] * len(z.r)),
        np.array([mask_left] * len(z.r)),
    )  # Mask in 3D (r, az, snapshot)
    mask_right, mask_left = (
        np.swapaxes(mask_right, 0, 1),
        np.swapaxes(mask_left, 0, 1),
    )  # Mask in 3D (az, r, snapshot)
    R, L = z.where(mask_right), z.where(mask_left)
    return R, L


def b(th, geopt, SH=False, names=["snap_z900", "snap_z600"]):  # TODO: Useless?
    """
    Computes the B parameter for a point, with the corresponding snapshot of geopt at
    600hPa and 900hPa

    Parameters
    ----------
    th: The direction (in degrees)
    geopt (xr.DataSet): The snapshots at both levels
    SH (bool): Set to True if the point is in the southern hemisphere
    names: names of the 900hPa and 600hPa geopt. variables in geopt.

    Returns
    -------
    B, the Hart phase space parameter for symetry.
    """
    if isinstance(names, str):
        z900 = geopt[names].sel(plev=900e2, method="nearest")
        print("Level " + str(z900.plev.values) + " is taken for 900hPa")
        z600 = geopt[names].sel(plev=600e2, method="nearest")
        print("Level " + str(z600.plev.values) + " is taken for 600hPa")
    else:
        z900 = geopt[names[0]]
        z600 = geopt[names[1]]

    dz = z600 - z900
    ΔZ_R, ΔZ_L = right_left_vector(dz, th)
    if SH:
        h = -1
    else:
        h = 1
    return (
        h
        * (
            ΔZ_R.weighted(dz.r).mean(["r", "az"])
            - ΔZ_L.weighted(dz.r).mean(["r", "az"])
        ).values
    )


def b_vector(th_vec, z900, z600, lat):
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
    # Curate input
    if type(th_vec) != np.ndarray:
        th_vec = th_vec.values

    dz = z600 - z900
    ΔZ_R, ΔZ_L = right_left_vector(dz, th_vec)
    h = np.where(lat < 0, -1, 1)
    return h * (
        ΔZ_R.weighted(dz.r).mean(["az", "r"])
        - ΔZ_L.weighted(dz.r).mean(["az", "r"])
    )


def vt(geopt, name="snap_zg"):
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
    z_max = geopt[name].max(["az", "r"])  # Maximum of Z at each level for each snapshot
    z_min = geopt[name].min(["az", "r"])  # Minimum of ...
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
