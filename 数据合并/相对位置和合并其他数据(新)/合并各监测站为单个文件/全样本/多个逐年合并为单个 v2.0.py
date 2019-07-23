# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/6/27 19:10

# -*- coding: utf-8 -*-
# 日期: 2019/6/27 14:47
# 作者: xcl
# 工具：PyCharm


import pandas as pd
import numpy as np
import os

input_file_path = "D:\\毕业论文程序\\整合数据\\汇总为单个文件_逐年\\"  # 不含2013
input_file_name = os.listdir(input_file_path)  # 文件名列表
output_file_path = "D:\\毕业论文程序\\整合数据\\汇总为单个文件_全样本\\"
print("文件个数:"+str(len(input_file_name)))

list_1 = []
for file_name in input_file_name:
    if "2013" not in file_name:
        print("处理监测站:"+file_name)
        data_1 = pd.read_excel(input_file_path + file_name)
        print(data_1["AOD值"][data_1["AOD值"] > 0].notnull().sum())
        list_1.append(data_1)
    else:
        print(str(file_name) + "不参与合并")
print("####################################开始合并###################################")
result = pd.concat(list_1, sort=True, axis=0)
# 补0
for c_name_2 in result.columns:
    result[c_name_2] = result[c_name_2].fillna(0)

result.to_excel(output_file_path + '自身与相邻站点PM_AOD_T-1_全样本.xlsx')


