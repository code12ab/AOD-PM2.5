# -*- coding: utf-8 -*-
# 日期: 2019/6/10 23:38
# 作者: xcl
# 工具：PyCharm

###########################################自己的数据 相邻站点的PM数据 ######################################################

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

data_location = pd.read_excel("位置距离.xlsx")
# print(data_location.head())
data_aod = "F:\\毕业论文程序\\气溶胶光学厚度\\日均\\"
data_pm = 'F:\\毕业论文程序\\污染物浓度\\整理\\日均\\'
data_sky_daily = "F:\\毕业论文程序\\气象数据\\整理\\日均\\2018\\"
data_sky_hourly = "F:\\毕业论文程序\\气象数据\\整理\\逐时均值\\2018\\"
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
#####################################################################合并部分2########################################

    if len(same_area_A1) != 0:
        xi = 0
        for area in same_area_A1:
            xi = xi + 1
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            data_to_merge.rename(columns={'监测站': 'A-1-监测站-%s' % xi, 'AOD值': 'A-1-AOD值-%s' % xi}, inplace=True)  # 重命名
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ##########以上几行完成了AOD
            data_to_merge_pm = pd.read_excel(data_pm + area + ".xlsx")
            data_to_merge_pm = data_to_merge_pm.set_index('日期')
            data_to_merge_pm.rename(columns={'日均PM2.5': 'A-1-日均PM2.5-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_pm], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            data_aod_outcome = data_aod_outcome.drop(columns=["X", "Y"])
            #########PM2.5############################3
            '''
            data_to_merge_sky_daily = pd.read_excel(data_sky_daily + area + ".xlsx")
            data_to_merge_sky_daily = data_to_merge_sky_daily.set_index('日期')
            for c_name in data_to_merge_sky_daily.columns:
                data_to_merge_sky_daily.rename(columns={c_name: 'A-1-' + c_name + '-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_daily], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ######################日均#########
            data_to_merge_sky_hourly = pd.read_excel(data_sky_hourly + area + ".xlsx")
            data_to_merge_sky_hourly = data_to_merge_sky_hourly.set_index('日期')
            for d_name in data_to_merge_sky_hourly.columns:
                if d_name != "temperature":
                    del data_to_merge_sky_hourly[d_name]
            data_to_merge_sky_hourly.rename(columns={"temperature": 'A-1-temperature-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_hourly["A-1-temperature-%s" % xi]],
                                         axis=1, join_axes=[data_aod_outcome.index])  # 合并
            #######################逐时###########
            '''
    for c_name_2 in data_aod_outcome.columns:
        data_aod_outcome[c_name_2] = data_aod_outcome[c_name_2].fillna(0)

    #######均值部分#############
    # 删除 Time变量 不然 下面的接着的循环 会出现 【最高温，最高温时间】这种列表
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "Time" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass
    for bianliang in var_x:
        bianliang_list = []
        for item_xx in data_aod_outcome.columns:
            if "A-1-" + bianliang in item_xx:
                bianliang_list.append(item_xx)
        if len(bianliang_list) != 0:
            data_aod_outcome["A1-%s-MEAN" % bianliang] = data_aod_outcome[bianliang_list].mean(axis=1)
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "A-1-" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass

    ##################################################################A2

    if len(same_area_A2) != 0:
        xi = 0
        for area in same_area_A2:
            xi = xi + 1
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            data_to_merge.rename(columns={'监测站': 'A-2-监测站-%s' % xi, 'AOD值': 'A-2-AOD值-%s' % xi}, inplace=True)  # 重命名
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ##########以上几行完成了AOD
            data_to_merge_pm = pd.read_excel(data_pm + area + ".xlsx")
            data_to_merge_pm = data_to_merge_pm.set_index('日期')
            data_to_merge_pm.rename(columns={'日均PM2.5': 'A-2-日均PM2.5-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_pm], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            data_aod_outcome = data_aod_outcome.drop(columns=["X", "Y"])
            #########PM2.5############################3
            '''
            data_to_merge_sky_daily = pd.read_excel(data_sky_daily + area + ".xlsx")
            data_to_merge_sky_daily = data_to_merge_sky_daily.set_index('日期')
            for c_name in data_to_merge_sky_daily.columns:
                data_to_merge_sky_daily.rename(columns={c_name: 'A-2-' + c_name + '-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_daily], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ######################日均#########
            data_to_merge_sky_hourly = pd.read_excel(data_sky_hourly + area + ".xlsx")
            data_to_merge_sky_hourly = data_to_merge_sky_hourly.set_index('日期')
            for d_name in data_to_merge_sky_hourly.columns:
                if d_name != "temperature":
                    del data_to_merge_sky_hourly[d_name]
            data_to_merge_sky_hourly.rename(columns={"temperature": 'A-2-temperature-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_hourly["A-2-temperature-%s" % xi]],
                                         axis=1, join_axes=[data_aod_outcome.index])  # 合并
            '''
    for c_name_2 in data_aod_outcome.columns:
        data_aod_outcome[c_name_2] = data_aod_outcome[c_name_2].fillna(0)
    #######均值部分#############
    # 删除 Time变量 不然 下面的接着的循环 会出现 【最高温，最高温时间】这种列表
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "Time" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass
    for bianliang in var_x:
        bianliang_list = []
        for item_xx in data_aod_outcome.columns:
            if "A-2-" + bianliang in item_xx:
                bianliang_list.append(item_xx)
        if len(bianliang_list) != 0:
            data_aod_outcome["A2-%s-MEAN" % bianliang] = data_aod_outcome[bianliang_list].mean(axis=1)
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "A-2-" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass

    ##################################################################A3

    if len(same_area_A3) != 0:
        xi = 0
        for area in same_area_A3:
            xi = xi + 1
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            data_to_merge.rename(columns={'监测站': 'A-3-监测站-%s' % xi, 'AOD值': 'A-3-AOD值-%s' % xi}, inplace=True)  # 重命名
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ##########以上几行完成了AOD
            data_to_merge_pm = pd.read_excel(data_pm + area + ".xlsx")
            data_to_merge_pm = data_to_merge_pm.set_index('日期')
            data_to_merge_pm.rename(columns={'日均PM2.5': 'A-3-日均PM2.5-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_pm], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            data_aod_outcome = data_aod_outcome.drop(columns=["X", "Y"])
            #########PM2.5############################3
            '''
            data_to_merge_sky_daily = pd.read_excel(data_sky_daily + area + ".xlsx")
            data_to_merge_sky_daily = data_to_merge_sky_daily.set_index('日期')
            for c_name in data_to_merge_sky_daily.columns:
                data_to_merge_sky_daily.rename(columns={c_name: 'A-3-' + c_name + '-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_daily], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ######################日均#########
            data_to_merge_sky_hourly = pd.read_excel(data_sky_hourly + area + ".xlsx")
            data_to_merge_sky_hourly = data_to_merge_sky_hourly.set_index('日期')
            for d_name in data_to_merge_sky_hourly.columns:
                if d_name != "temperature":
                    del data_to_merge_sky_hourly[d_name]
            data_to_merge_sky_hourly.rename(columns={"temperature": 'A-3-temperature-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_hourly["A-3-temperature-%s" % xi]],
                                         axis=1, join_axes=[data_aod_outcome.index])  # 合并
            '''
    for c_name_2 in data_aod_outcome.columns:
        data_aod_outcome[c_name_2] = data_aod_outcome[c_name_2].fillna(0)
    #######均值部分#############
    # 删除 Time变量 不然 下面的接着的循环 会出现 【最高温，最高温时间】这种列表
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "Time" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass
    for bianliang in var_x:
        bianliang_list = []
        for item_xx in data_aod_outcome.columns:
            if "A-3-" + bianliang in item_xx:
                bianliang_list.append(item_xx)
        if len(bianliang_list) != 0:
            data_aod_outcome["A3-%s-MEAN" % bianliang] = data_aod_outcome[bianliang_list].mean(axis=1)
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "A-3-" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass

    ##################################################################A4

    if len(same_area_A4) != 0:
        xi = 0
        for area in same_area_A4:
            xi = xi + 1
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            data_to_merge.rename(columns={'监测站': 'A-4-监测站-%s' % xi, 'AOD值': 'A-4-AOD值-%s' % xi}, inplace=True)  # 重命名
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ##########以上几行完成了AOD
            data_to_merge_pm = pd.read_excel(data_pm + area + ".xlsx")
            data_to_merge_pm = data_to_merge_pm.set_index('日期')
            data_to_merge_pm.rename(columns={'日均PM2.5': 'A-4-日均PM2.5-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_pm], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            data_aod_outcome = data_aod_outcome.drop(columns=["X", "Y"])
            #########PM2.5############################3
            '''
            data_to_merge_sky_daily = pd.read_excel(data_sky_daily + area + ".xlsx")
            data_to_merge_sky_daily = data_to_merge_sky_daily.set_index('日期')
            for c_name in data_to_merge_sky_daily.columns:
                data_to_merge_sky_daily.rename(columns={c_name: 'A-4-' + c_name + '-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_daily], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ######################日均#########
            data_to_merge_sky_hourly = pd.read_excel(data_sky_hourly + area + ".xlsx")
            data_to_merge_sky_hourly = data_to_merge_sky_hourly.set_index('日期')
            for d_name in data_to_merge_sky_hourly.columns:
                if d_name != "temperature":
                    del data_to_merge_sky_hourly[d_name]
            data_to_merge_sky_hourly.rename(columns={"temperature": 'A-4-temperature-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_hourly["A-4-temperature-%s" % xi]],
                                         axis=1, join_axes=[data_aod_outcome.index])  # 合并
            '''
    for c_name_2 in data_aod_outcome.columns:
        data_aod_outcome[c_name_2] = data_aod_outcome[c_name_2].fillna(0)
    #######均值部分#############
    # 删除 Time变量 不然 下面的接着的循环 会出现 【最高温，最高温时间】这种列表
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "Time" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass
    for bianliang in var_x:
        bianliang_list = []
        for item_xx in data_aod_outcome.columns:
            if "A-4-" + bianliang in item_xx:
                bianliang_list.append(item_xx)
        if len(bianliang_list) != 0:
            data_aod_outcome["A4-%s-MEAN" % bianliang] = data_aod_outcome[bianliang_list].mean(axis=1)
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "A-4-" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass

    ##################################################################A5

    if len(same_area_A5) != 0:
        xi = 0
        for area in same_area_A5:
            xi = xi + 1
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            data_to_merge.rename(columns={'监测站': 'A-5-监测站-%s' % xi, 'AOD值': 'A-5-AOD值-%s' % xi}, inplace=True)  # 重命名
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ##########以上几行完成了AOD
            data_to_merge_pm = pd.read_excel(data_pm + area + ".xlsx")
            data_to_merge_pm = data_to_merge_pm.set_index('日期')
            data_to_merge_pm.rename(columns={'日均PM2.5': 'A-5-日均PM2.5-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_pm], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            data_aod_outcome = data_aod_outcome.drop(columns=["X", "Y"])
            #########PM2.5############################3
            '''
            data_to_merge_sky_daily = pd.read_excel(data_sky_daily + area + ".xlsx")
            data_to_merge_sky_daily = data_to_merge_sky_daily.set_index('日期')
            for c_name in data_to_merge_sky_daily.columns:
                data_to_merge_sky_daily.rename(columns={c_name: 'A-5-' + c_name + '-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_daily], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ######################日均#########
            data_to_merge_sky_hourly = pd.read_excel(data_sky_hourly + area + ".xlsx")
            data_to_merge_sky_hourly = data_to_merge_sky_hourly.set_index('日期')
            for d_name in data_to_merge_sky_hourly.columns:
                if d_name != "temperature":
                    del data_to_merge_sky_hourly[d_name]
            data_to_merge_sky_hourly.rename(columns={"temperature": 'A-5-temperature-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_hourly["A-5-temperature-%s" % xi]],
                                         axis=1, join_axes=[data_aod_outcome.index])  # 合并
            '''
    for c_name_2 in data_aod_outcome.columns:
        data_aod_outcome[c_name_2] = data_aod_outcome[c_name_2].fillna(0)
    #######均值部分#############
    # 删除 Time变量 不然 下面的接着的循环 会出现 【最高温，最高温时间】这种列表
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "Time" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass
    for bianliang in var_x:
        bianliang_list = []
        for item_xx in data_aod_outcome.columns:
            if "A-5-" + bianliang in item_xx:
                bianliang_list.append(item_xx)
        if len(bianliang_list) != 0:
            data_aod_outcome["A5-%s-MEAN" % bianliang] = data_aod_outcome[bianliang_list].mean(axis=1)
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "A-5-" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass

    ##################################################################A6

    if len(same_area_A6) != 0:
        xi = 0
        for area in same_area_A6:
            xi = xi + 1
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            data_to_merge.rename(columns={'监测站': 'A-6-监测站-%s' % xi, 'AOD值': 'A-6-AOD值-%s' % xi}, inplace=True)  # 重命名
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ##########以上几行完成了AOD
            data_to_merge_pm = pd.read_excel(data_pm + area + ".xlsx")
            data_to_merge_pm = data_to_merge_pm.set_index('日期')
            data_to_merge_pm.rename(columns={'日均PM2.5': 'A-6-日均PM2.5-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_pm], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            data_aod_outcome = data_aod_outcome.drop(columns=["X", "Y"])
            #########PM2.5############################3
            '''
            data_to_merge_sky_daily = pd.read_excel(data_sky_daily + area + ".xlsx")
            data_to_merge_sky_daily = data_to_merge_sky_daily.set_index('日期')
            for c_name in data_to_merge_sky_daily.columns:
                data_to_merge_sky_daily.rename(columns={c_name: 'A-6-' + c_name + '-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_daily], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ######################日均#########
            data_to_merge_sky_hourly = pd.read_excel(data_sky_hourly + area + ".xlsx")
            data_to_merge_sky_hourly = data_to_merge_sky_hourly.set_index('日期')
            for d_name in data_to_merge_sky_hourly.columns:
                if d_name != "temperature":
                    del data_to_merge_sky_hourly[d_name]
            data_to_merge_sky_hourly.rename(columns={"temperature": 'A-6-temperature-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_hourly["A-6-temperature-%s" % xi]],
                                         axis=1, join_axes=[data_aod_outcome.index])  # 合并
            '''
    for c_name_2 in data_aod_outcome.columns:
        data_aod_outcome[c_name_2] = data_aod_outcome[c_name_2].fillna(0)
    #######均值部分#############
    # 删除 Time变量 不然 下面的接着的循环 会出现 【最高温，最高温时间】这种列表
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "Time" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass
    for bianliang in var_x:
        bianliang_list = []
        for item_xx in data_aod_outcome.columns:
            if "A-6-" + bianliang in item_xx:
                bianliang_list.append(item_xx)
        if len(bianliang_list) != 0:
            data_aod_outcome["A6-%s-MEAN" % bianliang] = data_aod_outcome[bianliang_list].mean(axis=1)
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "A-6-" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass

    ##################################################################A7

    if len(same_area_A7) != 0:
        xi = 0
        for area in same_area_A7:
            xi = xi + 1
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            data_to_merge.rename(columns={'监测站': 'A-7-监测站-%s' % xi, 'AOD值': 'A-7-AOD值-%s' % xi}, inplace=True)  # 重命名
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ##########以上几行完成了AOD
            data_to_merge_pm = pd.read_excel(data_pm + area + ".xlsx")
            data_to_merge_pm = data_to_merge_pm.set_index('日期')
            data_to_merge_pm.rename(columns={'日均PM2.5': 'A-7-日均PM2.5-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_pm], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            data_aod_outcome = data_aod_outcome.drop(columns=["X", "Y"])
            #########PM2.5############################3
            '''
            data_to_merge_sky_daily = pd.read_excel(data_sky_daily + area + ".xlsx")
            data_to_merge_sky_daily = data_to_merge_sky_daily.set_index('日期')
            for c_name in data_to_merge_sky_daily.columns:
                data_to_merge_sky_daily.rename(columns={c_name: 'A-7-' + c_name + '-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_daily], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ######################日均#########
            data_to_merge_sky_hourly = pd.read_excel(data_sky_hourly + area + ".xlsx")
            data_to_merge_sky_hourly = data_to_merge_sky_hourly.set_index('日期')
            for d_name in data_to_merge_sky_hourly.columns:
                if d_name != "temperature":
                    del data_to_merge_sky_hourly[d_name]
            data_to_merge_sky_hourly.rename(columns={"temperature": 'A-7-temperature-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_hourly["A-7-temperature-%s" % xi]],
                                         axis=1, join_axes=[data_aod_outcome.index])  # 合并
            '''
    for c_name_2 in data_aod_outcome.columns:
        data_aod_outcome[c_name_2] = data_aod_outcome[c_name_2].fillna(0)
    #######均值部分#############
    # 删除 Time变量 不然 下面的接着的循环 会出现 【最高温，最高温时间】这种列表
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "Time" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass
    for bianliang in var_x:
        bianliang_list = []
        for item_xx in data_aod_outcome.columns:
            if "A-7-" + bianliang in item_xx:
                bianliang_list.append(item_xx)
        if len(bianliang_list) != 0:
            data_aod_outcome["A7-%s-MEAN" % bianliang] = data_aod_outcome[bianliang_list].mean(axis=1)
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "A-7-" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass

    ##################################################################A8

    if len(same_area_A8) != 0:
        xi = 0
        for area in same_area_A8:
            xi = xi + 1
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            data_to_merge.rename(columns={'监测站': 'A-8-监测站-%s' % xi, 'AOD值': 'A-8-AOD值-%s' % xi}, inplace=True)  # 重命名
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ##########以上几行完成了AOD
            data_to_merge_pm = pd.read_excel(data_pm + area + ".xlsx")
            data_to_merge_pm = data_to_merge_pm.set_index('日期')
            data_to_merge_pm.rename(columns={'日均PM2.5': 'A-8-日均PM2.5-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_pm], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            data_aod_outcome = data_aod_outcome.drop(columns=["X", "Y"])
            #########PM2.5############################3
            '''
            data_to_merge_sky_daily = pd.read_excel(data_sky_daily + area + ".xlsx")
            data_to_merge_sky_daily = data_to_merge_sky_daily.set_index('日期')
            for c_name in data_to_merge_sky_daily.columns:
                data_to_merge_sky_daily.rename(columns={c_name: 'A-8-' + c_name + '-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_daily], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ######################日均#########
            data_to_merge_sky_hourly = pd.read_excel(data_sky_hourly + area + ".xlsx")
            data_to_merge_sky_hourly = data_to_merge_sky_hourly.set_index('日期')
            for d_name in data_to_merge_sky_hourly.columns:
                if d_name != "temperature":
                    del data_to_merge_sky_hourly[d_name]
            data_to_merge_sky_hourly.rename(columns={"temperature": 'A-8-temperature-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_hourly["A-8-temperature-%s" % xi]],
                                         axis=1, join_axes=[data_aod_outcome.index])  # 合并
            '''
    for c_name_2 in data_aod_outcome.columns:
        data_aod_outcome[c_name_2] = data_aod_outcome[c_name_2].fillna(0)
    #######均值部分#############
    # 删除 Time变量 不然 下面的接着的循环 会出现 【最高温，最高温时间】这种列表
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "Time" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass
    for bianliang in var_x:
        bianliang_list = []
        for item_xx in data_aod_outcome.columns:
            if "A-8-" + bianliang in item_xx:
                bianliang_list.append(item_xx)
        if len(bianliang_list) != 0:
            data_aod_outcome["A8-%s-MEAN" % bianliang] = data_aod_outcome[bianliang_list].mean(axis=1)
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "A-8-" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass

    #####################################################################合并部分BBBB########################################

    if len(same_area_B1) != 0:
        xi = 0
        for area in same_area_B1:
            xi = xi + 1
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            data_to_merge.rename(columns={'监测站': 'B-1-监测站-%s' % xi, 'AOD值': 'B-1-AOD值-%s' % xi}, inplace=True)  # 重命名
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ##########以上几行完成了AOD
            data_to_merge_pm = pd.read_excel(data_pm + area + ".xlsx")
            data_to_merge_pm = data_to_merge_pm.set_index('日期')
            data_to_merge_pm.rename(columns={'日均PM2.5': 'B-1-日均PM2.5-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_pm], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            data_aod_outcome = data_aod_outcome.drop(columns=["X", "Y"])
            #########PM2.5############################3
            '''
            data_to_merge_sky_daily = pd.read_excel(data_sky_daily + area + ".xlsx")
            data_to_merge_sky_daily = data_to_merge_sky_daily.set_index('日期')
            for c_name in data_to_merge_sky_daily.columns:
                data_to_merge_sky_daily.rename(columns={c_name: 'B-1-' + c_name + '-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_daily], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ######################日均#########
            data_to_merge_sky_hourly = pd.read_excel(data_sky_hourly + area + ".xlsx")
            data_to_merge_sky_hourly = data_to_merge_sky_hourly.set_index('日期')
            for d_name in data_to_merge_sky_hourly.columns:
                if d_name != "temperature":
                    del data_to_merge_sky_hourly[d_name]
            data_to_merge_sky_hourly.rename(columns={"temperature": 'B-1-temperature-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_hourly["B-1-temperature-%s" % xi]],
                                         axis=1, join_axes=[data_aod_outcome.index])  # 合并
            '''
    for c_name_2 in data_aod_outcome.columns:
        data_aod_outcome[c_name_2] = data_aod_outcome[c_name_2].fillna(0)
    #######均值部分#############
    # 删除 Time变量 不然 下面的接着的循环 会出现 【最高温，最高温时间】这种列表
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "Time" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass
    for bianliang in var_x:
        bianliang_list = []
        for item_xx in data_aod_outcome.columns:
            if "B-1-" + bianliang in item_xx:
                bianliang_list.append(item_xx)
        if len(bianliang_list) != 0:
            data_aod_outcome["B1-%s-MEAN" % bianliang] = data_aod_outcome[bianliang_list].mean(axis=1)
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "B-1-" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass

    ##################################################################B2

    if len(same_area_B2) != 0:
        xi = 0
        for area in same_area_B2:
            xi = xi + 1
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            data_to_merge.rename(columns={'监测站': 'B-2-监测站-%s' % xi, 'AOD值': 'B-2-AOD值-%s' % xi}, inplace=True)  # 重命名
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ##########以上几行完成了AOD
            data_to_merge_pm = pd.read_excel(data_pm + area + ".xlsx")
            data_to_merge_pm = data_to_merge_pm.set_index('日期')
            data_to_merge_pm.rename(columns={'日均PM2.5': 'B-2-日均PM2.5-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_pm], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            data_aod_outcome = data_aod_outcome.drop(columns=["X", "Y"])
            #########PM2.5############################3
            data_to_merge_sky_daily = pd.read_excel(data_sky_daily + area + ".xlsx")
            data_to_merge_sky_daily = data_to_merge_sky_daily.set_index('日期')
            for c_name in data_to_merge_sky_daily.columns:
                data_to_merge_sky_daily.rename(columns={c_name: 'B-2-' + c_name + '-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_daily], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ######################日均#########
            data_to_merge_sky_hourly = pd.read_excel(data_sky_hourly + area + ".xlsx")
            data_to_merge_sky_hourly = data_to_merge_sky_hourly.set_index('日期')
            for d_name in data_to_merge_sky_hourly.columns:
                if d_name != "temperature":
                    del data_to_merge_sky_hourly[d_name]
            data_to_merge_sky_hourly.rename(columns={"temperature": 'B-2-temperature-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_hourly["B-2-temperature-%s" % xi]],
                                         axis=1, join_axes=[data_aod_outcome.index])  # 合并
    for c_name_2 in data_aod_outcome.columns:
        data_aod_outcome[c_name_2] = data_aod_outcome[c_name_2].fillna(0)
    #######均值部分#############
    # 删除 Time变量 不然 下面的接着的循环 会出现 【最高温，最高温时间】这种列表
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "Time" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass
    for bianliang in var_x:
        bianliang_list = []
        for item_xx in data_aod_outcome.columns:
            if "B-2-" + bianliang in item_xx:
                bianliang_list.append(item_xx)
        if len(bianliang_list) != 0:
            data_aod_outcome["B2-%s-MEAN" % bianliang] = data_aod_outcome[bianliang_list].mean(axis=1)
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "B-2-" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass

    ##################################################################B3

    if len(same_area_B3) != 0:
        xi = 0
        for area in same_area_B3:
            xi = xi + 1
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            data_to_merge.rename(columns={'监测站': 'B-3-监测站-%s' % xi, 'AOD值': 'B-3-AOD值-%s' % xi}, inplace=True)  # 重命名
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ##########以上几行完成了AOD
            data_to_merge_pm = pd.read_excel(data_pm + area + ".xlsx")
            data_to_merge_pm = data_to_merge_pm.set_index('日期')
            data_to_merge_pm.rename(columns={'日均PM2.5': 'B-3-日均PM2.5-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_pm], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            data_aod_outcome = data_aod_outcome.drop(columns=["X", "Y"])
            #########PM2.5############################3
            '''
            data_to_merge_sky_daily = pd.read_excel(data_sky_daily + area + ".xlsx")
            data_to_merge_sky_daily = data_to_merge_sky_daily.set_index('日期')
            for c_name in data_to_merge_sky_daily.columns:
                data_to_merge_sky_daily.rename(columns={c_name: 'B-3-' + c_name + '-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_daily], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ######################日均#########
            data_to_merge_sky_hourly = pd.read_excel(data_sky_hourly + area + ".xlsx")
            data_to_merge_sky_hourly = data_to_merge_sky_hourly.set_index('日期')
            for d_name in data_to_merge_sky_hourly.columns:
                if d_name != "temperature":
                    del data_to_merge_sky_hourly[d_name]
            data_to_merge_sky_hourly.rename(columns={"temperature": 'B-3-temperature-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_hourly["B-3-temperature-%s" % xi]],
                                         axis=1, join_axes=[data_aod_outcome.index])  # 合并
            '''
    for c_name_2 in data_aod_outcome.columns:
        data_aod_outcome[c_name_2] = data_aod_outcome[c_name_2].fillna(0)
    #######均值部分#############
    # 删除 Time变量 不然 下面的接着的循环 会出现 【最高温，最高温时间】这种列表
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "Time" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass
    for bianliang in var_x:
        bianliang_list = []
        for item_xx in data_aod_outcome.columns:
            if "B-3-" + bianliang in item_xx:
                bianliang_list.append(item_xx)
        if len(bianliang_list) != 0:
            data_aod_outcome["B3-%s-MEAN" % bianliang] = data_aod_outcome[bianliang_list].mean(axis=1)
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "B-3-" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass

    ##################################################################B4

    if len(same_area_B4) != 0:
        xi = 0
        for area in same_area_B4:
            xi = xi + 1
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            data_to_merge.rename(columns={'监测站': 'B-4-监测站-%s' % xi, 'AOD值': 'B-4-AOD值-%s' % xi}, inplace=True)  # 重命名
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ##########以上几行完成了AOD
            data_to_merge_pm = pd.read_excel(data_pm + area + ".xlsx")
            data_to_merge_pm = data_to_merge_pm.set_index('日期')
            data_to_merge_pm.rename(columns={'日均PM2.5': 'B-4-日均PM2.5-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_pm], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            data_aod_outcome = data_aod_outcome.drop(columns=["X", "Y"])
            #########PM2.5############################
            '''
            data_to_merge_sky_daily = pd.read_excel(data_sky_daily + area + ".xlsx")
            data_to_merge_sky_daily = data_to_merge_sky_daily.set_index('日期')
            for c_name in data_to_merge_sky_daily.columns:
                data_to_merge_sky_daily.rename(columns={c_name: 'B-4-' + c_name + '-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_daily], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ######################日均#########
            data_to_merge_sky_hourly = pd.read_excel(data_sky_hourly + area + ".xlsx")
            data_to_merge_sky_hourly = data_to_merge_sky_hourly.set_index('日期')
            for d_name in data_to_merge_sky_hourly.columns:
                if d_name != "temperature":
                    del data_to_merge_sky_hourly[d_name]
            data_to_merge_sky_hourly.rename(columns={"temperature": 'B-4-temperature-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_hourly["B-4-temperature-%s" % xi]],
                                         axis=1, join_axes=[data_aod_outcome.index])  # 合并
            '''
    for c_name_2 in data_aod_outcome.columns:
        data_aod_outcome[c_name_2] = data_aod_outcome[c_name_2].fillna(0)
    #######均值部分#############
    # 删除 Time变量 不然 下面的接着的循环 会出现 【最高温，最高温时间】这种列表
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "Time" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass
    for bianliang in var_x:
        bianliang_list = []
        for item_xx in data_aod_outcome.columns:
            if "B-4-" + bianliang in item_xx:
                bianliang_list.append(item_xx)
        if len(bianliang_list) != 0:
            data_aod_outcome["B4-%s-MEAN" % bianliang] = data_aod_outcome[bianliang_list].mean(axis=1)
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "B-4-" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass

    ##################################################################B5

    if len(same_area_B5) != 0:
        xi = 0
        for area in same_area_B5:
            xi = xi + 1
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            data_to_merge.rename(columns={'监测站': 'B-5-监测站-%s' % xi, 'AOD值': 'B-5-AOD值-%s' % xi}, inplace=True)  # 重命名
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ##########以上几行完成了AOD
            data_to_merge_pm = pd.read_excel(data_pm + area + ".xlsx")
            data_to_merge_pm = data_to_merge_pm.set_index('日期')
            data_to_merge_pm.rename(columns={'日均PM2.5': 'B-5-日均PM2.5-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_pm], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            data_aod_outcome = data_aod_outcome.drop(columns=["X", "Y"])
            #########PM2.5############################
            '''
            data_to_merge_sky_daily = pd.read_excel(data_sky_daily + area + ".xlsx")
            data_to_merge_sky_daily = data_to_merge_sky_daily.set_index('日期')
            for c_name in data_to_merge_sky_daily.columns:
                data_to_merge_sky_daily.rename(columns={c_name: 'B-5-' + c_name + '-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_daily], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ######################日均#########
            data_to_merge_sky_hourly = pd.read_excel(data_sky_hourly + area + ".xlsx")
            data_to_merge_sky_hourly = data_to_merge_sky_hourly.set_index('日期')
            for d_name in data_to_merge_sky_hourly.columns:
                if d_name != "temperature":
                    del data_to_merge_sky_hourly[d_name]
            data_to_merge_sky_hourly.rename(columns={"temperature": 'B-5-temperature-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_hourly["B-5-temperature-%s" % xi]],
                                         axis=1, join_axes=[data_aod_outcome.index])  # 合并
            '''
    for c_name_2 in data_aod_outcome.columns:
        data_aod_outcome[c_name_2] = data_aod_outcome[c_name_2].fillna(0)
    #######均值部分#############
    # 删除 Time变量 不然 下面的接着的循环 会出现 【最高温，最高温时间】这种列表
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "Time" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass
    for bianliang in var_x:
        bianliang_list = []
        for item_xx in data_aod_outcome.columns:
            if "B-5-" + bianliang in item_xx:
                bianliang_list.append(item_xx)
        if len(bianliang_list) != 0:
            data_aod_outcome["B5-%s-MEAN" % bianliang] = data_aod_outcome[bianliang_list].mean(axis=1)
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "B-5-" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass

    ##################################################################B6

    if len(same_area_B6) != 0:
        xi = 0
        for area in same_area_B6:
            xi = xi + 1
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            data_to_merge.rename(columns={'监测站': 'B-6-监测站-%s' % xi, 'AOD值': 'B-6-AOD值-%s' % xi}, inplace=True)  # 重命名
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ##########以上几行完成了AOD
            data_to_merge_pm = pd.read_excel(data_pm + area + ".xlsx")
            data_to_merge_pm = data_to_merge_pm.set_index('日期')
            data_to_merge_pm.rename(columns={'日均PM2.5': 'B-6-日均PM2.5-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_pm], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            data_aod_outcome = data_aod_outcome.drop(columns=["X", "Y"])
            #########PM2.5############################
            '''
            data_to_merge_sky_daily = pd.read_excel(data_sky_daily + area + ".xlsx")
            data_to_merge_sky_daily = data_to_merge_sky_daily.set_index('日期')
            for c_name in data_to_merge_sky_daily.columns:
                data_to_merge_sky_daily.rename(columns={c_name: 'B-6-' + c_name + '-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_daily], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ######################日均#########
            data_to_merge_sky_hourly = pd.read_excel(data_sky_hourly + area + ".xlsx")
            data_to_merge_sky_hourly = data_to_merge_sky_hourly.set_index('日期')
            for d_name in data_to_merge_sky_hourly.columns:
                if d_name != "temperature":
                    del data_to_merge_sky_hourly[d_name]
            data_to_merge_sky_hourly.rename(columns={"temperature": 'B-6-temperature-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_hourly["B-6-temperature-%s" % xi]],
                                         axis=1, join_axes=[data_aod_outcome.index])  # 合并
            '''
    for c_name_2 in data_aod_outcome.columns:
        data_aod_outcome[c_name_2] = data_aod_outcome[c_name_2].fillna(0)
    #######均值部分#############
    # 删除 Time变量 不然 下面的接着的循环 会出现 【最高温，最高温时间】这种列表
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "Time" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass
    for bianliang in var_x:
        bianliang_list = []
        for item_xx in data_aod_outcome.columns:
            if "B-6-" + bianliang in item_xx:
                bianliang_list.append(item_xx)
        if len(bianliang_list) != 0:
            data_aod_outcome["B6-%s-MEAN" % bianliang] = data_aod_outcome[bianliang_list].mean(axis=1)
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "B-6-" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass

    ##################################################################B7

    if len(same_area_B7) != 0:
        xi = 0
        for area in same_area_B7:
            xi = xi + 1
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            data_to_merge.rename(columns={'监测站': 'B-7-监测站-%s' % xi, 'AOD值': 'B-7-AOD值-%s' % xi}, inplace=True)  # 重命名
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ##########以上几行完成了AOD
            data_to_merge_pm = pd.read_excel(data_pm + area + ".xlsx")
            data_to_merge_pm = data_to_merge_pm.set_index('日期')
            data_to_merge_pm.rename(columns={'日均PM2.5': 'B-7-日均PM2.5-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_pm], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            data_aod_outcome = data_aod_outcome.drop(columns=["X", "Y"])
            #########PM2.5############################
            '''
            data_to_merge_sky_daily = pd.read_excel(data_sky_daily + area + ".xlsx")
            data_to_merge_sky_daily = data_to_merge_sky_daily.set_index('日期')
            for c_name in data_to_merge_sky_daily.columns:
                data_to_merge_sky_daily.rename(columns={c_name: 'B-7-' + c_name + '-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_daily], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ######################日均#########
            data_to_merge_sky_hourly = pd.read_excel(data_sky_hourly + area + ".xlsx")
            data_to_merge_sky_hourly = data_to_merge_sky_hourly.set_index('日期')
            for d_name in data_to_merge_sky_hourly.columns:
                if d_name != "temperature":
                    del data_to_merge_sky_hourly[d_name]
            data_to_merge_sky_hourly.rename(columns={"temperature": 'B-7-temperature-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_hourly["B-7-temperature-%s" % xi]],
                                         axis=1, join_axes=[data_aod_outcome.index])  # 合并
            '''
    for c_name_2 in data_aod_outcome.columns:
        data_aod_outcome[c_name_2] = data_aod_outcome[c_name_2].fillna(0)
    #######均值部分#############
    # 删除 Time变量 不然 下面的接着的循环 会出现 【最高温，最高温时间】这种列表
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "Time" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass
    for bianliang in var_x:
        bianliang_list = []
        for item_xx in data_aod_outcome.columns:
            if "B-7-" + bianliang in item_xx:
                bianliang_list.append(item_xx)
        if len(bianliang_list) != 0:
            data_aod_outcome["B7-%s-MEAN" % bianliang] = data_aod_outcome[bianliang_list].mean(axis=1)
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "B-7-" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass

    ##################################################################B8

    if len(same_area_B8) != 0:
        xi = 0
        for area in same_area_B8:
            xi = xi + 1
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            data_to_merge.rename(columns={'监测站': 'B-8-监测站-%s' % xi, 'AOD值': 'B-8-AOD值-%s' % xi}, inplace=True)  # 重命名
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ##########以上几行完成了AOD
            data_to_merge_pm = pd.read_excel(data_pm + area + ".xlsx")
            data_to_merge_pm = data_to_merge_pm.set_index('日期')
            data_to_merge_pm.rename(columns={'日均PM2.5': 'B-8-日均PM2.5-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_pm], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            data_aod_outcome = data_aod_outcome.drop(columns=["X", "Y"])
            #########PM2.5############################
            '''
            data_to_merge_sky_daily = pd.read_excel(data_sky_daily + area + ".xlsx")
            data_to_merge_sky_daily = data_to_merge_sky_daily.set_index('日期')
            for c_name in data_to_merge_sky_daily.columns:
                data_to_merge_sky_daily.rename(columns={c_name: 'B-8-' + c_name + '-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_daily], axis=1,
                                         join_axes=[data_aod_outcome.index])  # 合并
            ######################日均#########
            data_to_merge_sky_hourly = pd.read_excel(data_sky_hourly + area + ".xlsx")
            data_to_merge_sky_hourly = data_to_merge_sky_hourly.set_index('日期')
            for d_name in data_to_merge_sky_hourly.columns:
                if d_name != "temperature":
                    del data_to_merge_sky_hourly[d_name]
            data_to_merge_sky_hourly.rename(columns={"temperature": 'B-8-temperature-%s' % xi}, inplace=True)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_hourly["B-8-temperature-%s" % xi]],
                                         axis=1, join_axes=[data_aod_outcome.index])  # 合并
            '''
    for c_name_2 in data_aod_outcome.columns:
        data_aod_outcome[c_name_2] = data_aod_outcome[c_name_2].fillna(0)
    #######均值部分#############
    # 删除 Time变量 不然 下面的接着的循环 会出现 【最高温，最高温时间】这种列表
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "Time" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass
    for bianliang in var_x:
        bianliang_list = []
        for item_xx in data_aod_outcome.columns:
            if "B-8-" + bianliang in item_xx:
                bianliang_list.append(item_xx)
        if len(bianliang_list) != 0:
            data_aod_outcome["B8-%s-MEAN" % bianliang] = data_aod_outcome[bianliang_list].mean(axis=1)
    for item_2 in data_aod_outcome.columns:  # 删除多的
        if "B-8-" in item_2:
            del data_aod_outcome[item_2]
        else:
            pass


    ############################################合并自己的数据########################################################
    #input_AOD = "F:\\毕业论文程序\\气溶胶光学厚度\\日均\\"+location+".xlsx"
    input_sky = "F:\\毕业论文程序\\气象数据\\整理\\日均\\2018\\"+location+".xlsx"
    input_PM = "F:\\毕业论文程序\\污染物浓度\\整理\\日均\\2018\\"+location+".xlsx"
    input_temperature_mean = "F:\\毕业论文程序\\气象数据\\整理\\逐时均值\\2018\\"+location+".xlsx"
    data_PM = pd.read_excel(input_PM, index_col="日期")
    #data_aod = pd.read_excel(input_AOD, index_col="日期")
    data_sky = pd.read_excel(input_sky, index_col='日期')
    # print(data_sky.head())
    # 这里是插入一天内气温的平均值
    data_temperature_mean = pd.read_excel(input_temperature_mean, index_col='日期')
    data_temperature_mean = data_temperature_mean["temperature"]
    #print(data_temperature_mean, location)  # 检测后发现索引列统一,没有问题
    # 合并数据
    #data = pd.concat([data_PM, data_aod_outcome, data_sky, data_temperature_mean], axis=1, sort=True)  # 会保留所有索引
    data_final = pd.concat([data_PM, data_aod_outcome, data_sky, data_temperature_mean], axis=1, join_axes=[data_aod_outcome.index])
    # print(data.head())
    # print(data.isnull().sum())  # 空值检查
    for cx_name_2 in data_final.columns:
        data_final[cx_name_2] = data_final[cx_name_2].fillna(0)
    data_final.to_excel("F:\\毕业论文程序\\整合数据\\整合2\\%s.xlsx" % location)
   # print(location)
