import os.path
import warnings
warnings.filterwarnings("ignore")
import numpy as np 
import scipy.io as sio
import piecewise_regression.davies as davies
from osgeo import gdal
from time import time
from tqdm import trange
from datetime import datetime
from pathlib import Path


datapth = r'.\Houston'

savepth = r'.\Houston'

city_name = "Houston"


start_time=time()
ts_filename= r"timeseries_clipped.tif"
print(os.path.join(datapth,ts_filename))

dataset = gdal.Open(os.path.join(datapth,ts_filename))
im_width = dataset.RasterXSize  
im_height = dataset.RasterYSize 
ts = dataset.ReadAsArray(0,0,im_width,im_height).transpose(1,2,0)*1000  # m to mm
del dataset
print(f"Read {ts_filename} done in {time()-start_time:.2f} seconds, image size: {ts.shape}")

date_filename= r"dates.mat"
dates=sio.loadmat(os.path.join(datapth,date_filename))
dates=dates['remainDate']

def date_to_decimal_year(date_str):
    date = datetime.strptime(date_str, '%Y%m%d')
    day_of_year = date.timetuple().tm_yday
    days_in_year = 365+(date.year%4==0)
    decimal_year = date.year + day_of_year  / days_in_year
    return decimal_year

x=np.array([date_to_decimal_year(date_str) for date_str in dates])

row_size=ts.shape[0]
col_size=ts.shape[1]

change_point_par_Pvalue=np.full((row_size, col_size), np.nan)
for i in trange(row_size):
    for j in range(col_size):
        y = ts[i,j,:]
        if np.sum(np.abs(y))==0:
            continue

        change_point_par_Pvalue[i,j] = davies.davies_test(x,y)
change_point_par_Fflag=change_point_par_Pvalue<0.05
print(f"Change point detection done in {time()-start_time:.2f} seconds")
sio.savemat(os.path.join(savepth,city_name+"_davies_test.mat"), {'change_point_par_Fflag': change_point_par_Fflag,
                                'change_point_par_Pvalue': change_point_par_Pvalue})


