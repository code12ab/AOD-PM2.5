# -*- coding: utf-8 -*-
# 日期: 2019/3/13 15:00
# 作者: xcl
# 工具：PyCharm

import pandas as pd
import numpy as np
# 参数
input_file = "F:\\毕业论文程序\\整合数据\\各地区\\日均\\总地区.xlsx"
output_file_xlsx = "F:\\毕业论文程序\\整合数据\\各地区\\日均\\总地区.xlsx"
# output_file_csv = "F:\\毕业论文程序\\整合数据\\各地区\\日均\\总地区.csv"
# 读取
data = pd.read_excel(input_file)


# 删除空值行
indexs = list(data[np.isnan(data['dewPoint'])].index)
if len(indexs) == 0:
    print("已完成行删除")
else:
    print("需要删除的行数", len(indexs))  # 按日期为索引删除时,会导致相同日期的其他非空白行被误删
data = data.drop(indexs)

# 删除建模不需要的列
if 'apparentTemperatureHigh' in data.columns:
    columns_drop = ['apparentTemperatureHigh', 'apparentTemperatureHighTime', 'apparentTemperatureLow',
                    'apparentTemperatureLowTime', 'apparentTemperatureMax', 'apparentTemperatureMaxTime',
                    'apparentTemperatureMin', 'apparentTemperatureMinTime', 'precipIntensityMax',
                    'precipIntensityMaxTime', 'precipProbability', 'temperatureHigh', 'temperatureHighTime',
                    'temperatureLow', 'temperatureLowTime', 'temperatureMax', 'temperatureMaxTime', 'temperatureMin',
                    'temperatureMinTime', 'uvIndexTime', 'windGustTime']
    data = data.drop(columns_drop, axis=1)
    print("需要删除的行数", len(columns_drop))
else:
    print("已完成列删除")


# 用0填补,根据官方说明
data['precipAccumulation'] = data['precipAccumulation'].fillna(value=0)
data['precipIntensity'] = data['precipIntensity'].fillna(value=0)
data['cloudCover'] = data['cloudCover'].fillna(value=0)
# 缺失用均值?线性?
data['pressure'] = data['pressure'].interpolate()  # 线性填充
data['windBearing'] = data['windBearing'].interpolate()  # 线性填充
data['windGust'] = data['windGust'].interpolate()  # 线性填充
data['windSpeed'] = data['windSpeed'].interpolate()  # 线性填充
data['visibility'] = data['visibility'].interpolate()  # 线性填充
# 均值填充
data['visibility'] = data['visibility'].fillna(data['visibility'].mean())  # 线性填充
data['windGust'] = data['windGust'].fillna(data['windGust'].mean())  # 线性填充
print(data.isnull().sum())  # 空值检查

# 修改日期格式
data["日期"] = data["日期"].dt.date


# 保存
data.to_excel(output_file_xlsx, index=False)
# data.to_csv(output_file_csv, encoding="utf_8_sig")  # 解决中文乱码;不知道什么原因不能直接用于R
