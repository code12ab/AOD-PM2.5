# -*- coding: utf-8 -*-
# 作者：xcl
# 时间：2019/6/20  23:52
# -*- coding: utf-8 -*-
# 作者：xcl
# 时间：2019/6/20  21:27

from sklearn.ensemble import AdaBoostRegressor
from keras.models import Sequential, Model
from keras import layers, Input
import keras
import numpy as np
import pandas as pd
from keras.utils import to_categorical
from sklearn.utils import shuffle
from sklearn.model_selection import KFold,StratifiedKFold
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


# 开始计算耗时
start_time = datetime.datetime.now()
# 读取
input_path = 'D:\\雨雪+2018_new_pm.xlsx'
data_all = pd.read_excel(input_path, index_col='日期')
del data_all['ozone'],
del data_all['ozone_T1']
"""
del data_all['pressure_T1']
del data_all['pressure']
"""
data_all = data_all.dropna()
# 打乱
data_all = shuffle(data_all, random_state=1027)

data_ts_df = data_all[['tm_mon', 'tm_mday',
                       'tm_wday', 'tm_yday', 'tm_week', 'id']]
# 虚拟变量
for ccc in data_ts_df.columns:
    data_ts_df[ccc] = data_ts_df[ccc].map(lambda x: str(x))
data_get_dummies1 = pd.get_dummies(data_ts_df[['tm_mon']], drop_first=True)
print(data_get_dummies1.columns)
data_get_dummies2 = pd.get_dummies(data_ts_df[['tm_mday']], drop_first=True)
data_get_dummies3 = pd.get_dummies(data_ts_df[['id']], drop_first=True)
data_dummies = pd.concat([data_get_dummies1,
                          data_get_dummies2,
                          data_get_dummies3,
                          data_ts_df[['tm_mon']]],
                         axis=1)
list1 = []
for ccc in data_dummies.columns:
    # print(ccc)
    if ccc != 'tm_mon':
        list1.append(ccc)

# 去掉无用列
data_to_std = data_all.drop(
    ['tm_mon', 'tm_mday', 'tm_wday', 'tm_yday', 'tm_week', 'id'], axis=1)

# 标准化
"""
data_to_std2 = MinMaxScaler().fit_transform(data_to_std)
data_to_std2 = pd.DataFrame(data_to_std2)
data_to_std2 = data_to_std2.set_index(data_to_std.index)
data_to_std2.columns = data_to_std.columns
data_out = pd.concat([data_dummies, data_to_std2], join='outer', axis=1)
"""
# 不标准化
data_out = pd.concat([data_dummies, data_to_std], join='outer', axis=1)
# 划分
"""
data_test = data_out[(data_out['tm_mon']=="2")|
                     (data_out['tm_mon']=="5")|
                    (data_out['tm_mon']=="8")|
                    (data_out['tm_mon']=="11")]
data_train = data_out[(data_out['tm_mon']=="1")|
                     (data_out['tm_mon']=='3')|
                    (data_out['tm_mon']=='5')|
                    (data_out['tm_mon']=='6')|
                     (data_out['tm_mon']=='7')|
                    (data_out['tm_mon']=='9')|
                    (data_out['tm_mon']=='10')|
                     (data_out['tm_mon']=='12')]
"""

data_test = data_out[(data_out['tm_mon'] == "1") |
                     (data_out['tm_mon'] == "4") |
                     (data_out['tm_mon'] == "10")]
data_train = data_out[(data_out['tm_mon'] == "12") |
                      (data_out['tm_mon'] == "3") |
                      (data_out['tm_mon'] == '2') |

                      (data_out['tm_mon'] == '5') |
                      (data_out['tm_mon'] == '7') |
                      (data_out['tm_mon'] == '8') |
                      (data_out['tm_mon'] == '6') |
                      (data_out['tm_mon'] == '9') |
                      (data_out['tm_mon'] == '11')]
# AOD
data_aod_test = data_test[['AOD_0']]
data_aod_train = data_train[['AOD_0']]


# 气象
data_sky_test = data_test[['apparentTemperatureHigh',
                           'apparentTemperatureLow',
                           'apparentTemperatureMax',
                           'apparentTemperatureMin',
                           'cloudCover',
                           'dewPoint',
                           'humidity',

                           'sunTime',
                           'temperatureHigh',
                           'temperatureLow',
                           'temperatureMax',
                           'temperatureMin',

                           'visibility',
                           'windBearing',
                           'windGust',
                           'windSpeed',
                           'apparentTemperature',
                           'temperature',

                           'pressure',
                           'precipIntensity',
                           'precipIntensityMax',
                           'precipAccumulation']]

data_sky_train = data_train[['apparentTemperatureHigh',
                             'apparentTemperatureLow',
                             'apparentTemperatureMax',
                             'apparentTemperatureMin',
                             'cloudCover',
                             'dewPoint',
                             'humidity',

                             'sunTime',
                             'temperatureHigh',
                             'temperatureLow',
                             'temperatureMax',
                             'temperatureMin',

                             'visibility',
                             'windBearing',
                             'windGust',
                             'windSpeed',
                             'apparentTemperature',
                             'temperature',

                             'pressure',
                             'precipIntensity',
                             'precipIntensityMax',
                             'precipAccumulation',
                             ]]

# 时间特征
data_time_test = data_test[['tm_mon_10',
                            'tm_mon_11',
                            'tm_mon_12',
                            'tm_mon_2',
                            'tm_mon_3',
                            'tm_mon_4',
                            'tm_mon_5',
                            'tm_mon_6',
                            'tm_mon_7',
                            'tm_mon_8',
                            'tm_mon_9',
                            ]]

data_time_train = data_train[['tm_mon_10',
                              'tm_mon_11',
                              'tm_mon_12',
                              'tm_mon_2',
                              'tm_mon_3',
                              'tm_mon_4',
                              'tm_mon_5',
                              'tm_mon_6',
                              'tm_mon_7',
                              'tm_mon_8',
                              'tm_mon_9',
                              ]]
# 空间特征
data_station_test = data_test[data_get_dummies3.columns]

data_station_train = data_train[data_get_dummies3.columns]
# 时滞
data_t1_test = data_test[['AOD_0_T1',
                          'cloudCover_T1',
                          'dewPoint_T1',
                          'humidity_T1',
                          'sunTime_T1',
                          'visibility_T1',
                          'windSpeed_T1',
                          'temperature_T1',
                          'pressure_T1',
                          'precipIntensity_T1',
                          'precipIntensityMax_T1',
                          'precipAccumulation_T1',
                          ]]
"""
data_t1_train = data_train[['AOD_0_T1',
                            'apparentTemperatureHigh_T1',
                            'apparentTemperatureLow_T1',
                            'apparentTemperatureMax_T1',
                            'apparentTemperatureMin_T1',
                            'cloudCover_T1',
                            'dewPoint_T1',
                            'humidity_T1',

                            'sunTime_T1',
                            'temperatureHigh_T1',
                            'temperatureLow_T1',
                            'temperatureMax_T1',
                            'temperatureMin_T1',

                            'visibility_T1',
                            'windBearing_T1',
                            'windGust_T1',
                            'windSpeed_T1',
                            'apparentTemperature_T1',
                            'temperature_T1',                          'pressure_T1',
                          'precipIntensity_T1',
                          'precipIntensityMax_T1',
                          'precipAccumulation_T1',]]
                          """
data_t1_train = data_train[['AOD_0_T1',
                            'cloudCover_T1',
                            'dewPoint_T1',
                            'humidity_T1',
                            'sunTime_T1',
                            'visibility_T1',
                            'windSpeed_T1',
                            'temperature_T1',
                            'pressure_T1',
                            'precipIntensity_T1',
                            'precipIntensityMax_T1',
                            'precipAccumulation_T1',
                            ]]
# NDVI
data_ndvi_test = data_test[['NDVI_0']]
data_ndvi_train = data_train[['NDVI_0']]
"""
data_ndvi_train = data_train[['tm_mday_10',
                              'tm_mday_11',
                              'tm_mday_12',
                              'tm_mday_13',
                              'tm_mday_14',
                              'tm_mday_15',
                              'tm_mday_16',
                              'tm_mday_17',
                              'tm_mday_18',
                              'tm_mday_19',
                              'tm_mday_2',
                              'tm_mday_20',
                              'tm_mday_21',
                              'tm_mday_22',
                              'tm_mday_23',
                              'tm_mday_24',
                              'tm_mday_25',
                              'tm_mday_26',
                              'tm_mday_27',
                              'tm_mday_28',
                              'tm_mday_29',
                              'tm_mday_3',
                              'tm_mday_30',
                              'tm_mday_31',
                              'tm_mday_4',
                              'tm_mday_5',
                              'tm_mday_6',
                              'tm_mday_7',
                              'tm_mday_8',
                              'tm_mday_9']]
"""
# AODS
data_aods_test = data_test[['AOD_1',
                            'AOD_2',
                            'AOD_3',
                            'AOD_4',
                            'AOD_5',
                            'AOD_6',
                            'AOD_7',
                            'AOD_8',
                            'AOD_9',
                            'AOD_10',
                            'AOD_11',
                            'AOD_12',
                            'AOD_13',
                            'AOD_14',
                            'AOD_15',
                            'AOD_16']]
data_aods_train = data_train[['AOD_1',
                              'AOD_2',
                              'AOD_3',
                              'AOD_4',
                              'AOD_5',
                              'AOD_6',
                              'AOD_7',
                              'AOD_8',
                              'AOD_9',
                              'AOD_10',
                              'AOD_11',
                              'AOD_12',
                              'AOD_13',
                              'AOD_14',
                              'AOD_15',
                              'AOD_16']]
# 污染物
data_pm_test = data_test[['PM25']]
data_pm_train = data_train[['PM25']]


# 输入1和2的变量数,维度 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!是否可以不同维度
inputAOD = Input(shape=(len(data_aod_test.columns),))
inputSky = Input(shape=(len(data_sky_test.columns),))
inputTime = Input(shape=(len(data_time_test.columns),))
inputStaion = Input(shape=(len(data_station_test.columns),))
inputT1 = Input(shape=(len(data_t1_test.columns),))
inputNDVI = Input(shape=(len(data_ndvi_test.columns),))
inputAODs = Input(shape=(len(data_aods_test.columns),))

# 输入1
x1 = layers.Dense(24, activation=keras.layers.advanced_activations.LeakyReLU(alpha=0.5))(inputAOD)
x1 = layers.Dense(3, activation=keras.layers.advanced_activations.LeakyReLU(alpha=0.5))(x1)
x1 = Model(inputs=inputAOD, outputs=x1)
# 输入2
x2 = layers.Dense(24, activation=keras.layers.advanced_activations.LeakyReLU(alpha=0.5))(inputSky)
x2 = layers.Dense(3, activation=keras.layers.advanced_activations.LeakyReLU(alpha=0.5))(x2)
x2 = Model(inputs=inputSky, outputs=x2)
# 输入3
x3 = layers.Dense(24, activation=keras.layers.advanced_activations.LeakyReLU(alpha=0.5))(inputTime)
x3 = layers.Dense(3, activation=keras.layers.advanced_activations.LeakyReLU(alpha=0.5))(x3)
x3 = Model(inputs=inputTime, outputs=x3)
# 输入4
x4 = layers.Dense(24, activation=keras.layers.advanced_activations.LeakyReLU(alpha=0.5))(inputStaion)
x4 = layers.Dense(3, activation=keras.layers.advanced_activations.LeakyReLU(alpha=0.5))(x4)
x4 = Model(inputs=inputStaion, outputs=x4)
# 输入5
x5 = layers.Dense(24, activation=keras.layers.advanced_activations.LeakyReLU(alpha=0.5))(inputT1)
x5 = layers.Dense(3, activation=keras.layers.advanced_activations.LeakyReLU(alpha=0.5))(x5)
x5 = Model(inputs=inputT1, outputs=x5)
# 输入6
x6 = layers.Dense(24, activation=keras.layers.advanced_activations.LeakyReLU(alpha=0.5))(inputNDVI)
x6 = layers.Dense(3, activation=keras.layers.advanced_activations.LeakyReLU(alpha=0.5))(x6)
x6 = Model(inputs=inputNDVI, outputs=x6)
# 输入7
x7 = layers.Dense(24, activation=keras.layers.advanced_activations.LeakyReLU(alpha=0.5))(inputAODs)
x7 = layers.Dense(3, activation=keras.layers.advanced_activations.LeakyReLU(alpha=0.5))(x7)
x7 = Model(inputs=inputAODs, outputs=x7)

combined = layers.concatenate([x1.output, x2.output,x3.output,x4.output,x5.output,x6.output,x7.output])
# 输出层
z = layers.Dense(12, activation=keras.layers.advanced_activations.LeakyReLU(alpha=0.5),
                 kernel_regularizer=keras.regularizers.l2(0.01))(combined)
z = core.Dropout(rate=0.01)(z)
z = layers.Dense(4, activation=keras.layers.advanced_activations.LeakyReLU(alpha=0.5),
                 kernel_regularizer=keras.regularizers.l2(0.01))(z)
z = layers.Dense(1, activation=keras.layers.advanced_activations.LeakyReLU(alpha=0.5),
                 kernel_regularizer=keras.regularizers.l2(0.01))(z)

# 建立模型
model = Model(inputs=[x1.input, x2.input, x3.input, x4.input,x5.input,x6.input, x7.input], outputs=z)
# 模型编译
model.compile(
    loss=['mean_absolute_error'],
    optimizer=keras.optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=0.00001),
    # optimizer=keras.optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=0.0),
    # optimizer=keras.optimizers.Adagrad(lr=0.01, epsilon=None, decay=0.00001),
    # optimizer=keras.optimizers.SGD(lr=0.01, momentum=0.0, decay=0.0, nesterov=False),
    # optimizer=keras.optimizers.Adam(lr=0.01, beta_1=0.9, beta_2=0.999),
    # epsilon=None, decay=0.0, amsgrad=False),
    metrics=["accuracy"])
model.fit([
    data_aod_train,
    data_sky_train,
    data_time_train,
    data_station_train,
    data_t1_train,
    data_ndvi_train,
    data_aods_train
],
    data_pm_train,
    epochs=1000,
    batch_size=512)



res = model.predict([data_aod_test,
                          data_sky_test,
                          data_time_test,
                          data_station_test,
                          data_t1_test,
                          data_ndvi_test,
                          data_aods_test])
datares = res - data_pm_test
datares.PM25 = datares.PM25.map(lambda x: abs(x))
data_predt = pd.concat([datares, data_pm_test], axis=1)
data_predt.columns = ["差值", '真']
data_predt['差值'] = data_predt['差值'].map(lambda x: abs(x))
data_predt['百分误'] = data_predt['差值'].div(data_predt["真"])
data_predt['差值2'] = data_predt['差值'].map(lambda x: x**2)

print(np.average(data_predt['差值']))
print(np.average(data_predt['百分误']))
print(np.average(data_predt['差值2']))
