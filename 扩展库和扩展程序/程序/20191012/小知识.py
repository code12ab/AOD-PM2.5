# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/26 18:07


# 库
import pandas as pd
import numpy as np



# SettingWithCopyWarning
# data_darksky_weather_ewm.loc[nub, columname] = data_darksky_weather_ewm_mid.loc[nub, columname]

"""
a = [1,2]
b = [3,4]
c = [i*j for i in a for j in b]
print(c)

d = 213
a = [j/d for j in a]
print(a)
"""
"""
a = [2,2,2]
b = [0 for x in range(len(a))]
list1 = []
list1.append(a)
list1.append(b)
print(list1)
list2 = np.array(list1)
print(list2)
"""

"""
a = [[1,2,3],[np.nan,3,5]]

a = np.array(a)
print(a,'\n', a.T)
w = [1,2,3]
# print(a)
b = a*w
print(b)
"""
""""
c = [[np.nan ,4],[np.nan,np.nan]]
c= np.array(c)
c = [j/j for j in c]
c= np.array(c)

c[c==np.nan]=0
print(c, c.__class__)

a = [j/j for j in a]
# print(np.array(a))
"""

a = [[1,2,3],[1,3,5]]
a = np.array(a)
b = a.sum(1)
print(a)
print(b)
print(b.__class__)