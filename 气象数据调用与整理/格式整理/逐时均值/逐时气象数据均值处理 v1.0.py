# -*- coding: utf-8 -*-
# 日期: 2019/3/13 14:29
# 作者: xcl
# 工具：PyCharm


import pandas as pd
import datetime
from datetime import datetime as dt
import os

# 批量读取


input_path = "F:\\毕业论文程序\\气象数据\\数据\\逐时\\"
output_path = "F:\\毕业论文程序\\气象数据\\整理\\逐时均值\\"
file_name_list = os.listdir(input_path)  # 文件名

for name in file_name_list:
    print("整理" + name + "中")
    file_name = name.replace(".xlsx", "")
    data = pd.read_excel(input_path + name)
    data["Index"] = data["time"]
    data = data.set_index('Index')
    # 将时间序列转换为指定的频率
    data = data.asfreq(freq='60min')
    data["time"] = data.index  # 补全信息,这个方法以后可能会经常使用到
    for key in data.columns:
        data["%s" % key] = data["%s" % key].interpolate()  # 线性填充
    '''
    for key in data.columns:
        data["%s" % key] = data["%s" % key].fillna(method='ffill')
    '''
    data["日期"] = data["time"].dt.date  # 新建日期列
    data["time_only"] = data["time"].dt.time  # 时间列只保留时间


    # print(data.head())

    # 时间生产函数,格式为str
    def date_range(begindate, enddate):
        dates = []
        dt_object = dt.strptime(begindate, "%H:%M:%S")
        date = begindate[:]
        while date <= enddate:
            dates.append(date)
            dt_object = dt_object + datetime.timedelta(hours=1)
            date = dt_object.strftime("%H:%M:%S")
        return dates


    hour_list = date_range("10:00:00", "14:00:00")
    index_time = []
    for key in hour_list:
        key = dt.strptime(key, "%H:%M:%S").time()
        index_time.append(key)

    '''
    loc_list = []
    for key in index_time:
        # loc = data["time_only"][data["time_only"].values != key].index.tolist()
        loc = data["time_only"][data["time_only"].values == key].index.tolist()
        loc_list.append(loc)
    print(len(loc_list))
    '''

    data = data.groupby("日期").mean()
    data.to_excel(output_path + "%s.xlsx" % file_name)




