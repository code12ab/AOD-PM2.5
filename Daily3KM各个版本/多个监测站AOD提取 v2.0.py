# -*- coding: utf-8 -*-
# 时间    : 2019/1/17 15:06
# 作者    : xcl

'''
功能介绍：
    1.批量导入监测站
    2.批量导入HDF文件
    3.批量计算个监测中AOD值
    4.经纬度计算距离
    5.计算程序耗时
    6.输出Excel、TXT文件
    7.程序完成后关机
    8.对指定区域,同日期,多文件的情况,增加了均值计算
    9.使用批量下载的文件
    10.文件名的天数转换为日期
    11.输出结果按日期,再按监测站排序
备注：
    所有结果输出在一个excel,中途输出问题导致前面白白耗费时间,且文件格式不理想,有待改进
'''

#因为采集AOD时会出现缺失值，因此计算r范围内均值时会出现warnings
#导入以下库来忽略该warnings
import warnings
warnings.filterwarnings('ignore')
from math import radians, cos, sin, asin, sqrt#经纬度计算距离
import pandas as pd #BDS
import numpy as np #BDS
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
#参数设置
r = 7500 #经纬度转换为的距离范围，监测站3KM半径范围内为观测区域
file_path = "E:\\modis04_3km_1\\" #HDF文件位置

#批量导入监测站
JCZ_file = pd.read_excel("监测站坐标.xlsx")
JCZ = []
for i in range(len(JCZ_file)):
    exec('JCZ%s = [JCZ_file["经度"][i],JCZ_file["纬度"][i],JCZ_file["城市"][i]+"-"+JCZ_file["监测点名称"][i]]' %i)
    exec("JCZ.append(JCZ%s)" %i) #exec可以执行字符串指令


#批量读取HDF文件,提取AOD值,并将结果添加到列表中
file_name = os.listdir(file_path)#文件名

print("监测站总数:",len(JCZ),"文件总数:",len(file_name))
aod_outcome_list = []
for hdf in file_name:
    HDF_FILR_URL =  file_path + hdf
    file = SD(HDF_FILR_URL)
    datasets_dic = file.datasets()
    '''
    #输出数据集名称
    for idx, sds in enumerate(datasets_dic.keys()):
        print(idx, sds)
    '''
    sds_obj1 = file.select('Longitude')  #选择经度
    sds_obj2 = file.select('Latitude')   #选择纬度
    sds_obj3 = file.select('Optical_Depth_Land_And_Ocean')  #产品质量最高的AOD数据集
    longitude = sds_obj1.get()  # 读取数据
    latitude = sds_obj2.get()
    aod = sds_obj3.get()
    longitude = pd.DataFrame(longitude) #格式转换
    latitude = pd.DataFrame(latitude)
    aod = pd.DataFrame(aod)
    for item in JCZ:
        aodlist = []
        #距离计算，提取监测站半径为r范围内的AOD值
        for i in range(longitude.shape[1]):  # 列
            for j in range(longitude.shape[0]):  # 行
                d = geodistance(longitude[i][j],latitude[i][j],item[0],item[1])
                if d > 0 and d < r and aod[i][j] > 0:
                    aodlist.append(aod[i][j])
        aod_outcome = "%s文件" % hdf, "%s" % item[2], np.average(aodlist)
        print("完成 %s文件" % hdf,"%s" % item[2])
        aod_outcome_list.append(aod_outcome)
#创建AOD结果列表,剔除冗余信息
aod_outcome_list_v2 = []
for item in aod_outcome_list:
    item = pd.Series(item)#格式转换
    # 截取文件名称,结果为获取数据的时间,格式为"年+第几天"
    item[0] = str(item[0])[10:17]
    # 修改日期格式为XX月XX日 #
    item[0] = float(str(time.strptime(item[0],'%Y%j')[1])+"."+str(time.strptime(item[0], '%Y%j')[2]))
    item = np.array(item)#格式转换
    aod_outcome_list_v2.append(item)

#避免输出结果字符串省略，四行设置都需要
pd.set_option('display.max_rows',None)#行
pd.set_option('display.max_columns',1000)#列
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)

aod_outcome_list_v2 = pd.DataFrame(aod_outcome_list_v2)#格式转换
#重设列名
aod_outcome_list_v2.columns = ['日期', '监测站',"AOD值"]
#同日期，多文件情况下的均值处理
aod_outcome_list_v2 = aod_outcome_list_v2.groupby(['日期',"监测站"]).mean()
#美化groupby均值计算后的数据框格式
aod_outcome_list_v2 =pd.Series(aod_outcome_list_v2["AOD值"])#AOD值按分组计算的结果
aod_outcome_list_v2.to_excel("AOD值提取结果.xlsx")#完整结果存入excel

#程序用时写入TXT
file=open('程序耗时.txt','w')
endtime = datetime.datetime.now()
file.write(str(endtime - starttime))
file.close()

#程序运行完成后关机
def shutdown_computer(seconds):
    print("程序已完成,"+ str(seconds) + '秒后将会关机')
    time.sleep(seconds)
    print('关机')
    os.system('shutdown -s -f -t 1')
#shutdown_computer(60)