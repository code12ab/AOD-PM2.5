# -*- coding: utf-8 -*-
# 作者：xcl
# 时间：2019/6/20  21:27 


from keras.models import Sequential, Model
from keras import layers, Input
import numpy as np
import pandas as pd
from keras.utils import to_categorical

# 读取

#data = pd.read_excel("相邻位置仅留PM和T-1.xlsx")
data = pd.read_excel("测试用数据.xlsx")
# 设置变量
data = data[data["AOD值"] > 0]
independent = ["AOD值", 'cloudCover', 'dewPoint', 'humidity', 'precipAccumulation', 'precipIntensity', 'pressure',
               'temperature', 'uvIndex', 'visibility', 'windSpeed', 'windBearing']
T_1 = ["AOD值-t-1", 'cloudCover-t-1', 'dewPoint-t-1', 'humidity-t-1', 'precipAccumulation-t-1', 'precipIntensity-t-1',
       'pressure-t-1', 'temperature-t-1', 'uvIndex-t-1', 'visibility-t-1', 'windSpeed-t-1', 'windBearing-t-1']

PM_list = ["A1-日均PM2.5-MEAN-t-1", "A2-日均PM2.5-MEAN-t-1", "A3-日均PM2.5-MEAN-t-1", "A4-日均PM2.5-MEAN-t-1",
           "A5-日均PM2.5-MEAN-t-1", "A6-日均PM2.5-MEAN-t-1", "A7-日均PM2.5-MEAN-t-1", "A8-日均PM2.5-MEAN-t-1",
           "B1-日均PM2.5-MEAN-t-1", "B2-日均PM2.5-MEAN-t-1", "B3-日均PM2.5-MEAN-t-1", "B4-日均PM2.5-MEAN-t-1",
           "B5-日均PM2.5-MEAN-t-1", "B6-日均PM2.5-MEAN-t-1", "B7-日均PM2.5-MEAN-t-1", "B8-日均PM2.5-MEAN-t-1",
           "日均PM2.5-t-1"]
dependent = ["日均PM2.5"]
independent = list(set(independent) | set(T_1))  # 合集
# 更改为数组格式
data_x1 = data[independent]
data_x2 = data[PM_list]
data_y = data[dependent]
data_x1 = np.array(data_x1)
data_x2 = np.array(data_x2)
data_y = np.array(data_y)
# print(len(data_x1))


#  尝试独热编码
'''
data_x1 = to_categorical(data_x1)
data_x2 = to_categorical(data_x2)
data_y = to_categorical(data_y)
'''
###################################################################################

# 输入1和2的变量数,维度
inputA = Input(shape=(24,))
inputB = Input(shape=(17,))

# 输入1
x = layers.Dense(8, activation="relu")(inputA)
x = layers.Dense(4, activation="relu")(x)
x = Model(inputs=inputA, outputs=x)

# 输入2
y = layers.Dense(64, activation="relu")(inputB)
y = layers.Dense(32, activation="relu")(y)
y = layers.Dense(4, activation="relu")(y)
y = Model(inputs=inputB, outputs=y)

# 合并多输入
combined = layers.concatenate([x.output, y.output])

# 输出层
z = layers.Dense(2, activation="relu")(combined)
z = layers.Dense(1, activation="linear")(z)

# 建立模型
model = Model(inputs=[x.input, y.input], outputs=z)

# 模型编译
model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
model.fit([data_x1, data_x2], data_y, epochs=1000, batch_size=128)



# 使用模型进行预测
out1 = model.predict([data_x1, data_x2])
out1 = pd.DataFrame(out1)
data_y = pd.DataFrame(data_y)

outcome1 = out1 - data_y
e_AME = abs(outcome1).mean()
#e_AME_std = outcome1.std()
# print("AME误差:", e)
e_MSE = (outcome1 ** 2).mean()
print("AME:", e_AME.values, "\n", "MSE:", e_MSE.values)
