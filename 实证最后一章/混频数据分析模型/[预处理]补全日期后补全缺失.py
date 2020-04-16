# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2020/4/10 16:37


# 库


import pandas as pd
import numpy as np
import os

input_data = 'C:\\Users\\iii\\Desktop\\ecm.xlsx'

output_data = 'C:\\Users\\iii\\Desktop\\ecm-fill.xlsx'
data1 = pd.read_excel(input_data, sheet_name="date-fill", index_col='date')
data1 = data1.interpolate()
data1 = data1.interpolate('pad')
data1 = data1.interpolate('bfill')
data1 = data1.interpolate('pad')
data1 = data1.interpolate('bfill')

# knn
'''
# from fancyimpute import KNN
data2 = pd.DataFrame(KNN(k=12).fit_transform(data1))
data2.columns = data1.columns
'''
print(data1.isnull().sum())
data1.to_excel(output_data)