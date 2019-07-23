# -*- coding: utf-8 -*-
# 作者：xcl
# 时间：2019/6/20  19:06 
from keras.models import Sequential, Model
from keras import layers, Input

import numpy as np
import pandas as pd
from keras.utils import to_categorical

# 读取
data = pd.read_excel("测试用数据.xlsx")
data = pd.read_excel("相邻位置仅留PM和T-1.xlsx")
# 设置变量
data = data[data["AOD值"] > 0]
independent = ["AOD值", 'cloudCover', 'dewPoint', 'humidity', 'precipAccumulation', 'precipIntensity', 'pressure',
               'temperature', 'uvIndex', 'visibility', 'windSpeed', 'windBearing']
T_1 =["AOD值-t-1", 'cloudCover-t-1', 'dewPoint-t-1', 'humidity-t-1', 'precipAccumulation-t-1', 'precipIntensity-t-1', 'pressure-t-1',
               'temperature-t-1', 'uvIndex-t-1', 'visibility-t-1', 'windSpeed-t-1', 'windBearing-t-1', "日均PM2.5-t-1"]
PM_list = ["A1-日均PM2.5-MEAN-t-1", "A2-日均PM2.5-MEAN-t-1", "A3-日均PM2.5-MEAN-t-1", "A4-日均PM2.5-MEAN-t-1",
           "A5-日均PM2.5-MEAN-t-1", "A6-日均PM2.5-MEAN-t-1", "A7-日均PM2.5-MEAN-t-1", "A8-日均PM2.5-MEAN-t-1",
           "B1-日均PM2.5-MEAN-t-1", "B2-日均PM2.5-MEAN-t-1", "B3-日均PM2.5-MEAN-t-1", "B4-日均PM2.5-MEAN-t-1",
           "B5-日均PM2.5-MEAN-t-1", "B6-日均PM2.5-MEAN-t-1", "B7-日均PM2.5-MEAN-t-1", "B8-日均PM2.5-MEAN-t-1"]
dependent = ["日均PM2.5"]
independent = list(set(independent) | set(T_1))  # 合集


data_x1 = data[independent]
data_x2 = data[T_1]
data_y = data[dependent]
data_x1 = np.array(data_x1)
data_x2 = np.array(data_x2)
data_y = np.array(data_y)
# print(len(data_x1))


#  尝试独热编码
#data_x1 = to_categorical(data_x1)
#data_x2 = to_categorical(data_x2)
#data_y = to_categorical(data_y)

###################################################################################


# define two sets of inputs
inputA = Input(shape=(25,))
inputB = Input(shape=(13,))

# the first branch operates on the first input
x = layers.Dense(8, activation="relu")(inputA)
x = layers.Dense(4, activation="relu")(x)
x = Model(inputs=inputA, outputs=x)

# the second branch opreates on the second input
y = layers.Dense(64, activation="relu")(inputB)
y = layers.Dense(32, activation="relu")(y)
y = layers.Dense(4, activation="relu")(y)
y = Model(inputs=inputB, outputs=y)

# combine the output of the two branches
combined = layers.concatenate([x.output, y.output])

# apply a FC layer and then a regression prediction on the
# combined outputs
z = layers.Dense(2, activation="relu")(combined)
z = layers.Dense(1, activation="linear")(z)

# our model will accept the inputs of the two branches and
# then output a single value
model = Model(inputs=[x.input, y.input], outputs=z)
##################      输入数据


model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
model.fit([data_x1, data_x2], data_y)

out1 = model.predict([data_x1, data_x2])
out1 = pd.DataFrame(out1)
data_y = pd.DataFrame(data_y)

outcome1 = out1 - data_y

e_AME = abs(outcome1).mean()
# print("AME误差:", e)
e_MSE = ((outcome1) ** 2).mean()

print("AME:", e_AME.values, "\n", "MSE:", e_MSE.values)
