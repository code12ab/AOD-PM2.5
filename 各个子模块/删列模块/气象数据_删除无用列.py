# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/14 9:12

# 库
import pandas as pd
import numpy as np
import math
from numpy import array
import os


mean_input_file_path = "D:\\毕业论文程序\\污染物浓度\\插值模块\\Res\多年合一\\"
sky_input_path = "D:\\毕业论文程序\\建模数据\\污染物\\"

list_different = []
input_file_names = os.listdir(mean_input_file_path)  # 文件名列表
for input_file_name in input_file_names:
    data_aods = pd.read_excel(mean_input_file_path+input_file_name)
    data_sky = pd.read_excel(sky_input_path+input_file_name)
    if len(data_aods["日期"]) > len(data_sky["日期"]):
        print("格式不一样")
        list_different.append(input_file_name)
    elif len(data_aods["日期"]) < len(data_sky["日期"]):
        print("格式不一样")
        list_different.append(input_file_name)
    else:
        print("格式一样")

print(list_different, len(list_different))