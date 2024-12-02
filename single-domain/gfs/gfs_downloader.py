import os
import datetime
import numpy as np
from time import sleep
import subprocess

import urllib.request

#%% Global variables
maxtry = 100
waitsec = 1

#%% Functions
def domsel(dom):
    if dom == 'global':
        gfsurl = 'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl'
        gfsopt = '&lev_10_m_above_ground=on&var_DPT=on&var_UGRD=on&var_VGRD=on&lev_mean_sea_level=on&var_PRMSL=on&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%2F'
        midsufgfsfile = 'pgrb2.0p25'
        
    return gfsurl, gfsopt, midsufgfsfile

def gfsdown(URL, gfslocalfile):
    
    try:
        os.makedirs(os.path.dirname(gfslocalfile))
    except(FileExistsError):
        pass
    except:
        raise
    
    for i in range(maxtry):
        try:
            response = urllib.request.urlopen(URL, timeout = 30)
            data = response.read()
            with open(gfslocalfile, 'wb') as f:  
                f.write(data)
            break
        except:
            print(f'Download Failed, Attemp : {i}')
            sleep(waitsec)
            continue
    else:
        raise StopIteration('Error: Maximum retry has been reached, DOWNDLOAD FAILED!')
    
    return(gfslocalfile)
    
def gendts():
    dtn = datetime.datetime.utcnow()
#    dtn = dtn = datetime.datetime(2018,9,18,17,59,0)
    if (dtn.hour >= 3) & (dtn.hour < 15):
        cycl = '00'
    elif (dtn.hour >= 15) & (dtn.hour <= 24):
        cycl = '12'
    else:
        cycl = '12'
        dtn = dtn - datetime.timedelta(hours = 12)
    
    dt = dtn.strftime('%Y%m%d')
    
    dts = dt + cycl
    
    return dts

def gengfsURL(outfol, ftime,dt,cycl,dom):
    fts = str(ftime).zfill(3)
    gfsurl, gfsopt, midsufgfsfile = domsel(dom)
    
    gfsfile = f'gfs.t{cycl}z.{midsufgfsfile}.f{fts}'
    URL = f"{gfsurl}?file={gfsfile}{gfsopt}gfs.{dt}%2F{cycl}%2Fatmos"
    gfslocalname = f'{gfsfile}'
    
    gfslocalfile = os.path.join(outfol,gfslocalname)
    
    return URL, gfslocalfile

def gfscheck(gfslocalfile):
    if os.path.isfile(gfslocalfile):
        line = subprocess.check_output(['tail', '-1', gfslocalfile])
        if line[-4:] == b'7777':
            return True
    else:
        return False

def main_downloader(outfol=None,dts=None,dom='global',maxt=240,onlycheck=False):
    if dts is None:
        dts = gendts()
        dt = dts[:8]
        cycl = dts[8:]
    else:
        dt = dts[:8]
        cycl = dts[8:]
        
    outd = os.path.join(outfol,dts)
    
    fcttime = np.arange(0,maxt+1,3)
    for fct in fcttime:
        URL, gfslocalfile = gengfsURL(outd,fct,dt,cycl,dom)
        hasilcheck = gfscheck(gfslocalfile)
        if hasilcheck:
            print('Checking file %s: OK' % gfslocalfile)
            continue
        else:
            if not onlycheck:
                print('Downloading %s' % gfslocalfile)
                gfsdown(URL, gfslocalfile)
    return True
    

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('output_directory',
                        help = 'Output directory where you want to store downloaded files')
    
    parser.add_argument('date',
                        help = 'Forecast date, format = "YYYYMMDDHH"')
    
    parser.add_argument('-d', action='store', dest='dom',
                        help='domain',
                        default = 'global')
    
    parser.add_argument('-t', action='store', dest='maxt',
                        help='Maximum forecast time, format = "t"',
                        default = 241)
    
    parser.add_argument('--version', action='version', version='%(prog)s 1.2 by luthfi.imanal@gmail.com')
    
    r = parser.parse_args()
    
    main_downloader(r.output_directory,
                    dts=r.date,
                    dom=r.dom,
                    maxt=int(r.maxt))
