# -*- coding: utf-8 -*-
# 时间    : 2019/1/15 10:19
# 作者    : xcl


'''

                              本文件可进行多个监测站的AOD值计算

'''

import math
import pandas as pd
import xlwt
import pandas as pd
import numpy as np
from pyhdf.SD import SD, SDC
import pprint

import datetime
starttime = datetime.datetime.now()
#long running
#do something other


# 文件读取
HDF_FILR_URL = "1011-1.hdf"
file = SD(HDF_FILR_URL)
# print(file.info())
datasets_dic = file.datasets()
'''
for idx, sds in enumerate(datasets_dic.keys()):
    print(idx, sds)
'''
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
# print(aod.shape,aod.info()) #矩阵大小
'''
#print(aod[450][650])#先列后行
'''
#监测站 坐标设置
#北京
JCZ1 = [116.366,39.8673]
JCZ2 = [116.170,40.2865]
JCZ3 = [116.434,39.9522]
JCZ4 = [116.434,39.8745]
JCZ5 = [116.473,39.9716]
JCZ6 = [116.361,39.9425]
JCZ7 = [116.315,39.9934]
JCZ8 = [116.720,40.1438]
JCZ9 = [116.644,40.3937]
JCZ10= [116.230,40.1952]
JCZ11= [116.407,40.0031]
JCZ12= [116.225,39.9279]

JCZ = [JCZ1,JCZ2,JCZ3,JCZ4,JCZ5,JCZ6,JCZ7,JCZ8,JCZ9,JCZ10,JCZ11,JCZ12]#JCZ13,JCZ14]
# AOD输出
# 计算平均数

def averagenum(num):
    nsum = 0
    for i in range(len(num)):
        nsum += num[i]
    return nsum / len(num)




for item in JCZ:
    aodlist = []
    for i in range(longitude.shape[1]):  # 列
        for j in range(longitude.shape[0]):  # 行
            d = ((longitude[i][j]) - item[0]) ** 2 + (latitude[i][j]-item[1])** 2 # 距离
            if d > 0 and d < 0.7744 and aod[i][j] > 0:
                aodlist.append(aod[i][j])
    print("%s监测站" %item,averagenum(aodlist))#批量改名

'''
for i in range(longitude.shape[1]):  # 列
    for j in range(longitude.shape[0]):  # 行
        for item in JCZ:
            d = ((longitude[i][j]) ** 2 - item[0] ** 2 + (latitude[i][j]) ** 2 - item[1] ** 2)  # 距离
            if d > 0 and d < 0.7744 and aod[i][j] > 0:
                aodlist.append(aod[i][j])
print(aodlist)
            #print("第一个监测站AOD：", averagenum(aodlist))
'''

endtime = datetime.datetime.now()
print(endtime - starttime)
