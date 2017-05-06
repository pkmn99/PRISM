# use mygeo enviroment for local machine
# zonal statistics to covert prism data to US county mean 
import numpy as np
import pandas as pd
import gdal, gdalconst
from affine import Affine
from rasterstats import zonal_stats
import cartopy.io.shapereader as shpreader

"""Define BilFile class to read data and attributes"""
class BilFile(object):
    def __init__(self, bil_path, bil_file):
        self.bil_file = bil_file
        self.bil_filepath = bil_path

    def get_array(self):
        gdal.GetDriverByName('EHdr').Register()
        ds = gdal.Open('/vsizip/' + self.bil_filepath + self.bil_file + '.zip/' + self.bil_file + '.bil')
        if not ds is None:
            self.ncol = ds.RasterXSize
            self.nrow = ds.RasterYSize
            self.affine = Affine.from_gdal(*ds.GetGeoTransform())
#             self.pixelWidth = self.affine[1]
#             self.pixelHeight = self.affine[5]
            band = ds.GetRasterBand(1)
            self.nodatavalue = band.GetNoDataValue()
            self.data = band.ReadAsArray()
        else:
            print('cannot find file')
        return self.data

"""
Get county level value for PRISM daily data
df = zonal_county_value(yyyymmdd_start, yyyymmdd_end, var='ppt')
yyyymmdd_start = '19810101'
yyyymmdd_start = '20151231'
var = 'ppt', 'tdmean', 'tmax', 'tmin', 'vpdmax', 'vpdmin'
"""
# 05/04/2017
def zonal_county_value(yyyymmdd_start, yyyymmdd_end, var='ppt'):
    # Load shapefile and construct pandas frame 
    shape_fn = '../../US_county_gis/counties.shp'
    shapes = shpreader.Reader(shape_fn)
    county_fips = [i.attributes['FIPS'] for i in shapes.records()]

    fn_path = '../data/daily/' + var  + '/'

    time_range = pd.period_range(start=yyyymmdd_start, end=yyyymmdd_end, freq='D')
    df = pd.DataFrame(np.zeros([len(time_range), len(county_fips)]).fill(np.nan),
                      index=time_range, columns=county_fips)

    # zonal statistics for each day 
    for t in time_range:
        yyyymmdd = t.strftime('%Y%m%d')
        fn_path = '../data/daily/' + var  + '/' + t.strftime('%Y') + '/'
        fn = 'PRISM_%s_stable_4kmD2_%s_bil' %(var, yyyymmdd)
        bil = BilFile(fn_path, fn)

        print(t)
        zs = zonal_stats(shape_fn, bil.get_array(), nodata=bil.nodatavalue, affine=bil.affine)
    
        # save zonal results
        df.loc[t]=[i['mean'] for i in zs]
        # Save to csv at the end of each year
        if (t.dayofyear == 365) | (t.dayofyear == 366):
            print('save file at the end of year %s'%t.strftime('%Y'))
            df[t.strftime('%Y')].to_csv('../data/county_level/%s_daily_%s_county.csv'%(var, t.strftime('%Y')))

    return df

def main():
    day_start = '20000101'
   # day_start = '20151229'
    day_end = '20151231'
    var = 'ppt'
    df = zonal_county_value(day_start, day_end, var='ppt')
    print('done')
   # df.to_csv('../data/county_level/%s_%s_%s_county.csv'%(var, day_start, day_end))

if __name__ == '__main__':
    main()
