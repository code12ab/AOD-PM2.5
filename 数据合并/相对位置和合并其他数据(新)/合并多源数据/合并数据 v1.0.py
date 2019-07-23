# -*- coding: utf-8 -*-
# 日期: 2019/6/8 15:59
# 作者: xcl
# 工具：PyCharm


# -*- coding: utf-8 -*-
# 日期: 2019/5/31 23:02
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
for location in data_location["name"]:
    #print(data_location[data_location["name"] == location])  # 按行输出
    data_aod_outcome = pd.read_excel(data_aod + location + ".xlsx")
    data_aod_outcome = data_aod_outcome.set_index('日期')
    data_need_to_extract = data_location[data_location["name"] == location]
    same_area = []
    for element in data_need_to_extract.columns:
        value_1 = data_need_to_extract[element].values  # 每个单元格的值
        #print(value_1)

        if value_1 == "A-1":  # 第一个区划
            #print(value_1)
            same_area.append(element)
    #print(same_area)
    if len(same_area) != 0:
        xi = 0
        for area in same_area:
            xi = xi + 1
            #print(area)
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            # print(data_to_merge.head())
            # 尝试把列名改成A-4-xxx 多一个 - 方便 删除
            data_to_merge.rename(columns={'监测站': 'A-1-监测站-%s' % xi, 'AOD值': 'A-1-AOD值-%s' % xi}, inplace=True)
            #print(data_to_merge.head())
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1, join_axes=[data_aod_outcome.index])
            data_aod_outcome['A-1-AOD值-%s' % xi] = data_aod_outcome['A-1-AOD值-%s' % xi].fillna(0)
    else:
        print("无临近监测站")
    '''
    if xi != 0:
        for xj in range(1, xi+1):
            print(xj)
    '''
    item_add = []
    for item in data_aod_outcome.columns:

        if "A-1-AOD值" in item:
            item_add.append(item)
            #print(item)
        else:
            pass

    if len(item_add) != 0:
        data_aod_outcome["A1-AOD-MEAN"] = data_aod_outcome[item_add].mean(axis=1)  # 均值换轴
    #    print("jisuanyici")

    for item_2 in data_aod_outcome.columns:
        if "A-1-" in item_2:
            data_aod_outcome = data_aod_outcome.drop(columns=[item_2])
            #print(item_2)
        else:
            pass



    #print(data_aod_outcome[item_add])
    print(data_aod_outcome.head())

    data_aod_outcome.to_excel("F:\\毕业论文程序\\整合数据\\整合1\\%s.xlsx" % location)

