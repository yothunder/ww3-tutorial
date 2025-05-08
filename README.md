# WAVEWATCH III® Tutorial

This repository contains WAVEWATCH III® (WW3) tutorial intended for STMKG lecture. It is a suplementary for this hands on notes https://coral-cake-624.notion.site/kuliah-praktik-pcln.

We assume that users have installed the WW3 model on their own computers. Otherwise, please follow the installation process from this link https://www.notion.so/WW3-Installation-147cec73bd5980108100c30f2dd9a164.

## Requirements

1. WAVEWATCH III® installed on the system
2. Libraries
    a. NETCDF
    b. HDF5
    c. OPENMP & MPI
3. Python for pre and post processing, with the following packages:
    a. numpy
    b. xarray
    c. netcdf4
    d. cdsapi
    e. pygrib

## Case Studies
### 1. Single domain
Running real case for a single domain using `ww3_shel`.

### 2. Multi domain
Running real case for nested domains (2 domains) using `ww3_multi`.

## Directory structure

```bash
ww3-case/
├── multi-domain/
│   ├── era5/
│   │   ├── era5_202401_0103.nc
│   │   ├── get_era5.py
│   │   ├── prep_era5.py
│   │   ├── wind.nc
│   │   ├── ww3_grid
│   │   ├── ww3_grid.inp
│   │   ├── ww3_prnc
│   │   └── ww3_prnc.inp
│   ├── sunda_11km/
│   │   ├── sunda_11km.depth
│   │   ├── sunda_11km.mask
│   │   ├── sunda_11km.obs
│   │   ├── ww3_grid
│   │   └── ww3_grid.inp
│   ├── sunda_5km/
│   │   ├── sunda_5km.depth
│   │   ├── sunda_5km.mask
│   │   ├── sunda_5km.obs
│   │   ├── ww3_grid
│   │   └── ww3_grid.inp
│   ├── ww3_multi
│   ├── ww3_multi.inp
│   ├── ww3_ounf
│   ├── ww3_ounf.inp
|   └── README.md
|
├── single-domain/
│   ├── gfs/
│   │   ├── gfs_downloader.py
│   │   ├── grib2ww3.py
│   │   ├── ww3_grid
│   │   ├── ww3_grid.inp
│   │   ├── ww3_prep
│   │   └── ww3_prep.inp
│   ├── sunda/
│   │   ├── sunda.depth
│   │   ├── sunda.mask
│   │   ├── sunda.meta
│   │   ├── sunda.obs
│   │   ├── ww3_grid
│   │   └── ww3_grid.inp
│   ├── grads2nc.py
│   ├── gx_outf
│   ├── gx_outf.inp
│   └── README.md
└── README.md
```