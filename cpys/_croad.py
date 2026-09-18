import numpy as np
from scipy.stats import linregress

from ._asymmetry import metres_per_degree, N


def rot(vorticity, z, p_bottom=70000, p_top=40000, method="regress"):
    """Thermal Rossby Number following `Croad et al. (2023) <https://doi.org/10.1029/2023GL105993>`_

    .. math::

        \\mathrm{Ro}_\\mathrm{T} = - \\frac{L}{N} \\frac{\\partial \\xi}{\\partial z}

    L = Horizontal length scale. This is fixed at 500km in Croad et al. (2023), but here
        it is determined by the radius (r) coordinate on the inputs. To apply the
        calculation at different radii, simply subset the inputs first.

    N = Brunt Vaisala frequency (0.01 s$^{-1}$)

    $\\xi$ = Vorticity (s$^{-1}$)

    $z$ = Height (m)

    Parameters
    ----------
    vorticity : xarray.DataArray
        Vorticity as
    z : xarray.DataArray
        Geopotential height
    p_bottom : int | None, optional
        Lowest pressure level to calculate vertical gradient (in Pa), by default 70000
        If p_bottom=None, p_bottom will be taken as the lowest point in vorticity/z
    p_top : int | None, optional
        Highest pressure level to calculate vertical gradient (in Pa), by default 40000
        If p_top=None, p_top will be taken as the highest point in vorticity/z
    method : str, optional
        Method used to calculate the vertical gradient

        * "regress" (default): A linear regression across all levels between p_bottom
          and p_top (inclusive)
        * "diff": A simple difference between the top and bottom

    Returns
    -------
    xarray.DataArray
        The
    """
    # r[0] gives spacing, r[-1] gives outer radius minus spacing (in degrees)
    radius = ((vorticity.r[0] + vorticity.r[-1]) * metres_per_degree).values

    vorticity = vorticity.weighted(vorticity.r).mean(["r", "az"])
    z = z.weighted(z.r).mean(["r", "az"])

    if method == "diff":
        if p_top is None:
            vort_top = vorticity.isel(level=0)
            z_top = z.isel(level=0)
        else:
            vort_top = vorticity.sel(level=p_top)
            z_top = z.sel(level=p_top)

        if p_bottom is None:
            vort_bottom = vorticity.isel(level=-1)
            z_bottom = z.isel(level=-1)
        else:
            vort_bottom = vorticity.sel(level=p_bottom)
            z_bottom = z.sel(level=p_bottom)

        dvort_dz = (vort_top - vort_bottom) / (z_top - z_bottom)

    elif method == "regress":
        p_bottom = np.inf if p_bottom is None else p_bottom
        p_top = 0 if p_top is None else p_top

        if vorticity.level[0] > vorticity.level[-1]:
            sl = slice(p_bottom, p_top)
        else:
            sl = slice(p_top, p_bottom)

        vorticity = vorticity.sel(level=sl)
        z = z.sel(level=sl)

        dvort_dz = linregress(z, vorticity, axis=1).slope

    return -dvort_dz * (radius / N)
