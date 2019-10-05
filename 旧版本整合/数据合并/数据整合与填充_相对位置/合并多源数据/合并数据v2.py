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

# -------------------------- 到此,已经完成了关于【相对位置+距离】的交叉表格----------------------------
# 表格结果为 列标题在行标题的第*分类上

data_location = pd.read_excel("table3.xlsx")
# print(data_location.head())
data_aod = "F:\\毕业论文程序\\气溶胶光学厚度\\日均\\"
data_pm = 'F:\\毕业论文程序\\污染物浓度\\整理\\日均\\'
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
            # print(data_to_merge.head())
            # 尝试把列名改成A-4-xxx 多一个 - 方便 删除
            data_to_merge.rename(columns={'监测站': 'A-1-监测站-%s' % xi, 'AOD值': 'A-1-AOD值-%s' % xi}, inplace=True)    # 重命名
            #print(data_to_merge.head())
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1, join_axes=[data_aod_outcome.index])  # 合并
            data_aod_outcome['A-1-AOD值-%s' % xi] = data_aod_outcome['A-1-AOD值-%s' % xi].fillna(0)
            ##########以上几行完成了AOD
            data_to_merge_pm = pd.read_excel(data_pm + area + ".xlsx")
            data_to_merge_pm = data_to_merge_pm.set_index('日期')
            data_to_merge_pm.rename(columns={'日均PM2.5': 'A-1-日均PM2.5-%s' % xi}, inplace=True)
            data_aod_outcome['A-1-日均PM2.5-%s' % xi] = data_aod_outcome['A-1-AOD值-%s' % xi].fillna(0)
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge_pm], axis=1,join_axes=[data_aod_outcome.index])  # 合并
            data_aod_outcome['A-1-日均PM2.5-%s' % xi] = data_aod_outcome['A-1-日均PM2.5-%s' % xi].fillna(0)
            data_aod_outcome = data_aod_outcome.drop(columns=["X", "Y"])
    else:
        print("无临近监测站")
    '''
    if xi != 0:
        for xj in range(1, xi+1):
            print(xj)
    '''
    #######均值部分#############
    item_add = []
    item_add_pm = []
    for item in data_aod_outcome.columns:
        if "A-1-AOD值" in item:
            item_add.append(item)
            #print(item)
        elif "A-1-日均" in data_aod_outcome.columns:
            item_add_pm.append(item)
        else:
            pass
    if len(item_add) != 0:
        data_aod_outcome["A1-AOD-MEAN"] = data_aod_outcome[item_add].mean(axis=1)  # 均值换轴
    #    print("jisuanyici")

    if len(item_add_pm) != 0:
        data_aod_outcome["A1-PM-MEAN"] = data_aod_outcome[item_add_pm].mean(axis=1)  # 均值换轴

    print(data_aod_outcome.head())
    #print(data_aod_outcome.columns)
    for item_2 in data_aod_outcome.columns: # 删除多的
        if "A-1-" in item_2:
            print(item_2)
            #data_aod_outcome = data_aod_outcome.drop(columns='A-1-日均PM2.5-1',axis=0)
            del data_aod_outcome[item_2]
        else:
            pass
#########################################################################A2
    if len(same_area_A2) != 0:
        xi = 0
        for area in same_area_A2:
            xi = xi + 1
            #print(area)
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            # print(data_to_merge.head())
            # 尝试把列名改成A-4-xxx 多一个 - 方便 删除
            data_to_merge.rename(columns={'监测站': 'A-2-监测站-%s' % xi, 'AOD值': 'A-2-AOD值-%s' % xi}, inplace=True)
            #print(data_to_merge.head())
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1, join_axes=[data_aod_outcome.index])
            data_aod_outcome['A-2-AOD值-%s' % xi] = data_aod_outcome['A-2-AOD值-%s' % xi].fillna(0)
    else:
        print("无临近监测站")
    '''
    if xi != 0:
        for xj in range(1, xi+1):
            print(xj)
    '''
    item_add = []
    for item in data_aod_outcome.columns:
        if "A-2-AOD值" in item:
            item_add.append(item)
            #print(item)
        else:
            pass
    if len(item_add) != 0:
        data_aod_outcome["A2-AOD-MEAN"] = data_aod_outcome[item_add].mean(axis=1)  # 均值换轴
    #    print("jisuanyici")
    for item_2 in data_aod_outcome.columns:
        if "A-2-" in item_2:
            data_aod_outcome = data_aod_outcome.drop(columns=[item_2])
            #print(item_2)
        else:
            pass

    #########################################################################A3
    if len(same_area_A3) != 0:
        xi = 0
        for area in same_area_A3:
            xi = xi + 1
            # print(area)
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            # print(data_to_merge.head())
            # 尝试把列名改成A-4-xxx 多一个 - 方便 删除
            data_to_merge.rename(columns={'监测站': 'A-3-监测站-%s' % xi, 'AOD值': 'A-3-AOD值-%s' % xi}, inplace=True)
            # print(data_to_merge.head())
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])
            data_aod_outcome['A-3-AOD值-%s' % xi] = data_aod_outcome['A-3-AOD值-%s' % xi].fillna(0)
    else:
        print("无临近监测站")
    '''
    if xi != 0:
        for xj in range(1, xi+1):
            print(xj)
    '''
    item_add = []
    for item in data_aod_outcome.columns:
        if "A-3-AOD值" in item:
            item_add.append(item)
            # print(item)
        else:
            pass
    if len(item_add) != 0:
        data_aod_outcome["A3-AOD-MEAN"] = data_aod_outcome[item_add].mean(axis=1)  # 均值换轴
    #    print("jisuanyici")
    for item_2 in data_aod_outcome.columns:
        if "A-3-" in item_2:
            data_aod_outcome = data_aod_outcome.drop(columns=[item_2])
            # print(item_2)
        else:
            pass

    #########################################################################A4
    if len(same_area_A4) != 0:
        xi = 0
        for area in same_area_A4:
            xi = xi + 1
            # print(area)
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            # print(data_to_merge.head())
            # 尝试把列名改成A-4-xxx 多一个 - 方便 删除
            data_to_merge.rename(columns={'监测站': 'A-4-监测站-%s' % xi, 'AOD值': 'A-4-AOD值-%s' % xi}, inplace=True)
            # print(data_to_merge.head())
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])
            data_aod_outcome['A-4-AOD值-%s' % xi] = data_aod_outcome['A-4-AOD值-%s' % xi].fillna(0)
    else:
        print("无临近监测站")
    '''
    if xi != 0:
        for xj in range(1, xi+1):
            print(xj)
    '''
    item_add = []
    for item in data_aod_outcome.columns:
        if "A-4-AOD值" in item:
            item_add.append(item)
            # print(item)
        else:
            pass
    if len(item_add) != 0:
        data_aod_outcome["A4-AOD-MEAN"] = data_aod_outcome[item_add].mean(axis=1)  # 均值换轴
    #    print("jisuanyici")
    for item_2 in data_aod_outcome.columns:
        if "A-4-" in item_2:
            data_aod_outcome = data_aod_outcome.drop(columns=[item_2])
            # print(item_2)
        else:
            pass


    #########################################################################A5
    if len(same_area_A5) != 0:
        xi = 0
        for area in same_area_A5:
            xi = xi + 1
            # print(area)
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            # print(data_to_merge.head())
            # 尝试把列名改成A-4-xxx 多一个 - 方便 删除
            data_to_merge.rename(columns={'监测站': 'A-5-监测站-%s' % xi, 'AOD值': 'A-5-AOD值-%s' % xi}, inplace=True)
            # print(data_to_merge.head())
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])
            data_aod_outcome['A-5-AOD值-%s' % xi] = data_aod_outcome['A-5-AOD值-%s' % xi].fillna(0)
    else:
        print("无临近监测站")
    '''
    if xi != 0:
        for xj in range(1, xi+1):
            print(xj)
    '''
    item_add = []
    for item in data_aod_outcome.columns:
        if "A-5-AOD值" in item:
            item_add.append(item)
            # print(item)
        else:
            pass
    if len(item_add) != 0:
        data_aod_outcome["A5-AOD-MEAN"] = data_aod_outcome[item_add].mean(axis=1)  # 均值换轴
    #    print("jisuanyici")
    for item_2 in data_aod_outcome.columns:
        if "A-5-" in item_2:
            data_aod_outcome = data_aod_outcome.drop(columns=[item_2])
            # print(item_2)
        else:
            pass


    #########################################################################A6
    if len(same_area_A6) != 0:
        xi = 0
        for area in same_area_A6:
            xi = xi + 1
            # print(area)
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            # print(data_to_merge.head())
            # 尝试把列名改成A-4-xxx 多一个 - 方便 删除
            data_to_merge.rename(columns={'监测站': 'A-6-监测站-%s' % xi, 'AOD值': 'A-6-AOD值-%s' % xi}, inplace=True)
            # print(data_to_merge.head())
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])
            data_aod_outcome['A-6-AOD值-%s' % xi] = data_aod_outcome['A-6-AOD值-%s' % xi].fillna(0)
    else:
        print("无临近监测站")
    '''
    if xi != 0:
        for xj in range(1, xi+1):
            print(xj)
    '''
    item_add = []
    for item in data_aod_outcome.columns:
        if "A-6-AOD值" in item:
            item_add.append(item)
            # print(item)
        else:
            pass
    if len(item_add) != 0:
        data_aod_outcome["A6-AOD-MEAN"] = data_aod_outcome[item_add].mean(axis=1)  # 均值换轴
    #    print("jisuanyici")
    for item_2 in data_aod_outcome.columns:
        if "A-6-" in item_2:
            data_aod_outcome = data_aod_outcome.drop(columns=[item_2])
            # print(item_2)
        else:
            pass


    #########################################################################A7
    if len(same_area_A7) != 0:
        xi = 0
        for area in same_area_A7:
            xi = xi + 1
            # print(area)
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            # print(data_to_merge.head())
            # 尝试把列名改成A-4-xxx 多一个 - 方便 删除
            data_to_merge.rename(columns={'监测站': 'A-7-监测站-%s' % xi, 'AOD值': 'A-7-AOD值-%s' % xi}, inplace=True)
            # print(data_to_merge.head())
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])
            data_aod_outcome['A-7-AOD值-%s' % xi] = data_aod_outcome['A-7-AOD值-%s' % xi].fillna(0)
    else:
        print("无临近监测站")
    '''
    if xi != 0:
        for xj in range(1, xi+1):
            print(xj)
    '''
    item_add = []
    for item in data_aod_outcome.columns:
        if "A-7-AOD值" in item:
            item_add.append(item)
            # print(item)
        else:
            pass
    if len(item_add) != 0:
        data_aod_outcome["A7-AOD-MEAN"] = data_aod_outcome[item_add].mean(axis=1)  # 均值换轴
    #    print("jisuanyici")
    for item_2 in data_aod_outcome.columns:
        if "A-7-" in item_2:
            data_aod_outcome = data_aod_outcome.drop(columns=[item_2])
            # print(item_2)
        else:
            pass


    #########################################################################A8
    if len(same_area_A8) != 0:
        xi = 0
        for area in same_area_A8:
            xi = xi + 1
            # print(area)
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            # print(data_to_merge.head())
            # 尝试把列名改成A-4-xxx 多一个 - 方便 删除
            data_to_merge.rename(columns={'监测站': 'A-8-监测站-%s' % xi, 'AOD值': 'A-8-AOD值-%s' % xi}, inplace=True)
            # print(data_to_merge.head())
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])
            data_aod_outcome['A-8-AOD值-%s' % xi] = data_aod_outcome['A-8-AOD值-%s' % xi].fillna(0)
    else:
        print("无临近监测站")
    '''
    if xi != 0:
        for xj in range(1, xi+1):
            print(xj)
    '''
    item_add = []
    for item in data_aod_outcome.columns:
        if "A-8-AOD值" in item:
            item_add.append(item)
            # print(item)
        else:
            pass
    if len(item_add) != 0:
        data_aod_outcome["A8-AOD-MEAN"] = data_aod_outcome[item_add].mean(axis=1)  # 均值换轴
    #    print("jisuanyici")
    for item_2 in data_aod_outcome.columns:
        if "A-8-" in item_2:
            data_aod_outcome = data_aod_outcome.drop(columns=[item_2])
            # print(item_2)
        else:
            pass

    #####################################################################合并部分2########################################

    if len(same_area_B1) != 0:
        xi = 0
        for area in same_area_B1:
            xi = xi + 1
            # print(area)
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            # print(data_to_merge.head())
            # 尝试把列名改成B-4-xxx 多一个 - 方便 删除
            data_to_merge.rename(columns={'监测站': 'B-1-监测站-%s' % xi, 'AOD值': 'B-1-AOD值-%s' % xi}, inplace=True)
            # print(data_to_merge.head())
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])
            data_aod_outcome['B-1-AOD值-%s' % xi] = data_aod_outcome['B-1-AOD值-%s' % xi].fillna(0)
    else:
        print("无临近监测站")
    '''
    if xi != 0:
        for xj in range(1, xi+1):
            print(xj)
    '''
    item_add = []
    for item in data_aod_outcome.columns:
        if "B-1-AOD值" in item:
            item_add.append(item)
            # print(item)
        else:
            pass
    if len(item_add) != 0:
        data_aod_outcome["B1-AOD-MEAN"] = data_aod_outcome[item_add].mean(axis=1)  # 均值换轴
    #    print("jisuanyici")
    for item_2 in data_aod_outcome.columns:
        if "B-1-" in item_2:
            data_aod_outcome = data_aod_outcome.drop(columns=[item_2])
            # print(item_2)
        else:
            pass
    #########################################################################B2
    if len(same_area_B2) != 0:
        xi = 0
        for area in same_area_B2:
            xi = xi + 1
            # print(area)
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            # print(data_to_merge.head())
            # 尝试把列名改成B-4-xxx 多一个 - 方便 删除
            data_to_merge.rename(columns={'监测站': 'B-2-监测站-%s' % xi, 'AOD值': 'B-2-AOD值-%s' % xi}, inplace=True)
            # print(data_to_merge.head())
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])
            data_aod_outcome['B-2-AOD值-%s' % xi] = data_aod_outcome['B-2-AOD值-%s' % xi].fillna(0)
    else:
        print("无临近监测站")
    '''
    if xi != 0:
        for xj in range(1, xi+1):
            print(xj)
    '''
    item_add = []
    for item in data_aod_outcome.columns:
        if "B-2-AOD值" in item:
            item_add.append(item)
            # print(item)
        else:
            pass
    if len(item_add) != 0:
        data_aod_outcome["B2-AOD-MEAN"] = data_aod_outcome[item_add].mean(axis=1)  # 均值换轴
    #    print("jisuanyici")
    for item_2 in data_aod_outcome.columns:
        if "B-2-" in item_2:
            data_aod_outcome = data_aod_outcome.drop(columns=[item_2])
            # print(item_2)
        else:
            pass

    #########################################################################B3
    if len(same_area_B3) != 0:
        xi = 0
        for area in same_area_B3:
            xi = xi + 1
            # print(area)
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            # print(data_to_merge.head())
            # 尝试把列名改成B-4-xxx 多一个 - 方便 删除
            data_to_merge.rename(columns={'监测站': 'B-3-监测站-%s' % xi, 'AOD值': 'B-3-AOD值-%s' % xi}, inplace=True)
            # print(data_to_merge.head())
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])
            data_aod_outcome['B-3-AOD值-%s' % xi] = data_aod_outcome['B-3-AOD值-%s' % xi].fillna(0)
    else:
        print("无临近监测站")
    '''
    if xi != 0:
        for xj in range(1, xi+1):
            print(xj)
    '''
    item_add = []
    for item in data_aod_outcome.columns:
        if "B-3-AOD值" in item:
            item_add.append(item)
            # print(item)
        else:
            pass
    if len(item_add) != 0:
        data_aod_outcome["B3-AOD-MEAN"] = data_aod_outcome[item_add].mean(axis=1)  # 均值换轴
    #    print("jisuanyici")
    for item_2 in data_aod_outcome.columns:
        if "B-3-" in item_2:
            data_aod_outcome = data_aod_outcome.drop(columns=[item_2])
            # print(item_2)
        else:
            pass

    #########################################################################B4
    if len(same_area_B4) != 0:
        xi = 0
        for area in same_area_B4:
            xi = xi + 1
            # print(area)
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            # print(data_to_merge.head())
            # 尝试把列名改成B-4-xxx 多一个 - 方便 删除
            data_to_merge.rename(columns={'监测站': 'B-4-监测站-%s' % xi, 'AOD值': 'B-4-AOD值-%s' % xi}, inplace=True)
            # print(data_to_merge.head())
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])
            data_aod_outcome['B-4-AOD值-%s' % xi] = data_aod_outcome['B-4-AOD值-%s' % xi].fillna(0)
    else:
        print("无临近监测站")
    '''
    if xi != 0:
        for xj in range(1, xi+1):
            print(xj)
    '''
    item_add = []
    for item in data_aod_outcome.columns:
        if "B-4-AOD值" in item:
            item_add.append(item)
            # print(item)
        else:
            pass
    if len(item_add) != 0:
        data_aod_outcome["B4-AOD-MEAN"] = data_aod_outcome[item_add].mean(axis=1)  # 均值换轴
    #    print("jisuanyici")
    for item_2 in data_aod_outcome.columns:
        if "B-4-" in item_2:
            data_aod_outcome = data_aod_outcome.drop(columns=[item_2])
            # print(item_2)
        else:
            pass

    #########################################################################B5
    if len(same_area_B5) != 0:
        xi = 0
        for area in same_area_B5:
            xi = xi + 1
            # print(area)
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            # print(data_to_merge.head())
            # 尝试把列名改成B-4-xxx 多一个 - 方便 删除
            data_to_merge.rename(columns={'监测站': 'B-5-监测站-%s' % xi, 'AOD值': 'B-5-AOD值-%s' % xi}, inplace=True)
            # print(data_to_merge.head())
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])
            data_aod_outcome['B-5-AOD值-%s' % xi] = data_aod_outcome['B-5-AOD值-%s' % xi].fillna(0)
    else:
        print("无临近监测站")
    '''
    if xi != 0:
        for xj in range(1, xi+1):
            print(xj)
    '''
    item_add = []
    for item in data_aod_outcome.columns:
        if "B-5-AOD值" in item:
            item_add.append(item)
            # print(item)
        else:
            pass
    if len(item_add) != 0:
        data_aod_outcome["B5-AOD-MEAN"] = data_aod_outcome[item_add].mean(axis=1)  # 均值换轴
    #    print("jisuanyici")
    for item_2 in data_aod_outcome.columns:
        if "B-5-" in item_2:
            data_aod_outcome = data_aod_outcome.drop(columns=[item_2])
            # print(item_2)
        else:
            pass

    #########################################################################B6
    if len(same_area_B6) != 0:
        xi = 0
        for area in same_area_B6:
            xi = xi + 1
            # print(area)
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            # print(data_to_merge.head())
            # 尝试把列名改成B-4-xxx 多一个 - 方便 删除
            data_to_merge.rename(columns={'监测站': 'B-6-监测站-%s' % xi, 'AOD值': 'B-6-AOD值-%s' % xi}, inplace=True)
            # print(data_to_merge.head())
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])
            data_aod_outcome['B-6-AOD值-%s' % xi] = data_aod_outcome['B-6-AOD值-%s' % xi].fillna(0)
    else:
        print("无临近监测站")
    '''
    if xi != 0:
        for xj in range(1, xi+1):
            print(xj)
    '''
    item_add = []
    for item in data_aod_outcome.columns:
        if "B-6-AOD值" in item:
            item_add.append(item)
            # print(item)
        else:
            pass
    if len(item_add) != 0:
        data_aod_outcome["B6-AOD-MEAN"] = data_aod_outcome[item_add].mean(axis=1)  # 均值换轴
    #    print("jisuanyici")
    for item_2 in data_aod_outcome.columns:
        if "B-6-" in item_2:
            data_aod_outcome = data_aod_outcome.drop(columns=[item_2])
            # print(item_2)
        else:
            pass

    #########################################################################B7
    if len(same_area_B7) != 0:
        xi = 0
        for area in same_area_B7:
            xi = xi + 1
            # print(area)
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            # print(data_to_merge.head())
            # 尝试把列名改成B-4-xxx 多一个 - 方便 删除
            data_to_merge.rename(columns={'监测站': 'B-7-监测站-%s' % xi, 'AOD值': 'B-7-AOD值-%s' % xi}, inplace=True)
            # print(data_to_merge.head())
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])
            data_aod_outcome['B-7-AOD值-%s' % xi] = data_aod_outcome['B-7-AOD值-%s' % xi].fillna(0)
    else:
        print("无临近监测站")
    '''
    if xi != 0:
        for xj in range(1, xi+1):
            print(xj)
    '''
    item_add = []
    for item in data_aod_outcome.columns:
        if "B-7-AOD值" in item:
            item_add.append(item)
            # print(item)
        else:
            pass
    if len(item_add) != 0:
        data_aod_outcome["B7-AOD-MEAN"] = data_aod_outcome[item_add].mean(axis=1)  # 均值换轴
    #    print("jisuanyici")
    for item_2 in data_aod_outcome.columns:
        if "B-7-" in item_2:
            data_aod_outcome = data_aod_outcome.drop(columns=[item_2])
            # print(item_2)
        else:
            pass

    #########################################################################B8
    if len(same_area_B8) != 0:
        xi = 0
        for area in same_area_B8:
            xi = xi + 1
            # print(area)
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            # print(data_to_merge.head())
            # 尝试把列名改成B-4-xxx 多一个 - 方便 删除
            data_to_merge.rename(columns={'监测站': 'B-8-监测站-%s' % xi, 'AOD值': 'B-8-AOD值-%s' % xi}, inplace=True)
            # print(data_to_merge.head())
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1,
                                         join_axes=[data_aod_outcome.index])
            data_aod_outcome['B-8-AOD值-%s' % xi] = data_aod_outcome['B-8-AOD值-%s' % xi].fillna(0)
    else:
        print("无临近监测站")
    '''
    if xi != 0:
        for xj in range(1, xi+1):
            print(xj)
    '''
    item_add = []
    for item in data_aod_outcome.columns:
        if "B-8-AOD值" in item:
            item_add.append(item)
            # print(item)
        else:
            pass
    if len(item_add) != 0:
        data_aod_outcome["B8-AOD-MEAN"] = data_aod_outcome[item_add].mean(axis=1)  # 均值换轴
    #    print("jisuanyici")
    for item_2 in data_aod_outcome.columns:
        if "B-8-" in item_2:
            data_aod_outcome = data_aod_outcome.drop(columns=[item_2])
            # print(item_2)
        else:
            pass




















































































































































































































    #print(data_aod_outcome[item_add])
    print(data_aod_outcome.head())

    data_aod_outcome.to_excel("F:\\毕业论文程序\\整合数据\\整合1\\%s.xlsx" % location)

