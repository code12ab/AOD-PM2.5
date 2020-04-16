# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2020/3/30 22:58


# 库
import pandas as pd
import numpy as np
import os

res = list()
input_path = 'D:\\毕业论文程序\\08到17年\\输入特征_补零再单位转换\\'
for year in [2008,2009,2010,2011,2012,2013,2014,2015,2016,2017]:
    data = pd.read_excel(input_path+"%s.xlsx" % year, index_col="日期")
    res.append(data)

result = pd.concat(res, axis=0)
result = result.fillna(method='pad')
result = result.fillna(method='bfill')
result = result.interpolate()
result.to_excel('D:\\毕业论文程序\\08到17年\\输入特征_十年\\08-17.xlsx')