# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/9/1 20:00


# 库
import pandas as pd
import numpy as np
import keras
from keras.layers import Input, Embedding, LSTM, Dense, concatenate, core, add
from keras.models import Model
import os
# 模块
# 当日天气模块
# 时滞天气模块
# 其他空气污染物模块
# 时空元属性模块
# 整体影响模块
# 第一个模块 当日天气模块
#




input1_aod = 'D:\\毕业论文程序\\建模数据\\气溶胶\\2018\\北京-东四.xlsx'
input3_ts = 'D:\\毕业论文程序\\建模数据\\时空特征\\2018\\北京-东四.xlsx'
input4_pm = 'D:\\毕业论文程序\\建模数据\\污染物\\2018\\北京-东四.xlsx'
input2_pm = 'D:\\毕业论文程序\\建模数据\\NDVI\\2018\\北京-东四.xlsx'
input5_pm = 'D:\\毕业论文程序\\建模数据\\气象\\2018\\北京-东四.xlsx'
input6_pm = 'D:\\毕业论文程序\\建模数据\\时滞\\2018\\北京-东四.xlsx'
aod = pd.read_excel(input4_pm, index_col ='日期')
print(aod.columns)


