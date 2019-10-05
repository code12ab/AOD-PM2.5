# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/7/15 13:02


import warnings
from math import radians, cos, sin, asin, sqrt  # 经纬度计算距离
import math
import pandas as pd  # BDS
import numpy as np  # BDS
from pyhdf.SD import SD  # 批量导入HDF
import datetime  # 程序耗时
import os  # 关机,批量文件
import time  # 关机
from numba import jit

warnings.filterwarnings('ignore')  # 忽略"number/0"的情况
# 开始计算耗时
start_time = datetime.datetime.now()
# 参数设置
# 定义 三个距离范围
dis1 = 8000
dis2 = 20000
dis3 = 50000


# 定义经纬度距离公式
@jit
def geo_distance(lng1, lat1, lng2, lat2):
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    d_lon = lng2 - lng1
    d_lat = lat2 - lat1
    a = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
    dis = 2 * asin(sqrt(a)) * 6371.393 * 1000  # 地球半径
    return dis  # 输出结果的单位为“米”


# 计算方位角函数
@jit
def azimuthAngle(x1, y1, x2, y2):
    angle = 0.0
    dx = x2 - x1
    dy = y2 - y1
    if x2 == x1:
        angle = math.pi / 2.0
        if y2 == y1:
            angle = 0.0
        elif y2 < y1:
            angle = 3.0 * math.pi / 2.0
    elif x2 > x1 and y2 > y1:
        angle = math.atan(dx / dy)
    elif x2 > x1 and y2 < y1:
        angle = math.pi / 2 + math.atan(-dy / dx)
    elif x2 < x1 and y2 < y1:
        angle = math.pi + math.atan(dx / dy)
    elif x2 < x1 and y2 > y1:
        angle = 3.0 * math.pi / 2.0 + math.atan(dy / -dx)
    return (angle * 180 / math.pi)


@jit(nogil=True)
# 此次,numpy切片的检索顺序是先"行"后"列"
def get_aod_list(longitude_df, latitude_df, aod_df, item_df1, item_df2):
    a0_list = []
    a1_list = []
    a2_list = []
    a3_list = []
    a4_list = []
    a5_list = []
    a6_list = []
    a7_list = []
    a8_list = []
    b1_list = []
    b2_list = []
    b3_list = []
    b4_list = []
    b5_list = []
    b6_list = []
    b7_list = []
    b8_list = []
    for row in range(longitude_df.shape[0]):  # 行 676
        for column in range(longitude_df.shape[1]):  # 列 451
            # 超过50KM的数值记为缺失-9999
            if item_df1 - 0.8 <= longitude_df[row][column] <= item_df1 + 0.8 and \
                    item_df2 - 0.5 <= latitude_df[row][column] <= item_df2 + 0.5:
                # 获取经纬度之间的距离
                d = geo_distance(
                    longitude_df[row][column],
                    latitude_df[row][column],
                    item_df1,
                    item_df2)  # item[0],item[1]
            else:
                d = -9999  # 表示缺失
            # 根据距离和经纬度分为到不同列表
            if (d > 0) and (d <= dis1) and aod_df[row][column] > 0:  # 第1个圆,自身
                a0_list.append(aod_df[row][column])  # 第1个列表
            elif (d > dis1) and (d <= dis2) and aod_df[row][column] > 0:  # 第2个圆,近邻
                angle_res = azimuthAngle(longitude_df[row][column], latitude_df[row][column],
                                         item_df1, item_df2)
                if 0 <= angle_res < 45:
                    a1_list.append(aod_df[row][column])
                elif 45 <= angle_res < 90:
                    a2_list.append(aod_df[row][column])
                elif 90 <= angle_res < 135:
                    a3_list.append(aod_df[row][column])
                elif 135 <= angle_res < 180:
                    a4_list.append(aod_df[row][column])
                elif 180 <= angle_res < 225:
                    a5_list.append(aod_df[row][column])
                elif 225 <= angle_res < 270:
                    a6_list.append(aod_df[row][column])
                elif 270 <= angle_res < 315:
                    a7_list.append(aod_df[row][column])
                else:
                    a8_list.append(aod_df[row][column])
            elif (d > dis2) and (d <= dis3) and aod_df[row][column] > 0:  # 第2个圆,近邻
                angle_res = azimuthAngle(longitude_df[row][column], latitude_df[row][column],
                                         item_df1, item_df2)
                if 0 <= angle_res < 45:
                    b1_list.append(aod_df[row][column])
                elif 45 <= angle_res < 90:
                    b2_list.append(aod_df[row][column])
                elif 90 <= angle_res < 135:
                    b3_list.append(aod_df[row][column])
                elif 135 <= angle_res < 180:
                    b4_list.append(aod_df[row][column])
                elif 180 <= angle_res < 225:
                    b5_list.append(aod_df[row][column])
                elif 225 <= angle_res < 270:
                    b6_list.append(aod_df[row][column])
                elif 270 <= angle_res < 315:
                    b7_list.append(aod_df[row][column])
                else:
                    b8_list.append(aod_df[row][column])

    return a0_list, a1_list, a2_list, a3_list, a4_list, a5_list, a6_list, a7_list, a8_list, \
           b1_list, b2_list, b3_list, b4_list, b5_list, b6_list, b7_list, b8_list


file_path = "D:\\test\\"  # HDF文件位置 TTT
output_file_path = "D:\\毕业论文程序\\气溶胶光学厚度\\"  # 结果的输出位置
# 批量读取HDF文件,提取AOD值,并将结果添加到列表中
file_name = os.listdir(file_path)  # 文件名



JCZ_file = pd.read_excel("D:\\毕业论文程序\\MODIS\\坐标\\站点列表-2018.11.08起.xlsx",sheet_name="样例1")
JCZ = []
# 批量导入监测站
for i in range(len(JCZ_file)):
    exec('JCZ%s = [JCZ_file["经度"][i],JCZ_file["纬度"][i],JCZ_file["城市"][i]+"-"+JCZ_file["监测点名称"][i]]' % i)
    exec("JCZ.append(JCZ%s)" % i)  # exec可以执行字符串指令
for item in JCZ:
    aod_outcome_list = []  # 每个监测站生成一个文件时
    a0_outcome_list = []
    a1_outcome_list = []
    a2_outcome_list = []
    a3_outcome_list = []
    a4_outcome_list = []
    a5_outcome_list = []
    a6_outcome_list = []
    a7_outcome_list = []
    a8_outcome_list = []
    b1_outcome_list = []
    b2_outcome_list = []
    b3_outcome_list = []
    b4_outcome_list = []
    b5_outcome_list = []
    b6_outcome_list = []
    b7_outcome_list = []
    b8_outcome_list = []
    date_list = []
    for hdf in file_name:
        HDF_FILE_URL = file_path + hdf
        file = SD(HDF_FILE_URL)
        sds_obj1 = file.select('Longitude')  # 选择经度
        sds_obj2 = file.select('Latitude')  # 选择纬度
        sds_obj3 = file.select('Optical_Depth_Land_And_Ocean')  # 产品质量最高的AOD数据集
        longitude = sds_obj1.get()  # 读取数据
        latitude = sds_obj2.get()
        aod = sds_obj3.get()
        # 经度加±0.1，纬度加±0.075，这样7.5KM圈的范围也包含对了，避免出现四分之三元在文件内，四分之一不在二忽略文件
        if np.min(longitude) - 0.8 <= item[0] <= np.max(longitude) + 0.8 and \
                np.min(latitude) - 0.5 <= item[1] <= np.max(latitude) + 0.5:
            # 距离计算，提取监测站半径为r范围内的AOD值!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            aod_list = get_aod_list(longitude, latitude, aod, item[0], item[1])  # 内含一个文件的17个列表
            # 把返回的列表值取均值
            a0_value = "%s文件" % hdf, "%s" % item[2], np.average(aod_list[0])
            a1_value = "%s文件" % hdf, "%s" % item[2], np.average(aod_list[1])
            a2_value = "%s文件" % hdf, "%s" % item[2], np.average(aod_list[2])
            a3_value = "%s文件" % hdf, "%s" % item[2], np.average(aod_list[3])
            a4_value = "%s文件" % hdf, "%s" % item[2], np.average(aod_list[4])
            a5_value = "%s文件" % hdf, "%s" % item[2], np.average(aod_list[5])
            a6_value = "%s文件" % hdf, "%s" % item[2], np.average(aod_list[6])
            a7_value = "%s文件" % hdf, "%s" % item[2], np.average(aod_list[7])
            a8_value = "%s文件" % hdf, "%s" % item[2], np.average(aod_list[8])
            b1_value = "%s文件" % hdf, "%s" % item[2], np.average(aod_list[9])
            b2_value = "%s文件" % hdf, "%s" % item[2], np.average(aod_list[10])
            b3_value = "%s文件" % hdf, "%s" % item[2], np.average(aod_list[11])
            b4_value = "%s文件" % hdf, "%s" % item[2], np.average(aod_list[12])
            b5_value = "%s文件" % hdf, "%s" % item[2], np.average(aod_list[13])
            b6_value = "%s文件" % hdf, "%s" % item[2], np.average(aod_list[14])
            b7_value = "%s文件" % hdf, "%s" % item[2], np.average(aod_list[15])
            b8_value = "%s文件" % hdf, "%s" % item[2], np.average(aod_list[16])
            # 添加进列表
            aod_outcome_list.append(a0_value)
            a1_outcome_list.append(a1_value)
            a2_outcome_list.append(a2_value)
            a3_outcome_list.append(a3_value)
            a4_outcome_list.append(a4_value)
            a5_outcome_list.append(a5_value)
            a6_outcome_list.append(a6_value)
            a7_outcome_list.append(a7_value)
            a8_outcome_list.append(a8_value)
            b1_outcome_list.append(b1_value)
            b2_outcome_list.append(b2_value)
            b3_outcome_list.append(b3_value)
            b4_outcome_list.append(b4_value)
            b5_outcome_list.append(b5_value)
            b6_outcome_list.append(b6_value)
            b7_outcome_list.append(b7_value)
            b8_outcome_list.append(b8_value)
            # 进度提示
            print("完成 %s文件" % hdf, "%s" % item[2])
            '''
            area_list = "%s文件" % hdf, np.average(area_list)  # 文件名,站点名,结果 移除站点名之后加
            aod_outcome = "%s文件" % hdf, "%s" % item[2], np.average(aod_list)
            '''
        else:
            print("%s站点不包含于文件%s范围中" % (item[2], hdf))
    # 上一个for循环结束
    aod_outcome_list_v2 = []  # 每个监测站生成一个文件时
    aod_outcome_list_v3 = []
    total_list = [aod_outcome_list, a1_outcome_list, a2_outcome_list, a3_outcome_list, a4_outcome_list, a5_outcome_list, a6_outcome_list, a7_outcome_list, a8_outcome_list,
       b1_outcome_list, b2_outcome_list, b3_outcome_list, b4_outcome_list, b5_outcome_list, b6_outcome_list, b7_outcome_list, b8_outcome_list]
    for area_list in total_list:
        for element in area_list:
            element = pd.Series(element)
            # 截取文件名称,结果为获取数据的时间,格式为"年+第几天"
            element[0] = str(element[0])[10:17]  # 如2018123
            # 修改日期格式为XX月XX日
            element[0] = time.strptime(element[0], '%Y%j')
            element[0] = time.strftime("%Y-%m-%d ", element[0])
            element = np.array(element)  # 格式转换
            element = pd.DataFrame(element)
            aod_outcome_list_v2.append(element)
            aod_outcome_list_v2 = pd.Series(aod_outcome_list_v2)
        aod_outcome_list_v3.append(aod_outcome_list_v2)
    # 数据框参数
    pd.set_option('display.max_rows', None)  # 行
    pd.set_option('display.max_columns', 1000)  # 列
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)
    aod_outcome_list_v3 = pd.DataFrame(aod_outcome_list_v3)  # 格式转换
    # 重设列名
    '''
    aod_outcome_list_v3.columns = ['日期0', '监测站0', "AOD值0",
                                   '日期1', '监测站1', "AOD值1",
                                   '日期2', '监测站2', "AOD值2",
                                   '日期3', '监测站3', "AOD值3",
                                   '日期4', '监测站4', "AOD值4",
                                   '日期5', '监测站5', "AOD值5",
                                   '日期6', '监测站6', "AOD值6",
                                   '日期7', '监测站7', "AOD值7",
                                   '日期8', '监测站8', "AOD值8",
                                   '日期9', '监测站9', "AOD值9",
                                   '日期10', '监测站10', "AOD值10",
                                   '日期11', '监测站11', "AOD值11",
                                   '日期12', '监测站12', "AOD值12",
                                   '日期13', '监测站13', "AOD值13",
                                   '日期14', '监测站14', "AOD值14",
                                   '日期15', '监测站15', "AOD值15",
                                   '日期16', '监测站16', "AOD值16"]
    del aod_outcome_list_v3["日期1", "日期2", "日期3", "日期4", "日期5", "日期6", "日期7", "日期8", "日期9", "日期10", "日期11", "日期12", "日期13", "日期14", "日期15", "日期16",]
    del aod_outcome_list_v3["监测站1", "监测站2", "监测站3", "监测站4", "监测站5", "监测站6", "监测站7", "监测站8", "监测站9", "监测站10", "监测站11", "监测站12", "监测站13", "监测站14", "监测站15", "监测站16",]
    '''
    # 同日期，多文件情况下的均值处理
    #aod_outcome_list_v3 = aod_outcome_list_v3.groupby(['日期', "监测站"]).mean()
    # 美化group by均值计算后的数据框格式
    #aod_outcome_list_v3 = pd.Series(aod_outcome_list_v3["AOD值"])  # AOD值按分组计算的结果
    aod_outcome_list_v3.to_excel(output_file_path + "%s.xlsx" % item[2])  # 完整结果存入excel

# 程序用时写入文件
end_time = datetime.datetime.now()
print(str(end_time - start_time))



