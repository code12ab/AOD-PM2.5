# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/7 11:10


# 库
from multiprocessing import Process  # 多线程,提高CPU利用率
import copy
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import numpy as np
import os

# 思路
# K循环 插补 去 参数b

# 库
from multiprocessing import Process  # 多线程,提高CPU利用率
import warnings
from math import radians, cos, sin, asin, sqrt, degrees, atan2  # 经纬度计算距离
import pandas as pd  # BDS
import numpy as np  # BDS
from pyhdf.SD import SD  # 批量导入HDF
import datetime  # 程序耗时
import os  # 关机,批量文件
import time  # 关机
from numba import jit

warnings.filterwarnings('ignore')  # 忽略"number/0"的情况
start_time = datetime.datetime.now()  # 耗时计算
# 参数设置
dis1 = 8000  # 同心圆范围
dis2 = 20000
dis3 = 50000

# 文件设置
output_file_path = "D:\\毕业论文程序\\气溶胶光学厚度\\空间转换模块\\Terra\\2018\\"  # 结果的输出位置

location_xy_input_file = "D:\\毕业论文程序\\MODIS\\坐标\\站点列表-2018.11.08起.xlsx"
exist_file_list = os.listdir(output_file_path)
# 定义经纬度距离公式




JCZ_file = pd.read_excel(
    location_xy_input_file,
    sheet_name="样例1")
JCZ = []
# 批量导入监测站
for i in range(len(JCZ_file)):
    exec(
        'JCZ%s = [JCZ_file["经度"][i],JCZ_file["纬度"][i],JCZ_file["城市"][i]+"-"+JCZ_file["监测点名称"][i]]' %
        i)
    exec("JCZ.append(JCZ%s)" % i)  # exec可以执行字符串指令
for item in JCZ:
    if item[2]+".xlsx" in exist_file_list:
        print("文件已经存在")
        continue
    print("%s不存在" % item)