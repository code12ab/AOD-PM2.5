# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/6 16:59

# 库
import pandas as pd
import numpy as np
import os

a = [1, 4, 4, 0]
b = [4, 4, 4, 0]
c = [np.nan, 4, np.nan, 3]
d = [4, 4, np.nan, np.nan]

c = pd.DataFrame([a, b, c, d])
'''             weight
KNN        0.476610
ewm        0.032811
IDW        0.476610
Iterative  0.013969
运行完成!
             weight
KNN        0.241128
ewm        0.205460
IDW        0.419197
Iterative  0.134215
运行完成!'''
print(c)
print("\n", c.std())
print("\n", c.mean())  # mean(1) 横向均值 mean() 顺着均值，列的

mean_output_file_path = "D:\\毕业论文程序\\气溶胶光学厚度\\插值模块\\Mean\\2018\\北京-定陵.xlsx"

data_KNN = pd.read_excel(mean_output_file_path, sheet_name="KNN")
print(data_KNN.index)
print(data_KNN.columns)

print(data_KNN[["日期", "AOD_0"]])