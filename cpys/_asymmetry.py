from metpy.constants import earth_avg_radius, earth_avg_angular_vel, earth_gravity
import numpy as np
import xarray as xr


metres_per_degree = (2 * np.pi * earth_avg_radius / 360).magnitude
N = 0.01
theta_0 = 273


def right_left(z, angle):
    """
    Separate geopotential field into left and right of the th line.

    Parameters
    ----------
    z: xarray.DataArray
        The geopotential field
    angle :
        The propagation direction (in degrees anticlockwise from East)

    Returns
    -------
    left, right (2 xr.DataArray): The left and right side of the z. field.
    """
    # matrix of az x r
    az = np.broadcast_to(z.az, [len(z.r), len(z.az)])

    angle = -np.subtract.outer(np.asarray(angle), az) % 360

    # Mask in 3D (az, r, snapshot)
    mask_right = angle > 180

    return z.where(mask_right), z.where(~mask_right)


def b(variable, lat=None, angle=None, *, method="Hart"):
    r"""
    Computes the asymmetry (B) parameter for the given variable

    For example, to calculate the Hart B parameter pass the thickness of the 900-600hPa
    layer as the variable, and include the latitude and angle

    Parameters
    ----------
    variable : xarray.DataArray
        The variable to calculate the asymmetry over with dimensions
        (time (optional), azimuth (az), radius (r))
    lat : array_like | float
        The latitude at each time
    angle : array_like | float
        The propagation direction at each time
    method : str, default="Hart"
        Which version of the B parameter to calculate

        * :code:`"Hart"` (default): Calculate the Hart B parameter. The asymmetry in the
          variable relative to the propagation direction and corrected for hemisphere
          (using latitude). Typically the variable should be the thickness of the
          900-600hPa layer
        * :code:`"max"`: The maximum asymmetry across all angles. Latitude and angle are
          not needed for this version
        * :code:`"Croad"`: Calculate the Croad B parameter. The maximum asymmetry across
          all angles scaled by $\frac{1}{f_0 L N}\frac{g}{\theta_0}$. Typically the
          variable should be the depth average potential temperature from 925-700hPa.
          Latitude is needed, but not angle for this version.


    Returns
    -------
    numpy.ndarray
        The phase space parameter for asymmetry
    """
    if method.lower() == "hart":
        thickness_r, thickness_l = right_left(variable, angle)
        h = np.where(lat < 0, -1, 1)
        return (
            h
            * (
                thickness_r.weighted(thickness_r.r).mean(["az", "r"])
                - thickness_l.weighted(thickness_l.r).mean(["az", "r"])
            ).values
        )
    elif method.lower() == "max":
        return b_max(variable)
    elif method.lower() == "croad":
        return b_max_croad(variable, lat)


def b_max_croad(theta, lat):
    """Calculate the asymmetry parameter following Croad et al. (2023)

    Parameters
    ----------
    theta : xarray.DataArray
    lat : xarray.DataArray
    """
    f0 = 2 * earth_avg_angular_vel.magnitude * np.sin(np.deg2rad(lat.values))

    # r[0] gives spacing, r[-1] gives outer radius minus spacing (in degrees)
    radius = (theta.r[0] + theta.r[-1]) * metres_per_degree

    return earth_gravity.magnitude / (f0 * radius.values * N * theta_0) * b_max(theta)


def b_max(variable):
    """
    Computes maximum of the asymmetry across all angles

    Parameters
    ----------
    variable : xarray.DataArray

    Returns
    -------
    numpy.ndarray
        The phase space parameter for asymmetry.
    """
    diffs = []
    nhalfs = len(variable.az) // 2
    for n in range(nhalfs):
        idx = np.array([False] * n + [True] * nhalfs + [False] * (nhalfs - n))
        diffs.append(
            np.abs(
                variable.isel(az=idx).weighted(variable.r).mean(["az", "r"])
                - variable.isel(az=~idx).weighted(variable.r).mean(["az", "r"])
            ).expand_dims(dim=dict(az=[variable.az.values[n]]), axis=1)
        )
    return xr.concat(diffs, dim="az").max(dim="az").values
