# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/9/21 23:54


# 库
from random import choice
import random
from sklearn.ensemble import AdaBoostRegressor
from keras.models import Sequential, Model
from keras import layers, Input
import keras
from keras.utils import to_categorical
from sklearn.utils import shuffle
from sklearn.model_selection import KFold, StratifiedKFold
import datetime  # 程序耗时

import pandas as pd
import keras
from keras.layers import Input, Embedding, LSTM, Dense, concatenate, core, add
from keras.models import Model
import os
import copy
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle
starttime = datetime.datetime.now()

input_path = 'D:\\data - 副本.xlsx'

data_all = pd.read_excel(input_path, index_col='日期')

"""
del data_all['pressure_T1']
del data_all['pressure']
"""
data_all = data_all.dropna()
data_ts_df = data_all[['tm_mon',  'id','经度','纬度'
                       ,'tstamps']]
# 虚拟变量
for ccc in data_ts_df.columns:
    data_ts_df[ccc] = data_ts_df[ccc].map(lambda x: str(x))
data_dummies = pd.concat([
                          data_ts_df[['tm_mon']],
                          data_ts_df[['id']],
                            data_ts_df[['经度']],
                            data_ts_df[['纬度']],
                            data_ts_df[['tstamps']]],
                            axis=1)
"""
list1 = []
for ccc in data_dummies.columns:
    # print(ccc)
    if ccc != 'tm_mon':
        list1.append(ccc)
"""

# 去掉无用列
data_to_std = data_all.drop(
    ['tm_mon', 'id','经度','纬度'
                       ,'tstamps'], axis=1)


# 标准化
"""
data_std = copy.deepcopy(data_to_std)
#mean_pm = data_std['PM25'].mean()# 49.65522239999188
#std_pm = data_std['PM25'].std()# 39.39446197985595
#print(mean_pm)
#print(std_pm)
max_pm = data_std['PM25'].max()#388
min_pm = data_std['PM25'].min()#1
print(max_pm)
print(min_pm)

for col in data_std:
    #mean = data_std[col].mean()
    max = data_std[col].max()
    #std = data_std[col].std()
    min = data_std[col].min()
    data_std[col] = data_std[col].map(lambda x:(x-min)/(max-min))

"""
# 标准化前的数据矩阵
data_out2 = pd.concat([data_dummies, data_to_std], join='outer', axis=1)  # 标准化前的真实值

# 标准化后的数据矩阵
#data_out = pd.concat([data_dummies, data_std], join='outer', axis=1)
# 更改格式
"""
data_out['tm_mon'] = data_out['tm_mon'].map(lambda x: float(x))
data_out['经度'] = data_out['经度'].map(lambda x: float(x))
data_out['纬度'] = data_out['纬度'].map(lambda x: float(x))
"""
data_out2['tm_mon'] = data_out2['tm_mon'].map(lambda x: float(x))
data_out2['经度'] = data_out2['经度'].map(lambda x: float(x))
data_out2['纬度'] = data_out2['纬度'].map(lambda x: float(x))

# 划分
idlist = list(range(1, 153))
slice1 = random.sample(idlist, 38)  # 从list中随机获取5个元素，作为一个片断返回
slice2 = []
for idx in idlist:
    if idx not in slice1:
        idx = str(idx)
        slice2.append(idx)
slice1 = [str(j) for j in slice1]
"""
data_test2 = data_out2[data_out2['id'].isin(slice1)]
"""
# print(data_test2.PM25)  # 这才是真实值

# 划分标准化后的训练集测试集, 用于训练
data_test = data_out2[data_out2['id'].isin(slice1)]
data_train = data_out2[data_out2['id'].isin(slice2)]
"""
data_test2.to_excel('D:\\data_test\\data_true.xlsx')
"""
# print(data_test2.PM25)  # 这才是真实值

# 划分标准化后的训练集测试集, 用于训练
data_test.to_excel('D:\\data_test\\data_test.xlsx')
data_train.to_excel('D:\\data_test\\data_train.xlsx')