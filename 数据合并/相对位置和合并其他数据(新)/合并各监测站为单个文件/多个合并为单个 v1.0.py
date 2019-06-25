# -*- coding: utf-8 -*-
# 日期: 2019/6/9 14:47
# 作者: xcl
# 工具：PyCharm


import pandas as pd
import numpy as np
import os

input_file_path = "D:\\毕业论文程序\\整合数据\\T-1\\"
input_file_name = os.listdir(input_file_path)  # 文件名列表
print("文件个数:"+str(len(input_file_name)))

list_1 = []
for file_name in input_file_name:
    print("处理监测站:"+file_name)
    data_1 = pd.read_excel(input_file_path + file_name)
    list_1.append(data_1)

print("####################################开始合并###################################")
result = pd.concat(list_1, sort=True, axis=0)
# 补0
for c_name_2 in result.columns:
    result[c_name_2] = result[c_name_2].fillna(0)

result.to_excel('相邻位置仅留PM和T-1.xlsx')


