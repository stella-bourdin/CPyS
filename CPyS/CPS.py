




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

    A = pd.DataFrame([list(z.az.values)] * len(z.snapshot))  # matrix of az x snapshot
    mask = np.array((A.lt(th, 0) & A.ge(th - 180, 0)) | A.ge(th + 180, 0))  # Mask in 2D (az, snapshot)
    mask = np.array([mask] * len(z.r))  # Mask in 3D (r, az, snapshot)
    mask = np.swapaxes(mask, 0, 1)  # Mask in 3D (az, r, snapshot)
    R, L = z.where(mask), z.where(
        ~mask
    )
    return R, L


def area_weights(field):
    """
    Computes the weights needed for the weighted mean of polar field.

    Parameters
    ----------
    field (xr.DataArray): The geopotential field

    Returns
    -------
    w (xr.DataArray): The weights corresponding to the area wrt the radius.
    """
    δ = (field.r[1] - field.r[0]) / 2
    w = (field.r + δ) ** 2 - (field.r - δ) ** 2
    return w


def B(th, geopt, SH=False, names=["snap_z900", "snap_z600"]):
    """
    Computes the B parameter for a point, with the corresponding snapshot of geopt at 600hPa and 900hPa

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
    if type(names) == str:
        z900 = geopt[names].sel(plev=900e2, method="nearest")
        print("Level " + str(z900.plev.values) + " is taken for 900hPa")
        z600 = geopt[names].sel(plev=600e2, method="nearest")
        print("Level " + str(z600.plev.values) + " is taken for 600hPa")
    else:
        z900 = geopt[names[0]]
        z600 = geopt[names[1]]

    ΔZ = z600 - z900
    ΔZ_R, ΔZ_L = right_left_vector(ΔZ, th)
    if SH:
        h = -1
    else:
        h = 1
    return h * (
            ΔZ_R.weighted(area_weights(ΔZ_R)).mean(["r", "az"])
            - ΔZ_L.weighted(area_weights(ΔZ_L)).mean(["r", "az"])
    ).values


def B_vector(th_vec, z900, z600, lat):
    """
    Computes the B parameter for a vector of points, with the corresponding snapshot of geopt at 600hPa and 900hPa

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
    ΔZ = z600 - z900
    ΔZ_R, ΔZ_L = right_left_vector(ΔZ, th_vec)
    h = np.where(lat < 0, -1, 1)
    return h * (
        ΔZ_R.weighted(area_weights(ΔZ_R)).mean(["az", "r"])
        - ΔZ_L.weighted(area_weights(ΔZ_L)).mean(["az", "r"])
    )


def VT_simple(z900, z600,z300):
    """
    Computes V_T^U and V_T^L parameters for the given snapshot of geopt at 300, 600 and 900 hPa

    Parameters
    ----------
    z900 : The geopotential at 900 hPa
    z600 : The geopotential at 600 hPa
    z300 : The geopotential at 300 hPa

    Returns
    -------
    VTL, VTU : The Hart Phase Space parameters for upper and lower thremal wind respectively.
    """
    δz300 = np.abs(z300.max(["r", "az"]) - z300.min(["r", "az"]))
    δz600 = np.abs(z600.max(["r", "az"]) - z600.min(["r", "az"]))
    δz900 = np.abs(z900.max(["r", "az"]) - z900.min(["r", "az"]))
    VTL = 750 * (δz900 - δz600) / (900 - 600)
    VTU = 450 * (δz600 - δz300) / (600 - 300)
    return VTL, VTU

def VT_gradient(geopt, name = "snap_zg") : #TODO : Accelerer en vectorisant
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
    from sklearn.linear_model import LinearRegression
    Z_max = geopt[name].max(["az", "r"]) # Maximum of Z at each level for each snapshot
    Z_min = geopt[name].min(["az", "r"]) # Minimum of ...
    ΔZ = Z_max - Z_min  # Fonction of snapshot & plev
    ΔZ_bottom = ΔZ.sel(plev=slice(950e2, 600e2)) # Lower troposphere
    ΔZ_top = ΔZ.sel(plev=slice(600e2, 250e2))    # Upper tropo
    X = np.log(ΔZ_bottom.plev).values.reshape(-1, 1)
    VTL = [LinearRegression().fit(X, y).coef_[0] if not np.isnan(y).any() else np.nan for y in ΔZ_bottom.values]
    X = np.log(ΔZ_top.plev).values.reshape(-1, 1)
    VTU = [LinearRegression().fit(X, y).coef_[0] for y in ΔZ_top.values]
    return VTL, VTU


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
    VTL, VTU = VT_gradient(geopt, name = geopt_name)

    # Output
    tracks = tracks.assign(VTL=VTL, VTU=VTU)
    #np.seterr(**old_settings)

    return tracks

if __name__ == "__main__":
    import numpy as np
    import pandas as pd
    import xarray as xr

    # Tests theta
    assert theta(0,1,0,0) == 0.0 # Eastward
    assert theta(0,0,0,1) == 90.0 # Northward
    assert theta(0,-1,0,0) == 180.0 # Westward
    assert theta(0,0,0,-1) == 270.0 # Southward

    assert theta_track([0,1,1,0,0], [0,0,1,1,0]) == [0.0, 90.0, 180, 270.0, 270.0]

    #tracks = pd.read_csv("CPyS/tests/Dale.csv")
    #geopt = xr.open_dataset("CPyS/tests/Dale.nc")
    #tracks_CPS = compute_CPS_parameters(tracks, geopt)