# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/18 20:41


# 库
import pandas as pd
import numpy as np
import os

# HDF文件位置
file_path = "d:\\myd2014_14\\"
# 下载列表
csv = "d:\\501368303.csv"
# 批量读取
dir_str = file_path  # 文件位置
file_name = os.listdir(dir_str)  # 文件名, 含'.hdf'
# 输出错误文件
error_file = []
# 检验
name_csv = pd.read_csv(csv)
print(name_csv.name)
for name in name_csv.name:
    if name in file_name:
        print(name, ",OK")
    elif "checksums_" in name:
        print(name, ",checksums")
    else:
        print(name, ",NOT OK")
        error_file.append(name)

# 结果
print(error_file)