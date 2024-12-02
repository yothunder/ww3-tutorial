import os
import subprocess

def grib2ww3(fgrdir,fout,maxt = 240):
    import pygrib
    import datetime
    import numpy as np
    
    outf, outnamei = os.path.split(fout)
    outname, extt = os.path.splitext(outnamei)
    fouti = os.path.join(outf,'%s.fdt' % outname)
    dt0 = None
    
    try:
        os.remove(fout)
    except:
        pass
    
    for root, dirs, files in os.walk(fgrdir, topdown=False):
        for name in sorted(files):
            fgr = os.path.join(root,name)
            print(f'Processing file: {fgr}')
            try:
                grbs = pygrib.open(fgr)
                g = grbs[1]
                dtni = g.analDate + datetime.timedelta(hours = g['endStep'])
                if g['endStep'] > maxt:
                    break
                if not dt0:
                    dt0 = dtni
            except:
                print(f'Warning, invalid file {fgr} : Skip')
                continue
            
            with open(fout,'a') as fo:
                fo.write(dtni.strftime('%Y%m%d %H%M%S'))
                fo.write('\n')
            
            g_sel = grbs.select(shortName = '10u')
            g = g_sel[0]
            u = g['values']
            u = np.flip(u,0)
            form = (('%.2f'+' ')*u.shape[1])[:-1]
            for i in range(u.shape[0]):
                with open(fout,'a') as fo:
                    fo.write(form % tuple(u[i,:]))
                    fo.write('\n')
                    
            g_sel = grbs.select(shortName = '10v')
            g = g_sel[0]
            v = g['values']
            v = np.flip(v,0)
            for i in range(v.shape[0]):
                with open(fout,'a') as fo:
                    fo.write(form % tuple(v[i,:]))
                    fo.write('\n')
    
    if not os.path.exists(fouti):
        subprocess.run(["touch", f"{fouti}"])
        
    #with open(fouti,'w') as fo:
    #    fo.write(dt0.strftime('%Y%m%d%H'))
                    
if __name__ == '__main__':
    grib_dir = '/mnt/d/bak/gfs/2019050300'
    fout = '/tmp/tesww3.txt'
    maxt = 72
    
    import argparse
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('grib_dir',
                        help = 'Grib directory, where you store grib files. If grib files are not available, it will be automatically downloaded to this directory')
    
    parser.add_argument('output_file',
                        help = 'Output file. Full path. Example : /tmp/gfsww3.txt')
    
#    parser.add_argument('-d', action='store', dest='dom',
#                        help='domain',
#                        default = 'global')
    
    parser.add_argument('-t', action='store', dest='maxt',
                        help='Maximum forecast time, format = "t"',
                        default = 240)
    
    subparsers = parser.add_subparsers(dest='subcommand',help='Select mode <archive> or <convert>.')
    
    parse_a = subparsers.add_parser('archive',
                                    help='In this mode script will automatically check grib files, and download them, and grib directory will be <grib_dir>/<date>. date will be required')
    
    parse_a.add_argument('date',
                         help = 'Forecast date, format = "YYYYMMDDHH"')
    
    
    parse_b = subparsers.add_parser('convert',
                                    help='In this mode, download and check will be disabled, and grib directory will be <grib_dir>')
    
    
    
    parser.add_argument('--version', action='version', version='%(prog)s 1.2 by luthfi.imanal@gmail.com')
    
    r = parser.parse_args()
    
    if r.subcommand == 'archive':
        grib_dir = os.path.join(r.grib_dir,r.date)
        from gfs_downloader import main_downloader
        main_downloader(r.grib_dir,
                        dts=r.date,
                        maxt=int(r.maxt))
    else:
        grib_dir = r.grib_dir
    
    grib2ww3(grib_dir,
             r.output_file,
             maxt = int(r.maxt))
