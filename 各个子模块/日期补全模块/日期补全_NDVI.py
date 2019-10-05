# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/23 13:46


# 库
import pandas as pd
import numpy as np
import os


for year in [2018]:
    input_path = "D:\\毕业论文程序\\NDVI\\插值模块\\Mean\\%s\\" % year
    output_path = "D:\\毕业论文程序\\NDVI\\%s_日期补全\\" % year
    fillna_path = "D:\\毕业论文程序\\NDVI\\%s_线性填充\\" % year

    file_name = os.listdir(input_path)
    # 创建完全的日期列
    if year == 2014:
        c = pd.date_range(
            start='5/13/%s' %
            year,
            end='12/31/%s' %
            year)  # 月日年
    elif year != "多年合一":
        c = pd.date_range(
            start='1/1/%s' %
            year,
            end='12/31/%s' %
            year)  # 月日年
    else:
        c = pd.date_range(start='5/13/2014', end='12/31/2018')  # 月日年
    c = pd.DataFrame(c)
    c.columns = ["日期"]
    c["日期"] = c["日期"].map(lambda x: str(x)[0:10])

    # 合并
    for name in file_name:
        data_raw = pd.read_excel(input_path + name)
        data_raw["日期"] = data_raw["日期"].map(lambda x: str(x)[0:10])
        if year == 2016:
            if len(data_raw.index) < 366:  # 365 366 365*5+1
                data = pd.merge(
                    left=data_raw, right=c, on="日期", how="right")
                data = data.set_index("日期")
                data = data.sort_index(axis=0)
                data.to_excel(output_path + name)
            else:
                data_raw = data_raw.set_index("日期")
                data_raw.to_excel(output_path + name)
        elif year == 2014:
            if len(data_raw.index) < 233:  # 365 366 365*5+1
                data = pd.merge(
                    left=data_raw, right=c, on="日期", how="right")
                data = data.set_index("日期")
                data = data.sort_index(axis=0)
                data.to_excel(output_path + name)
        elif year == "多年合一":
            if len(data_raw.index) < 365 * 4 + 1 + 233:  # 365 366 365*5+1
                data = pd.merge(
                    left=data_raw, right=c, on="日期", how="right")
                data = data.set_index("日期")
                data = data.sort_index(axis=0)
                data.to_excel(output_path + name)
            else:
                data_raw = data_raw.set_index("日期")
                data_raw.to_excel(output_path + name)
        else:
            if len(data_raw.index) < 365:  # 365 366 365*5+1
                data = pd.merge(
                    left=data_raw, right=c, on="日期", how="right")
                data = data.set_index("日期")
                data = data.sort_index(axis=0)
                data.to_excel(output_path + name)
            else:
                data_raw = data_raw.set_index("日期")
                data_raw.to_excel(output_path + name)

    for name in file_name:
        data = pd.read_excel(output_path+name, index_col='日期')
        for key in data.columns:
            if 'NDVI' in key:
                data["%s" % key] = data["%s" % key].interpolate()  # 线性填充
        data.to_excel(fillna_path+name)