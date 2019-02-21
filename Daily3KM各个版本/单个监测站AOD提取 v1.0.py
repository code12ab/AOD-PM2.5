# -*- coding: utf-8 -*-
# 时间    : 2019/1/15 9:04
# 作者    : xcl


'''

                              本文件可进行一个监测站的AOD值计算

'''

import math
import pandas as pd
import xlwt
import pandas as pd
import numpy as np
from pyhdf.SD import SD, SDC
import pprint

#文件读取
HDF_FILR_URL = "1001-1.hdf"
file = SD(HDF_FILR_URL)
#print(file.info())
datasets_dic = file.datasets()

for idx, sds in enumerate(datasets_dic.keys()):
    print(idx, sds)

sds_obj1 = file.select('Longitude')  # select sds
sds_obj2 = file.select('Latitude')  # select sds
sds_obj3 = file.select('Optical_Depth_Land_And_Ocean')  # select sds
longitude = sds_obj1.get()  # get sds data
latitude = sds_obj2.get()  # get sds data
aod = sds_obj3.get()  # get sds data

# 参数设置
longitude = pd.DataFrame(longitude)
latitude = pd.DataFrame(latitude)
aod = pd.DataFrame(aod)
#print(aod.shape,aod.info()) #矩阵大小
'''
#print(aod[450][650])#先列后行
'''
JCZ1 = [116.473,39.9716]

#AOD输出
aodlist = []
for i in range(longitude.shape[1]):#列
    for j in range(longitude.shape[0]):#行
        d = ((longitude[i][j]) ** 2 - JCZ1[0] ** 2 + (latitude[i][j]) ** 2 - JCZ1[1] ** 2)  # 距离
        if d > 0 and d < 0.7 and aod[i][j] > 0:
            aodlist.append(aod[i][j])

#计算平均数
def averagenum(num):
    nsum = 0
    for i in range(len(num)):
        nsum += num[i]
    return nsum / len(num)

print("第一个监测站AOD：",averagenum(aodlist))