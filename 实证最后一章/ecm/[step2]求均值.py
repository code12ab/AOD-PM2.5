# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2020/3/31 20:02


# 库
import pandas as pd
import numpy as np
import os

input_data = 'D:\\毕业论文程序\\08到17年\\输出特征\\result08-17.xlsx'
output_data = 'D:\\毕业论文程序\\08到17年\\输出特征\\mean08-17.xlsx'
data1 = pd.read_excel(input_data)
data1['日期'] = data1['日期'].map(lambda x: x[0:7])
data2 = data1.groupby(['日期', "id"]).mean()
data3 = data2.groupby(['日期']).mean()
data3.to_excel(output_data)
