import numpy as np
from scipy.stats import linregress


def vt(geopt, p_bottom=None, p_top=None):
    r"""Calculate the Hart thermal wind parameter

    $$\frac{\partial \Delta Z}{\partial \mathrm{ln} p}\Bigg\rvert_{p_0}^{p_1} = -\lvert V_T \rvert$$

    $\Delta Z$ is the difference between the maximum and minimum geopotential height
    within the search radius (500km for Hart, radius of input here)

    $p$ is pressure level. $p_0$ is the bottom pressure level and $p_1$ is the top
    pressure level

    For the Hart phase space:

    - $V_T^L$ uses $p_0=900$hPa and $p_1=600$hPa
    - and $V_T^U$ uses $p_0=600$hPa and $p_1=300$hPa

    Parameters
    ----------
    geopt : xarray.DataArray
        Geopotential height (in metres) as a function of
        (pressure (plev), azimuth (az), radius (r)) and optionally time

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
