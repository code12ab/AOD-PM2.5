# -*- coding: utf-8 -*-
# 时间    : 2019/1/17 9:23
# 作者    : xcl



'''
                            批量添加监测站
                            增加经纬度计算距离
                            忽略空列表计算均值而产生的warnings
'''

#因为采集AOD时会出现缺失值，因此计算范围内均值时会出现warnings
#导入以下库来忽略该warnings
import warnings
warnings.filterwarnings('ignore')
#相关库
from math import radians, cos, sin, asin, sqrt
#import xlwt
import pandas as pd
import numpy as np
from pyhdf.SD import SD, SDC
# #import pprint
import datetime

#计算耗时
starttime = datetime.datetime.now()
#定义经纬度距离公式
def geodistance(lng1,lat1,lng2,lat2):
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    dlon=lng2-lng1
    dlat=lat2-lat1
    a=sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    dis=2*asin(sqrt(a))*6371*1000
    return(dis)

import os
dir_str = r"C:\\Users\\Administrator\\Desktop\\MODIS\\HDF"
file_name = os.listdir(dir_str)
file_dir = [os.path.join(dir_str, x) for x in file_name]
#print(file_dir)#,file_name)

#outcome = "C:\\Users\\Administrator\\Desktop\\MODIS\\outcome.xlsx"
file_handle=open('1.txt',mode='a+')

#参数设置
#经纬度转换为的距离范围，监测站3KM半径范围内为观测区域
r = 3000
#监测站
JCZ_file = pd.read_excel("JCZ.xlsx")
JCZ = []
for i in range(len(JCZ_file)):
    JCZ1 = [JCZ_file["经度"][i],JCZ_file["纬度"][i],JCZ_file["城市"][i]+"-"+JCZ_file["监测点名称"][i]]
    exec('JCZ%s = [JCZ_file["经度"][i],JCZ_file["纬度"][i],JCZ_file["城市"][i]+"-"+JCZ_file["监测点名称"][i]]' %i)
    exec("JCZ.append(JCZ%s)" %i)
print("监测站总数",len(JCZ),"个")
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
                d = geodistance(longitude[i][j],latitude[i][j],item[0],item[1])
                '''
                #方法二，弃用
                vec1 = np.array([longitude[i][j], latitude[i][j]])
                vec2 = np.array([item[0], item[1]])
                d = np.linalg.norm(vec1 - vec2)# 欧式距离
                #d = ((longitude[i][j]) - item[0])** 2 + ((latitude[i][j]) - item[1]) ** 2 # 欧式距离
                '''
                if d > 0 and d < r and aod[i][j] > 0:
                    aodlist.append(aod[i][j])
        #print("%s文件的%s监测站AOD值:" % (hdf,item[2]), np.average(aodlist))  # 批量改名，一次输出
        aod_outcome = "%s文件" % hdf,"%s" % item[2], np.average(aodlist)
        print("完成 %s文件" % hdf,"%s" % item[2])
        aod_outcome_list.append(aod_outcome)
#print(aod_outcome_list)#结果查看
aod_outcome_list_v2 = []
for item in aod_outcome_list:
    item = pd.Series(item)
    #替换掉冗余字符
    item[0] = item[0].replace("C:\\\\Users\\\\Administrator\\\\Desktop\\\\MODIS\\\\HDF", "")
    item[0] = item[0].replace("\\", "")
    item[0] = item[0].replace(".hdf文件", "")
    item = np.array(item)
    aod_outcome_list_v2.append(item)
#避免字符串省略，四行设置都需要
pd.set_option('display.max_rows',None)#行
pd.set_option('display.max_columns',1000)#列
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)

#写入TXT
aod_outcome_list_v2 = pd.DataFrame(aod_outcome_list_v2)
aod_outcome_list_v2.columns = ['日期', '监测站', 'AOD值']
file=open('data.txt','w')
file.write(str(aod_outcome_list_v2));
file.close()
# 计算所用时间
endtime = datetime.datetime.now()
print(endtime - starttime)

file=open('TIME.txt','w')
file.write(str(endtime - starttime));
file.close()





#运行完关机

import os
import time


def shutdown_computer(seconds):
    print(str(seconds) + u' 秒后将会关机...')
    time.sleep(seconds)
    print('关机啦。。。')
    os.system('shutdown -s -f -t 1')

shutdown_computer(60)