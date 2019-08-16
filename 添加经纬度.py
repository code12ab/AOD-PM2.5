# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/7 11:10


# 库
from multiprocessing import Process  # 多线程,提高CPU利用率
import copy
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import numpy as np
import os

# 思路
# K循环 插补 去 参数b

# 库
from multiprocessing import Process  # 多线程,提高CPU利用率
import warnings
from math import radians, cos, sin, asin, sqrt, degrees, atan2  # 经纬度计算距离
import pandas as pd  # BDS
import numpy as np  # BDS
from pyhdf.SD import SD  # 批量导入HDF
import datetime  # 程序耗时
import os  # 关机,批量文件
import time  # 关机
from numba import jit
import os
import numpy as np
from osgeo import gdal
import glob
import gdal
import pandas as pd
from pandas import DataFrame
#首先读取tif文件
path = r"D:\DATA\try.tif"
hdf = "C:\\Users\\iii\\Desktop\\MYD13A2.A2019121.h26v03.006.2019137234541.hdf"

dataset = gdal.Open(hdf)
im_width = dataset.RasterXSize;#获取宽度
im_height = dataset.RasterYSize;#获取长度


data1 = dataset.ReadAsArray(0,0,im_width,im_height)  #读取ndvi时序数据，三维矩阵

# print(dir(dataset))
# print(dataset.GetMetadata_List())



in_ds = gdal.Open(hdf)
datasets = in_ds.GetSubDatasets()
gdal.Warp('D:/reprojection02.tif', datasets[0][0], dstSRS='EPSG:4326')   # 等经纬度投影
# print(datasets[0][0])  # 1 km 16 days NDVI
root_ds = None



list_tif = glob.glob('D:\data\*.tif')
out_path = 'D:/'

for tif in list_tif:
    in_ds = gdal.Open(tif)
    (filepath, fullname) = os.path.split(tif)
    (prename, suffix) = os.path.splitext(fullname)

    if in_ds is None:
        print('Could not open the file ' + tif)
    else:
        # 将MODIS原始数据类型转化为反射率
        red = in_ds.GetRasterBand(1).ReadAsArray() * 0.0001  # 1km ndvi 转化
        print(red)
        print(dir(in_ds))

        print(in_ds.RasterXSize)



from osgeo import gdal

gdal.AllRegister()
dataset = gdal.Open('D:\\reprojection02.tif')

adfGeoTransform = dataset.GetGeoTransform()

# 左上角地理坐标
print(adfGeoTransform[0])
print(adfGeoTransform[3])

nXSize = dataset.RasterXSize #列数
nYSize = dataset.RasterYSize #行数

arrSlope = [] # 用于存储每个像素的（X，Y）坐标
for i in range(nYSize):
    row = []
    for j in range(nXSize):
        px = adfGeoTransform[0] + i * adfGeoTransform[1] + j * adfGeoTransform[2]
        py = adfGeoTransform[3] + i * adfGeoTransform[4] + j * adfGeoTransform[5]
        col = [px, py]
        row.append(col)
    arrSlope.append(row)

#  print(len(arrSlope))

arrSlope = pd.DataFrame(arrSlope)
arrSlope.to_excel("xy.xlsx")
