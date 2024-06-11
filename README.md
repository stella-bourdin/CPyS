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
snaps # Content of snaps
```




<div><svg style="position: absolute; width: 0; height: 0; overflow: hidden">
<defs>
<symbol id="icon-database" viewBox="0 0 32 32">
<path d="M16 0c-8.837 0-16 2.239-16 5v4c0 2.761 7.163 5 16 5s16-2.239 16-5v-4c0-2.761-7.163-5-16-5z"></path>
<path d="M16 17c-8.837 0-16-2.239-16-5v6c0 2.761 7.163 5 16 5s16-2.239 16-5v-6c0 2.761-7.163 5-16 5z"></path>
<path d="M16 26c-8.837 0-16-2.239-16-5v6c0 2.761 7.163 5 16 5s16-2.239 16-5v-6c0 2.761-7.163 5-16 5z"></path>
</symbol>
<symbol id="icon-file-text2" viewBox="0 0 32 32">
<path d="M28.681 7.159c-0.694-0.947-1.662-2.053-2.724-3.116s-2.169-2.030-3.116-2.724c-1.612-1.182-2.393-1.319-2.841-1.319h-15.5c-1.378 0-2.5 1.121-2.5 2.5v27c0 1.378 1.122 2.5 2.5 2.5h23c1.378 0 2.5-1.122 2.5-2.5v-19.5c0-0.448-0.137-1.23-1.319-2.841zM24.543 5.457c0.959 0.959 1.712 1.825 2.268 2.543h-4.811v-4.811c0.718 0.556 1.584 1.309 2.543 2.268zM28 29.5c0 0.271-0.229 0.5-0.5 0.5h-23c-0.271 0-0.5-0.229-0.5-0.5v-27c0-0.271 0.229-0.5 0.5-0.5 0 0 15.499-0 15.5 0v7c0 0.552 0.448 1 1 1h7v19.5z"></path>
<path d="M23 26h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
<path d="M23 22h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
<path d="M23 18h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
</symbol>
</defs>
</svg>
<style>/* CSS stylesheet for displaying xarray objects in jupyterlab.
 *
 */

:root {
  --xr-font-color0: var(--jp-content-font-color0, rgba(0, 0, 0, 1));
  --xr-font-color2: var(--jp-content-font-color2, rgba(0, 0, 0, 0.54));
  --xr-font-color3: var(--jp-content-font-color3, rgba(0, 0, 0, 0.38));
  --xr-border-color: var(--jp-border-color2, #e0e0e0);
  --xr-disabled-color: var(--jp-layout-color3, #bdbdbd);
  --xr-background-color: var(--jp-layout-color0, white);
  --xr-background-color-row-even: var(--jp-layout-color1, white);
  --xr-background-color-row-odd: var(--jp-layout-color2, #eeeeee);
}

html[theme=dark],
body[data-theme=dark],
body.vscode-dark {
  --xr-font-color0: rgba(255, 255, 255, 1);
  --xr-font-color2: rgba(255, 255, 255, 0.54);
  --xr-font-color3: rgba(255, 255, 255, 0.38);
  --xr-border-color: #1F1F1F;
  --xr-disabled-color: #515151;
  --xr-background-color: #111111;
  --xr-background-color-row-even: #111111;
  --xr-background-color-row-odd: #313131;
}

.xr-wrap {
  display: block !important;
  min-width: 300px;
  max-width: 700px;
}

.xr-text-repr-fallback {
  /* fallback to plain text repr when CSS is not injected (untrusted notebook) */
  display: none;
}

.xr-header {
  padding-top: 6px;
  padding-bottom: 6px;
  margin-bottom: 4px;
  border-bottom: solid 1px var(--xr-border-color);
}

.xr-header > div,
.xr-header > ul {
  display: inline;
  margin-top: 0;
  margin-bottom: 0;
}

.xr-obj-type,
.xr-array-name {
  margin-left: 2px;
  margin-right: 10px;
}

.xr-obj-type {
  color: var(--xr-font-color2);
}

.xr-sections {
  padding-left: 0 !important;
  display: grid;
  grid-template-columns: 150px auto auto 1fr 20px 20px;
}

.xr-section-item {
  display: contents;
}

.xr-section-item input {
  display: none;
}

.xr-section-item input + label {
  color: var(--xr-disabled-color);
}

.xr-section-item input:enabled + label {
  cursor: pointer;
  color: var(--xr-font-color2);
}

.xr-section-item input:enabled + label:hover {
  color: var(--xr-font-color0);
}

.xr-section-summary {
  grid-column: 1;
  color: var(--xr-font-color2);
  font-weight: 500;
}

.xr-section-summary > span {
  display: inline-block;
  padding-left: 0.5em;
}

.xr-section-summary-in:disabled + label {
  color: var(--xr-font-color2);
}

.xr-section-summary-in + label:before {
  display: inline-block;
  content: '►';
  font-size: 11px;
  width: 15px;
  text-align: center;
}

.xr-section-summary-in:disabled + label:before {
  color: var(--xr-disabled-color);
}

.xr-section-summary-in:checked + label:before {
  content: '▼';
}

.xr-section-summary-in:checked + label > span {
  display: none;
}

.xr-section-summary,
.xr-section-inline-details {
  padding-top: 4px;
  padding-bottom: 4px;
}

.xr-section-inline-details {
  grid-column: 2 / -1;
}

.xr-section-details {
  display: none;
  grid-column: 1 / -1;
  margin-bottom: 5px;
}

.xr-section-summary-in:checked ~ .xr-section-details {
  display: contents;
}

.xr-array-wrap {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: 20px auto;
}

.xr-array-wrap > label {
  grid-column: 1;
  vertical-align: top;
}

.xr-preview {
  color: var(--xr-font-color3);
}

.xr-array-preview,
.xr-array-data {
  padding: 0 5px !important;
  grid-column: 2;
}

.xr-array-data,
.xr-array-in:checked ~ .xr-array-preview {
  display: none;
}

.xr-array-in:checked ~ .xr-array-data,
.xr-array-preview {
  display: inline-block;
}

.xr-dim-list {
  display: inline-block !important;
  list-style: none;
  padding: 0 !important;
  margin: 0;
}

.xr-dim-list li {
  display: inline-block;
  padding: 0;
  margin: 0;
}

.xr-dim-list:before {
  content: '(';
}

.xr-dim-list:after {
  content: ')';
}

.xr-dim-list li:not(:last-child):after {
  content: ',';
  padding-right: 5px;
}

.xr-has-index {
  font-weight: bold;
}

.xr-var-list,
.xr-var-item {
  display: contents;
}

.xr-var-item > div,
.xr-var-item label,
.xr-var-item > .xr-var-name span {
  background-color: var(--xr-background-color-row-even);
  margin-bottom: 0;
}

.xr-var-item > .xr-var-name:hover span {
  padding-right: 5px;
}

.xr-var-list > li:nth-child(odd) > div,
.xr-var-list > li:nth-child(odd) > label,
.xr-var-list > li:nth-child(odd) > .xr-var-name span {
  background-color: var(--xr-background-color-row-odd);
}

.xr-var-name {
  grid-column: 1;
}

.xr-var-dims {
  grid-column: 2;
}

.xr-var-dtype {
  grid-column: 3;
  text-align: right;
  color: var(--xr-font-color2);
}

.xr-var-preview {
  grid-column: 4;
}

.xr-index-preview {
  grid-column: 2 / 5;
  color: var(--xr-font-color2);
}

.xr-var-name,
.xr-var-dims,
.xr-var-dtype,
.xr-preview,
.xr-attrs dt {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-right: 10px;
}

.xr-var-name:hover,
.xr-var-dims:hover,
.xr-var-dtype:hover,
.xr-attrs dt:hover {
  overflow: visible;
  width: auto;
  z-index: 1;
}

.xr-var-attrs,
.xr-var-data,
.xr-index-data {
  display: none;
  background-color: var(--xr-background-color) !important;
  padding-bottom: 5px !important;
}

.xr-var-attrs-in:checked ~ .xr-var-attrs,
.xr-var-data-in:checked ~ .xr-var-data,
.xr-index-data-in:checked ~ .xr-index-data {
  display: block;
}

.xr-var-data > table {
  float: right;
}

.xr-var-name span,
.xr-var-data,
.xr-index-name div,
.xr-index-data,
.xr-attrs {
  padding-left: 25px !important;
}

.xr-attrs,
.xr-var-attrs,
.xr-var-data,
.xr-index-data {
  grid-column: 1 / -1;
}

dl.xr-attrs {
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: 125px auto;
}

.xr-attrs dt,
.xr-attrs dd {
  padding: 0;
  margin: 0;
  float: left;
  padding-right: 10px;
  width: auto;
}

.xr-attrs dt {
  font-weight: normal;
  grid-column: 1;
}

.xr-attrs dt:hover span {
  display: inline-block;
  background: var(--xr-background-color);
  padding-right: 10px;
}

.xr-attrs dd {
  grid-column: 2;
  white-space: pre-wrap;
  word-break: break-all;
}

.xr-icon-database,
.xr-icon-file-text2,
.xr-no-icon {
  display: inline-block;
  vertical-align: middle;
  width: 1em;
  height: 1.5em !important;
  stroke-width: 0;
  stroke: currentColor;
  fill: currentColor;
}
</style><pre class='xr-text-repr-fallback'>&lt;xarray.Dataset&gt; Size: 4MB
Dimensions:      (az: 16, r: 50, snapshot: 35, level: 37)
Coordinates:
  * az           (az) float64 128B 0.0 22.5 45.0 67.5 ... 292.5 315.0 337.5
  * r            (r) float64 400B 0.1 0.3 0.5 0.7 0.9 ... 9.1 9.3 9.5 9.7 9.9
  * level        (level) int32 148B 100 200 300 500 ... 92500 95000 97500 100000
Dimensions without coordinates: snapshot
Data variables:
    snap_pathid  (snapshot) int32 140B ...
    snap_lon     (snapshot) float64 280B ...
    snap_lat     (snapshot) float64 280B ...
    snap_time    (snapshot) datetime64[ns] 280B ...
    snap_zg      (snapshot, level, r, az) float32 4MB ...
    zg           (level, r, az) float32 118kB ...</pre><div class='xr-wrap' style='display:none'><div class='xr-header'><div class='xr-obj-type'>xarray.Dataset</div></div><ul class='xr-sections'><li class='xr-section-item'><input id='section-1f9dd7eb-9070-4243-ab0a-0cc6656794cb' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-1f9dd7eb-9070-4243-ab0a-0cc6656794cb' class='xr-section-summary'  title='Expand/collapse section'>Dimensions:</label><div class='xr-section-inline-details'><ul class='xr-dim-list'><li><span class='xr-has-index'>az</span>: 16</li><li><span class='xr-has-index'>r</span>: 50</li><li><span>snapshot</span>: 35</li><li><span class='xr-has-index'>level</span>: 37</li></ul></div><div class='xr-section-details'></div></li><li class='xr-section-item'><input id='section-1b6a8485-124b-423f-8629-cafba6a86b39' class='xr-section-summary-in' type='checkbox'  checked><label for='section-1b6a8485-124b-423f-8629-cafba6a86b39' class='xr-section-summary' >Coordinates: <span>(3)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>az</span></div><div class='xr-var-dims'>(az)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 22.5 45.0 ... 292.5 315.0 337.5</div><input id='attrs-e1b591e4-2234-4381-9292-1872d170e091' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-e1b591e4-2234-4381-9292-1872d170e091' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-988cb114-eba0-4b5a-afdf-84abdb608de6' class='xr-var-data-in' type='checkbox'><label for='data-988cb114-eba0-4b5a-afdf-84abdb608de6' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>name :</span></dt><dd>stereographic azimuth angle</dd><dt><span>units :</span></dt><dd>degrees</dd></dl></div><div class='xr-var-data'><pre>array([  0. ,  22.5,  45. ,  67.5,  90. , 112.5, 135. , 157.5, 180. , 202.5,
       225. , 247.5, 270. , 292.5, 315. , 337.5])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>r</span></div><div class='xr-var-dims'>(r)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.1 0.3 0.5 0.7 ... 9.3 9.5 9.7 9.9</div><input id='attrs-59024970-ca03-4e1e-b472-44ce9e6a931a' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-59024970-ca03-4e1e-b472-44ce9e6a931a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-afbc7e20-f5f2-4918-964d-85e885b830aa' class='xr-var-data-in' type='checkbox'><label for='data-afbc7e20-f5f2-4918-964d-85e885b830aa' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>name :</span></dt><dd>stereographic great circle distance</dd><dt><span>units :</span></dt><dd>degrees</dd></dl></div><div class='xr-var-data'><pre>array([0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5, 2.7,
       2.9, 3.1, 3.3, 3.5, 3.7, 3.9, 4.1, 4.3, 4.5, 4.7, 4.9, 5.1, 5.3, 5.5,
       5.7, 5.9, 6.1, 6.3, 6.5, 6.7, 6.9, 7.1, 7.3, 7.5, 7.7, 7.9, 8.1, 8.3,
       8.5, 8.7, 8.9, 9.1, 9.3, 9.5, 9.7, 9.9])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>level</span></div><div class='xr-var-dims'>(level)</div><div class='xr-var-dtype'>int32</div><div class='xr-var-preview xr-preview'>100 200 300 ... 95000 97500 100000</div><input id='attrs-e511559d-4dcc-42b2-b22d-8254e89ec814' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-e511559d-4dcc-42b2-b22d-8254e89ec814' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-769308f6-1256-42b0-8359-3debfa9fd413' class='xr-var-data-in' type='checkbox'><label for='data-769308f6-1256-42b0-8359-3debfa9fd413' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([   100,    200,    300,    500,    700,   1000,   2000,   3000,   5000,
         7000,  10000,  12500,  15000,  17500,  20000,  22500,  25000,  30000,
        35000,  40000,  45000,  50000,  55000,  60000,  65000,  70000,  75000,
        77500,  80000,  82500,  85000,  87500,  90000,  92500,  95000,  97500,
       100000], dtype=int32)</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-0381f344-b353-4c8f-9118-dc4e27d41235' class='xr-section-summary-in' type='checkbox'  checked><label for='section-0381f344-b353-4c8f-9118-dc4e27d41235' class='xr-section-summary' >Data variables: <span>(6)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span>snap_pathid</span></div><div class='xr-var-dims'>(snapshot)</div><div class='xr-var-dtype'>int32</div><div class='xr-var-preview xr-preview'>...</div><input id='attrs-dd83232b-c34d-471e-97c8-a091d7a3fcac' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-dd83232b-c34d-471e-97c8-a091d7a3fcac' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-aad8b988-7ce5-4c52-ac21-54e4bcc8e827' class='xr-var-data-in' type='checkbox'><label for='data-aad8b988-7ce5-4c52-ac21-54e4bcc8e827' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>[35 values with dtype=int32]</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>snap_lon</span></div><div class='xr-var-dims'>(snapshot)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>...</div><input id='attrs-24098ab4-7c85-4170-9de5-5c01cefeca44' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-24098ab4-7c85-4170-9de5-5c01cefeca44' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-608c0b8a-cefe-4496-acf5-7b04062c1db3' class='xr-var-data-in' type='checkbox'><label for='data-608c0b8a-cefe-4496-acf5-7b04062c1db3' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>units :</span></dt><dd>degrees_east</dd></dl></div><div class='xr-var-data'><pre>[35 values with dtype=float64]</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>snap_lat</span></div><div class='xr-var-dims'>(snapshot)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>...</div><input id='attrs-a964bd63-a71a-420d-b464-90837daabc7b' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-a964bd63-a71a-420d-b464-90837daabc7b' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ec6228e8-cbd0-4d9f-ab5a-d73bdb161566' class='xr-var-data-in' type='checkbox'><label for='data-ec6228e8-cbd0-4d9f-ab5a-d73bdb161566' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>units :</span></dt><dd>degrees_north</dd></dl></div><div class='xr-var-data'><pre>[35 values with dtype=float64]</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>snap_time</span></div><div class='xr-var-dims'>(snapshot)</div><div class='xr-var-dtype'>datetime64[ns]</div><div class='xr-var-preview xr-preview'>...</div><input id='attrs-7486e226-08c1-4da3-b69b-308b7bb164e0' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-7486e226-08c1-4da3-b69b-308b7bb164e0' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-8a65a61b-08c0-4296-a35c-c8342d9fb467' class='xr-var-data-in' type='checkbox'><label for='data-8a65a61b-08c0-4296-a35c-c8342d9fb467' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>[35 values with dtype=datetime64[ns]]</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>snap_zg</span></div><div class='xr-var-dims'>(snapshot, level, r, az)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>...</div><input id='attrs-b4112da5-4737-4479-a1f1-877d796779f7' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-b4112da5-4737-4479-a1f1-877d796779f7' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ea3469b8-6e18-42cc-8763-760d3a988225' class='xr-var-data-in' type='checkbox'><label for='data-ea3469b8-6e18-42cc-8763-760d3a988225' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>[1036000 values with dtype=float32]</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>zg</span></div><div class='xr-var-dims'>(level, r, az)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>...</div><input id='attrs-177ef57f-df4e-4f3b-ad03-2de294c83496' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-177ef57f-df4e-4f3b-ad03-2de294c83496' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-9038225b-dcfa-4c48-a13c-c8c4409eb126' class='xr-var-data-in' type='checkbox'><label for='data-9038225b-dcfa-4c48-a13c-c8c4409eb126' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>[29600 values with dtype=float32]</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-a5995ef6-289f-489e-9c3e-2f58a9dff0aa' class='xr-section-summary-in' type='checkbox'  ><label for='section-a5995ef6-289f-489e-9c3e-2f58a9dff0aa' class='xr-section-summary' >Indexes: <span>(3)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-index-name'><div>az</div></div><div class='xr-index-preview'>PandasIndex</div><div></div><input id='index-dc69c6b6-46e8-4d03-a99c-0e2cde0db337' class='xr-index-data-in' type='checkbox'/><label for='index-dc69c6b6-46e8-4d03-a99c-0e2cde0db337' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Index([  0.0,  22.5,  45.0,  67.5,  90.0, 112.5, 135.0, 157.5, 180.0, 202.5,
       225.0, 247.5, 270.0, 292.5, 315.0, 337.5],
      dtype=&#x27;float64&#x27;, name=&#x27;az&#x27;))</pre></div></li><li class='xr-var-item'><div class='xr-index-name'><div>r</div></div><div class='xr-index-preview'>PandasIndex</div><div></div><input id='index-b3e91c8d-60ed-4368-aea6-86ed2760a415' class='xr-index-data-in' type='checkbox'/><label for='index-b3e91c8d-60ed-4368-aea6-86ed2760a415' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Index([                0.1, 0.30000000000000004,                 0.5,
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
      dtype=&#x27;float64&#x27;, name=&#x27;r&#x27;))</pre></div></li><li class='xr-var-item'><div class='xr-index-name'><div>level</div></div><div class='xr-index-preview'>PandasIndex</div><div></div><input id='index-3df98780-e29d-495b-a155-b5fd40290228' class='xr-index-data-in' type='checkbox'/><label for='index-3df98780-e29d-495b-a155-b5fd40290228' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Index([   100,    200,    300,    500,    700,   1000,   2000,   3000,   5000,
         7000,  10000,  12500,  15000,  17500,  20000,  22500,  25000,  30000,
        35000,  40000,  45000,  50000,  55000,  60000,  65000,  70000,  75000,
        77500,  80000,  82500,  85000,  87500,  90000,  92500,  95000,  97500,
       100000],
      dtype=&#x27;int32&#x27;, name=&#x27;level&#x27;))</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-ff255528-961d-475b-9483-9e236a89e948' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-ff255528-961d-475b-9483-9e236a89e948' class='xr-section-summary'  title='Expand/collapse section'>Attributes: <span>(0)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><dl class='xr-attrs'></dl></div></li></ul></div></div>



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


    
![png](output_12_0.png)
    


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


```python

```
