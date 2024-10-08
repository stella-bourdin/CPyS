from .theta import theta_multitrack
from .B import B_vector
from .VT import VT
import pandas as pd
import numpy as np
import xarray as xr


def compute_CPS_parameters(
    tracks,
    geopt,
    geopt_name="snap_zg",
    plev_name="level",
    verbose=True,
):
    """
    Computes the three (+ theta) Hart parameters for all the points in tracks.

    Parameters
    ----------
    tracks (pd.DataFrame): The set of TC points
    geopt (xr.DataSet): The geopotential snapshots associated with the tracks
        level coordinate must be in Pa.
    geopt_name (str): Provide the name of the 3D (plev, r, az) geopt snapshots variables as a string.
    plev_name (str): name of the vertical coordinate in the geopt file.

    Returns
    -------
    tracks (pd.DataFrame): The set of TC points with four new columns corresponding to the parameters
    """

    # Curate input
    ## geopt snapshots
    geopt = geopt.rename({plev_name: "plev"})  # Change vertical coordinate name
    geopt = geopt.where(np.abs(geopt[geopt_name]) < 1e10)

    ## tracks
    ### Test type
    if type(tracks) == xr.Dataset:
        tracks = tracks.to_dataframe()
    elif type(tracks) == pd.DataFrame:
        pass
    else: 
        print("Type of tracks not recognized. Please provide a pandas dataframe or an xarray dataset.\nNote: If you are using huracanpy to load the tracks, the object is an xarray Dataset.")
        return None
              
    ### Time
    if "time" not in tracks.columns: ## Todo: Replace with huracanpy's get time?
        tracks["time"] = pd.to_datetime(
            tracks.year.astype(str) + '-' +
            tracks.month.astype(str) + '-' +
            tracks.day.astype(str) + '-' +
            tracks.hour.astype(str) + ":00:00"
        )

    # 1/ B computation
    if verbose:
        print("Computing B...")
    ## Select 900 & 600 hPa levels
    z900, z600 = (
        geopt[geopt_name].sel(plev=900e2, method="nearest"),
        geopt[geopt_name].sel(plev=600e2, method="nearest"),
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
    if "theta" not in tracks.columns:
        tracks = tracks.assign(theta=theta_multitrack(tracks))

    ## B computation
    tracks = tracks.assign(
        B=B_vector(tracks.theta.values, z900, z600, tracks.lat.values)
    )

    # 2/ VTL & VTU computation
    if verbose:
        print("Computing VTL & VTU...")
    geopt = geopt.sortby("plev", ascending=False)
    VTL, VTU = VT(geopt, name=geopt_name)

    # Output
    tracks = tracks.assign(VTL=VTL, VTU=VTU)

    return tracks


if __name__ == "__main__":
    import xarray as xr

    # Test theta_multitrack
    tracks = pd.read_csv("tests/Dale.csv", index_col=False)
    geopt = xr.open_dataset("tests/Dale.nc")

    df = compute_CPS_parameters(tracks, geopt)
