# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/6/26 21:16


################################ for循环,相对简练的代码;但仍可以合并A与B两类进一步简化
################################ 自身的数据 相邻站点的PM、AOD数据

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
coordinate_file_path = "D:\\毕业论文程序\\MODIS\\坐标\\"
JCZ_file = pd.read_excel(coordinate_file_path + "监测站坐标toDarkSkyAPI.xlsx", sheet_name="汇总")  # 监测站坐标toDarkSkyAPI


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
data_aod = "D:\\毕业论文程序\\气溶胶光学厚度\\日均\\2018\\"
data_pm = 'D:\\毕业论文程序\\污染物浓度\\整理\\日均\\2018\\'
data_sky_daily = "D:\\毕业论文程序\\气象数据\\整理\\日均\\2018\\"
data_sky_hourly = "D:\\毕业论文程序\\气象数据\\整理\\逐时均值\\2018\\"


for location in data_location["name"]:
    #print(data_location[data_location["name"] == location])  # 按行输出
    data_aod_outcome = pd.read_excel(data_aod + location + ".xlsx")
    data_aod_outcome = data_aod_outcome.set_index('日期')
    data_need_to_extract = data_location[data_location["name"] == location]

    # 批量生成列表
    def creat_list_A(a, num):
        global t_A
        class test(object):
            def __init__(self):
                pass
        t_A = test()
        for ix in range(1, num):
            setattr(t_A, "same_area_%s" % a + str(ix), [])
        # print(t.__dict__)
        # print(t.a1)
    def creat_list_B(a, num):
        global t_B
        class test(object):
            def __init__(self):
                pass
        t_B = test()
        for ix in range(1, num):
            setattr(t_B, "same_area_%s" % a + str(ix), [])
        # print(t.__dict__)
        # print(t.a1)

    creat_list_A("A", 9)
    creat_list_B("B", 9)

    # 对应位置的监测站添加进对应列表
    for element in data_need_to_extract.columns:
        value_1 = data_need_to_extract[element].values  # 每个单元格的值
        for i in range(1, 9):
            if value_1 == "A-%s" % i:
                exec('t_A.same_area_%s%s.append(element)' % ("A", i))  # 把添加进列表
    for element in data_need_to_extract.columns:
        value_1 = data_need_to_extract[element].values  # 每个单元格的值
        for i in range(1, 9):
            if value_1 == "B-%s" % i:
                exec('t_B.same_area_%s%s.append(element)' % ("B", i))  # 把添加进列表
    #print(location, t_B.same_area_B4)
    '''
    #######################  BUG ################## 暂时停用 ####################### 提示没有对应的列表属性
    for dis_ab in list(["A", "B"]):
        creat_list(dis_ab, 9)
        for element in data_need_to_extract.columns:
            value_1 = data_need_to_extract[element].values  # 每个单元格的值
            # print(value_1)
            for j in range(1, 9):
                # print(i)
                if value_1 == "%s-%s" % (dis_ab, j):
                    exec('t.same_area_%s%s.append(element)' % (dis_ab, j))  # 把添加进列表
        print(dir(t))
        print(t.same_area_B2, )
    '''
    ###########################################AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    for ixx in range(1, 9):
        t_A_object = "same_area_A"+str(ixx)

        if len(t_A.__getattribute__("same_area_A"+str(ixx))) != 0:
            xi = 0
            for area in t_A.__getattribute__("same_area_A"+str(ixx)):
                xi = xi + 1
                data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
                data_to_merge = data_to_merge.set_index('日期')
                data_to_merge.rename(columns={'监测站': 'A-%s-监测站-%s' % (ixx, xi), 'AOD值': 'A-%s-AOD值-%s' % (ixx, xi)}, inplace=True)  # 重命名
                data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                             join_axes=[data_aod_outcome.index])  # 合并
                ##########以上几行完成了AOD
                data_to_merge_pm = pd.read_excel(data_pm + area + ".xlsx")
                data_to_merge_pm = data_to_merge_pm.set_index('日期')
                data_to_merge_pm.rename(columns={'日均PM2.5': 'A-%s-日均PM2.5-%s' % (ixx, xi)}, inplace=True)
                data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_pm], axis=1,
                                             join_axes=[data_aod_outcome.index])  # 合并
                data_aod_outcome = data_aod_outcome.drop(columns=["X", "Y"])
                #########PM2.5############################3
                '''
                data_to_merge_sky_daily = pd.read_excel(data_sky_daily + area + ".xlsx")
                data_to_merge_sky_daily = data_to_merge_sky_daily.set_index('日期')
                for c_name in data_to_merge_sky_daily.columns:
                    data_to_merge_sky_daily.rename(columns={c_name: 'A-%s-' % ixx + c_name + '-%s' % xi}, inplace=True)
                data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_daily], axis=1,
                                             join_axes=[data_aod_outcome.index])  # 合并
                ######################以上完成天气日均#########
                data_to_merge_sky_hourly = pd.read_excel(data_sky_hourly + area + ".xlsx")
                data_to_merge_sky_hourly = data_to_merge_sky_hourly.set_index('日期')
                for d_name in data_to_merge_sky_hourly.columns:
                    if d_name != "temperature":
                        del data_to_merge_sky_hourly[d_name]
                data_to_merge_sky_hourly.rename(columns={"temperature": 'A-%s-temperature-%s' % (ixx, xi)}, inplace=True)
                data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_hourly["A-%s-temperature-%s" % (ixx, xi)]],
                                             axis=1, join_axes=[data_aod_outcome.index])  # 合并
                #######################以上完成气温，从逐时中提取出的日均值，文件本事已经处理为均值###########
                '''
        data_aod_outcome["监测站"] = data_aod_outcome["监测站"].fillna(method='pad')  # 监测站特殊处理
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
                if "A-%s-" % ixx + bianliang in item_xx:
                    bianliang_list.append(item_xx)
            if len(bianliang_list) != 0:
                data_aod_outcome["A%s-%s-MEAN" % (ixx, bianliang)] = data_aod_outcome[bianliang_list].mean(axis=1)
        for item_2 in data_aod_outcome.columns:  # 删除多的
            if "A-%s-" % ixx in item_2:
                del data_aod_outcome[item_2]
            else:
                pass
###########################################BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
    for ixx in range(1, 9):
        t_B_object = "same_area_B"+str(ixx)

        if len(t_B.__getattribute__("same_area_B"+str(ixx))) != 0:
            xi = 0
            for area in t_B.__getattribute__("same_area_B"+str(ixx)):
                xi = xi + 1
                data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
                data_to_merge = data_to_merge.set_index('日期')
                data_to_merge.rename(columns={'监测站': 'B-%s-监测站-%s' % (ixx, xi), 'AOD值': 'B-%s-AOD值-%s' % (ixx, xi)}, inplace=True)  # 重命名
                data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                             join_axes=[data_aod_outcome.index])  # 合并
                ##########以上几行完成了AOD
                data_to_merge_pm = pd.read_excel(data_pm + area + ".xlsx")
                data_to_merge_pm = data_to_merge_pm.set_index('日期')
                data_to_merge_pm.rename(columns={'日均PM2.5': 'B-%s-日均PM2.5-%s' % (ixx, xi)}, inplace=True)
                data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_pm], axis=1,
                                             join_axes=[data_aod_outcome.index])  # 合并
                data_aod_outcome = data_aod_outcome.drop(columns=["X", "Y"])
                #########PM2.5############################3
                '''
                data_to_merge_sky_daily = pd.read_excel(data_sky_daily + area + ".xlsx")
                data_to_merge_sky_daily = data_to_merge_sky_daily.set_index('日期')
                for c_name in data_to_merge_sky_daily.columns:
                    data_to_merge_sky_daily.rename(columns={c_name: 'B-%s-' % ixx + c_name + '-%s' % xi}, inplace=True)
                data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_daily], axis=1,
                                             join_axes=[data_aod_outcome.index])  # 合并
                ######################以上完成天气日均#########
                data_to_merge_sky_hourly = pd.read_excel(data_sky_hourly + area + ".xlsx")
                data_to_merge_sky_hourly = data_to_merge_sky_hourly.set_index('日期')
                for d_name in data_to_merge_sky_hourly.columns:
                    if d_name != "temperature":
                        del data_to_merge_sky_hourly[d_name]
                data_to_merge_sky_hourly.rename(columns={"temperature": 'B-%s-temperature-%s' % (ixx, xi)}, inplace=True)
                data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_sky_hourly["B-%s-temperature-%s" % (ixx, xi)]],
                                             axis=1, join_axes=[data_aod_outcome.index])  # 合并
                #######################以上完成气温，从逐时中提取出的日均值，文件本事已经处理为均值###########
                '''
        data_aod_outcome["监测站"] = data_aod_outcome["监测站"].fillna(method='pad')  # 监测站特殊处理
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
                if "B-%s-" % ixx + bianliang in item_xx:
                    bianliang_list.append(item_xx)
            if len(bianliang_list) != 0:
                data_aod_outcome["B%s-%s-MEAN" % (ixx, bianliang)] = data_aod_outcome[bianliang_list].mean(axis=1)
        for item_2 in data_aod_outcome.columns:  # 删除多的
            if "B-%s-" % ixx in item_2:
                del data_aod_outcome[item_2]
            else:
                pass

    ############################################合并自己的数据########################################################
    #input_AOD = "D:\\毕业论文程序\\气溶胶光学厚度\\日均\\"+location+".xlsx"
    input_sky = "D:\\毕业论文程序\\气象数据\\整理\\日均\\2018\\"+location+".xlsx"
    input_PM = "D:\\毕业论文程序\\污染物浓度\\整理\\日均\\2018\\"+location+".xlsx"
    input_temperature_mean = "D:\\毕业论文程序\\气象数据\\整理\\逐时均值\\2018\\"+location+".xlsx"
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

    data_final["监测站"] = data_final["监测站"].fillna(method='pad')  # 监测站特殊处理
    for cx_name_2 in data_final.columns:
        data_final[cx_name_2] = data_final[cx_name_2].fillna(0)
    data_final.to_excel("D:\\毕业论文程序\\整合数据\\自身与相邻站点PM_AOD\\2018\\%s.xlsx" % location)
    print("完成", location)
    # print(location)
