# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/26 10:22


# 库
import pandas as pd
import numpy as np
import os

input_daily_path = "D:\\毕业论文程序\\气象数据\\整理\\日均\\2018\\"
input_hourly_path = "D:\\毕业论文程序\\气象数据\\整理\\逐时均值\\2018\\"
output_screen_path = "D:\\毕业论文程序\\气象数据\\变量筛选模块\\2018_不补全\\"

input_name_list = os.listdir(input_daily_path)
saved_list = os.listdir(output_screen_path)
for name in input_name_list:
    if name in saved_list:
        continue
    data_daily = pd.read_excel(input_daily_path + name)
    if "ozone" not in data_daily.columns:
        data_daily["ozone"] = np.nan
    if "pressure" not in data_daily.columns:
        data_daily["pressure"] = np.nan

    data_hourly = pd.read_excel(input_hourly_path + name)
    if "ozone" not in data_hourly.columns:
        data_hourly["ozone"] = np.nan
    if "pressure" not in data_hourly.columns:
        data_hourly["pressure"] = np.nan
    if "precipAccumulation" not in data_hourly.columns:
        data_hourly["precipAccumulation"] = np.nan


    data_hourly_merge = data_hourly[['日期',
                                     "apparentTemperature",
                                     "temperature"]]


    data_out = pd.merge(left=data_daily, right=data_hourly_merge,how = "left", on='日期')



    # 排序和输出
    data_out = data_out.sort_values("日期", ascending=True)
    data_out = data_out.set_index("日期")
    data_out.to_excel(output_screen_path + name)
    print(data_out.columns)
    print("Finished", name)
