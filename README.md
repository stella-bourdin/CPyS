# CPyS : A package for efficient computation of the Cyclone Phase Space parameters
Author: Stella Bourdin, stella.bourdin@physics.ox.ac.uk . Please reach out for any question!

## Installation
```python
# Download the package very simply with pip
pip install CPyS
```

## Preliminaries

<div>
<img src="CPyS.png" width="350"/>
</div>


1. You need a csv file which contains your track(s) (`tracks.csv` hereafter, but you can name it as you wish). This csv can be the output of TempestExtremes' StitchNodes, or it can be obtained from TRACK's output with a code similar to the one at the bottom at this page. It needs to contains at least the longitude and the latitude of the points, named `lon` and `lat`. If several tracks are in the file, it is advised to have a `track_id` variable to distinguish among the tracks. Otherwise, the value of $\theta$ and $B$ for the last point of each track will be wrong. If your csv file has any other additional columns, they will be kept through the process, although not used.
2. You need a NetCDF file with the geopotential height (in m) at several levels from 900 to 300hPa (at least five are recommended) covering the region where your tracks are (`geopt.nc` hereafter, but you can name it as you wish).
3. Use TempestExtremes' NodeFileCompose to obtain snapshots of the geopotential field along the track(s). Use a code similar to that below, adapted to your data:

```
NodeFileCompose \
    --in_nodefile "tracks.csv" \
    --in_nodefile_type SN \
    --in_fmt "(auto)" \
    --in_data "geopt.nc" \
    --out_grid "RAD" \     # Use radial grid for circular snapshots along the tracks
    --dx 0.5 --resx 10  \  # Snapshots dimension along the radial axis : 10 steps every 0.5° = 500km
    --out_data "snaps.nc" \
    --var "z(:)" \      # Change z to the name of the geopt variable in your data.
    --varout "zg" \     # Your snapshots will be named "snap_zg"
    --snapshots \       # Make sure to output individual snapshots
    --latname latitude --lonname longitude \  # Change to the names in your geopt.nc file
    --regional          # Use this option if your geopt.nc file is not global
```

**NB : NodeFileCompose does not output the value of the vertical coordinate. Be careful to change it before using the snapshots with CPyS**

*This example is based on the track of Typhoon Dale. `Dale.csv` contains the track data, and `Dale.nc` contains the snapshots.*

## Loading the data


```python
# Load the csv data using pandas, or your favorite function.
import pandas as pd
track = pd.read_csv("Dale.csv")
track[["track_id", "time", "lon", "lat"]].head() # Extract of the track file
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>track_id</th>
      <th>time</th>
      <th>lon</th>
      <th>lat</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1277</td>
      <td>1996-11-05 00:00:00</td>
      <td>150.50</td>
      <td>9.00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1277</td>
      <td>1996-11-05 06:00:00</td>
      <td>152.00</td>
      <td>10.25</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1277</td>
      <td>1996-11-05 12:00:00</td>
      <td>152.25</td>
      <td>11.25</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1277</td>
      <td>1996-11-05 18:00:00</td>
      <td>151.50</td>
      <td>12.00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1277</td>
      <td>1996-11-06 00:00:00</td>
      <td>150.50</td>
      <td>11.25</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Load the snapshots file with xarray
import xarray as xr
snaps = xr.open_dataset("Dale.nc")
#snaps["level"] = [...] # !! Change the vertical variable here if necessary. It must be in Pa.
snaps.snap_zg # Content of snap_zg
```

<pre class='xr-text-repr-fallback'>&lt;xarray.DataArray &#x27;snap_zg&#x27; (snapshot: 35, level: 37, r: 50, az: 16)&gt;
[1036000 values with dtype=float32]
Coordinates:
  * az       (az) float64 0.0 22.5 45.0 67.5 90.0 ... 270.0 292.5 315.0 337.5
  * r        (r) float64 0.1 0.3 0.5 0.7 0.9 1.1 1.3 ... 8.9 9.1 9.3 9.5 9.7 9.9
  * level    (level) int32 100 200 300 500 700 ... 92500 95000 97500 100000
Dimensions without coordinates: snapshot</pre><div class='xr-wrap' style='display:none'><div class='xr-header'><div class='xr-obj-type'>xarray.DataArray</div><div class='xr-array-name'>'snap_zg'</div><ul class='xr-dim-list'><li><span>snapshot</span>: 35</li><li><span class='xr-has-index'>level</span>: 37</li><li><span class='xr-has-index'>r</span>: 50</li><li><span class='xr-has-index'>az</span>: 16</li></ul></div><ul class='xr-sections'><li class='xr-section-item'><div class='xr-array-wrap'><input id='section-0c803f81-1c57-4ad7-b712-72b289adf433' class='xr-array-in' type='checkbox' checked><label for='section-0c803f81-1c57-4ad7-b712-72b289adf433' title='Show/hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-array-preview xr-preview'><span>...</span></div><div class='xr-array-data'><pre>[1036000 values with dtype=float32]</pre></div></div></li><li class='xr-section-item'><input id='section-8060792d-1e9b-4508-aa2d-8247fd25fa53' class='xr-section-summary-in' type='checkbox'  checked><label for='section-8060792d-1e9b-4508-aa2d-8247fd25fa53' class='xr-section-summary' >Coordinates: <span>(3)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>az</span></div><div class='xr-var-dims'>(az)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 22.5 45.0 ... 292.5 315.0 337.5</div><input id='attrs-d7c84815-6a28-453a-8c98-ef0da5db1e0f' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-d7c84815-6a28-453a-8c98-ef0da5db1e0f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ca805b77-9d1b-4ed7-abd4-64d893bc122b' class='xr-var-data-in' type='checkbox'><label for='data-ca805b77-9d1b-4ed7-abd4-64d893bc122b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>name :</span></dt><dd>stereographic azimuth angle</dd><dt><span>units :</span></dt><dd>degrees</dd></dl></div><div class='xr-var-data'><pre>array([  0. ,  22.5,  45. ,  67.5,  90. , 112.5, 135. , 157.5, 180. , 202.5,
       225. , 247.5, 270. , 292.5, 315. , 337.5])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>r</span></div><div class='xr-var-dims'>(r)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.1 0.3 0.5 0.7 ... 9.3 9.5 9.7 9.9</div><input id='attrs-9684fce0-bd91-4f4f-a30d-02a18b6d8701' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-9684fce0-bd91-4f4f-a30d-02a18b6d8701' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-e0003eb6-3163-4f88-992f-bb87823a49a3' class='xr-var-data-in' type='checkbox'><label for='data-e0003eb6-3163-4f88-992f-bb87823a49a3' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>name :</span></dt><dd>stereographic great circle distance</dd><dt><span>units :</span></dt><dd>degrees</dd></dl></div><div class='xr-var-data'><pre>array([0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5, 2.7,
       2.9, 3.1, 3.3, 3.5, 3.7, 3.9, 4.1, 4.3, 4.5, 4.7, 4.9, 5.1, 5.3, 5.5,
       5.7, 5.9, 6.1, 6.3, 6.5, 6.7, 6.9, 7.1, 7.3, 7.5, 7.7, 7.9, 8.1, 8.3,
       8.5, 8.7, 8.9, 9.1, 9.3, 9.5, 9.7, 9.9])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>level</span></div><div class='xr-var-dims'>(level)</div><div class='xr-var-dtype'>int32</div><div class='xr-var-preview xr-preview'>100 200 300 ... 95000 97500 100000</div><input id='attrs-4ef50e5b-114c-4708-a5f4-caddbd1220dd' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-4ef50e5b-114c-4708-a5f4-caddbd1220dd' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-936eea9f-1839-4740-bf19-1a5dfc5f8383' class='xr-var-data-in' type='checkbox'><label for='data-936eea9f-1839-4740-bf19-1a5dfc5f8383' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([   100,    200,    300,    500,    700,   1000,   2000,   3000,   5000,
         7000,  10000,  12500,  15000,  17500,  20000,  22500,  25000,  30000,
        35000,  40000,  45000,  50000,  55000,  60000,  65000,  70000,  75000,
        77500,  80000,  82500,  85000,  87500,  90000,  92500,  95000,  97500,
       100000], dtype=int32)</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-ea0ce0e2-e584-4f2b-91b1-4b9417deb4f8' class='xr-section-summary-in' type='checkbox'  ><label for='section-ea0ce0e2-e584-4f2b-91b1-4b9417deb4f8' class='xr-section-summary' >Indexes: <span>(3)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-index-name'><div>az</div></div><div class='xr-index-preview'>PandasIndex</div><div></div><input id='index-ba1a294c-70d8-4220-8547-606eb18e8912' class='xr-index-data-in' type='checkbox'/><label for='index-ba1a294c-70d8-4220-8547-606eb18e8912' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Float64Index([  0.0,  22.5,  45.0,  67.5,  90.0, 112.5, 135.0, 157.5, 180.0,
              202.5, 225.0, 247.5, 270.0, 292.5, 315.0, 337.5],
             dtype=&#x27;float64&#x27;, name=&#x27;az&#x27;))</pre></div></li><li class='xr-var-item'><div class='xr-index-name'><div>r</div></div><div class='xr-index-preview'>PandasIndex</div><div></div><input id='index-602ed039-010a-452f-8f08-13fe69262476' class='xr-index-data-in' type='checkbox'/><label for='index-602ed039-010a-452f-8f08-13fe69262476' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Float64Index([                0.1, 0.30000000000000004,                 0.5,
               0.7000000000000001,                 0.9,                 1.1,
                              1.3,                 1.5,  1.7000000000000002,
               1.9000000000000001,                 2.1,  2.3000000000000003,
                              2.5,                 2.7,  2.9000000000000004,
                              3.1,  3.3000000000000003,                 3.5,
                              3.7,  3.9000000000000004,  4.1000000000000005,
                              4.3,                 4.5,                 4.7,
                              4.9,  5.1000000000000005,   5.300000000000001,
                              5.5,                 5.7,                 5.9,
               6.1000000000000005,   6.300000000000001,                 6.5,
                              6.7,                 6.9,  7.1000000000000005,
                7.300000000000001,                 7.5,                 7.7,
                              7.9,                 8.1,                 8.3,
                              8.5,   8.700000000000001,                 8.9,
                              9.1,                 9.3,                 9.5,
                9.700000000000001,                 9.9],
             dtype=&#x27;float64&#x27;, name=&#x27;r&#x27;))</pre></div></li><li class='xr-var-item'><div class='xr-index-name'><div>level</div></div><div class='xr-index-preview'>PandasIndex</div><div></div><input id='index-acbe0d5e-fc74-407d-8218-03a3428e7d6e' class='xr-index-data-in' type='checkbox'/><label for='index-acbe0d5e-fc74-407d-8218-03a3428e7d6e' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Int64Index([   100,    200,    300,    500,    700,   1000,   2000,   3000,
              5000,   7000,  10000,  12500,  15000,  17500,  20000,  22500,
             25000,  30000,  35000,  40000,  45000,  50000,  55000,  60000,
             65000,  70000,  75000,  77500,  80000,  82500,  85000,  87500,
             90000,  92500,  95000,  97500, 100000],
           dtype=&#x27;int64&#x27;, name=&#x27;level&#x27;))</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-330a79af-3ace-49e1-b2c3-8e278d6cf6ed' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-330a79af-3ace-49e1-b2c3-8e278d6cf6ed' class='xr-section-summary'  title='Expand/collapse section'>Attributes: <span>(0)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><dl class='xr-attrs'></dl></div></li></ul></div></div>



## Computation of the CPS parameters


```python
from CPyS import compute_CPS_parameters
```


```python
track_w_CPS_params = compute_CPS_parameters(track, snaps)
track_w_CPS_params[["track_id", "time", "lon", "lat", "theta", "B", "VTL", "VTU"]].head() # Results!
```

    Computing B...
    Level 90000 is taken for 900hPa
    Level 60000 is taken for 600hPa
    
    Computing VTL & VTU...





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>track_id</th>
      <th>time</th>
      <th>lon</th>
      <th>lat</th>
      <th>theta</th>
      <th>B</th>
      <th>VTL</th>
      <th>VTU</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1277</td>
      <td>1996-11-05 00:00:00</td>
      <td>150.50</td>
      <td>9.00</td>
      <td>39.805571</td>
      <td>-2.858689</td>
      <td>48.728841</td>
      <td>36.933898</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1277</td>
      <td>1996-11-05 06:00:00</td>
      <td>152.00</td>
      <td>10.25</td>
      <td>75.963757</td>
      <td>-6.972262</td>
      <td>74.375981</td>
      <td>47.726629</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1277</td>
      <td>1996-11-05 12:00:00</td>
      <td>152.25</td>
      <td>11.25</td>
      <td>135.000000</td>
      <td>-10.449450</td>
      <td>81.880806</td>
      <td>54.397699</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1277</td>
      <td>1996-11-05 18:00:00</td>
      <td>151.50</td>
      <td>12.00</td>
      <td>216.869898</td>
      <td>-0.754497</td>
      <td>120.169291</td>
      <td>116.594427</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1277</td>
      <td>1996-11-06 00:00:00</td>
      <td>150.50</td>
      <td>11.25</td>
      <td>270.000000</td>
      <td>11.002904</td>
      <td>119.258912</td>
      <td>107.699136</td>
    </tr>
  </tbody>
</table>
</div>



## Plot of the phase space diagram
I have included a simple function to plot the two traditionnal phase space diagrams.


```python
from CPyS import plot_CPS
```


```python
plot_CPS(track_w_CPS_params, title = "Dale")
```


    
![png](demo/output_10_0.png)
    


## Appendix


```python
# Code for reading TRACK files as pd dataframe, which you can then store as csv with tracks.to_csv("file.csv")
def read_TRACKfiles(
    file="tests/TRACK/19501951.dat",
    origin="HRMIP",
    season="19501951",
):
    """
    Parameters
    ----------
    file (str): Path to the TRACK output file
    origin (str): 'ERA5' or 'HRMIP'
    season (str): If None, is read from the data

    Returns
    -------
    pd.DataFrame
        Columns as described in the module header
    """

    # Define parameters according to the file origin
    if origin == "ERA5":
        data_vars = _TRACK_data_vars
        time_format = "calendar"
    else:
        data_vars = _HRMIP_TRACK_data_vars
        time_format = "time_step"

    # Read the TRACK output file
    f = open(file)
    tracks = pd.DataFrame()
    line0 = f.readline()
    line1 = f.readline()
    line2 = f.readline()
    nb_tracks = int(line2.split()[1])
    c = 0
    track_id = 0
    time_step = []
    lon = []
    lat = []
    data = [[]]
    for line in f:
        if line.startswith("TRACK_ID"):
            data = pd.DataFrame(
                np.array(data), columns=data_vars[: np.shape(np.array(data))[1]]
            )
            tracks = pd.concat([
                tracks,
                pd.DataFrame(
                    {
                        "track_id": [track_id] * len(time_step),
                        "time_step": time_step,
                        "lon": lon,
                        "lat": lat,
                    }
                ).join(data)]
            )
            c += 1
            if season == None:
                season = line.split()[-1][:-6]
            track_id = str(season) + "-" + str(c)
            time_step = []
            lon = []
            lat = []
            data = []

        elif line.startswith("POINT_NUM"):
            pass
        else:
            time_step.append(line.split()[0])
            lon.append(float(line.split()[1]))
            lat.append(float(line.split()[2]))
            rest = line.split()[3:]
            mask = np.array(rest) == "&"
            data.append(np.array(rest)[~mask])
    f.close()

    # Format the data
    SH = tracks.lat.mean() < 0
    if SH:
        tracks["track_id"] = "S" + tracks.track_id
        start = np.datetime64(str(int(season) - 1) + "-07-01 00:00:00")
    else:
        tracks["track_id"] = "N" + tracks.track_id
        start = np.datetime64(season + "-01-01 00:00:00")
    if time_format == "calendar":
        tracks["year"] = season
        tracks["month"] = tracks.time_step.str[-6:-4]
        tracks["day"] = tracks.time_step.str[-4:-2]
        tracks["hour"] = tracks.time_step.str[-2:]
        tracks["time"] = get_time(tracks.year, tracks.month, tracks.day, tracks.hour)
        tracks["delta"] = tracks["time"] - np.datetime64(season[-4:] + "-01-01 00")
        tracks["time"] = tracks["delta"] + start
    elif time_format == "time_step":
        tracks["time"] = [
            start + np.timedelta64(ts * 6, "h") for ts in tracks.time_step.astype(int)
        ]
    else:
        print("Please enter a valid time_format")
    time = pd.DatetimeIndex(tracks.time)
    tracks["year"] = time.year
    tracks["month"] = time.month
    tracks["day"] = time.day
    tracks["hour"] = time.hour
    tracks["hemisphere"] = "S" if SH else "N"
    tracks = add_season(tracks)
    tracks["basin"] = get_basin(tracks.lon, tracks.lat)
    if "vor850" in tracks.columns:
        tracks["vor850"] = tracks.vor850.astype(float)
    if "vor_tracked" in tracks.columns:
        tracks["vor_tracked"] = tracks.vor_tracked.astype(float)
    if "slp" not in tracks.columns:
        tracks["slp"] = np.nan
        tracks["sshs"] = np.nan
    else:
        tracks["slp"] = tracks.slp.astype(float)
        tracks["sshs"] = sshs_from_pres(tracks.slp)
    if "wind10" not in tracks.columns:
        tracks["wind10"] = np.nan
    else:
        tracks["wind10"] = tracks.wind10.astype(float)
    tracks["ACE"] = tracks.wind10 ** 2 * 1e-4
    if "wind925" not in tracks.columns:
        tracks["wind925"] = np.nan
    else:
        tracks["wind925"] = tracks.wind925.astype(float)
    return tracks

# Note that you need to define a list of columns that corresponds to your data, such as:
_HRMIP_TRACK_data_vars = [
    "vor_tracked",
    "lon2",
    "lat2",
    "vor850",
    "lon3",
    "lat3",
    "vor700",
    "lon4",
    "lat4",
    "vor600",
    "lon5",
    "lat5",
    "vor500",
    "lon6",
    "lat6",
    "vor250",
    "lon7",
    "lat7",
    "wind10",
]
_TRACK_data_vars = [
    "vor_tracked",
    "lon1",
    "lat1",
    "vor850",
    "lon2",
    "lat2",
    "vor700",
    "lon3",
    "lat3",
    "vor600",
    "lon4",
    "lat4",
    "vor500",
    "lon5",
    "lat5",
    "vor400",
    "lon6",
    "lat6",
    "vor300",
    "lon7",
    "lat7",
    "vor200",
    "lon8",
    "lat8",
    "slp",
    "lon9",
    "lat9",
    "wind925",
    "lon10",
    "lat10",
    "wind10",
]
```
