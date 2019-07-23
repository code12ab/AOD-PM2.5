# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/7/15 13:02

from multiprocessing import Process  # 多线程,提高CPU利用率
import warnings
from math import radians, cos, sin, asin, sqrt  # 经纬度计算距离
import pandas as pd  # BDS
import numpy as np  # BDS
from pyhdf.SD import SD  # 批量导入HDF
import datetime  # 程序耗时
import os  # 关机,批量文件
import time  # 关机
from numba import jit

'''
多线程 + 函数定义置于循环外
自动关机雏形已建立
'''

warnings.filterwarnings('ignore')  # 忽略"number/0"的情况
# 开始计算耗时
start_time = datetime.datetime.now()


HDF_FILE_URL = 'MYD13A2.A2015201.h26v05.006.2015304025556.hdf'
file = SD(HDF_FILE_URL)

data_sets_dic = file.datasets()
#输出数据集名称
for idx in enumerate(data_sets_dic.keys()):
    print(idx)

'''
sds_obj1 = file.select('Longitude')  # 选择经度
sds_obj2 = file.select('Latitude')  # 选择纬度
sds_obj3 = file.select('Optical_Depth_Land_And_Ocean')  # 产品质量最高的AOD数据集
longitude = sds_obj1.get()  # 读取数据
latitude = sds_obj2.get()
aod = sds_obj3.get()
'''

sds_obj1 = file.select('1 km 16 days view zenith angle')  # 选择经度

data = sds_obj1.get()
print(data.shape)

print(data)
print(np.max(data))