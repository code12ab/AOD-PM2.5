# -*- coding: utf-8 -*-
# 日期: 2019/2/25 16:52
# 作者: xcl
# 工具：PyCharm

import pandas as pd
import numpy as np
import os

input_file_path = "F:\\毕业论文程序\\气象数据\\整理\\combine\\"
input_file_name = os.listdir(input_file_path)  # 文件名列表

for file_name in input_file_name:
    # 读取数据
    input_AOD = "F:\\毕业论文程序\\气溶胶光学厚度\\combine\\"+file_name
    input_sky = "F:\\毕业论文程序\\气象数据\\整理\\combine\\"+file_name
    input_PM = "F:\\毕业论文程序\\污染物浓度\\整理\\combine\\"+file_name
    output_name = input_AOD.replace("F:\\毕业论文程序\\气溶胶光学厚度\\combine\\", "")
    output_name = output_name.replace(".xlsx", "")
    data_PM = pd.read_excel(input_PM, index_col="日期")
    data_aod = pd.read_excel(input_AOD, index_col="日期")
    data_sky = pd.read_excel(input_sky, index_col='日期')
    # 合并数据
    data = pd.concat([data_PM, data_aod, data_sky], axis=1)
    # print(data.isnull().sum())  # 空值检查

    # 处理残缺值
    # 删除AOD值为空的数据
    indexs = list(data[np.isnan(data['AOD值'])].index)  # 获取AOD值为空的数据的索引
    data = data.drop(indexs)  # 删除
    # 删除PM2.5为空的数据
    data = data[data["PM2.5浓度"] > 0]
    data.index = data.index.date
    data["日期"] = data.index
    data = data.set_index('日期')
    # 输出文件,格式xls
    data.to_excel("F:\\毕业论文程序\\整合数据\\各监测站\\combine\\%s.xlsx" % output_name)  # 用于ArcGIS 10.2 Map
