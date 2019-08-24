# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/7 11:10


# 库
import pandas as pd
import os
"""
output_file_path = "D:\\毕业论文程序\\气象数据\\整理\\日均\\%s\\" % 2018  # 气象数据存储路径
saved_list = os.listdir(output_file_path)

non_full_list = []
for item in saved_list:
     data = pd.read_excel(output_file_path+item)
     if len(data.index) != 365:
          print(item)
          non_full_list.append(item)
print(len(non_full_list))
"""

"""
import pandas as pd
import datetime
from datetime import datetime as dt
import os

# 批量读取

input_path = 'C:\\Users\\iii\\Desktop\\保定-地表水厂.xlsx'
data = pd.read_excel(input_path)
# print(data.head())
data["Index"] = data["time"]
data = data.set_index('Index')
# 将时间序列转换为指定的频率
data = data.asfreq(freq='1440min')  # 补全信息,这个方法以后可能会经常使用到
data["time"] = data.index
data["日期"] = data["time"].dt.date  # 新建日期列
data["日期"] = data["日期"].map(lambda x: str(x))  # 改成字符串格式 方便日后合并
data = data.set_index('日期')
data = data.drop(["time"], axis=1)  # 日均条件下删除无关列


print(data.index, len(data.index))
"""
a = [1,1,3,4]
b = set(a)
a = list(b)
print(b[1])

print(b)