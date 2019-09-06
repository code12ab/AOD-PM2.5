# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/1 21:51
import pandas as pd
import keras
from keras.layers import Input, Embedding, LSTM, Dense, concatenate, core, add
from keras.models import Model
import os
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# 读取
input_path = 'D:\\全2018_日出足够.xlsx'
data_all = pd.read_excel(input_path, index_col='日期')
data_all = data_all.dropna()

data_ts_df = data_all[['tm_mon', 'tm_mday', 'tm_wday', 'tm_yday', 'tm_week','id']]
# 虚拟变量
for ccc in data_ts_df.columns:
    data_ts_df[ccc] = data_ts_df[ccc].map(lambda x : str(x))
data_get_dummies1 = pd.get_dummies(data_ts_df[['tm_mon']],drop_first=True)
data_get_dummies2 = pd.get_dummies(data_ts_df[['tm_mday']], drop_first=True)
data_get_dummies3 = pd.get_dummies(data_ts_df[['id']], drop_first=True)
data_dummies = pd.concat([data_get_dummies1,data_get_dummies2,data_get_dummies3,data_ts_df[['tm_mon']]], axis =1)
print(data_dummies.columns, len(data_dummies.columns))
# 去掉无用列
data_to_std = data_all.drop(['tm_mon', 'tm_mday', 'tm_wday', 'tm_yday', 'tm_week','id'], axis=1)
# 标准化
from sklearn.preprocessing import MinMaxScaler
data_to_std2= MinMaxScaler().fit_transform(data_to_std)
data_to_std2 = pd.DataFrame(data_to_std2)
data_to_std2 = data_to_std2.set_index(data_to_std.index)
data_to_std2.columns = data_to_std.columns
print(data_to_std2.shape)
print(data_ts_df.shape)
data_out = pd.concat([data_dummies, data_to_std2],join='outer', axis=1)

#data_out2.to_csv('test.csv')

data_test = data_out[(data_out['tm_mon']==1)|
                     (data_out['tm_mon']==4)|
                    (data_out['tm_mon']==7)|
                    (data_out['tm_mon']==10)]
data_train = data_out[(data_out['tm_mon']==3)|
                     (data_out['tm_mon']==2)|
                    (data_out['tm_mon']==6)|
                    (data_out['tm_mon']==5)|
                     (data_out['tm_mon']==9)|
                    (data_out['tm_mon']==8)|
                    (data_out['tm_mon']==12)|
                     (data_out['tm_mon']==11)]

# AOD
data_aod_test = data_test[['AOD_0']]
data_aods_test = data_test[[
                     'AOD_1',
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

data_aod_train = data_train[['AOD_0']]
data_aods_train = data_train[[
                     'AOD_1',
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
# 气象
data_sky_test = data_test[['apparentTemperatureHigh',
                     'apparentTemperatureLow',
                     'apparentTemperatureMax',
                     'apparentTemperatureMin',
                     'cloudCover',
                     'dewPoint',
                     'humidity',
                     'pressure',
                     'sunTime',
                     'temperatureHigh',
                     'temperatureLow',
                     'temperatureMax',
                     'temperatureMin',
                     'uvIndex',
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
                     'pressure',
                     'sunTime',
                     'temperatureHigh',
                     'temperatureLow',
                     'temperatureMax',
                     'temperatureMin',
                     'uvIndex',
                     'visibility',
                     'windBearing',
                     'windGust',
                     'windSpeed',
                     'apparentTemperature',
                     'temperature']]
# 时空特征
data_ts_test = data_test[['id_124',
    'id_51',
    'id_42',
    'tm_mday_29',
    'tm_mon_5',
    'id_128',
    'id_85',
    'id_65',
    'id_52',
    'id_44',
    'tm_mday_19',
    'id_136',
    'id_103',
    'id_34',
    'id_106',
    'id_68',
    'id_122',
    'tm_mon_3',
    'tm_mday_6',
    'tm_mday_16',
    'tm_mon_6',
    'id_2',
    'tm_mday_8',
    'id_83',
    'id_64',
    'tm_mday_24',
    'id_138',
    'id_70',
    'id_110',
    'id_32',
    'id_105',
    'id_98',
    'id_97',
    'id_150',
    'tm_mday_22',
    'tm_mday_25',
    'id_39',
    'id_148',
    'tm_mday_30',
    'id_41',
    'id_146',
    'id_147',
    'id_46',
    'tm_mday_13',
    'id_58',
    'tm_mday_9',
    'tm_mon_12',
    'tm_mon_8',
    'id_40',
    'id_62',
    'id_50',
    'id_37',
    'tm_mday_10',
    'tm_mon_4',
    'id_144',
    'tm_mday_5',
    'id_137',
    'tm_mon_10',
    'id_28',
    'id_43',
    'id_80',
    'id_143',
    'id_121',
    'tm_mday_21',
    'id_56',
    'id_33',
    'id_127',
    'tm_mday_27',
    'id_82',
    'id_38',
    'id_102',
    'tm_mday_20',
    'id_60',
    'id_76',
    'tm_mday_23',
    'id_99',
    'id_54',
    'tm_mday_12',
    'id_59',
    'id_151',
    'id_126',
    'id_55',
    'id_81',
    'tm_mday_31',
    'tm_mday_2',
    'id_129',
    'id_48',
    'tm_mday_14',
    'tm_mon_11',
    'id_74',
    'id_75',
    'id_120',
    'tm_mday_28',
    'id_134',
    'id_108',
    'id_117',
    'id_57',
    'tm_mon_2',
    'tm_mday_17',
    'id_26',
    'id_95',
    'id_118',
    'id_49',
    'id_67',
    'id_69',
    'id_107',
    'id_79',
    'id_66',
    'id_35',
    'id_53',
    'id_114',
    'tm_mon_7',
    'id_104',
    'tm_mon_9',
    'id_96',
    'tm_mday_7',
    'id_133',
    'tm_mday_11',
    'id_78',
    'id_115',
    'tm_mday_15',
    'id_139',
    'id_100',
    'id_63',
    'id_112',
    'tm_mday_18',
    'id_131',
    'id_142',
    'id_47',
    'id_36',
    'id_130',
    'id_141',
    'id_111',
    'id_71',
    'id_84',
    'tm_mday_26',
    'id_61',
    'id_135',
    'id_72',
    'id_113',
    'id_145',
    'id_116',
    'tm_mday_4',
    'tm_mday_3',
    'id_119',
    'id_1',
    'id_77',
    'id_3',
    'id_109',
    'id_101',
    'id_123',
    'id_73',
    'id_45',
    'id_125',
    'id_149',
    'id_132',
    'id_86',
    'id_140']]
data_ts_train = data_train[[    'id_124',
    'id_51',
    'id_42',
    'tm_mday_29',
    'tm_mon_5',
    'id_128',
    'id_85',
    'id_65',
    'id_52',
    'id_44',
    'tm_mday_19',
    'id_136',
    'id_103',
    'id_34',
    'id_106',
    'id_68',
    'id_122',
    'tm_mon_3',
    'tm_mday_6',
    'tm_mday_16',
    'tm_mon_6',
    'id_2',
    'tm_mday_8',
    'id_83',
    'id_64',
    'tm_mday_24',
    'id_138',
    'id_70',
    'id_110',
    'id_32',
    'id_105',
    'id_98',
    'id_97',
    'id_150',
    'tm_mday_22',
    'tm_mday_25',
    'id_39',
    'id_148',
    'tm_mday_30',
    'id_41',
    'id_146',
    'id_147',
    'id_46',
    'tm_mday_13',
    'id_58',
    'tm_mday_9',
    'tm_mon_12',
    'tm_mon_8',
    'id_40',
    'id_62',
    'id_50',
    'id_37',
    'tm_mday_10',
    'tm_mon_4',
    'id_144',
    'tm_mday_5',
    'id_137',
    'tm_mon_10',
    'id_28',
    'id_43',
    'id_80',
    'id_143',
    'id_121',
    'tm_mday_21',
    'id_56',
    'id_33',
    'id_127',
    'tm_mday_27',
    'id_82',
    'id_38',
    'id_102',
    'tm_mday_20',
    'id_60',
    'id_76',
    'tm_mday_23',
    'id_99',
    'id_54',
    'tm_mday_12',
    'id_59',
    'id_151',
    'id_126',
    'id_55',
    'id_81',
    'tm_mday_31',
    'tm_mday_2',
    'id_129',
    'id_48',
    'tm_mday_14',
    'tm_mon_11',
    'id_74',
    'id_75',
    'id_120',
    'tm_mday_28',
    'id_134',
    'id_108',
    'id_117',
    'id_57',
    'tm_mon_2',
    'tm_mday_17',
    'id_26',
    'id_95',
    'id_118',
    'id_49',
    'id_67',
    'id_69',
    'id_107',
    'id_79',
    'id_66',
    'id_35',
    'id_53',
    'id_114',
    'tm_mon_7',
    'id_104',
    'tm_mon_9',
    'id_96',
    'tm_mday_7',
    'id_133',
    'tm_mday_11',
    'id_78',
    'id_115',
    'tm_mday_15',
    'id_139',
    'id_100',
    'id_63',
    'id_112',
    'tm_mday_18',
    'id_131',
    'id_142',
    'id_47',
    'id_36',
    'id_130',
    'id_141',
    'id_111',
    'id_71',
    'id_84',
    'tm_mday_26',
    'id_61',
    'id_135',
    'id_72',
    'id_113',
    'id_145',
    'id_116',
    'tm_mday_4',
    'tm_mday_3',
    'id_119',
    'id_1',
    'id_77',
    'id_3',
    'id_109',
    'id_101',
    'id_123',
    'id_73',
    'id_45',
    'id_125',
    'id_149',
    'id_132',
    'id_86',
    'id_140']]
# 时滞
data_t1_test = data_test[['AOD_0_T1',
                    'apparentTemperatureHigh_T1',
                    'apparentTemperatureLow_T1',
                    'apparentTemperatureMax_T1',
                    'apparentTemperatureMin_T1',
                    'cloudCover_T1',
                    'dewPoint_T1',
                    'humidity_T1',
                    'pressure_T1',
                    'sunriseTime_T1',
                    'sunsetTime_T1',
                    'temperatureHigh_T1',
                    'temperatureLow_T1',
                    'temperatureMax_T1',
                    'temperatureMin_T1',
                    'uvIndex_T1',
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
                    'pressure_T1',
                    'sunriseTime_T1',
                    'sunsetTime_T1',
                    'temperatureHigh_T1',
                    'temperatureLow_T1',
                    'temperatureMax_T1',
                    'temperatureMin_T1',
                    'uvIndex_T1',
                    'visibility_T1',
                    'windBearing_T1',
                    'windGust_T1',
                    'windSpeed_T1',
                    'apparentTemperature_T1',
                    'temperature_T1']]
# NDVI
data_ndvi_test = data_test[['NDVI_0','AOD_1',
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
data_ndvi_train = data_train[['NDVI_0','AOD_1',
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
# 第一个模块 当日天气模块
#
# 输入层
Meteorology_input = Input(shape=(len(data_sky_test.columns),), name="Meteorology_input")
AODs_input = Input(shape=(len(data_aod_test.columns),), name="AODs_input")
# 因素融合层
meteorology_concat = concatenate([Meteorology_input, AODs_input])
# 全连接层
meteorology_x = Dense(
    24,
    activation=keras.layers.LeakyReLU(alpha=0.4),
    name="FullConnectionMA_1")(meteorology_concat)
# 残差层
meteorology_residual_connection = Dense(
    16,
    activation=keras.layers.LeakyReLU(alpha=0.3),
    name="ResidualConnectionMA")(meteorology_x)
meteorology_residual_connection = Dense(
    24,
    activation=keras.layers.LeakyReLU(alpha=0.4),
    name="FullConnectionMA_RC")(meteorology_residual_connection)
meteorology_residual_connection = add(
    [meteorology_x, meteorology_residual_connection], name="ResidualConnectionMA_Add")
# 全连接层
meteorology_x = Dense(
    12,
    activation=keras.layers.LeakyReLU(alpha=0.4),
    name="FullConnectionMA_2")(meteorology_residual_connection)
# Dropout
meteorology_y = core.Dropout(
    rate=0.5, name="Meteorology_Module")(meteorology_x)
# 模型层
model_meteorology = Model(
    inputs=[
        Meteorology_input,
        AODs_input],
    outputs=meteorology_y)
# 第二个模块 时滞天气模块

Weather_input = Input(shape=(len(data_t1_test.columns),), name="Weather_input")  # 只添加新的因素即可
# AODs_input = Input(shape=(17,), name="AODs_input")
# 因素融合层
weather_concat = concatenate([Weather_input, AODs_input])
# 全连接层
weather_x = Dense(
    24,
    activation=keras.layers.LeakyReLU(alpha=0.4),
    name="FullConnectionWA_1")(weather_concat)
# 残差层
weather_residual_connection = Dense(
    12,
    activation=keras.layers.LeakyReLU(alpha=0.4),
    name="ResidualConnectionWA")(weather_x)
weather_residual_connection = Dense(
    24,
    activation=keras.layers.LeakyReLU(alpha=0.4),
    name="FullConnectionWAForRC")(weather_residual_connection)
weather_residual_connection = add(
    [weather_x, weather_residual_connection], name="ResidualConnectionWA_Add")
# 全连接层
weather_x = Dense(
    12,
    activation=keras.layers.LeakyReLU(alpha=0.4),
    name="FullConnectionWA_2")(weather_residual_connection)
# Dropout
# use `rate` instead of `keep_prob`. r=1-p.
weather_y = core.Dropout(rate=0.5, name="Weather_Module")(weather_x)

# 模型层
model_weather = Model(inputs=[Weather_input, AODs_input], outputs=weather_y)


# 第三个模块 其他空气污染物模块 更改为ndvi
# 输入层
OtherPollution_input = Input(shape=(len(data_ndvi_test.columns),))
# 因素融合层
otherpollution_concat = concatenate([OtherPollution_input, AODs_input])
# 全连接层
otherpollution_x = Dense(
    24,
    activation=keras.layers.LeakyReLU(alpha=0.4),
    name="FullConnectionOPA_1")(otherpollution_concat)
# 残差层
otherpollution_residual_connection = Dense(
    8,
    activation=keras.layers.LeakyReLU(alpha=0.4),
    name="ResidualConnectionOPA")(otherpollution_x)
otherpollution_residual_connection = Dense(
    24,
    activation=keras.layers.LeakyReLU(alpha=0.4),
    name="FullConnectionOPA_RC")(otherpollution_residual_connection)
otherpollution_residual_connection = add(
    [otherpollution_x, otherpollution_residual_connection], name="ResidualConnectionOPA_Add")
# 全连接层
otherpollution_x = Dense(
    6,
    activation=keras.layers.LeakyReLU(alpha=0.4),
    name="FullConnectionOPA_2")(otherpollution_residual_connection)
# Dropout
otherpollution_y = core.Dropout(
    rate=0.5, name="OtherPollution_Module")(otherpollution_x)
# 模型层
model_otherpollution = Model(
    inputs=[
        OtherPollution_input,
        AODs_input],
    outputs=otherpollution_y)

###### 第四个模块 时空元属性模块
# 输入层
TimeStation_input = Input(shape=(len(data_ts_train.columns),), name="TimeStation_input")

# 因素融合层
timestation_concat = concatenate([TimeStation_input, AODs_input])
# 全连接层
timestation_x = Dense(
    24,
    activation=keras.layers.LeakyReLU(alpha=0.4),
    name="FullConnectionOTSA_1")(timestation_concat)
# 残差层
timestation_residual_connection = Dense(
    8,
    activation=keras.layers.LeakyReLU(alpha=0.4),
    name="ResidualConnectionTSA")(timestation_x)
timestation_residual_connection = Dense(
    24,
    activation=keras.layers.LeakyReLU(alpha=0.4),
    name="FullConnectionTSA_RC")(timestation_residual_connection)
timestation_residual_connection = add(
    [timestation_x, timestation_residual_connection], name="ResidualConnectionTSA_Add")
# 全连接层
timestation_x = Dense(
    8,
    activation=keras.layers.LeakyReLU(alpha=0.4),
    name="FullConnectionTSA_2")(timestation_residual_connection)
timestation_x = Dense(
    4,
    activation=keras.layers.LeakyReLU(alpha=0.4),
    name="FullConnectionTSA_222")(timestation_x)
# Dropout
timestation_y = core.Dropout(
    rate=0.5, name="TimeStation_Module")(timestation_x)
# 模型层
model_timestation = Model(
    inputs=[
        TimeStation_input,
        AODs_input],
    outputs=timestation_y)
# 第五个模块 整体影响模块
# 因素融合层
allin_concat = concatenate([Meteorology_input,
                            Weather_input,
                            OtherPollution_input,
                            TimeStation_input,
                            AODs_input])
# 全连接层
allin_x = Dense(
    48,
    activation=keras.layers.LeakyReLU(alpha=0.2),
    name="FullConnectionAIA_1")(allin_concat)
# 残差层
allin_residual_connection = Dense(
    24,
    activation=keras.layers.LeakyReLU(alpha=0.2),
    name="ResidualConnectionAIA")(allin_x)
allin_residual_connection = Dense(
    48,
    activation=keras.layers.LeakyReLU(alpha=0.2),
    name="FullConnectionAIA_RC")(allin_residual_connection)
allin_residual_connection = add(
    [allin_x, allin_residual_connection], name="ResidualConnectionAIA_Add")
# 全连接层
allin_x = Dense(18, activation=keras.layers.LeakyReLU(alpha=0.2),
                name="FullConnectionAIA_2")(allin_residual_connection)
# Dropout
allin_y = core.Dropout(rate=0.6, name="AllIn_Module")(allin_x)
# 模型层
model_allin = Model(
    inputs=[
        Meteorology_input,
        Weather_input,
        OtherPollution_input,
        TimeStation_input,
        AODs_input],
    outputs=allin_y)

# 最后的融合
# 捕捉的影响的融合层
res_concat = concatenate([model_meteorology.output,
                          model_weather.output,
                          model_otherpollution.output,
                          model_timestation.output,
                          model_allin.output])
# 全连接层
res_x = Dense(
    64,
    name="ResFullConnectionResModelForLast")(res_concat)
# 残差连接层
res_residual_connection = Dense(
    48,
    name="ResidualConnectionLast")(res_x)
res_residual_connection = Dense(
    64,
    name="FullConnectionLast_RC")(res_residual_connection)
res_residual_connection = add(
    [res_x, res_residual_connection], name="ResidualConnectionLast_Add")
# 全连接层
res_x = Dense(24, activation=keras.layers.ELU(alpha=0.4),
              name="FullConnectionLast_2")(res_residual_connection)
res_x2 = Dense(8, activation=keras.layers.ELU(alpha=0.4),
              name="FullConnectionLast_2x")(res_x)
# Dropout
res_y = core.Dropout(rate=0.1, name="Res_Module")(res_x2)
# sigmoid 最终融合结果
res_outcome = Dense(
    1,
    activation='sigmoid',
    kernel_regularizer=keras.regularizers.l2(0.01),
    name="sigmoid_FC")(res_y)
# 编译最终模型
model_last = Model(
    inputs=[
        Meteorology_input,
        Weather_input,
        OtherPollution_input,
        TimeStation_input,
        AODs_input],
    outputs=res_outcome)
model_last.compile(loss="mse",
                   optimizer=keras.optimizers.Adam(lr=0.1, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False),
                   metrics=["accuracy"])


# print(model_last.summary())
model_last.fit([data_sky_train,data_t1_train,data_ndvi_train,data_ts_train,data_aod_train],data_pm_train,
               epochs = 2000,
               batch_size =512)

res = model_last.predict([data_sky_test,data_t1_test,data_ndvi_test,data_ts_test,data_aod_test])
datares = res - data_pm_test
datares.PM25 = datares.PM25.map(lambda x: abs(x))
print(np.average(datares))

data_predt = pd.concat([datares,data_pm_test], axis=1)
data_predt.columns = ["差值",'真']
data_predt['差值'] = data_predt['差值'].map(lambda x: abs(x))
data_predt['百分误'] = data_predt['差值'].div(data_predt["真"])

data_predt.to_excel('baifenwu2.xlsx')

# os.system('shutdown -s -f -t 60')