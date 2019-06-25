# -*- coding: utf-8 -*-
# 日期: 2019/4/14 16:03
# 作者: xcl
# 工具：PyCharm


import pandas as pd
import numpy as np
import os


input_file_path = "F:\\毕业论文程序\\整合数据\\整合2\\"
outpu_file_path = "F:\\毕业论文程序\\整合数据\\T-1\\"
input_file_name = os.listdir(input_file_path)  # 文件名列表
print("文件个数:"+str(len(input_file_name)))


for file_name in input_file_name:
    print("处理监测站:"+file_name)
    data = pd.read_excel(input_file_path + file_name)
    data = data.set_index("日期")
    # t-1
    for ccc in data.columns:
        data["%s-t-1" % ccc] = data[ccc].shift(periods=1, axis=0)  # 下移动 列移动
    # 补0
    for cx_name_2 in data.columns:
        data[cx_name_2] = data[cx_name_2].fillna(0)
    # 存
    data.to_excel(outpu_file_path+file_name)
