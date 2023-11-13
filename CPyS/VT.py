def VT(geopt, name = "snap_zg") : #TODO : Accelerer en vectorisant
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
