# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/26 17:45


# 库
import pandas as pd
import numpy as np
import os

# 路径
input_file_path = "D:\\毕业论文程序\\气象数据\\变量筛选模块\\2018_不补全\\"
output_file_path = "D:\\毕业论文程序\\气象数据\\筛除字符串\\2018_不补全\\"
file_name_list = os.listdir(input_file_path)
saved_list = os.listdir(output_file_path)
for file in file_name_list:
    data = pd.read_excel(input_file_path + file)
    data_out = data[['日期',
                     'apparentTemperatureHigh',
                     'apparentTemperatureLow',
                     'apparentTemperatureMax',
                     'apparentTemperatureMin',
                     'cloudCover',
                     'dewPoint',
                     'humidity',
                     'moonPhase',
                     'ozone',
                     'precipAccumulation',
                     'precipIntensity',
                     'precipIntensityMax',
                     'pressure',
                     'sunriseTime',
                     'sunsetTime',
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
    data_out = data_out.set_index("日期")
    data_out.to_excel(output_file_path+file)
