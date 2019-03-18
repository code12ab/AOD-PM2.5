# -*- coding: utf-8 -*-
# 日期: 2019/3/7 8:51
# 作者: xcl
# 工具：PyCharm


import pandas as pd
import numpy as np
import os

input_file_path = "F:\\毕业论文程序\\气象数据\\整理\\Aqua\\"
input_file_name = os.listdir(input_file_path)  # 文件名列表

# 源

for file_name in input_file_name:
    # 读取数据
    input_AOD = "F:\\毕业论文程序\\气溶胶光学厚度\\Aqua\\"+file_name
    input_sky = "F:\\毕业论文程序\\气象数据\\整理\\Aqua\\"+file_name
    input_PM = "F:\\毕业论文程序\\污染物浓度\\整理\\Aqua\\"+file_name

    data_PM = pd.read_excel(input_PM, index_col="日期")
    data_aod = pd.read_excel(input_AOD, index_col="日期")
    data_sky = pd.read_excel(input_sky, index_col='日期')
    # 合并数据
    data = pd.concat([data_PM, data_aod, data_sky], axis=1)
    # print(data.isnull().sum())  # 空值检查

    count_1 = len(data_aod["AOD值"][data_aod["AOD值"] > 0])
    count_2 = len(data_PM["PM2.5浓度"][data_PM["PM2.5浓度"] > 0])
    count_3 = len(data_sky["pressure"][data_sky["pressure"] > 0])

    print(file_name, ":{AOD:", count_1, ";    PM2.5:", count_2, ";    SkyAPI:", count_3, "}")
'''
# 匹配后
input_file_path = "F:\\毕业论文程序\\整合数据\\各监测站\\Aqua\\"
input_file_name_match = os.listdir(input_file_path)  # 文件名列表
for file_name in input_file_name_match:
    # 读取数据
    input_file = "F:\\毕业论文程序\\整合数据\\各监测站\\Aqua\\"+file_name
    data = pd.read_excel(input_file, index_col="日期")
    count = len(data["AOD值"][data["AOD值"] > 0])
    print("匹配后", count)
'''