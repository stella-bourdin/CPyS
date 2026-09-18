In this folder are tracks and snapshots for 8 test cases, issued from the three reference papers for this work. 
- Floyd 1999 from Hart 2003
- Mitch 1998 from Hart 2003
- Olga 2001 from Hart 2003
- WarmSecl 1982 from Hart 2003
- Ciaran 2024 from Besson 2025
- Domingos 2024 from Besson 2025
- Cyclone A 2020 from Croad 2023 (named CroadA)
- Cyclone B 2020 from Croad 2023 (named CroadB)

* Hart, R. E. (2003). A cyclone phase space derived from thermal wind and thermal asymmetry. Monthly weather review, 131(4), 585-616.
* Croad, H. L., Methven, J., Harvey, B., Keeley, S. P., & Volonté, A. (2023). 
The role of boundary layer processes in summer-time Arctic cyclones. Weather and Climate Dynamics, 4(3), 617-638.
* Besson, M., Rivière, G., & Fromang, S. (2025). A cyclone phase space dedicated to extratropical cyclones. EGUsphere, 2025, 1-30.

Tracks were obtained using TempestExtremes, with either TC detection or ETC detection setting, using ERA5. 
They are centered on SLP minima. 

Snapshots of geopotential, vorticity and temperature were obtained using the command below. 
In the NetCDF files 
- Vertical levels are, in hPa,  [   1,    2,    3,    5,    7,   10,   20,   30,   50,   70,  100,  125,
        150,  175,  200,  225,  250,  300,  350,  400,  450,  500,  550,  600,
        650,  700,  750,  775,  800,  825,  850,  875,  900,  925,  950,  975,
       1000]
- Geopotential units are  m**2 s**-2

NodeFileCompose \
    --in_nodefile data/cases_tracks/${name}_${year}.csv \
    --in_nodefile_type "SN" \
    --in_data_list "tmp/filelist_$name.txt" \
    --out_grid "RAD" \
    --out_data "data/snaps/${name}_${year}.nc" \
    --var "geopt(:),ta(:),vo(:)" \
	--varout "geopt,ta,vo" \
    --snapshots \
    --latname "latitude" --lonname "longitude" \
	--dx 0.1 --resx 50 --resa 16