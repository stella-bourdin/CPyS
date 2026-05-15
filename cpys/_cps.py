import numpy as np

from ._theta import theta
from ._hart import b, vt


def compute_cps_parameters(
    tracks,
    geopt,
    plev_name="level",
    verbose=True,
    p_bottom=900e2,
    p_mid=600e2,
    p_top=250e2,
    p_bottom_vtl=950e2,
    p_top_vtl=None,
    p_bottom_vtu=None,
    p_top_vtu=None,
):
    """
    Computes the three (+ theta) Hart parameters for all the points in tracks.

    Parameters
    ----------
    tracks : xarray.Dataset
        The set of TC points
    geopt : xarray.DataArray
        The geopotential snapshots associated with the tracks level coordinate must be
        in Pa.
    plev_name : str
        The name of the vertical coordinate in the geopt file.

    Returns
    -------
    xarray.Dataset
        The set of TC points with four new variable corresponding to the CPS
        parameters (B, VTL, VTU) and the angle (theta)
    """
    # Curate input
    # Pressure levels
    if p_bottom_vtl is None:
        p_bottom_vtl = p_bottom
    if p_top_vtl is None:
        p_top_vtl = p_mid
    if p_bottom_vtu is None:
        p_bottom_vtu = p_mid
    if p_top_vtu is None:
        p_top_vtu = p_top

    ## geopt snapshots
    geopt = geopt.rename({plev_name: "plev"})  # Change vertical coordinate name
    geopt = geopt.where(np.abs(geopt) < 1e10)

    # 1/ B computation
    if verbose:
        print("Computing B...")
    ## Select 900 & 600 hPa levels
    z900, z600 = (
        geopt.sel(plev=p_bottom, method="nearest"),
        geopt.sel(plev=p_mid, method="nearest"),
    )
    if verbose:
        print(
            f"Level {z900.plev.values} is taken for 900hPa\n"
            f"Level {z600.plev.values} is taken for 600hPa\n"
        )

    ## theta computation
    if "theta" not in tracks:
        tracks = tracks.assign(theta=theta(tracks))

    ## B computation
    asymmetry = b(tracks["theta"], z900, z600, tracks.lat.values)

    # 2/ VTL & VTU computation
    if verbose:
        print("Computing VTL & VTU...")

    vtl = vt(geopt.sel(plev=slice(p_top_vtl, p_bottom_vtl)))
    vtu = vt(geopt.sel(plev=slice(p_top_vtu, p_bottom_vtu)))

    # Output
    return tracks.assign(
        B=("record", asymmetry),
        VTL=("record", vtl),
        VTU=("record", vtu)
    )
