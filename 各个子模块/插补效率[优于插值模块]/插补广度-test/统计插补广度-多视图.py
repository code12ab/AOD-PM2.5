# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2020/3/11 10:05


# 库
import pandas as pd
import numpy as np
import os

null0_knn = list()
null1_knn = list()
null2_knn = list()
null3_knn = list()
null4_knn = list()

null0_ewm = list()
null1_ewm = list()
null2_ewm = list()
null3_ewm = list()
null4_ewm = list()

null0_idw = list()
null1_idw = list()
null2_idw = list()
null3_idw = list()
null4_idw = list()

null0_iter = list()
null1_iter = list()
null2_iter = list()
null3_iter = list()
null4_iter = list()
# 路径
# input_path = "d:\\毕业论文程序\\气溶胶光学厚度\\空间转换模块\\Aqua\\2018_日期补全\\"
# output_path = "d:\\毕业论文程序\\气溶胶光学厚度\\空间转换模块\\Aqua\\2018_all\\"
# input_path = "d:\\毕业论文程序\\NDVI\\DATA\\MOD2018\\"
# output_path = "d:\\毕业论文程序\\NDVI\\DATA\\MODALL\\"
# input_path ='D:\\毕业论文程序\\污染物浓度\\整理\\PM\\2018_日期补全\\'
# output_path ='D:\\毕业论文程序\\污染物浓度\\整理\\PM\\2018_all\\'

input_path4 = "d:\\毕业论文程序\\气象数据\\插值模块\\Res\\2018\\"  # 还有时间滞后

input_file_names = os.listdir(input_path4)  # 文件名列表, **.xlsx

for name in input_file_names:
    data4_iter = pd.read_excel(input_path4 + name, index_col="日期")
    # print(name)
    # print(len(data3_iter.index)*len(data3_iter.columns))  # 一共多少数据量
    # print(data3_iter.isnull().sum().sum())  # 多列需要俩sum()

    # iter 部分
    queshi4_iter = data4_iter.isnull().sum().sum() / (len(data4_iter.index) * len(data4_iter.columns))
    null4_iter.append(queshi4_iter)
    print("完成:", name)

print( "xx:", np.average(null4_iter))
print('气象还需要考虑逐时和日数据都缺失的部分，这部分在文件里没有体现（日期没补全）')