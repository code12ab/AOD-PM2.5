# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/9/3 23:25

import pandas as pd
import keras
from keras.layers import Input, Embedding, LSTM, Dense, concatenate, core, add
from keras.models import Model
import os
import copy
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle


# 读取
input_path = 'D:\\全2018_不补全+日出足够.xlsx'
data_all = pd.read_excel(input_path, index_col='日期')
del data_all['ozone'],
del data_all['ozone_T1']
del data_all['pressure_T1']
del data_all['pressure']
data_all = data_all.dropna()
# 打乱
data_all = shuffle(data_all,random_state=1027)

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
data_to_std2 = MinMaxScaler().fit_transform(data_to_std)
data_to_std2 = pd.DataFrame(data_to_std2)
data_to_std2 = data_to_std2.set_index(data_to_std.index)
data_to_std2.columns = data_to_std.columns
data_out = pd.concat([data_dummies, data_to_std2], join='outer', axis=1)

# 不标准化
# data_out = pd.concat([data_dummies, data_to_std], join='outer', axis=1)
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

data_test = data_out[(data_out['tm_mon'] == "4") |
                     (data_out['tm_mon'] == "7") |
                     (data_out['tm_mon'] == "10")]
data_train = data_out[(data_out['tm_mon'] == "3") |
                      (data_out['tm_mon'] == "1") |
                      (data_out['tm_mon'] == '2') |
                      (data_out['tm_mon'] == '5') |
                      (data_out['tm_mon'] == '6') |
                      (data_out['tm_mon'] == '8') |
                      (data_out['tm_mon'] == '9') |
                      (data_out['tm_mon'] == '12') |
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
                           'temperature']]

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
                             'temperature']]

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
data_station_test = data_test[['id_1',
                               'id_100',
                               'id_101',
                               'id_102',
                               'id_103',
                               'id_104',
                               'id_105',
                               'id_106',
                               'id_107',
                               'id_108',
                               'id_109',
                               'id_110',
                               'id_111',
                               'id_112',
                               'id_113',
                               'id_114',
                               'id_115',
                               'id_116',
                               'id_117',
                               'id_118',
                               'id_119',
                               'id_120',
                               'id_121',
                               'id_122',
                               'id_123',
                               'id_124',
                               'id_125',
                               'id_126',
                               'id_127',
                               'id_128',
                               'id_129',
                               'id_130',
                               'id_131',
                               'id_132',
                               'id_133',
                               'id_134',
                               'id_135',
                               'id_136',
                               'id_137',
                               'id_138',
                               'id_139',
                               'id_140',
                               'id_141',
                               'id_142',
                               'id_143',
                               'id_144',
                               'id_145',
                               'id_146',
                               'id_147',
                               'id_148',
                               'id_149',
                               'id_150',
                               'id_151',
                               'id_2',
                               'id_26',
                               'id_28',
                               'id_3',
                               'id_32',
                               'id_33',
                               'id_34',
                               'id_35',
                               'id_36',
                               'id_37',
                               'id_38',
                               'id_39',
                               'id_40',
                               'id_41',
                               'id_42',
                               'id_43',
                               'id_44',
                               'id_45',
                               'id_46',
                               'id_47',
                               'id_48',
                               'id_49',
                               'id_50',
                               'id_51',
                               'id_52',
                               'id_53',
                               'id_54',
                               'id_55',
                               'id_56',
                               'id_57',
                               'id_58',
                               'id_59',
                               'id_60',
                               'id_61',
                               'id_62',
                               'id_63',
                               'id_64',
                               'id_65',
                               'id_66',
                               'id_67',
                               'id_68',
                               'id_69',
                               'id_70',
                               'id_71',
                               'id_72',
                               'id_73',
                               'id_74',
                               'id_75',
                               'id_76',
                               'id_77',
                               'id_78',
                               'id_79',
                               'id_80',
                               'id_81',
                               'id_82',
                               'id_83',
                               'id_84',
                               'id_85',
                               'id_86',
                               'id_95',
                               'id_96',
                               'id_97',
                               'id_98',
                               'id_99']]

data_station_train = data_train[['id_1',
                                 'id_100',
                                 'id_101',
                                 'id_102',
                                 'id_103',
                                 'id_104',
                                 'id_105',
                                 'id_106',
                                 'id_107',
                                 'id_108',
                                 'id_109',
                                 'id_110',
                                 'id_111',
                                 'id_112',
                                 'id_113',
                                 'id_114',
                                 'id_115',
                                 'id_116',
                                 'id_117',
                                 'id_118',
                                 'id_119',
                                 'id_120',
                                 'id_121',
                                 'id_122',
                                 'id_123',
                                 'id_124',
                                 'id_125',
                                 'id_126',
                                 'id_127',
                                 'id_128',
                                 'id_129',
                                 'id_130',
                                 'id_131',
                                 'id_132',
                                 'id_133',
                                 'id_134',
                                 'id_135',
                                 'id_136',
                                 'id_137',
                                 'id_138',
                                 'id_139',
                                 'id_140',
                                 'id_141',
                                 'id_142',
                                 'id_143',
                                 'id_144',
                                 'id_145',
                                 'id_146',
                                 'id_147',
                                 'id_148',
                                 'id_149',
                                 'id_150',
                                 'id_151',
                                 'id_2',
                                 'id_26',
                                 'id_28',
                                 'id_3',
                                 'id_32',
                                 'id_33',
                                 'id_34',
                                 'id_35',
                                 'id_36',
                                 'id_37',
                                 'id_38',
                                 'id_39',
                                 'id_40',
                                 'id_41',
                                 'id_42',
                                 'id_43',
                                 'id_44',
                                 'id_45',
                                 'id_46',
                                 'id_47',
                                 'id_48',
                                 'id_49',
                                 'id_50',
                                 'id_51',
                                 'id_52',
                                 'id_53',
                                 'id_54',
                                 'id_55',
                                 'id_56',
                                 'id_57',
                                 'id_58',
                                 'id_59',
                                 'id_60',
                                 'id_61',
                                 'id_62',
                                 'id_63',
                                 'id_64',
                                 'id_65',
                                 'id_66',
                                 'id_67',
                                 'id_68',
                                 'id_69',
                                 'id_70',
                                 'id_71',
                                 'id_72',
                                 'id_73',
                                 'id_74',
                                 'id_75',
                                 'id_76',
                                 'id_77',
                                 'id_78',
                                 'id_79',
                                 'id_80',
                                 'id_81',
                                 'id_82',
                                 'id_83',
                                 'id_84',
                                 'id_85',
                                 'id_86',
                                 'id_95',
                                 'id_96',
                                 'id_97',
                                 'id_98',
                                 'id_99']]
# 时滞
data_t1_test = data_test[['AOD_0_T1',
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
                          'temperature_T1']]

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
                            'temperature_T1']]
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
# 输入层 全部

AOD_input = Input(shape=(len(data_aod_test.columns),), name="AOD_input")  # AOD
AODs_input = Input(shape=(len(data_aods_test.columns),),
                   name="AODs_input")  # AODs

Meteorology_input = Input(
    shape=(len(data_sky_test.columns),), name="Meteorology_input")  # 气象

Weather_input = Input(shape=(len(data_t1_test.columns),),
                      name="Weather_input")  # 时滞

Ndvi_input = Input(shape=(len(data_ndvi_test.columns),),
                   name="NDVI_input")  # NDVI

Time_input = Input(shape=(len(data_time_test.columns),),
                   name="Time_input")  # 时间

Station_input = Input(
    shape=(len(data_station_test.columns),), name="Station_input")  # 空间
# 融合层
aods_concat = AODs_input  # AOD + AODs

meteorology_concat = Meteorology_input  # AOD + 气象

weather_concat = Weather_input  # AOD + 时滞

ndvi_concat = Ndvi_input # AOD + NDVI

time_concat = Time_input # AOD + 时间
station_concat = Station_input  # AOD + 空间

allin_concat = AOD_input  # 全
# 全连接层 1

# AOD + AODs
aods_x1 = Dense(24,
                activation=keras.layers.ELU(alpha=0.1),
                name="FC1_aods")(aods_concat)

# AOD + 气象
meteorology_x1 = Dense(
    24, activation=keras.layers.ELU(alpha=0.1), name="FC1_meteorology")(meteorology_concat)

# AOD + 时滞
weather_x1 = Dense(24,
                   activation=keras.layers.ELU(alpha=0.1),
                   name="FC1_T1")(weather_concat)

# AOD + NDVI
ndvi_x1 = Dense(24,
                activation=keras.layers.ELU(alpha=0.1),
                name="FC1_NDVI")(ndvi_concat)

# AOD + 时间
time_x1 = Dense(24,
                activation=keras.layers.ELU(alpha=0.1),
                name="FC1_Time")(time_concat)

# AOD + 空间
station_x1 = Dense(24,
                   activation=keras.layers.ELU(alpha=0.1),
                   name="FC1_Station")(station_concat)

# 全部特征
allin_x1 = Dense(24,
                 activation=keras.layers.ELU(alpha=0.1),
                 name="FC11_AIA")(allin_concat)
# 残差层


# AOD + AODs
aods_residual_connection1 = Dense(8,
                                  activation=keras.layers.ELU(alpha=0.1),
                                  name="ResidualConnectionAODs")(aods_x1)

aods_residual_connection2 = Dense(
    24, activation=keras.layers.advanced_activations.ELU(
        alpha=1.0), name="FullConnectionAOD_RC")(aods_residual_connection1)
# aods_residual_connection = add([aods_x, aods_residual_connection],
# name="ResidualConnectionAODs_Add")  # 原先版本
aods_residual_output = add([aods_x1,
                            aods_residual_connection2],
                           name="ResidualConnectionAODs_Add")


# AOD + 气象
meteorology_residual_connection1 = Dense(
    8, activation=keras.layers.ELU(alpha=0.1), name="ResidualConnectionMA")(meteorology_x1)

meteorology_residual_connection2 = Dense(
    24, activation=keras.layers.ELU(alpha=0.1), name="FullConnectionMA_RC")(meteorology_residual_connection1)

meteorology_residual_output = add(
    [meteorology_x1, meteorology_residual_connection2], name="ResidualConnectionMA_Add")


# AOD + 时滞
weather_residual_connection1 = Dense(
    8, activation=keras.layers.ELU(alpha=0.1), name="ResidualConnectionWA")(weather_x1)

weather_residual_connection2 = Dense(
    24, activation=keras.layers.ELU(alpha=0.1), name="FullConnectionWAForRC")(weather_residual_connection1)

weather_residual_output = add([weather_x1,
                               weather_residual_connection2],
                              name="ResidualConnectionWA_Add")


# AOD + NDVI
ndvi_residual_connection1 = Dense(
    8, activation=keras.layers.ELU(alpha=0.1), name="ResidualConnectionNDVI")(ndvi_x1)

ndvi_residual_connection2 = Dense(
    24, activation=keras.layers.ELU(alpha=0.1), name="FullConnectionNDVI_RC")(ndvi_residual_connection1)

ndvi_residual_output = add([ndvi_x1,
                            ndvi_residual_connection2],
                           name="ResidualConnectionNDVI_Add")


# AOD + 时间
time_residual_connection1 = Dense(
    8, activation=keras.layers.ELU(alpha=0.1), name="ResidualConnectionTime")(time_x1)

time_residual_connection2 = Dense(
    24, activation=keras.layers.ELU(alpha=0.1), name="FullConnectionTime_RC")(time_residual_connection1)

time_residual_output = add([time_x1,
                            time_residual_connection2],
                           name="ResidualConnectionTime_Add")


# AOD + 空间
station_residual_connection1 = Dense(
    8, activation=keras.layers.ELU(alpha=0.1), name="ResidualConnectionStation")(station_x1)

station_residual_connection2 = Dense(
    24, activation=keras.layers.ELU(alpha=0.1), name="FullConnectionStation_RC")(station_residual_connection1)

station_residual_output = add([station_x1,
                               station_residual_connection2],
                              name="ResidualConnectionStation_Add")


# 全部特征
allin_residual_connection1 = Dense(
    8, activation=keras.layers.ELU(alpha=0.1), name="ResidualConnectionAIA")(allin_x1)

allin_residual_connection2 = Dense(
    24, activation=keras.layers.ELU(alpha=0.1), name="FullConnectionAIA_RC")(allin_residual_connection1)

allin_residual_output = add([allin_x1,
                             allin_residual_connection2],
                            name="ResidualConnectionAIA_Add")

# 全连接层 2


# AOD + AODs
aods_x2 = Dense(4,
                activation=keras.layers.ELU(alpha=0.1),
                name="FullConnectionAODs_2")(aods_residual_output)


# AOD + 气象
meteorology_x2 = Dense(4,
                       activation=keras.layers.LeakyReLU(alpha=0.1),
                       name="FullConnectionMA_2")(meteorology_residual_output)


# AOD + 时滞
weather_x2 = Dense(4,
                   activation=keras.layers.ELU(alpha=0.1),
                   name="FullConnectionWA_2")(weather_residual_output)


# AOD + NDVI
ndvi_x2 = Dense(4,
                activation=keras.layers.ELU(alpha=0.1),
                name="FullConnectionNDVI_2")(ndvi_residual_output)


# AOD + 时间
time_x2 = Dense(4,
                activation=keras.layers.ELU(alpha=0.1),
                name="FullConnectionTime_2")(time_residual_output)


# AOD + 空间
station_x2 = Dense(4,
                   activation=keras.layers.ELU(alpha=0.1),
                   name="FullConnectionStation_2")(station_residual_output)


# 全部特征
allin_x2 = Dense(4,
                 activation=keras.layers.ELU(alpha=0.1),
                 name="FullConnectionAIA_2")(allin_residual_output)

# Dropout


# AOD + AODs
aods_y = core.Dropout(rate=0.05,
                      name="Aods_Module")(aods_x2)


# AOD + 气象
meteorology_y = core.Dropout(rate=0.05,
                             name="Meteorology_Module")(meteorology_x2)


# AOD + 时滞
weather_y = core.Dropout(rate=0.05,
                         name="Weather_Module")(weather_x2)


# AOD + NDVI
ndvi_y = core.Dropout(rate=0.05,
                      name="NDVI_Module")(ndvi_x2)


# AOD + 时间
time_y = core.Dropout(rate=0.05,
                      name="Time_Module")(time_x2)

# AOD + 空间
station_y = core.Dropout(rate=0.05,
                         name="Station_Module")(station_x2)


# 全部特征
allin_y = core.Dropout(rate=0.05,
                       name="AllIn_Module")(allin_x2)


# 模型层

# 输入顺序： 气象 时滞 NDVI 时间 空间 AODs AOD

# AOD + AODs
model_aods = Model(
    inputs=[
        AODs_input],
    outputs=aods_y)


# AOD + 气象
model_meteorology = Model(
    inputs=[
        Meteorology_input,
        ],
    outputs=meteorology_y)


# AOD + 时滞
model_weather = Model(
    inputs=[Weather_input,
            ],
    outputs=weather_y)


# AOD + NDVI
model_ndvi = Model(
    inputs=[
        Ndvi_input,
        ],
    outputs=ndvi_y)

# AOD + 时间
model_time = Model(
    inputs=[
        Time_input,
        ],
    outputs=time_y)

# AOD + 空间
model_station = Model(
    inputs=[
        Station_input,
        ],
    outputs=station_y)
# 全部特征 AOD
model_allin = Model(
    inputs=[
            AOD_input],
    outputs=allin_y)


# 最后的融合

# 捕捉的影响的融合层
res_concat = concatenate([
    model_aods.output,
    model_meteorology.output,
    model_weather.output,
    model_ndvi.output,
    model_time.output,
    model_station.output,
    model_allin.output])

# 全连接层 1
res_x1 = Dense(24,
               name="ResFullConnectionResModelForLast")(res_concat)


# 残差连接层
res_residual_connection1 = Dense(8,
                                 name="ResidualConnectionLast")(res_x1)

res_residual_connection2 = Dense(
    24, name="FullConnectionLast_RC")(res_residual_connection1)

res_residual_output = add(
    [res_x1, res_residual_connection2], name="ResidualConnectionLast_Add")


# 全连接层 2
res_x2 = Dense(8,
               activation=keras.layers.ELU(alpha=0.1),
               name="FullConnectionLast_2")(res_residual_output)
res_x3 = Dense(4,
               activation=keras.layers.ELU(alpha=0.1),
               name="FullConnectionLast_2x")(res_x2)
# Dropout
res_y = core.Dropout(rate=0.05,
                     name="Res_Module")(res_x3)


# 最终融合结果
res_outcome = Dense(
    1,
    activation=keras.layers.ELU(alpha=0.1),
    kernel_regularizer=keras.regularizers.l2(0.1),
    name="sigmoid_FC")(res_y)
# 正则化

# 编译最终模型
# 输入顺序： 气象 时滞 NDVI 时间 空间 AODs AOD
model_last = Model(
    inputs=[
        Meteorology_input,
        Weather_input,
        Ndvi_input,
        Time_input,
        Station_input,
        AODs_input,
        AOD_input],
    outputs=res_outcome)

model_last.compile(
    loss="mse",
    optimizer=keras.optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=0.0),
    #     optimizer=keras.optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=0.0),  #
    # optimizer=keras.optimizers.Adagrad(lr=0.01, epsilon=None, decay=0.0),
    # optimizer=keras.optimizers.SGD(lr=0.01, momentum=0.0, decay=0.0, nesterov=False),
    # optimizer=keras.optimizers.Adam(lr=0.01, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False),
    metrics=["accuracy"])


# 格式转换
data_sky_train = np.array(data_sky_train)
data_t1_train = np.array(data_t1_train)
data_ndvi_train = np.array(data_ndvi_train)
data_time_train = np.array(data_time_train)
data_station_train = np.array(data_station_train)
data_aods_train = np.array(data_aods_train)
data_aod_train = np.array(data_aod_train)

data_sky_test = np.array(data_sky_test)
data_t1_test = np.array(data_t1_test)
data_ndvi_test = np.array(data_ndvi_test)
data_time_test = np.array(data_time_test)
data_station_test = np.array(data_station_test)
data_aods_test = np.array(data_aods_test)
data_aod_test = np.array(data_aod_test)

# 运行
# 输入顺序： 气象 时滞 NDVI 时间 空间 AODs AOD
model_last.fit([
    data_sky_train,
    data_t1_train,
    data_ndvi_train,
    data_time_train,
    data_station_train,
    data_aods_train,
    data_aod_train
],
    data_pm_train,
    epochs=30000,
    batch_size=1024)


res = model_last.predict([data_sky_test,
                          data_t1_test,
                          data_ndvi_test,
                          data_time_test,
                          data_station_test,
                          data_aods_test,
                          data_aod_test])
datares = res - data_pm_test
datares.PM25 = datares.PM25.map(lambda x: abs(x))
data_predt = pd.concat([datares, data_pm_test], axis=1)
data_predt.columns = ["差值", '真']
data_predt['差值'] = data_predt['差值'].map(lambda x: abs(x))
data_predt['百分误'] = data_predt['差值'].div(data_predt["真"])

data_predt.to_excel('C:\\Users\\iii\\Desktop\\error2.xlsx')
