# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/10/9 15:42


# 库
import pandas as pd
import numpy as np
import os

df1 = pd.read_excel('D:\\雨雪+2018_new_pm_aod_interpolate线性2.xlsx')
df2 = pd.read_excel('D:\\id+x+y+aod+pm.xlsx')
"""
df3 = pd.merge(df1,df2,how='left',on ='id')
df3['id2'] = df3['id2'].fillna(method='pad')
df3 = df3.dropna()
df3 = df3.set_index('日期')
"""
df3 = pd.merge(df1,df2,how='left',on ='tm_mon')
df3['tm_mon2'] = df3['tm_mon'].fillna(method='pad')
df3 = df3.dropna()
df3 = df3.set_index('日期')
df3.to_excel('D:\\雨雪+2018_new_pm_aod_interpolate线性ID2+季度.xlsx')