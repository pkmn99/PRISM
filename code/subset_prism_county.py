"""
Extract a subset of prism data based on state fips
"""
#05/18/17

from os.path import basename
import numpy as np
import pandas as pd

my_fips = '17'
#state_fips = pd.read_csv('../../US_county_gis/state_fips.csv')

source_path = '../data/county_level/'
out_path = source_path + '/subset/'
#var = ['ppt', 'tmax', 'tmin']
var = ['ppt']

#tmin_daily_2014_county.csv
for v in var:
    for y in range(1981, 1987):
        print('Extracting var:%s for year %s'%(v,y)) 
        fn = v + '_daily_' + str(y) + '_county'
        data = pd.read_csv(source_path + fn + '.csv', index_col=0)
        data.loc[:,data.columns.str.startswith(my_fips)].to_csv(out_path+fn+'_fips'+my_fips+'.csv')

