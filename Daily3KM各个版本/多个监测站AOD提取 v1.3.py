#import math
#import xlwt
import pandas as pd
import numpy as np
from pyhdf.SD import SD, SDC
# #import pprint
import datetime

#计算耗时
starttime = datetime.datetime.now()

import os
dir_str = r"C:\\Users\\Administrator\\Desktop\\MODIS\\HDF"
file_name = os.listdir(dir_str)
file_dir = [os.path.join(dir_str, x) for x in file_name]
#print(file_dir)#,file_name)

outcome = "C:\\Users\\Administrator\\Desktop\\MODIS\\outcome.xlsx"
file_handle=open('1.txt',mode='a+')

JCZ1 = [116.366,39.8673,"万寿西宫"]
JCZ2 = [116.170,40.2865,"定陵"]
JCZ3 = [116.434,39.9522,"东四"]
JCZ4 = [116.434,39.8745,"天坛"]
JCZ5 = [116.473,39.9716,"农展馆"]
JCZ6 = [116.361,39.9425,"官园"]
JCZ7 = [116.315,39.9934,"海淀区万柳"]
JCZ8 = [116.720,40.1438,"顺义新城"]
JCZ9 = [116.644,40.3937,"怀柔区"]
JCZ10= [116.230,40.1952,"昌平区"]
JCZ11= [116.407,40.0031,"奥体中心"]
JCZ12= [116.225,39.9279,"古城"]

JCZ = [JCZ1,JCZ2,JCZ3,JCZ4,JCZ5,JCZ6,JCZ7,JCZ8,JCZ9,JCZ10,JCZ11,JCZ12]#JCZ13,JCZ14]
# 文件读取

aod_outcome_list = []
for hdf in file_dir:
    HDF_FILR_URL = hdf
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
    longitude = pd.DataFrame(longitude)
    latitude = pd.DataFrame(latitude)
    aod = pd.DataFrame(aod)
    for item in JCZ:
        aodlist = []
        for i in range(longitude.shape[1]):  # 列
            for j in range(longitude.shape[0]):  # 行
                vec1 = np.array([longitude[i][j], latitude[i][j]])
                vec2 = np.array([item[0], item[1]])
                d = np.linalg.norm(vec1 - vec2)
                # d = ((longitude[i][j]) ** 2 - item[0] ** 2 + (latitude[i][j]) ** 2 - item[1] ** 2)  # 距离，公式有误
                if d > 0 and d < 0.88 and aod[i][j] > 0:
                    aodlist.append(aod[i][j])
        #print("%s文件的%s监测站AOD值:" % (hdf,item[2]), np.average(aodlist))  # 批量改名，一次输出
        aod_outcome = "%s文件" % hdf,"%s监测站AOD值" % item[2], np.average(aodlist)
        aod_outcome_list.append(aod_outcome)
print(aod_outcome_list)

#避免字符串省略，四行设置都需要
pd.set_option('display.max_rows',None)#行
pd.set_option('display.max_columns',1000)#列
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)

#写入TXT
aod_outcome_list = pd.DataFrame(aod_outcome_list)
file=open('data.txt','w')
file.write(str(aod_outcome_list));
file.close()
# 计算所用时间
endtime = datetime.datetime.now()
print(endtime - starttime)
'''
                                        批量处理多个HDF文件,尝试写入excel or txt
'''

