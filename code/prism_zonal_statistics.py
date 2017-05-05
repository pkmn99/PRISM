# use mygeo enviroment for local machine
# zonal statistics to covert prism data to US county mean 
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
    # shape_fn = '../data/US_county_gis/counties.shp'
    # Load shapefile and construct pandas frame 
    shape_fn = '../../US_county_gis/counties.shp'
    shapes = shpreader.Reader(shape_fn)
    county_fips = [i.attributes['FIPS'] for i in shapes.records()]
    df = pd.DataFrame({'FIPS': county_fips})

    fn_path = '../data/daily/' + var  + '/'

    time_range = pd.period_range(start=yyyymmdd_start, end=yyyymmdd_end, freq='D')

    # zonal statistics for each day 
    for t in time_range:
        yyyymmdd = t.strftime('%Y%m%d')
        fn_path = '../data/daily/' + var  + '/' + t.strftime('%Y') + '/'
        fn = 'PRISM_%s_stable_4kmD2_%s_bil' %(var, yyyymmdd)
        bil = BilFile(fn_path, fn)
        print(t)
#         zs = my_zonal_statistics(shape_fn, bil.get_array(), bil.nodatavalue, bil.affine)
        zs = zonal_stats(shape_fn, bil.get_array(), nodata=bil.nodatavalue, affine=bil.affine)
    
        # save zonal results as one column of df
        df[t]=[i['mean'] for i in zs]
        
    return df

def main():
    df = zonal_county_value('20000101', '20151231', var='ppt')
    print('OK')

if __name__ == '__main__':
    main()
