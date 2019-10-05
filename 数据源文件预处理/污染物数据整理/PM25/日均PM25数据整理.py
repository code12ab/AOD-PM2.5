# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/9 1:10



# 相关库
import time
import os
import pandas as pd
import warnings
from datetime import datetime as dt
import datetime

# 第一部分
# 参数设置
'''
path_list = ["D:\\站点_20140513-20141231\\",
             "D:\\站点_20150101-20151231\\",
             "D:\\站点_20160101-20161231\\",
             "D:\\站点_20170101-20171231\\",
             "D:\\站点_20180101-20181231\\"]
'''

path_list = ["D:\\DATA_毕业论文\\监测点\\站点180101-181231\\"]
save_year = 2018
"""
# 文件夹循环
for path in path_list:
    input_file_path = path
    input_file_name = os.listdir(input_file_path)  # 文件名
    output_file_path = "D:\\毕业论文程序\\污染物浓度\\污染物数据\\日均\\%s_new\\" % save_year
    JCZ_data = pd.read_excel(
        "D:\\毕业论文程序\\MODIS\\坐标\\监测站坐标.xlsx",
        sheet_name="汇总")
    # JCZ_data = pd.read_excel("D:\\毕业论文程序\\MODIS\\坐标\\监测站坐标.xlsx",
    # sheet_name="北京2019")  # 适用于北京2019年
    JCZ_number = JCZ_data["监测点编码"]

    # 主程序, 主要部分
    i = 0
    for number in JCZ_number:
        i += 1
        print("当前进度:%.2f%%" % (i / (len(JCZ_number)*len(path_list)) * 100))
        error = []
        outcome_list_PM25 = []
        for file in input_file_name:
            # print(file)
            date = file.replace("china_sites_", "").replace(".csv", "")  # 中国站点
            # 日期格式: 使用文件名更改
            date = time.strptime(date, '%Y%m%d')
            date = time.strftime("%Y-%m-%d", date)
            date = dt.strptime(date, '%Y-%m-%d').date()
            try:
                data = pd.read_csv(input_file_path + file, encoding='utf8')
                data = data[data["hour"] == 23]
                data_PM25 = data[data["type"] == "PM2.5_24h"]
                data_PM25 = data_PM25[["%s" % number]]
                # 设置日期
                data_PM25["日期"] = date
                # 添加进列表
                outcome_list_PM25.append(data_PM25)
            except Exception as e:
                print(file, "报错:", e)
        outcome_PM25 = pd.concat(outcome_list_PM25)
        # 修改列名
        outcome_PM25.rename(columns={"%s" % number: 'PM25'}, inplace=True)
        # 排序
        outcome_PM25 = outcome_PM25.sort_values("日期", ascending=True)
        # 重设索引
        outcome_PM25 = outcome_PM25.set_index("日期")
        # 输出
        outcome_PM25.to_excel(output_file_path + "%s污染物浓度.xlsx" % number)
"""

print("================ 开始第二部分 ==================")
# 第二部分: 更改日期为T-1, 增加站点名称列

warnings.filterwarnings('ignore')  # 代码中仅进行新列的赋值,不对数据源做修改,因此可以忽略该警告
# 参数设置
input_file_path = "D:\\毕业论文程序\\污染物浓度\\污染物数据\\日均\\%s_new\\" % save_year
input_file_name = os.listdir(input_file_path)  # 文件名
output_file_path = "D:\\毕业论文程序\\污染物浓度\\整理\\全部污染物\\%s_new\\" % save_year
JCZ_NAME = pd.read_excel("D:\\毕业论文程序\\MODIS\\坐标\\监测站坐标.xlsx", sheet_name="汇总")


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

    # 读取数据
    data = pd.read_excel(input_file_path+JCZ+"污染物浓度.xlsx")
    data["日期"] = data["日期"].dt.date
    # 输出
    data = data.set_index('日期')
    data.to_excel(output_file_path + "%s.xlsx" % JCZ_new_name)
