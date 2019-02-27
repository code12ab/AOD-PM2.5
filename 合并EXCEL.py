# -*- coding: utf-8 -*-
# 日期: 2019/2/23 19:36
# 作者: xcl
# 工具：PyCharm

import pandas as pd
import os
# 参数设置
r = 7500   # 参照文献;经纬度转换为的距离范围,监测站3KM半径范围内为观测区域
input_file_path = "F:\\毕业论文程序\\整合数据\\各监测站\\"  # HDF文件位置 TTT
output_file_path = "F:\\毕业论文程序\\整合数据\\各地区\\"  # 结果的输出位置

# 批量读取
file_name = os.listdir(input_file_path)  # 文件名

list_file = []
for file in file_name:
    data = pd.read_excel(input_file_path+file)
    list_file.append(data)

df = pd.concat(list_file, sort=True)

# print(df.isnull().sum())

# 删除值为空的数据
df = df.dropna()
# print(df.isnull().sum())

# 删除全0列
print(df.std())
df_std = pd.DataFrame(df.std())
list_0 = []
# print(df_sum.index)
# print(df_sum[0]["AOD值"])
for key in df_std.index:
    if df_std[0]["%s" % key] == 0:
        print(key)
        list_0.append(key)
df = df.drop(list_0, axis=1)

# 索引
df["日期"] = df["日期"].dt.date
df = df.set_index('日期')
# 导出
df.to_excel(output_file_path+"Beijing.xls")
