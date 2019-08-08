# -*- coding: utf-8 -*-
# 日期: 2019/6/8 22:04
# 作者: xcl
# 工具：PyCharm

# -*- coding: utf-8 -*-
# 日期: 2019/6/8 16:13
# 作者: xcl
# 工具：PyCharm



# 相关库
from math import radians, cos, sin, asin, sqrt
from darksky import forecast  # DarkSkyAPI
import time  # 年度时间范围生成
from datetime import datetime as dt  # 时间戳日期转换
import pandas as pd  # BDS

import numpy as np
# import datetime
import math
import os

# 文件格式设置
pd.set_option('display.width', 6666)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大列，None为显示所有列

# 参数设置
distance1 = 50000
distance2 = 100000

# 读取文件
coordinate_file_path = "F:\\毕业论文程序\\MODIS\\坐标\\"
JCZ_file = pd.read_excel(coordinate_file_path + "监测站坐标toDarkSkyAPI.xlsx", sheet_name="汇总")  # 监测站坐标toDarkSkyAPI

# 输出位置

out_path = "F:\\毕业论文程序\\整合数据\\整合1\\"
# 创建新数据框
coordinates = pd.DataFrame()
coordinates["xs"] = JCZ_file["经度"]
coordinates["ys"] = JCZ_file["纬度"]
coordinates["names"] = JCZ_file["城市"] + "-" + JCZ_file["监测点名称"]
# print(coordinates)


# 变量参数

var_x = ["AOD", "日均PM2.5", 'temperature',
         'apparentTemperatureHigh',
         'apparentTemperatureLow',
          'apparentTemperatureMax', 'apparentTemperatureMin',
         'cloudCover', 'dewPoint', 'humidity', 'icon', 'moonPhase', 'precipAccumulation'
                                                                                                  'precipIntensity',
         'precipIntensityMax',
         'precipProbability', 'precipType',
         'pressure', 'summary', 'temperatureHigh', 'temperatureLow',
         'temperatureMax',  'temperatureMin',
         'uvIndex',  'visibility', 'windBearing', 'windGust',  'windSpeed'
         ]
Time_list = [ 'apparentTemperatureHighTime',
              'apparentTemperatureLowTime', 'apparentTemperatureMaxTime','apparentTemperatureMinTime','precipIntensityMaxTime',
              'temperatureLowTime','sunriseTime', 'sunsetTime','temperatureHighTime','temperatureMinTime',
              'windGustTime','uvIndexTime', 'temperatureMaxTime',]
# -------------------------- 到此,已经完成了关于【相对位置+距离】的交叉表格----------------------------
# 表格结果为 列标题在行标题的第*分类上

data_location = pd.read_excel("table3.xlsx")
# print(data_location.head())
data_aod = "F:\\毕业论文程序\\气溶胶光学厚度\\日均\\"
data_pm = 'F:\\毕业论文程序\\污染物浓度\\整理\\日均\\'
data_sky_daily = "F:\\毕业论文程序\\气象数据\\整理\\日均\\2018\\"
data_sky_hourly = "F:\\毕业论文程序\\气象数据\\整理\\逐时均值\\"
for location in data_location["name"]:
    #print(data_location[data_location["name"] == location])  # 按行输出
    data_aod_outcome = pd.read_excel(data_aod + location + ".xlsx")
    data_aod_outcome = data_aod_outcome.set_index('日期')
    data_need_to_extract = data_location[data_location["name"] == location]
    # 有待替换！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    same_area_A1 = []
    same_area_A2 = []
    same_area_A3 = []
    same_area_A4 = []
    same_area_A5 = []
    same_area_A6 = []
    same_area_A7 = []
    same_area_A8 = []
    same_area_B1 = []
    same_area_B2 = []
    same_area_B3 = []
    same_area_B4 = []
    same_area_B5 = []
    same_area_B6 = []
    same_area_B7 = []
    same_area_B8 = []
    for element in data_need_to_extract.columns:
        value_1 = data_need_to_extract[element].values  # 每个单元格的值
        #print(value_1)
        if value_1 == "A-1":  # 第一个区划
            #print(value_1)
            same_area_A1.append(element)
        if value_1 == "A-2":  # 第一个区划
            #print(value_1)
            same_area_A2.append(element)
        if value_1 == "A-3":  # 第一个区划
            #print(value_1)
            same_area_A3.append(element)
        if value_1 == "A-4":  # 第一个区划
            #print(value_1)
            same_area_A4.append(element)
        if value_1 == "A-5":  # 第一个区划
            #print(value_1)
            same_area_A5.append(element)
        if value_1 == "A-6":  # 第一个区划
            #print(value_1)
            same_area_A6.append(element)
        if value_1 == "A-7":  # 第一个区划
            #print(value_1)
            same_area_A7.append(element)
        if value_1 == "A-8":  # 第一个区划
            #print(value_1)
            same_area_A8.append(element)
        if value_1 == "B-1":  # 第一个区划
            #print(value_1)
            same_area_B1.append(element)
        if value_1 == "B-2":  # 第一个区划
            #print(value_1)
            same_area_B2.append(element)
        if value_1 == "B-3":  # 第一个区划
            #print(value_1)
            same_area_B3.append(element)
        if value_1 == "B-4":  # 第一个区划
            #print(value_1)
            same_area_B4.append(element)
        if value_1 == "B-5":  # 第一个区划
            #print(value_1)
            same_area_B5.append(element)
        if value_1 == "B-6":  # 第一个区划
            #print(value_1)
            same_area_B6.append(element)
        if value_1 == "B-7":  # 第一个区划
            #print(value_1)
            same_area_B7.append(element)
        if value_1 == "B-8":  # 第一个区划
            #print(value_1)
            same_area_B8.append(element)
    #print(same_area_A1)

#####################################################################合并部分2########################################

    if len(same_area_A1) != 0:
        xi = 0
        for area in same_area_A1:
            xi = xi + 1
            #print(area)
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            data_to_merge.rename(columns={'监测站': 'A-1-监测站-%s' % xi, 'AOD值': 'A-1-AOD值-%s' % xi}, inplace=True)    # 重命名
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1, join_axes=[data_aod_outcome.index])  # 合并
            ##########以上几行完成了AOD
            data_to_merge_pm = pd.read_excel(data_pm + area + ".xlsx")
            data_to_merge_pm = data_to_merge_pm.set_index('日期')
            data_to_merge_pm.rename(columns={'日均PM2.5': 'A-1-日均PM2.5-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_pm], axis=1, join_axes=[data_aod_outcome.index])  # 合并
            data_aod_outcome = data_aod_outcome.drop(columns=["X", "Y"])
            #########PM2.5############################3
            data_to_merge_sky_daily = pd.read_excel(data_sky_daily + area + ".xlsx")
            data_to_merge_sky_daily = data_to_merge_sky_daily.set_index('日期')
            for c_name in data_to_merge_sky_daily.columns:
                data_to_merge_sky_daily.rename(columns={c_name: 'A-1-'+c_name+'-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_daily], axis=1, join_axes=[data_aod_outcome.index])  # 合并
            ######################日均#########
            data_to_merge_sky_hourly = pd.read_excel(data_sky_hourly + area + ".xlsx")
            data_to_merge_sky_hourly = data_to_merge_sky_hourly.set_index('日期')

            for d_name in data_to_merge_sky_hourly.columns:
                if d_name != "temperature":
                    del data_to_merge_sky_hourly[d_name]
            data_to_merge_sky_hourly.rename(columns={"temperature": 'A-1-temperature-%s' % xi}, inplace=True)

            #data_aod_outcome["A-1-temperature-%s" % xi] = data_to_merge_sky_hourly["temperature"]
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_hourly["A-1-temperature-%s" % xi]], axis=1, join_axes=[data_aod_outcome.index])  # 合并
            #print(data_aod_outcome.columns)
   # print(data_aod_outcome.head())
    '''
    if xi != 0:
        for xj in range(1, xi+1):
            print(xj)
    '''
    for c_name_2 in data_aod_outcome.columns:
        data_aod_outcome[c_name_2] = data_aod_outcome[c_name_2].fillna(0)
    #######均值部分#############
    '''
    item_add = []
    item_add_pm = []
    item_add_sky_daily = []
    for item in data_aod_outcome.columns:
        if "A-1-AOD值" in item:
            item_add.append(item)
        if "A-1-日均PM2.5" in item:
            item_add_pm.append(item)
    if len(item_add) != 0:
        data_aod_outcome["A1-AOD-MEAN"] = data_aod_outcome[item_add].mean(axis=1)  # 均值换轴
    if len(item_add_pm) != 0:
        data_aod_outcome["A1-PM-MEAN"] = data_aod_outcome[item_add_pm].mean(axis=1)  # 均值换轴
    for item_2 in data_aod_outcome.columns: # 删除多的
        if "A-1-" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass
    #print(data_aod_outcome.head())
    '''
    # 删除 Time变量 不然 下面的接着的循环 会出现 【最高温，最高温时间】这种列表
    for item_2 in data_aod_outcome.columns: # 删除多的
        if "Time" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass

    for bianliang in var_x:
        bianliang_list = []
        for item_xx in data_aod_outcome.columns:
            if "A-1-"+bianliang in item_xx:
                bianliang_list.append(item_xx)
                #print(bianliang_list)
        if len(bianliang_list) != 0:
            data_aod_outcome["A1-%s-MEAN" % bianliang] = data_aod_outcome[bianliang_list].mean(axis=1)

    for item_2 in data_aod_outcome.columns: # 删除多的
        if "A-1-" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass
    for cx_name_2 in data_aod_outcome.columns:
        data_aod_outcome[cx_name_2] = data_aod_outcome[cx_name_2].fillna(0)
    data_aod_outcome.to_excel("F:\\毕业论文程序\\整合数据\\整合1\\%s.xlsx" % location)
   # print(location)
