""" Download PRISM data from FTP to current dir.
PRISM data is for Recent Years (Jan 1981 - Sep 2016)

Usage::
download_prism(var, time_scale, start_year, end_year)
time_scale: 'daily' or 'monthly' 
var: 'ppt','tdmin', 'tmax', 'tmin', 'vpdmax', 'vpdmin'
start_year: 1981 ~ 2016
end_year: 1981 ~ 2016
source: http://www.prism.oregonstate.edu/recent/
04/20/2017
"""
import ftplib
import os

def download_prism(var, time_scale, start_year, end_year):

    print ('Download PRISM %s %s from %d to %d' %(time_scale, var, start_year, end_year))
    print ('Create folder %s/%s in destination dir if not exist'%(time_scale, var))
    os.chdir('../data/')
    
    currdir=os.getcwd()
    path = '%s/%s/'%(time_scale,var)
    
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)
    
    print ('Connect to PRISM FTP')
    ftp = ftplib.FTP('prism.nacse.org') 
    ftp.login()
    ftp.cwd('%s/%s/' %(time_scale, var))
    
    for y in range(start_year, end_year):
        # Create year folder
        if not os.path.exists(str(y)):
            os.makedirs(str(y))
        os.chdir(str(y))
        print('Downloading data for Year %d'%y)
        ftp.cwd('%d/' %y)
        fn_list = ftp.nlst()
        fn_list.sort()
        for fn in fn_list:
            print(fn)
            ftp.retrbinary("RETR " + fn ,open(fn, 'wb').write)
        ftp.cwd('../')
        os.chdir('../')
    
    print('Download complete, close FTP connection')
    ftp.quit()
    os.chdir(currdir)

def main():
    time_scale = 'monthly' 
    start_year = 1981
    end_year = 2016
   # download_prism('ppt', time_scale, start_year, end_year)
    download_prism('tmax', time_scale, start_year, end_year)
    download_prism('tmin', time_scale, start_year, end_year)
    download_prism('tdmin', time_scale, start_year, end_year)
    download_prism('vpdmax', time_scale, start_year, end_year)
    download_prism('vpdmin', time_scale, start_year, end_year)

if __name__ == "__main__":
    main()
