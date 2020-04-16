# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/9/21 19:40


# 库
import pandas as pd
import numpy as np
import os

# 读取
# input_path = 'D:\\雨雪+2018_new_pm.xlsx'
for year in [2008,2009,2010,2011,2012,2013,2014,2015,2016,2017]:

    input_path = 'D:\\毕业论文程序\\08到17年\\输入特征_补零再单位转换\\%s.xlsx' % year
    data_all = pd.read_excel(input_path, index_col='日期')
    del data_all['ozone'],
    del data_all['ozone_T1']


    for i in range(0,17):
        data_all['AOD_%s' % i] = data_all['AOD_%s' % i].map(lambda x: (1/1000)*x)
        data_all['AOD_%s_T1' % i] = data_all['AOD_%s_T1' % i].map(lambda x: (1/1000)*x)


    data_all['atempHL'] = data_all['apparentTemperatureHigh'] - data_all['apparentTemperatureLow']
    data_all['atempMM'] = data_all['apparentTemperatureMax'] - data_all['apparentTemperatureMin']

    data_all['tempHL'] = data_all['temperatureHigh'] - data_all['temperatureLow']
    data_all['tempMM'] = data_all['temperatureMax'] - data_all['temperatureMin']

    # 温差搞成摄氏度
    data_all['tempMM'] = data_all['tempMM'].map(lambda x: (x-32)/1.8)
    data_all['tempHL'] = data_all['tempHL'].map(lambda x: (x-32)/1.8)
    data_all['atempMM'] = data_all['atempMM'].map(lambda x: (x-32)/1.8)
    data_all['atempHL'] = data_all['atempHL'].map(lambda x: (x-32)/1.8)

    # 英里时 变 米每秒
    data_all['windSpeed_T1'] = data_all['windSpeed_T1'].map(lambda x: 0.44704*x)
    data_all['windSpeed'] = data_all['windSpeed'].map(lambda x: (x-32)/0.44704*x)
    data_all['windGust_T1'] = data_all['windGust_T1'].map(lambda x: (x-32)/0.44704*x)
    data_all['windGust'] = data_all['windGust'].map(lambda x: (x-32)/0.44704*x)

    # 补全
    data_all['NDVI_0'] = data_all['NDVI_0'].fillna(method='ffill')
    # 英里 转 米

    data_all['visibility'] = data_all['visibility'].map(lambda x: 1.609344*x)
    data_all['visibility_T1'] = data_all['visibility_T1'].map(lambda x: 1.609344*x)

    data_all.to_excel('D:\\毕业论文程序\\08到17年\\输入特征_补零再单位转换\\%s.xlsx' % year)