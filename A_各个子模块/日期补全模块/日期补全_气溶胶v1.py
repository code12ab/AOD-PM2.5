# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/20 19:33

"""
思路: 先使用.date_range创建完整日期列, 再使用merge合并
"""

# 库
import pandas as pd
import numpy as np
import os

# path
for modis in ["Terra", "Aqua"]:
    for year in [2014, 2015, 2016, 2017, 2018, "多年合一"]:
        input_path = "D:\\毕业论文程序\\气溶胶光学厚度\\空间转换模块\\%s\\%s\\" % (modis, year)
        output_path = "D:\\毕业论文程序\\气溶胶光学厚度\\空间转换模块\\%s\\%s_日期补全\\" % (
            modis, year)
        file_name = os.listdir(input_path)
        # 创建完全的日期列
        if year != "多年合一":
            c = pd.date_range(
                start='1/1/%s' %
                year,
                end='12/31/%s' %
                year)  # 月日年
        else:
            c = pd.date_range(start='1/1/2014', end='12/31/2018')  # 月日年
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
            elif year == "多年合一":
                if len(data_raw.index) < 365 * 5 + 1:  # 365 366 365*5+1
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
            print("已完成:", modis, year, name)
