import cProfile as profile
import pstats

import huracanpy
import xarray as xr

import cpys

geopt = xr.open_dataset("Dale.nc").snap_zg
tracks = huracanpy.load("Dale.csv")

profile.run("cpys.compute_cps_parameters(tracks, geopt)", "stats")

stats = pstats.Stats("stats")
stats.sort_stats("cumulative")
stats.print_stats(0.01)