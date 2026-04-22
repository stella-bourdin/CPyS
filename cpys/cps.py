import numpy as np

from .theta import theta
from ._hart import b_vector, vt


def compute_cps_parameters(
    tracks,
    geopt,
    plev_name="level",
    verbose=True,
):
    """
    Computes the three (+ theta) Hart parameters for all the points in tracks.

    Parameters
    ----------
    tracks (xarray.Dataset): The set of TC points
    geopt (xarray.DataArray): The geopotential snapshots associated with the tracks
        level coordinate must be in Pa.
    plev_name (str): name of the vertical coordinate in the geopt file.

    Returns
    -------
    tracks (pd.DataFrame): The set of TC points with four new columns corresponding to the parameters
    """

    # Curate input
    ## geopt snapshots
    geopt = geopt.rename({plev_name: "plev"})  # Change vertical coordinate name
    geopt = geopt.where(np.abs(geopt) < 1e10)

    # 1/ B computation
    if verbose:
        print("Computing B...")
    ## Select 900 & 600 hPa levels
    z900, z600 = (
        geopt.sel(plev=900e2, method="nearest"),
        geopt.sel(plev=600e2, method="nearest"),
    )
    if verbose:
        print(
            "Level "
            + str(z900.plev.values)
            + " is taken for 900hPa"
            + "\n"
            + "Level "
            + str(z600.plev.values)
            + " is taken for 600hPa"
            + "\n"
        )

    ## theta computation
    if "theta" not in tracks:
        angle = theta(tracks)
    else:
        angle = tracks.theta

    ## B computation
    tracks = tracks.assign(
        B=b_vector(angle, z900, z600, tracks.lat.values)
    )

    # 2/ VTL & VTU computation
    if verbose:
        print("Computing VTL & VTU...")
    geopt = geopt.sortby("plev", ascending=False)
    vtl, vtu = vt(geopt)

    # Output
    tracks = tracks.assign(VTL=vtl, VTU=vtu)

    return tracks
