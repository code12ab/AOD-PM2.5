# -*- coding: utf-8 -*-

'''
按列变化

'''
# 库
import pandas as pd
import numpy as np
import os,random
from sklearn.preprocessing import StandardScaler
# 划分
data = [[1,2,3,4],[22,33,44,55],[23,1,55,2]]
data = pd.DataFrame(data)

ss = StandardScaler()
std_data = ss.fit_transform(data)
origin_data= ss.inverse_transform(std_data[0])
print(std_data[0])
print('data is ','\n',data)
print('after standard ','\n',std_data)
print('after inverse ','\n',origin_data)
print('after standard mean and std is ','\n',np.mean(std_data), np.std(std_data))


d = [-1.41306768, -0.67318066, -1.38543883 ,-0.66594284]
print(ss.inverse_transform(d))



d2 = [1,44,12,5,1,231]
d3 = np.array(d2).reshape(1,-1)
print(d3)
print("SSFIT",ss.fit_transform(d3))
