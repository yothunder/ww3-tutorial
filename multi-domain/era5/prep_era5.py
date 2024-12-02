import os
import xarray as xr 

fname = 'era5_202401_0103.nc'
ds = xr.open_dataset(fname)
ds = ds.rename({'valid_time':'time'})
ds = ds.reindex(latitude=ds.latitude[::-1])
if os.path.exists("wind.nc"):
    os.remove('wind.nc')
ds.to_netcdf(f"wind.nc")
