# -*- coding: utf-8 -*-
# 时间    : 2019/1/18 8:50
# 作者    : xcl

'''
功能介绍：
    1.批量导入监测站
    2.批量导入HDF文件
    3.批量计算个监测中AOD值
    4.经纬度计算距离
    5.计算程序耗时
    6.输出TXT文件
    7.程序完成后关机
新增：
    8.对指定区域,同日期,多文件的情况,增加了均值计算
'''

#因为采集AOD时会出现缺失值，因此计算范围内均值时会出现warnings
#导入以下库来忽略该warnings
import warnings
warnings.filterwarnings('ignore')
from math import radians, cos, sin, asin, sqrt#经纬度计算距离
import pandas as pd
import numpy as np
from pyhdf.SD import SD, SDC #批量导入HDF
import datetime#程序耗时
import os#关机,批量文件
import time#关机.耗时
#开始计算耗时
starttime = datetime.datetime.now()
#定义经纬度距离公式
def geodistance(lng1,lat1,lng2,lat2):
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    dlon=lng2-lng1
    dlat=lat2-lat1
    a=sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    dis=2*asin(sqrt(a))*6371.393*1000#地球半径
    return(dis)#输出结果的单位为“米”
#批量导入HDF文件
dir_str = r"C:\\Users\\Administrator\\Desktop\\MODIS\\HDF"
file_name = os.listdir(dir_str)
file_dir = [os.path.join(dir_str, x) for x in file_name]
#参数设置
#经纬度转换为的距离范围，监测站3KM半径范围内为观测区域
r = 3000
#批量导入监测站
JCZ_file = pd.read_excel("JCZ.xlsx")
JCZ = []
for i in range(len(JCZ_file)):
    JCZ1 = [JCZ_file["经度"][i],JCZ_file["纬度"][i],JCZ_file["城市"][i]+"-"+JCZ_file["监测点名称"][i]]
    exec('JCZ%s = [JCZ_file["经度"][i],JCZ_file["纬度"][i],JCZ_file["城市"][i]+"-"+JCZ_file["监测点名称"][i]]' %i)
    exec("JCZ.append(JCZ%s)" %i)
print("监测站总数",len(JCZ),"个")
#文件读取HDF文件
aod_outcome_list = []
for hdf in file_dir:
    HDF_FILR_URL = hdf
    file = SD(HDF_FILR_URL)
    # print(file.info())
    datasets_dic = file.datasets()
    '''
    #输出数据集名称
    for idx, sds in enumerate(datasets_dic.keys()):
        print(idx, sds)
    '''
    sds_obj1 = file.select('Longitude')  #选择经度
    sds_obj2 = file.select('Latitude')   #选择纬度
    sds_obj3 = file.select('Optical_Depth_Land_And_Ocean')  #AOD数据集,反演质量最高的AOD集;另一个质量低，覆盖区域多
    longitude = sds_obj1.get()  # 读取数据
    latitude = sds_obj2.get()
    aod = sds_obj3.get()
    longitude = pd.DataFrame(longitude) #格式转换
    latitude = pd.DataFrame(latitude)
    aod = pd.DataFrame(aod)
    for item in JCZ:
        aodlist = []
        #距离计算，获取监测站半径为r范围内的AOD值
        for i in range(longitude.shape[1]):  # 列
            for j in range(longitude.shape[0]):  # 行
                d = geodistance(longitude[i][j],latitude[i][j],item[0],item[1])
                if d > 0 and d < r and aod[i][j] > 0:
                    aodlist.append(aod[i][j])
        aod_outcome = "%s文件" % hdf,"%s文件" % hdf, "%s" % item[2], np.average(aodlist)
        print("完成 %s文件" % hdf,"%s" % item[2])
        aod_outcome_list.append(aod_outcome)
#创建AOD结果列表,剔除冗余信息
aod_outcome_list_v2 = []
for item in aod_outcome_list:
    item = pd.Series(item)#格式转换
    #替换掉冗余字符
    #设置文件列数据格式
    item[0] = item[0].replace("C:\\\\Users\\\\Administrator\\\\Desktop\\\\MODIS\\\\HDF", "")
    item[0] = item[0].replace("\\", "")
    item[0] = item[0].replace(".hdf文件", "")
    #设置日期列数据格式
    item[1] = item[1].replace("C:\\\\Users\\\\Administrator\\\\Desktop\\\\MODIS\\\\HDF", "")
    item[1] = item[1].replace("\\", "")
    item[1] = item[1].replace(".hdf文件", "")
    item[1] = item[1].replace("-1", "")
    item[1] = item[1].replace("-2", "")
    item[1] = item[1].replace("-3", "")
    item[1] = item[1].replace("-4", "")
    item[1] = item[1].replace("-5", "")
    item[1] = item[1].replace("-6", "")#一天内包含指定区域的文件,不会超过6个,目前最多见到的是4个。
    item = np.array(item)#格式转换
    aod_outcome_list_v2.append(item)
#避免输出结果字符串省略，四行设置都需要
pd.set_option('display.max_rows',None)#行
pd.set_option('display.max_columns',1000)#列
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)
#AOD结果写入TXT
aod_outcome_list_v2 = pd.DataFrame(aod_outcome_list_v2)#格式转换
#重设列名
aod_outcome_list_v2.columns = ['文件名', '日期', '监测站',"AOD值"]
#同日期，多文件情况下的均值处理
aod_outcome_list_v2 = aod_outcome_list_v2.groupby(['日期',"监测站"]).mean()
#获取列名
#print(aod_outcome_list_v2.columns.values.tolist())

#美化groupby均值计算后的数据框格式
aod_outcome_list_v2 =pd.Series(aod_outcome_list_v2["AOD值"])#AOD值按分组计算的结果
aod_outcome_list_v2.to_excel("AOD值提取结果.xlsx")#结果存入excel
#结果存入TXT
file=open('AOD值提取结果.txt','w')
file.write(str(aod_outcome_list_v2));
file.close()
#计算耗时结果
endtime = datetime.datetime.now()
print(endtime - starttime)
#程序用时写入TXT
file=open('程序耗时.txt','w')
file.write(str(endtime - starttime));
file.close()
#程序运行完成后关机
def shutdown_computer(seconds):
    print(str(seconds) + u' 秒后将会关机')
    time.sleep(seconds)
    print('关机')
    os.system('shutdown -s -f -t 1')
#shutdown_computer(60)