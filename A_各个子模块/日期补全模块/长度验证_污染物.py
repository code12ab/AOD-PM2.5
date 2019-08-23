# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/23 13:58


# 库
import pandas as pd
import numpy as np
import math
from numpy import array
import os


for year in [2014, 2015, 2016, 2017, 2018, "多年合一"]:
    output_path = "D:\\毕业论文程序\\污染物浓度\\整理\\全部污染物\\%s_日期补全\\" % year
    file_name = os.listdir(output_path)
    print("==========", year,len(file_name), "==========")
    for name in file_name:
        data_raw = pd.read_excel(output_path + name)
        if len(data_raw.index) == 365:
            print(year, name)
        elif len(data_raw.index) == 366:
            print(year,name)
        elif len(data_raw.index) == 365 * 4 + 1 + 233:
            print(year,name)
        elif len(data_raw.index) == 233:
            print(year, name)
        else:
            print("==============================", year, name, "==============================")  # 问题文件
