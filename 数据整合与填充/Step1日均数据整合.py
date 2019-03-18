# -*- coding: utf-8 -*-
# 日期: 2019/2/25 16:52
# 作者: xcl
# 工具：PyCharm

import pandas as pd
import numpy as np
import os

input_file_path = "F:\\毕业论文程序\\气象数据\\整理\\日均\\"
input_file_name = os.listdir(input_file_path)  # 文件名列表
print(len(input_file_name))

for file_name in input_file_name:
    # 读取数据
    input_AOD = "F:\\毕业论文程序\\气溶胶光学厚度\\日均\\"+file_name
    input_sky = "F:\\毕业论文程序\\气象数据\\整理\\日均\\"+file_name
    input_PM = "F:\\毕业论文程序\\污染物浓度\\整理\\日均\\"+file_name
    input_temperature_mean = "F:\\毕业论文程序\\气象数据\\整理\\逐时均值\\"+file_name
    output_name = input_AOD.replace("F:\\毕业论文程序\\气溶胶光学厚度\\日均\\", "")
    output_name = output_name.replace(".xlsx", "")
    data_PM = pd.read_excel(input_PM, index_col="日期")
    data_aod = pd.read_excel(input_AOD, index_col="日期")
    data_sky = pd.read_excel(input_sky, index_col='日期')
    # print(data_sky.head())
    # 这里是插入一天内气温的平均值
    data_temperature_mean = pd.read_excel(input_temperature_mean, index_col='日期')
    data_temperature_mean = data_temperature_mean["temperature"]
    # 合并数据
    data = pd.concat([data_PM, data_aod, data_sky, data_temperature_mean], axis=1, sort=True)  # 会保留所有索引
    # print(data.head())
    # print(data.isnull().sum())  # 空值检查

    # 处理残缺值

    indexs = list(data[np.isnan(data['AOD值'])].index)  # 获取AOD值为空的数据的索引
    data = data.drop(indexs)  # 删除
    # 删除PM2.5为空的数据
    # data = data[data["PM2.5浓度"] > 0]
    data = data[data["日均PM2.5"] > 0]
    # 日均下日期已经为dt.date
    # data.index = data.index.date  # 如果报错, 尝试dt.date
    data["日期"] = data.index
    data = data.set_index('日期')

    # 输出文件,格式xls
    if len(data["AOD值"]) > 1:
        data.to_excel("F:\\毕业论文程序\\整合数据\\各监测站\\日均\\%s.xlsx" % output_name)  # 用于ArcGIS 10.2 Map
