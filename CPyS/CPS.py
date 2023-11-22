from .theta import theta_multitrack
from .B import B_vector
from .VT import VT

def compute_CPS_parameters(
    tracks, geopt, geopt_name = "snap_zg", plev_name="level",
):
    """
    Computes the three (+ theta) Hart parameters for all the points in tracks.

    Parameters
    ----------
    tracks (pd.DataFrame): The set of TC points
    geopt (xr.DataSet): The geopotential snapshots associated with the tracks
        level coordinate must be named plev, in Pa.
    names (str) : Provide the name of the 3D (plev, r, az) geopt snapshots variables as a string.

    Returns
    -------
    tracks (pd.DataFrame): The set of TC points with four new columns corresponding to the parameters
    """

    #old_settings = np.seterr(divide='ignore', invalid='ignore')

    geopt = geopt.rename({plev_name:"plev"})

    # 1/ B computation
    ## Select 900 & 600 hPa levels
    z900, z600 = geopt[geopt_name].sel(plev = 900e2, method = "nearest"), \
                       geopt[geopt_name].sel(plev = 600e2, method = "nearest"),
    print("Level "+str(z900.plev.values)+" is taken for 900hPa"+"\n"+
          "Level "+str(z600.plev.values)+" is taken for 600hPa"+"\n")

    ## theta computation
    if "theta" not in tracks.columns :
        tracks = tracks.assign(theta=theta_multitrack(tracks))

    ## B computation
    tracks = tracks.assign(
        B=B_vector(tracks.theta.values, z900, z600, tracks.lat.values)
    )

    # 2/ VTL & VTU computation
    geopt = geopt.sortby("plev", ascending = False)
    VTL, VTU = VT(geopt, name = geopt_name)

    # Output
    tracks = tracks.assign(VTL=VTL, VTU=VTU)
    #np.seterr(**old_settings)

    return tracks

if __name__ == "__main__":
    pass