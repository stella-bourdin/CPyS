# CPyS : A package for efficient computation of the Cyclone Phase Space parameters
Author: Stella Bourdin, stella.bourdin@physics.ox.ac.uk . Please reach out for any question!

## Installation


```python
# Download the package very simply with pip
pip install CPyS
```

## Preliminaries
1. You need a csv file which contains your track(s) (`tracks.csv` hereafter, but you can name it as you wish). This csv can be the output of TempestExtremes' StitchNodes, or it can be obtained from TRACK's output with a code similar to the one at the bottom at this page. It needs to contains at least the longitude and the latitude of the points, named `lon` and `lat`. If several tracks are in the file, it is advised to have a `track_id` variable to distinguish among the tracks. Otherwise, the value of $\theta$ and $B$ for the last point of each track will be wrong. If your csv file has any other additional columns, they will be kept through the process, although not used.
2. You need a NetCDF file with the geopotential at several levels from 900 to 300hPa (at least five are recommended) covering the region where your tracks are (`geopt.nc` hereafter, but you can name it as you wish).
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
track[["track_id", "time", "lon", "lat"]] # Extract of the track file
```




<div>
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
    <tr>
      <th>5</th>
      <td>1277</td>
      <td>1996-11-06 06:00:00</td>
      <td>150.50</td>
      <td>11.00</td>
    </tr>
    <tr>
      <th>6</th>
      <td>1277</td>
      <td>1996-11-06 12:00:00</td>
      <td>150.00</td>
      <td>11.75</td>
    </tr>
    <tr>
      <th>7</th>
      <td>1277</td>
      <td>1996-11-06 18:00:00</td>
      <td>148.75</td>
      <td>11.50</td>
    </tr>
    <tr>
      <th>8</th>
      <td>1277</td>
      <td>1996-11-07 00:00:00</td>
      <td>148.75</td>
      <td>11.00</td>
    </tr>
    <tr>
      <th>9</th>
      <td>1277</td>
      <td>1996-11-07 06:00:00</td>
      <td>147.75</td>
      <td>11.25</td>
    </tr>
    <tr>
      <th>10</th>
      <td>1277</td>
      <td>1996-11-07 12:00:00</td>
      <td>146.50</td>
      <td>11.50</td>
    </tr>
    <tr>
      <th>11</th>
      <td>1277</td>
      <td>1996-11-07 18:00:00</td>
      <td>145.00</td>
      <td>11.75</td>
    </tr>
    <tr>
      <th>12</th>
      <td>1277</td>
      <td>1996-11-08 00:00:00</td>
      <td>143.25</td>
      <td>11.75</td>
    </tr>
    <tr>
      <th>13</th>
      <td>1277</td>
      <td>1996-11-08 06:00:00</td>
      <td>142.00</td>
      <td>11.75</td>
    </tr>
    <tr>
      <th>14</th>
      <td>1277</td>
      <td>1996-11-08 12:00:00</td>
      <td>141.00</td>
      <td>11.75</td>
    </tr>
    <tr>
      <th>15</th>
      <td>1277</td>
      <td>1996-11-08 18:00:00</td>
      <td>139.50</td>
      <td>12.25</td>
    </tr>
    <tr>
      <th>16</th>
      <td>1277</td>
      <td>1996-11-09 00:00:00</td>
      <td>138.25</td>
      <td>12.75</td>
    </tr>
    <tr>
      <th>17</th>
      <td>1277</td>
      <td>1996-11-09 06:00:00</td>
      <td>137.00</td>
      <td>13.25</td>
    </tr>
    <tr>
      <th>18</th>
      <td>1277</td>
      <td>1996-11-09 12:00:00</td>
      <td>136.00</td>
      <td>14.25</td>
    </tr>
    <tr>
      <th>19</th>
      <td>1277</td>
      <td>1996-11-09 18:00:00</td>
      <td>135.00</td>
      <td>15.25</td>
    </tr>
    <tr>
      <th>20</th>
      <td>1277</td>
      <td>1996-11-10 00:00:00</td>
      <td>133.75</td>
      <td>16.50</td>
    </tr>
    <tr>
      <th>21</th>
      <td>1277</td>
      <td>1996-11-10 06:00:00</td>
      <td>132.75</td>
      <td>17.50</td>
    </tr>
    <tr>
      <th>22</th>
      <td>1277</td>
      <td>1996-11-10 12:00:00</td>
      <td>131.75</td>
      <td>18.50</td>
    </tr>
    <tr>
      <th>23</th>
      <td>1277</td>
      <td>1996-11-10 18:00:00</td>
      <td>131.25</td>
      <td>19.50</td>
    </tr>
    <tr>
      <th>24</th>
      <td>1277</td>
      <td>1996-11-11 00:00:00</td>
      <td>130.75</td>
      <td>20.75</td>
    </tr>
    <tr>
      <th>25</th>
      <td>1277</td>
      <td>1996-11-11 06:00:00</td>
      <td>131.00</td>
      <td>21.75</td>
    </tr>
    <tr>
      <th>26</th>
      <td>1277</td>
      <td>1996-11-11 12:00:00</td>
      <td>131.25</td>
      <td>22.75</td>
    </tr>
    <tr>
      <th>27</th>
      <td>1277</td>
      <td>1996-11-11 18:00:00</td>
      <td>132.00</td>
      <td>24.00</td>
    </tr>
    <tr>
      <th>28</th>
      <td>1277</td>
      <td>1996-11-12 00:00:00</td>
      <td>132.75</td>
      <td>25.25</td>
    </tr>
    <tr>
      <th>29</th>
      <td>1277</td>
      <td>1996-11-12 06:00:00</td>
      <td>133.75</td>
      <td>26.25</td>
    </tr>
    <tr>
      <th>30</th>
      <td>1277</td>
      <td>1996-11-12 12:00:00</td>
      <td>135.50</td>
      <td>27.50</td>
    </tr>
    <tr>
      <th>31</th>
      <td>1277</td>
      <td>1996-11-12 18:00:00</td>
      <td>138.50</td>
      <td>28.50</td>
    </tr>
    <tr>
      <th>32</th>
      <td>1277</td>
      <td>1996-11-13 00:00:00</td>
      <td>142.75</td>
      <td>30.50</td>
    </tr>
    <tr>
      <th>33</th>
      <td>1277</td>
      <td>1996-11-13 06:00:00</td>
      <td>148.00</td>
      <td>32.50</td>
    </tr>
    <tr>
      <th>34</th>
      <td>1277</td>
      <td>1996-11-13 12:00:00</td>
      <td>155.00</td>
      <td>36.50</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Load the snapshots file with xarray
import xarray as xr
snaps = xr.open_dataset("Dale.nc")
#snaps["level"] = [...] # !! Change the vertical variable here if necessary. It must be in Pa.
```


```python
# Snapshots dimensions
snaps.snap_zg.dims
```




    ('snapshot', 'level', 'r', 'az')




```python
# Dimensions
snaps.coords
```




    Coordinates:
      * az       (az) float64 128B 0.0 22.5 45.0 67.5 ... 270.0 292.5 315.0 337.5
      * r        (r) float64 400B 0.1 0.3 0.5 0.7 0.9 1.1 ... 9.1 9.3 9.5 9.7 9.9
      * level    (level) int32 148B 100 200 300 500 700 ... 92500 95000 97500 100000



## Computation of the CPS parameters


```python
from CPyS import compute_CPS_parameters
```


```python
track_w_CPS_params = compute_CPS_parameters(track, snaps)
track_w_CPS_params[["track_id", "time", "lon", "lat", "theta", "B", "VTL", "VTU"]] # Results!
```

    Computing B...
    Level 90000 is taken for 900hPa
    Level 60000 is taken for 600hPa
    
    Computing VTL & VTU...





<div>
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
    <tr>
      <th>5</th>
      <td>1277</td>
      <td>1996-11-06 06:00:00</td>
      <td>150.50</td>
      <td>11.00</td>
      <td>123.690068</td>
      <td>-7.824734</td>
      <td>122.372489</td>
      <td>105.959700</td>
    </tr>
    <tr>
      <th>6</th>
      <td>1277</td>
      <td>1996-11-06 12:00:00</td>
      <td>150.00</td>
      <td>11.75</td>
      <td>191.309932</td>
      <td>-1.379825</td>
      <td>142.778913</td>
      <td>106.332585</td>
    </tr>
    <tr>
      <th>7</th>
      <td>1277</td>
      <td>1996-11-06 18:00:00</td>
      <td>148.75</td>
      <td>11.50</td>
      <td>270.000000</td>
      <td>2.639275</td>
      <td>128.205585</td>
      <td>116.285513</td>
    </tr>
    <tr>
      <th>8</th>
      <td>1277</td>
      <td>1996-11-07 00:00:00</td>
      <td>148.75</td>
      <td>11.00</td>
      <td>165.963757</td>
      <td>3.478431</td>
      <td>151.808066</td>
      <td>132.191755</td>
    </tr>
    <tr>
      <th>9</th>
      <td>1277</td>
      <td>1996-11-07 06:00:00</td>
      <td>147.75</td>
      <td>11.25</td>
      <td>168.690068</td>
      <td>1.628800</td>
      <td>157.627609</td>
      <td>130.330405</td>
    </tr>
    <tr>
      <th>10</th>
      <td>1277</td>
      <td>1996-11-07 12:00:00</td>
      <td>146.50</td>
      <td>11.50</td>
      <td>170.537678</td>
      <td>2.838853</td>
      <td>168.825123</td>
      <td>140.099883</td>
    </tr>
    <tr>
      <th>11</th>
      <td>1277</td>
      <td>1996-11-07 18:00:00</td>
      <td>145.00</td>
      <td>11.75</td>
      <td>180.000000</td>
      <td>3.555864</td>
      <td>165.303199</td>
      <td>166.089468</td>
    </tr>
    <tr>
      <th>12</th>
      <td>1277</td>
      <td>1996-11-08 00:00:00</td>
      <td>143.25</td>
      <td>11.75</td>
      <td>180.000000</td>
      <td>4.846188</td>
      <td>202.031166</td>
      <td>197.741404</td>
    </tr>
    <tr>
      <th>13</th>
      <td>1277</td>
      <td>1996-11-08 06:00:00</td>
      <td>142.00</td>
      <td>11.75</td>
      <td>180.000000</td>
      <td>8.541439</td>
      <td>200.608822</td>
      <td>231.410117</td>
    </tr>
    <tr>
      <th>14</th>
      <td>1277</td>
      <td>1996-11-08 12:00:00</td>
      <td>141.00</td>
      <td>11.75</td>
      <td>161.565051</td>
      <td>7.499349</td>
      <td>231.229205</td>
      <td>275.971821</td>
    </tr>
    <tr>
      <th>15</th>
      <td>1277</td>
      <td>1996-11-08 18:00:00</td>
      <td>139.50</td>
      <td>12.25</td>
      <td>158.198591</td>
      <td>8.350890</td>
      <td>221.525033</td>
      <td>301.511912</td>
    </tr>
    <tr>
      <th>16</th>
      <td>1277</td>
      <td>1996-11-09 00:00:00</td>
      <td>138.25</td>
      <td>12.75</td>
      <td>158.198591</td>
      <td>13.814835</td>
      <td>201.318918</td>
      <td>325.515701</td>
    </tr>
    <tr>
      <th>17</th>
      <td>1277</td>
      <td>1996-11-09 06:00:00</td>
      <td>137.00</td>
      <td>13.25</td>
      <td>135.000000</td>
      <td>9.081773</td>
      <td>199.958096</td>
      <td>327.971192</td>
    </tr>
    <tr>
      <th>18</th>
      <td>1277</td>
      <td>1996-11-09 12:00:00</td>
      <td>136.00</td>
      <td>14.25</td>
      <td>135.000000</td>
      <td>8.773186</td>
      <td>168.909787</td>
      <td>338.476551</td>
    </tr>
    <tr>
      <th>19</th>
      <td>1277</td>
      <td>1996-11-09 18:00:00</td>
      <td>135.00</td>
      <td>15.25</td>
      <td>135.000000</td>
      <td>3.275680</td>
      <td>203.648746</td>
      <td>315.273011</td>
    </tr>
    <tr>
      <th>20</th>
      <td>1277</td>
      <td>1996-11-10 00:00:00</td>
      <td>133.75</td>
      <td>16.50</td>
      <td>135.000000</td>
      <td>1.542190</td>
      <td>224.866598</td>
      <td>390.489712</td>
    </tr>
    <tr>
      <th>21</th>
      <td>1277</td>
      <td>1996-11-10 06:00:00</td>
      <td>132.75</td>
      <td>17.50</td>
      <td>135.000000</td>
      <td>2.163576</td>
      <td>234.454862</td>
      <td>357.229220</td>
    </tr>
    <tr>
      <th>22</th>
      <td>1277</td>
      <td>1996-11-10 12:00:00</td>
      <td>131.75</td>
      <td>18.50</td>
      <td>116.565051</td>
      <td>-4.552958</td>
      <td>251.703436</td>
      <td>369.438634</td>
    </tr>
    <tr>
      <th>23</th>
      <td>1277</td>
      <td>1996-11-10 18:00:00</td>
      <td>131.25</td>
      <td>19.50</td>
      <td>111.801409</td>
      <td>-4.863091</td>
      <td>248.684975</td>
      <td>388.123252</td>
    </tr>
    <tr>
      <th>24</th>
      <td>1277</td>
      <td>1996-11-11 00:00:00</td>
      <td>130.75</td>
      <td>20.75</td>
      <td>75.963757</td>
      <td>-5.425436</td>
      <td>225.197118</td>
      <td>402.630643</td>
    </tr>
    <tr>
      <th>25</th>
      <td>1277</td>
      <td>1996-11-11 06:00:00</td>
      <td>131.00</td>
      <td>21.75</td>
      <td>75.963757</td>
      <td>-0.924122</td>
      <td>197.898618</td>
      <td>386.382148</td>
    </tr>
    <tr>
      <th>26</th>
      <td>1277</td>
      <td>1996-11-11 12:00:00</td>
      <td>131.25</td>
      <td>22.75</td>
      <td>59.036243</td>
      <td>13.115511</td>
      <td>214.416774</td>
      <td>364.826074</td>
    </tr>
    <tr>
      <th>27</th>
      <td>1277</td>
      <td>1996-11-11 18:00:00</td>
      <td>132.00</td>
      <td>24.00</td>
      <td>59.036243</td>
      <td>22.026497</td>
      <td>193.967018</td>
      <td>320.715098</td>
    </tr>
    <tr>
      <th>28</th>
      <td>1277</td>
      <td>1996-11-12 00:00:00</td>
      <td>132.75</td>
      <td>25.25</td>
      <td>45.000000</td>
      <td>47.103238</td>
      <td>143.214635</td>
      <td>216.606582</td>
    </tr>
    <tr>
      <th>29</th>
      <td>1277</td>
      <td>1996-11-12 06:00:00</td>
      <td>133.75</td>
      <td>26.25</td>
      <td>35.537678</td>
      <td>66.173683</td>
      <td>179.447963</td>
      <td>103.050376</td>
    </tr>
    <tr>
      <th>30</th>
      <td>1277</td>
      <td>1996-11-12 12:00:00</td>
      <td>135.50</td>
      <td>27.50</td>
      <td>18.434949</td>
      <td>84.836855</td>
      <td>132.319875</td>
      <td>-99.523735</td>
    </tr>
    <tr>
      <th>31</th>
      <td>1277</td>
      <td>1996-11-12 18:00:00</td>
      <td>138.50</td>
      <td>28.50</td>
      <td>25.201124</td>
      <td>110.467675</td>
      <td>113.114828</td>
      <td>-158.705783</td>
    </tr>
    <tr>
      <th>32</th>
      <td>1277</td>
      <td>1996-11-13 00:00:00</td>
      <td>142.75</td>
      <td>30.50</td>
      <td>20.854458</td>
      <td>136.636961</td>
      <td>-101.234583</td>
      <td>-313.597616</td>
    </tr>
    <tr>
      <th>33</th>
      <td>1277</td>
      <td>1996-11-13 06:00:00</td>
      <td>148.00</td>
      <td>32.50</td>
      <td>29.744881</td>
      <td>173.836766</td>
      <td>-393.814981</td>
      <td>-413.435704</td>
    </tr>
    <tr>
      <th>34</th>
      <td>1277</td>
      <td>1996-11-13 12:00:00</td>
      <td>155.00</td>
      <td>36.50</td>
      <td>29.744881</td>
      <td>242.850398</td>
      <td>-732.284368</td>
      <td>-589.779152</td>
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
    
