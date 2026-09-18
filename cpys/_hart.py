import numpy as np
from scipy.stats import linregress


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
