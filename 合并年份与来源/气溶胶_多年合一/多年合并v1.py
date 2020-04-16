# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/21 8:21


# 库
import pandas as pd
# import numpy as np
import os

# 路径
# input_path = "d:\\毕业论文程序\\气溶胶光学厚度\\空间转换模块\\Aqua\\2018_日期补全\\"
# output_path = "d:\\毕业论文程序\\气溶胶光学厚度\\空间转换模块\\Aqua\\2018_all\\"
# input_path = "d:\\毕业论文程序\\NDVI\\DATA\\MOD2018\\"
# output_path = "d:\\毕业论文程序\\NDVI\\DATA\\MODALL\\"
# input_path ='D:\\毕业论文程序\\污染物浓度\\整理\\PM\\2018_日期补全\\'
# output_path ='D:\\毕业论文程序\\污染物浓度\\整理\\PM\\2018_all\\'

input_path = 'D:\\毕业论文程序\\污染物浓度\\整理\\PM\\2018_new\\'
output_path = 'D:\\'

file_name = os.listdir(input_path)  # 获取文件名

data_list = []
nub = 1
for name in file_name:
    data = pd.read_excel(input_path+name, index_col ='日期')
    data['id'] = str(nub)
    data_list.append(data)
    print(name, "完成")
    nub += 1
data_all = pd.concat(data_list,axis =1)
print(data_all.isnull().sum())
data_all.PM25 = data_all.PM25.interpolate()
data_all.to_excel(output_path+"PM2018_all.xlsx")
