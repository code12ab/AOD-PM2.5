# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/26 10:22


# 库
import pandas as pd
import numpy as np
import os


for year in [2008,2009,2010,2011,2012,2013,2014,2015,2016,2017]:
    input_daily_path = "D:\\毕业论文程序\\气象数据\\整理\\日均\\%s\\" % year
    input_hourly_path = "D:\\毕业论文程序\\气象数据\\整理\\逐时均值\\%s\\" % year
    output_screen_path = "D:\\毕业论文程序\\气象数据\\变量筛选模块\\%s\\" % year

    input_name_list = os.listdir(input_daily_path)
    saved_list = os.listdir(output_screen_path)
    for name in input_name_list:
        print(name)
        if name in saved_list:
            continue
        if name == "保定-华电二区.xlsx":
            continue
        data_daily = pd.read_excel(input_daily_path + name)
        if "ozone" not in data_daily.columns:
            data_daily["ozone"] = np.nan
        if "pressure" not in data_daily.columns:
            data_daily["pressure"] = np.nan
        if "precipAccumulation" not in data_daily.columns:
            data_daily["precipAccumulation"] = np.nan
        if "precipIntensity" not in data_daily.columns:
            data_daily["precipIntensity"] = np.nan
        if "precipIntensityMax" not in data_daily.columns:
            data_daily["precipIntensityMax"] = np.nan
        if "icon" not in data_daily.columns:
            data_daily["icon"] = np.nan
        if "precipType" not in data_daily.columns:
            data_daily["precipType"] = np.nan

        data_hourly = pd.read_excel(input_hourly_path + name)
        if "ozone" not in data_hourly.columns:
            data_hourly["ozone"] = np.nan
        if "pressure" not in data_hourly.columns:
            data_hourly["pressure"] = np.nan
        if "precipAccumulation" not in data_hourly.columns:
            data_hourly["precipAccumulation"] = np.nan
        if "precipIntensity" not in data_hourly.columns:
            data_hourly["precipIntensity"] = np.nan

        """
        Index(['日期', 'apparentTemperature', 'cloudCover', 'dewPoint', 'humidity',
           'ozone', 'precipAccumulation', 'precipIntensity', 'precipProbability',
           'pressure', 'temperature', 'uvIndex', 'visibility', 'windBearing',
           'windGust', 'windSpeed'],
          dtype='object')
        重复:'cloudCover', 'dewPoint', 'humidity','ozone', 'precipAccumulation', 'precipIntensity', 'pressure',
                'uvIndex', 'visibility', 'windBearing', 'windGust', 'windSpeed'
         """

        data_hourly_duplicate = data_hourly[['日期',
                                             'cloudCover',
                                             'dewPoint',
                                             'humidity',
                                             'ozone',
                                             'precipAccumulation',
                                             'precipIntensity',
                                             'pressure',
                                             'uvIndex',
                                             'visibility',
                                             'windBearing',
                                             'windGust',
                                             'windSpeed']]
        data_hourly_merge = data_hourly[['日期',
                                         "apparentTemperature",
                                         "temperature"]]
        data_daily_merge = data_daily[['日期',
                                       'apparentTemperatureHigh',
                                       'apparentTemperatureLow',
                                       'apparentTemperatureMax',
                                       'apparentTemperatureMin',
                                       'cloudCover',
                                       'dewPoint',
                                       'humidity',
                                       'icon',
                                       'moonPhase',
                                       'ozone',
                                       'precipAccumulation',
                                       'precipIntensity',
                                       'precipIntensityMax',
                                       'precipType',
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
                                       'windSpeed']]

        idx_list = []  # 逐时多于日均的日期
        for idx in data_hourly_duplicate["日期"]:
            if idx not in data_daily_merge["日期"].values:
                idx_list.append(idx)
        # print(idx_list)

        if len(idx_list) > 0:
            data_hourly_duplicate = data_hourly_duplicate.set_index("日期")
            data_hourly_to_add = data_hourly_duplicate.reindex(index=idx_list)  # 通过修改索引获得筛选数据
            data_hourly_duplicate = data_hourly_duplicate.reset_index(drop=False)
            data_hourly_to_add = data_hourly_to_add.reset_index(drop=False)
            # print(data_hourly_to_add)
            data_daily_merge = pd.concat([data_daily_merge, data_hourly_to_add], keys="日期", sort=True)  # 合并日均和逐时多出来的数据

        if len(data_daily_merge.index) <= len(data_hourly_merge.index):  # 合并逐时[体感温度][温度]和日均
            data_out = pd.merge(
                left=data_daily_merge,
                right=data_hourly_merge,
                how="right",
                on="日期")
        else:
            data_out = pd.merge(
                left=data_daily_merge,
                right=data_hourly_merge,
                how="left",
                on="日期")

        # 排序和输出
        data_out = data_out.sort_values("日期", ascending=True)
        data_out = data_out.set_index("日期")
        data_out.to_excel(output_screen_path + name)
        print(data_out.columns)
        print("Finished", name)
