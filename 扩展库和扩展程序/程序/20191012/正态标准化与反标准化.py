# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/10/6 8:29


# 库
import pandas as pd
import numpy as np
import os,random
from sklearn.preprocessing import StandardScaler
# 划分
data = np.random.uniform(0, 100, 10)[:, np.newaxis]
ss = StandardScaler()
std_data = ss.fit_transform(data)
origin_data= ss.inverse_transform(std_data[1:5])
print('data is ',data)
print('after standard ',std_data)
print('after inverse ',origin_data)
print('after standard mean and std is ',np.mean(std_data), np.std(std_data))