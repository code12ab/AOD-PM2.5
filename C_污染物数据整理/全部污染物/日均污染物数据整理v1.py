# -*- coding: utf-8 -*-
# 日期: 2019/3/11 13:33
# 作者: xcl
# 工具：PyCharm

import os
import pandas as pd
import warnings
from datetime import datetime as dt

# 第一部分
'''
# 按监测站编号建立污染物浓度文件

# 相关库
import time


# 参数设置
input_file_path = "F:\\MODIS DATA\\污染物浓度_2018\\"
input_file_name = os.listdir(input_file_path)  # 文件名
output_file_path = "F:\\毕业论文程序\\污染物浓度\\污染物数据\\日均\\"
error_path = "F:\\毕业论文程序\\污染物浓度\\error\\"
JCZ_data = pd.read_excel("F:\\毕业论文程序\\MODIS\\坐标\\监测站坐标.xlsx", sheet_name="汇总")
JCZ_number = JCZ_data["监测点编码"]

# 主程序
i = 0
for number in JCZ_number:
    i += 1
    print("当前进度:%.2f%%" % (i/len(JCZ_number)*100))
    error = []
    outcome_list = []
    # print(number)
    for file in input_file_name:
        # print(file)
        date = file.replace("china_sites_", "").replace(".csv", "")
        date = time.strptime(date, '%Y%m%d')
        date = time.strftime("%Y-%m-%d", date)
        date = dt.strptime(date, '%Y-%m-%d').date()
        try:
            data = pd.read_csv(input_file_path+file)
            data = data[(data["type"] == "PM2.5") & (data["hour"] == 23)]
            data = data[["hour", "%s" % number]]  # 获取时间列,污染物数据列
            data["日期"] = date
            outcome_list.append(data)
            # print(file, "正常")
        except Exception as e:
            print(file, "报错:", e)
            problem = file, e
            error.append(problem)

    outcome = pd.concat(outcome_list)
    outcome = outcome.sort_values("日期", ascending=True)
    outcome = outcome.set_index('日期')
    outcome.to_excel(output_file_path+"%s污染物浓度.xlsx" % number)
    pd.DataFrame(error).to_excel(error_path+"error.xlsx")
'''

warnings.filterwarnings('ignore')  # 代码中仅进行新列的赋值,不对数据源做修改,因此可以忽略该警告
# 参数设置
input_file_path = "F:\\毕业论文程序\\污染物浓度\\污染物数据\\日均\\"
input_file_name = os.listdir(input_file_path)  # 文件名
output_file_path = "F:\\毕业论文程序\\污染物浓度\\整理\\日均\\"
JCZ_NAME = pd.read_excel("F:\\毕业论文程序\\MODIS\\坐标\\监测站坐标.xlsx", sheet_name="汇总")
# JCZ_NAME格式为df,监测站编码,监测点名称,城市,经度,纬度
# print(input_file_name)
# print(JCZ_NAME.head())

i = -1
for JCZ in input_file_name:
    i += 1
    print("进度:%.2f%%" % (i / (len(input_file_name) - 1) * 100))
    # print(JCZ)
    JCZ = JCZ.replace("污染物浓度.xlsx", "")
    # 获取对应监测点编码的名称和坐标信息
    JCZ_info = JCZ_NAME[JCZ_NAME["监测点编码"] == JCZ]
    # 为统一数据保存命名方式为"城市-监测站名称"
    JCZ_new_name = JCZ_info["城市"] + "-" + JCZ_info["监测点名称"]
    # JCZ_new_name = pd.DataFrame(JCZ_new_name)
    JCZ_new_name = JCZ_new_name.values[0]
    # print(JCZ_new_name.values)
    # print(JCZ_info.__class__)

    # 读取数据
    data = pd.read_excel(input_file_path + JCZ + "污染物浓度.xlsx")
    data.columns = ["日期", "hour", "日均PM2.5"]
    data["日期"] = data["日期"].dt.date
    data = data.drop(["hour"], axis=1)
    data["X"] = JCZ_info["经度"][i]
    data["Y"] = JCZ_info["纬度"][i]
    data = data.set_index('日期')
    data.to_excel(output_file_path + "%s.xlsx" % JCZ_new_name)
