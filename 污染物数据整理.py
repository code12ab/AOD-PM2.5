# -*- coding:utf-8 -*- 
# 日期：2019/2/15 11:02
# 作者：xcl
# 工具：PyCharm
# 处理PM2.5污染物浓度
import os
import pandas as pd
import warnings
from datetime import datetime as dt
'''
# 第一部分
"""已完成"""
# 按监测站编号建立污染物浓度文件

# 相关库
import time


# 参数设置
input_file_path = "F:\\MODIS DATA\\污染物_2018\\"
input_file_name = os.listdir(input_file_path)  # 文件名
output_file_path = "F:\\毕业论文程序\\污染物浓度\\污染物数据\\"
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
            data = data[data["type"] == "PM2.5"]
            data = data[["hour", "%s" % number]]  # 获取时间列,污染物数据列
            data = data[(data["hour"] <= 14) & (data["hour"] >= 10)]
            data["日期"] = date
            outcome_list.append(data)
            # print(file, "正常")
        except Exception as e:
            print(file, "报错")
            problem = file, e
            error.append(problem)

    outcome = pd.concat(outcome_list)
    outcome = outcome.sort_values("日期", ascending=True)
    outcome = outcome.set_index('日期')
    outcome.to_excel(output_file_path+"%s污染物浓度.xlsx" % number)
    pd.DataFrame(error).to_excel(error_path+"error.xlsx")

'''

# 第二部分,按过境时间计算均值
warnings.filterwarnings('ignore')  # 代码中仅进行新列的赋值,不对数据源做修改,因此可以忽略该警告
# 参数设置
input_file_path = "F:\\毕业论文程序\\污染物浓度\\污染物数据\\"
input_file_name = os.listdir(input_file_path)  # 文件名
output_file_path = "F:\\毕业论文程序\\污染物浓度\\整理\\"
JCZ_NAME = pd.read_excel("F:\\毕业论文程序\\MODIS\\坐标\\监测站坐标.xlsx", sheet_name="汇总")
# JCZ_NAME格式为df,监测站编码,监测点名称,城市,经度,纬度
# print(input_file_name)
# print(JCZ_NAME.head())

i = -1
for JCZ in input_file_name:
    i += 1
    print("进度:%.2f%%" % (i/(len(input_file_name)-1)*100))
    # print(JCZ)
    JCZ = JCZ.replace("污染物浓度.xlsx", "")
    # 获取对应监测点编码的名称和坐标信息
    JCZ_info = JCZ_NAME[JCZ_NAME["监测点编码"] == JCZ]
    # 为统一数据保存命名方式为"城市-监测站名称"
    JCZ_new_name = JCZ_info["城市"]+"-"+JCZ_info["监测点名称"]
    # JCZ_new_name = pd.DataFrame(JCZ_new_name)
    JCZ_new_name = JCZ_new_name.values[0]
    # print(JCZ_new_name.values)
    # print(JCZ_info.__class__)

    # 读取数据
    data = pd.read_excel(input_file_path+JCZ+"污染物浓度.xlsx")
    data.columns = ["日期", "hour", "PM2.5浓度"]
    data["日期"] = data["日期"].dt.date

    # 筛选10:00到14:00之间的数据,用于Aqua-Terra,12时数据
    data_combine = data[(data["hour"] <= 14) & (data["hour"] >= 10)]
    data_combine["X"] = JCZ_info["经度"][i]
    data_combine["Y"] = JCZ_info["纬度"][i]
    data_combine = data_combine.groupby("日期").mean()
    # data_combine["日期"] = data_combine["日期"].dt.date
    data_combine.to_excel(output_file_path + "combine\\%s.xlsx" % JCZ_new_name)

    # 筛选10:00到11:00之间的数据,用于Terra,10:30时数据,上午过境
    data_Terra = data[(data["hour"] <= 11) & (data["hour"] >= 10)]
    data_Terra["X"] = JCZ_info["经度"][i]
    data_Terra["Y"] = JCZ_info["纬度"][i]
    data_Terra = data_Terra.groupby("日期").mean()
    # data_Terra["日期"] = data_Terra["日期"].dt.date
    data_Terra.to_excel(output_file_path + "Terra\\%s.xlsx" % JCZ_new_name)

    # 筛选13:00到14:00之间的数据,用于Aqua,13:30时数据,下午过境
    data_Aqua = data[(data["hour"] <= 14) & (data["hour"] >= 13)]
    # print(data_Aqua.head(5))
    data_Aqua["X"] = JCZ_info["经度"][i]
    data_Aqua["Y"] = JCZ_info["纬度"][i]
    data_Aqua = data_Aqua.groupby("日期").mean()
    # data_Aqua["日期"] = data_Aqua["日期"].dt.date
    data_Aqua.to_excel(output_file_path + "Aqua\\%s.xlsx" % JCZ_new_name)
