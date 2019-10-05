# -*- coding: utf-8 -*-
# 日期: 2019/3/19 23:25
# 作者: xcl
# 工具：PyCharm

import warnings
from math import radians, cos, sin, asin, sqrt  # 经纬度计算距离
import pandas as pd  # BDS
import numpy as np  # BDS
from pyhdf.SD import SD  # 批量导入HDF
import datetime  # 程序耗时
import os  # 关机,批量文件
import time  # 关机
from numba import jit
warnings.filterwarnings('ignore')
# 开始计算耗时
start_time = datetime.datetime.now()


# 定义经纬度距离公式
@jit
def geo_distance(lng1, lat1, lng2, lat2):
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    d_lon = lng2 - lng1
    d_lat = lat2 - lat1
    a = sin(d_lat/2)**2 + cos(lat1) * cos(lat2) * sin(d_lon/2)**2
    dis = 2*asin(sqrt(a))*6371.393*1000  # 地球半径
    return dis  # 输出结果的单位为“米”


# 参数设置
r = 7500   # 参照文献;经纬度转换为的距离范围,监测站3KM半径范围内为观测区域
file_path = "F:\\MODIS DATA\\modis04_3km_T_2017\\"  # HDF文件位置 TTT
output_file_path = "F:\\毕业论文程序\\气溶胶光学厚度\\Terra\\2017\\"  # 结果的输出位置
JCZ_file = pd.read_excel("F:\\毕业论文程序\\MODIS\\坐标\\监测站坐标.xlsx")

JCZ = []
# 批量导入监测站
for i in range(len(JCZ_file)):
    exec('JCZ%s = [JCZ_file["经度"][i],JCZ_file["纬度"][i],JCZ_file["城市"][i]+"-"+JCZ_file["监测点名称"][i]]' % i)
    exec("JCZ.append(JCZ%s)" % i)  # exec可以执行字符串指令


# 批量读取HDF文件,提取AOD值,并将结果添加到列表中
file_name = os.listdir(file_path)  # 文件名
print("监测站总数:", len(JCZ), "文件总数:", len(file_name))
'''
aod_outcome_list = []#输出到一个文件时
'''
i = 0
for item in JCZ:
    aod_outcome_list = []  # 每个监测站生成一个文件时
    j = 0
    for hdf in file_name:
        i = i + 1
        j = j + 1
        HDF_FILE_URL = file_path + hdf
        file = SD(HDF_FILE_URL)
        data_sets_dic = file.datasets()
        '''
        #输出数据集名称
        for idx, sds in enumerate(data_sets_dic.keys()):
            print(idx, sds)
        '''
        sds_obj1 = file.select('Longitude')  # 选择经度
        sds_obj2 = file.select('Latitude')  # 选择纬度
        sds_obj3 = file.select('Optical_Depth_Land_And_Ocean')  # 产品质量最高的AOD数据集
        longitude = sds_obj1.get()  # 读取数据
        latitude = sds_obj2.get()
        aod = sds_obj3.get()
        longitude = np.array(longitude)  # 格式转换
        latitude = np.array(latitude)
        aod = np.array(aod)
    # 距离计算，提取监测站半径为r范围内的AOD值
        aod_list = []

        @jit(nogil=True)
        # 此次,numpy切片的检索顺序是先"行"后"列"
        def get_aod_list(longitude_df, latitude_df, aod_df):
            for row in range(longitude_df.shape[0]):  # 行 676
                for column in range(longitude_df.shape[1]):  # 列 451
                    d = geo_distance(longitude_df[row][column], latitude_df[row][column], item[0], item[1])
                    if (d > 0) and (d < r) and aod_df[row][column] > 0:
                        aod_list.append(aod_df[row][column])
        get_aod_list(longitude, latitude, aod)
        aod_outcome = "%s文件" % hdf, "%s" % item[2], np.average(aod_list)
        # 进度
        print("完成 %s文件" % hdf, "%s" % item[2], "监测站进度:%.2f%%" % (j/len(file_name)*100),
              "总进度:%.2f%%" % (100*i/(len(JCZ)*len(file_name))))
        aod_outcome_list.append(aod_outcome)

    aod_outcome_list_v2 = []
    for element in aod_outcome_list:
        element = pd.Series(element)  # 格式转换
        # 截取文件名称,结果为获取数据的时间,格式为"年+第几天"
        element[0] = str(element[0])[10:17]  # 如2018123
        # 修改日期格式为XX月XX日
        element[0] = time.strptime(element[0], '%Y%j')
        element[0] = time.strftime("%Y-%m-%d ", element[0])
        element = np.array(element)  # 格式转换
        aod_outcome_list_v2.append(element)
    # 避免输出结果字符串省略，四行设置都需要
    pd.set_option('display.max_rows', None)  # 行
    pd.set_option('display.max_columns', 1000)  # 列
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)
    aod_outcome_list_v2 = pd.DataFrame(aod_outcome_list_v2)  # 格式转换
    # 重设列名
    aod_outcome_list_v2.columns = ['日期', '监测站', "AOD值"]
    # 同日期，多文件情况下的均值处理
    aod_outcome_list_v2 = aod_outcome_list_v2.groupby(['日期', "监测站"]).mean()
    # 美化group by均值计算后的数据框格式
    aod_outcome_list_v2 = pd.Series(aod_outcome_list_v2["AOD值"])  # AOD值按分组计算的结果
    aod_outcome_list_v2.to_excel(output_file_path+"%s.xlsx" % item[2])  # 完整结果存入excel

# 程序用时写入文件
file = open('程序耗时.txt', 'w')
end_time = datetime.datetime.now()
file.write(str(end_time - start_time))
file.close()


# 程序运行完成后关机
def shutdown_computer(seconds):
    print("程序已完成," + str(seconds) + '秒后将会关机')
    time.sleep(seconds)
    print('关机')
    os.system('shutdown -s -f -t 1')


# shutdown_computer(60)
