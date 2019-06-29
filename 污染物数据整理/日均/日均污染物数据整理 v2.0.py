# -*- coding: utf-8 -*-
# 日期: 2019/3/18 10:38
# 作者: xcl
# 工具：PyCharm


import os
import pandas as pd
import warnings
from datetime import datetime as dt
import datetime


# 第一部分

# 按监测站编号建立污染物浓度文件

# 相关库
import time

# 参数设置
input_file_path = "D:\\DATA\\2019\\"
input_file_name = os.listdir(input_file_path)  # 文件名
output_file_path = "D:\\毕业论文程序\\污染物浓度\\污染物数据\\日均\\2019\\"
error_path = "D:\\毕业论文程序\\污染物浓度\\error\\"
JCZ_data = pd.read_excel("D:\\毕业论文程序\\MODIS\\坐标\\监测站坐标.xlsx", sheet_name="汇总")
#JCZ_data = pd.read_excel("D:\\毕业论文程序\\MODIS\\坐标\\监测站坐标.xlsx", sheet_name="北京2019")  # 适用于北京2019年
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
        #date = file.replace("china_sites_", "").replace(".csv", "")
        date = file.replace("beijing_all_", "").replace(".csv", "")  # 适用于北京
        #date = file.replace("china_cities_", "").replace(".csv", "")
        date = time.strptime(date, '%Y%m%d')
        date = time.strftime("%Y-%m-%d", date)
        date = dt.strptime(date, '%Y-%m-%d').date()
        try:
            data = pd.read_csv(input_file_path+file, encoding='utf8')
            data = data[(data["type"] == "PM2.5_24h") & (data["hour"] == 0)]
            
            # 今日0时的24小时平均滑动值是前一天的24小时PM2.5均值
            # print(file)
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


# 第二部分

warnings.filterwarnings('ignore')  # 代码中仅进行新列的赋值,不对数据源做修改,因此可以忽略该警告
# 参数设置
input_file_path = "D:\\毕业论文程序\\污染物浓度\\污染物数据\\日均\\2019\\"
input_file_name = os.listdir(input_file_path)  # 文件名
output_file_path = "D:\\毕业论文程序\\污染物浓度\\整理\\日均\\2019\\"
JCZ_NAME = pd.read_excel("D:\\毕业论文程序\\MODIS\\坐标\\监测站坐标.xlsx", sheet_name="汇总")
#JCZ_NAME = pd.read_excel("D:\\毕业论文程序\\MODIS\\坐标\\监测站坐标.xlsx", sheet_name="北京2019")  # 适用于北京2019年
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
    data.columns = ["日期", "hour", "日均PM2.5"]
    data["日期"] = data["日期"].dt.date
    '''
          今日0时的24小时平均滑动值是前一天的24小时PM2.5均值
    '''

    def get_day(date_input, step=0):
        """获取指定日期date(形如"xxxx-xx-xx")之前或之后的多少天的日期, 返回值为字符串格式的日期"""
        date_input = str(date_input)  # 转化为字符串方便合并
        l_input = date_input.split("-")
        y = int(l_input[0])
        m = int(l_input[1])
        d = int(l_input[2])
        old_date = datetime.datetime(y, m, d)
        new_date = (old_date + datetime.timedelta(days=step)).strftime('%Y-%m-%d')
        # print(new_date)
        return new_date


    data["日期"] = data["日期"].map(lambda x: get_day(x, -1))  # 今日的0时PM2.5_24h对应前一天PM2.5日均值
    data = data.drop(["hour"], axis=1)
    print(JCZ_info)
    
    data["X"] = JCZ_info["经度"][i]
    data["Y"] = JCZ_info["纬度"][i]
    
    # 以下仅在北京2019年下使用
    '''
    data["X"] = JCZ_info["经度"]
    data["Y"] = JCZ_info["纬度"]
    data['X'] = data['X'].fillna(method='pad')
    data['Y'] = data['Y'].fillna(method='pad')  # 用前一个值补充坐标
    '''
    # 输出
    data = data.set_index('日期')
    data.to_excel(output_file_path + "%s.xlsx" % JCZ_new_name)
