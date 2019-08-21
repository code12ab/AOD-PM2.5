# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/8 19:38

# 库
import pandas as pd
import numpy as np
import math
from numpy import array
import os


for modis in ["Terra", "Aqua"]:
    for year in [2014, 2015, 2016, 2017, 2018, "多年合一"]:
        output_path = "D:\\毕业论文程序\\气溶胶光学厚度\\空间转换模块\\%s\\%s_日期补全\\" % (modis, year)
        file_name = os.listdir(output_path)
        print("==========", year, modis, len(file_name), "==========")
        for name in file_name:
            data_raw = pd.read_excel(output_path + name)
            if len(data_raw.index) == 365:
                print(year, modis, name)
            elif len(data_raw.index) == 366:
                print(year, modis, name)
            elif len(data_raw.index) == 365 * 5 + 1:
                print(year, modis, name)
            else:
                print("==========", year, modis, name, "==========")
