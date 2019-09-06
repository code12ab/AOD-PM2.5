# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/9/1 19:28


# 库
import pandas as pd
import numpy as np
import os

aod_path = 'D:\\毕业论文程序\\建模数据\\气溶胶\\2018\\'
darksky_path = 'D:\\毕业论文程序\\建模数据\\气象\\2018_不补全\\'
out_path = 'D:\\毕业论文程序\\建模数据\\时滞\\2018_不补全\\'
file_list = os.listdir(aod_path)

for file in file_list:
    data_sky = pd.read_excel(darksky_path + file)
    data_aod = pd.read_excel(aod_path + file)
    data = pd.merge(left=data_aod, right=data_sky, how='right', on='日期')
    # T - 1
    data = data.set_index('日期')
    for ccc in data.columns:
        data[ccc] = data[ccc].shift(periods=1, axis=0)
    """
    if len(data.index) == 365:
        for ddd in data.columns:
            data.loc['2018-01-01', ddd] = float(data[ddd].mean())
    """
    # print(data.columns)
    data.columns = [
        'AOD_0_T1',
        'AOD_1_T1',
        'AOD_2_T1',
        'AOD_3_T1',
        'AOD_4_T1',
        'AOD_5_T1',
        'AOD_6_T1',
        'AOD_7_T1',
        'AOD_8_T1',
        'AOD_9_T1',
        'AOD_10_T1',
        'AOD_11_T1',
        'AOD_12_T1',
        'AOD_13_T1',
        'AOD_14_T1',
        'AOD_15_T1',
        'AOD_16_T1',
        'apparentTemperatureHigh_T1',
        'apparentTemperatureLow_T1',
        'apparentTemperatureMax_T1',
        'apparentTemperatureMin_T1',
        'cloudCover_T1',
        'dewPoint_T1',
        'humidity_T1',
        'moonPhase_T1',
        'ozone_T1',
        'precipAccumulation_T1',
        'precipIntensity_T1',
        'precipIntensityMax_T1',
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
        'temperature_T1']
    data.to_excel(out_path + file)
