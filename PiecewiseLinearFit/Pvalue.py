import warnings
warnings.filterwarnings("ignore")
import numpy as np 
import scipy.io as sio
from multiprocessing import Pool,Array
import piecewise_regression.davies as davies

from osgeo import gdal
from time import time
from tqdm import trange
from datetime import datetime
from pathlib import Path

start_time=time()
city_name="AUS_409_Melbourne"
ts_filename=city_name+"/timeseries_f32.tif"
dataset = gdal.Open(ts_filename)
im_width = dataset.RasterXSize  
im_height = dataset.RasterYSize  
ts = dataset.ReadAsArray(0,0,im_width,im_height).transpose(1,2,0)
del dataset  
print(f"Read {ts_filename} done in {time()-start_time:.2f} seconds, image size: {ts.shape}")

date_filename=city_name+"/dates.mat"
dates=sio.loadmat(date_filename)
dates=dates['remainDate']

def date_to_decimal_year(date_str):    
    date = datetime.strptime(date_str, '%Y%m%d')
    day_of_year = date.timetuple().tm_yday    
    days_in_year = 365+(date.year%4==0)
    decimal_year = date.year + day_of_year  / days_in_year    
    return decimal_year

x=np.array([date_to_decimal_year(date_str) for date_str in dates])
# min_dist=np.sum((x[0]+1)>=x).item()/x.shape[0]
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
sio.savemat(city_name+"/davies_test.mat", {'change_point_par_Fflag': change_point_par_Fflag,
                                'change_point_par_Pvalue': change_point_par_Pvalue})
