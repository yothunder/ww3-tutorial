import os
import pandas as pd
import numpy as np
import logging
from datetime import datetime
from multiprocessing import Pool
import xgrads
from netCDF4 import date2num
import warnings
import xarray as xr

def grads2netcdf(ctl_file:str, nc_out:str):
    print(f"GrADS to NetCDF Converter ...")
    cwd = os.getcwd()
    if not os.path.exists(os.path.dirname(nc_out)):
        os.makedirs(os.path.dirname(nc_out))
    dset = xgrads.open_CtlDataset(ctl_file)
    baserun = pd.to_datetime(dset.time.data[0])
    hs = dset.hs.compute().data.astype(float)
    hs[hs < 0] = np.nan
    hmax = hs.astype(float) * 2.0
    dirc = np.rad2deg(dset.dir.compute()).data.astype(float)
    dirc[dirc < -360] = np.nan
    dp = np.rad2deg(dset.dp.compute()).data.astype(float)
    dp[dp < -360] = np.nan
    uwnd = dset.uwnd.compute().data.astype(float) * 1.943844492457
    uwnd[uwnd < -100] = np.nan
    vwnd = dset.vwnd.compute().data.astype(float) * 1.943844492457
    vwnd[vwnd < -100] = np.nan
    lm = dset.lm.compute().data.astype(float)
    lm[lm < 0] = np.nan
    t01 = dset.t01.compute().data.astype(float)
    t01[t01 < 0] = np.nan
    phs00 = dset.phs00.compute().data.astype(float)
    phs00[phs00 < 0] = np.nan
    phs01 = dset.phs01.compute().data.astype(float)
    phs01[phs01 < 0] = np.nan
    phs02 = dset.phs02.compute().data.astype(float)
    phs02[phs02 < 0] = np.nan
    ptp00 = dset.ptp00.compute().data.astype(float)
    ptp00[ptp00 < 0] = np.nan
    ptp01 = dset.ptp01.compute().data.astype(float)
    ptp01[ptp01 < 0] = np.nan
    ptp02 = dset.ptp02.compute().data.astype(float)
    ptp02[ptp02 < 0] = np.nan
    pdi00 = np.rad2deg(dset.pdi00.compute().data.astype(float))
    pdi00[pdi00 < -360] = np.nan
    pdi01 = np.rad2deg(dset.pdi01.compute().data.astype(float))
    pdi01[pdi01 < -360] = np.nan
    pdi02 = np.rad2deg(dset.pdi02.compute().data.astype(float))
    pdi02[pdi02 < -360] = np.nan
    t_unit = baserun.strftime("minute since %Y-%m-%d %H:00")
    t_calendar = "gregorian"
    dft = pd.to_datetime(dset.time.dt.strftime("%Y%m%d%H%M"))
    time = xr.DataArray(
        data = date2num(list(dft), units=t_unit, calendar=t_calendar),
        dims = ['time']
        ).astype(dtype=np.int32)

    dset = xr.Dataset(data_vars = {
        'hs' : xr.DataArray(
            data = hs,
            dims = ['time','lat','lon'],
            coords = {
                "time": time,
                "lat" : dset.lat.data,
                "lon" : dset.lon.data
            }
        ),
        'hmax' : xr.DataArray(
            data = hmax,
            dims = ['time','lat','lon'],
            coords = {
                "time": time,
                "lat" : dset.lat.data,
                "lon" : dset.lon.data
            }
        ),
        'dir' : xr.DataArray(
            data = dirc,
            dims = ['time','lat','lon'],
            coords = {
                "time": time,
                "lat" : dset.lat.data,
                "lon" : dset.lon.data
            }
        ),
        'dp' : xr.DataArray(
            data = dp,
            dims = ['time','lat','lon'],
            coords = {
                "time": time,
                "lat" : dset.lat.data,
                "lon" : dset.lon.data
            }
        ),
        'lm' : xr.DataArray(
            data = lm,
            dims = ['time','lat','lon'],
            coords = {
                "time": time,
                "lat" : dset.lat.data,
                "lon" : dset.lon.data
            }
        ),
        't01' : xr.DataArray(
            data = t01,
            dims = ['time','lat','lon'],
            coords = {
                "time": time,
                "lat" : dset.lat.data,
                "lon" : dset.lon.data
            }
        ),
        'uwnd' : xr.DataArray(
            data = uwnd,
            dims = ['time','lat','lon'],
            coords = {
                "time": time,
                "lat" : dset.lat.data,
                "lon" : dset.lon.data
            }
        ),
        'vwnd' : xr.DataArray(
            data = vwnd,
            dims = ['time','lat','lon'],
            coords = {
                "time": time,
                "lat" : dset.lat.data,
                "lon" : dset.lon.data
            }
        ),
        'phs00' : xr.DataArray(
            data = phs00,
            dims = ['time','lat','lon'],
            coords = {
                "time": time,
                "lat" : dset.lat.data,
                "lon" : dset.lon.data
            }
        ),
        'phs01' : xr.DataArray(
            data = phs01,
            dims = ['time','lat','lon'],
            coords = {
                "time": time,
                "lat" : dset.lat.data,
                "lon" : dset.lon.data
            }
        ),
        'phs02' : xr.DataArray(
            data = phs02,
            dims = ['time','lat','lon'],
            coords = {
                "time": time,
                "lat" : dset.lat.data,
                "lon" : dset.lon.data
            }
        ),
        'ptp00' : xr.DataArray(
            data = ptp00,
            dims = ['time','lat','lon'],
            coords = {
                "time": time,
                "lat" : dset.lat.data,
                "lon" : dset.lon.data
            }
        ),
        'ptp01' : xr.DataArray(
            data = ptp01,
            dims = ['time','lat','lon'],
            coords = {
                "time": time,
                "lat" : dset.lat.data,
                "lon" : dset.lon.data
            }
        ),
        'ptp02' : xr.DataArray(
            data = ptp02,
            dims = ['time','lat','lon'],
            coords = {
                "time": time,
                "lat" : dset.lat.data,
                "lon" : dset.lon.data
            }
        ),
            'ptp02' : xr.DataArray(
            data = ptp02,
            dims = ['time','lat','lon'],
            coords = {
                "time": time,
                "lat" : dset.lat.data,
                "lon" : dset.lon.data
            }
        ),    
        'pdi00' : xr.DataArray(
            data = pdi00,
            dims = ['time','lat','lon'],
            coords = {
                "time": time,
                "lat" : dset.lat.data,
                "lon" : dset.lon.data
            }
        ),    
        'pdi01' : xr.DataArray(
            data = pdi01,
            dims = ['time','lat','lon'],
            coords = {
                "time": time,
                "lat" : dset.lat.data,
                "lon" : dset.lon.data
            }
        ),
        'pdi02' : xr.DataArray(
            data = ptp02,
            dims = ['time','lat','lon'],
            coords = {
                "time": time,
                "lat" : dset.lat.data,
                "lon" : dset.lon.data
            }
        ),
    })

    dset.lat.attrs = {
        "long_name" : "Latitude", 
        "standard_name" : "latitude", 
        "units" : "degrees_north"
    }
    dset.lon.attrs = {
        "long_name" : "Longitude", 
        "standard_name" : "longitude", 
        "units" : "degrees_east"
    }
    dset.time.attrs = {
        "long_name" : "Time", 
        "standard_name" : "time",
        "units": t_unit,
        "calendar": t_calendar 
    }
    dset.hs.attrs = {
        "long_name" : "Significant wave height", 
        "standard_name" : "sea_surface_wave_significant_height",
        "units":"m"
    }
    dset.lm.attrs = {
        "long_name" : "Wave Length", 
        "standard_name" : "sea_surface_wave_mean_wavelength_from_variance_spectral_density_inverse_wavenumber_moment", 
        "units" : "m"
    }
    dset.t01.attrs = {
        "long_name" : "Wave Period", 
        "standard_name" : "sea_surface_wave_significant_period", 
        "units" : "s"
    }
    dset.dir.attrs = {
        "long_name" : "Mean Wave Direction", 
        "standard_name" : "sea_surface_mean_wave_from_direction", 
        "units" : "degree"
    }
    dset.dp.attrs = {
        "long_name" : "Peak Wave Direction", 
        "standard_name" : "sea_surface_peak_wave_from_direction", 
        "units" : "degree"
    }
    dset.phs00.attrs = {
        "long_name" : "Wind Sea Height", 
        "standard_name" : "sea_surface_wind_wave_significant_height", 
        "units":"m"
    }
    dset.phs01.attrs = {
        "long_name" : "Primary Swell Height", 
        "standard_name" : "sea_surface_primary_swell_wave_significant_height", 
        "units" : "m"
    }
    dset.phs02.attrs = {
        "long_name" : "Secondary Swell Height", 
        "standard_name" : "sea_surface_secondary_swell_wave_significant_height", 
        "units" : "m"
    }
    dset.ptp00.attrs = {
        "long_name" : "Wind Sea Period", 
        "standard_name" : "sea_surface_wind_wave_period", 
        "units" : "s"
    }
    dset.ptp01.attrs = {
        "long_name" : "Primary Swell Period", 
        "standard_name" : "sea_surface_primary_swell_wave_mean_period", 
        "units" : "s"
    }
    dset.ptp02.attrs = {
        "long_name" : "Secondary Swell Period", 
        "standard_name" : "sea_surface_secondary_swell_wave_mean_period", 
        "units" : "s"
    }
    dset.pdi00.attrs = {
        "long_name" : "Wind Sea Direction", 
        "standard_name" : "sea_surface_wind_wave_from_direction", 
        "units" : "degree"
    }
    dset.pdi01.attrs = {
        "long_name" : "Primary Swell Direction", 
        "standard_name" : "sea_surface_primary_swell_wave_from_direction", 
        "units" : "degree"
    }
    dset.pdi02.attrs = {
        "long_name" : "Secondary Swell Direction", 
        "standard_name" : "sea_surface_secondary_swell_wave_from_direction", 
        "units" : "degree"
    }
    dset.uwnd.attrs = {
        "long_name" : "Eastward Wind Speed", 
        "standard_name" : "eastward_wind", 
        "units" : "knot"
    }
    dset.vwnd.attrs = {
        "long_name" : "Northward Wind", 
        "standard_name" : "northward_wind", 
        "units" : "knot"
    }
    dset.hmax.attrs = {
        "long_name" : "Maximum Wave Height", 
        "standard_name" : "sea_surface_wave_maximum_height", 
        "units" : "m"
    }
    dset.attrs = {
        "source": "Inawaves - BMKG Ocean Forecast System (OFS)",
        "description": "Inawaves Model - Forecast",
        "institution": "BMKG - Center For Marine Meteorology",
        "email": "produksi.maritim@bmkg.go.id",
        "Conventions" : "CF-1.8"
    }
    dset.to_netcdf(nc_out, encoding={
        "hs" : {"dtype":"float64", "zlib":"true", "least_significant_digit":3, "complevel":4},
        "hmax" : {"dtype":"float64", "zlib":"true", "least_significant_digit":3, "complevel":4},
        "dir" : {"dtype":"float64", "zlib":"true", "least_significant_digit":3, "complevel":4},
        "dp" : {"dtype":"float64", "zlib":"true", "least_significant_digit":3, "complevel":4},
        "lm" : {"dtype":"float64", "zlib":"true", "least_significant_digit":3, "complevel":4},
        "t01" : {"dtype":"float64", "zlib":"true", "least_significant_digit":3, "complevel":4},
        "uwnd" : {"dtype":"float64", "zlib":"true", "least_significant_digit":3, "complevel":4},
        "vwnd" : {"dtype":"float64", "zlib":"true", "least_significant_digit":3, "complevel":4},
        "phs00" : {"dtype":"float64", "zlib":"true", "least_significant_digit":3, "complevel":4},
        "phs01" : {"dtype":"float64", "zlib":"true", "least_significant_digit":3, "complevel":4},
        "phs02" : {"dtype":"float64", "zlib":"true", "least_significant_digit":3, "complevel":4},
        "ptp00" : {"dtype":"float64", "zlib":"true", "least_significant_digit":3, "complevel":4},
        "ptp01" : {"dtype":"float64", "zlib":"true", "least_significant_digit":3, "complevel":4},
        "ptp02" : {"dtype":"float64", "zlib":"true", "least_significant_digit":3, "complevel":4},
        "ptp02" : {"dtype":"float64", "zlib":"true", "least_significant_digit":3, "complevel":4},
        "pdi00" : {"dtype":"float64", "zlib":"true", "least_significant_digit":3, "complevel":4},
        "pdi01" : {"dtype":"float64", "zlib":"true", "least_significant_digit":3, "complevel":4},
        "pdi02" : {"dtype":"float64", "zlib":"true", "least_significant_digit":3, "complevel":4},
    }, format="NETCDF4_CLASSIC")
    print(f"File saved at {nc_out}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="GrADS to NetCDF Converter",
        epilog="Example:python grads2nc.py /path/to/ww3.ctl /path/to/ww3.nc"
    )
    parser.add_argument("ctl_file", type=str, help="ctl file.", metavar="ctl_file")
    parser.add_argument("nc_out", type=str, help="nc out file.", metavar="nc_out")
    args = parser.parse_args()
    grads2netcdf(args.ctl_file, args.nc_out)