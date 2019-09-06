# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/26 21:23

# 库
import pandas as pd
import numpy as np
import os

# 日期补全
for year in [2018]:
    input_path = "D:\\毕业论文程序\\气象数据\\筛除字符串\\%s_不补全\\" % year
    output_path = "D:\\毕业论文程序\\气象数据\\筛除字符串\\%s_不补全\\" % year
    file_name = os.listdir(input_path)
    for name in file_name:
        data_raw = pd.read_excel(input_path + name, index_col="日期")
        if len(data_raw.index) > 365:
            data_raw = data_raw.drop(["2017-12-31"])
            data_raw.to_excel(output_path+name)
        if len(data_raw.index) != 365:
            print(name, "的index不等于365")
