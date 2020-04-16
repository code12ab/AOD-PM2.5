# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2020/4/12 20:48


# 库
import pandas as pd
import numpy as np
import os


input_data = 'C:\\Users\\iii\\Desktop\\汇总ecm-fill.xlsx'

data_0 = pd.read_excel(input_data, index_col='日期全')
print(data_0.columns)



# 改用notebook
