# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/10/2 21:23


# 库
import pandas as pd
import numpy as np
import os
# 前
# input_path = "d:\\毕业论文程序\\气溶胶光学厚度\\空间转换模块\\Terra\\2018_all\\"
# input_path = "d:\\毕业论文程序\\NDVI\\DATA\\MYDALL\\"  # O对应T
# input_path ='D:\\毕业论文程序\\污染物浓度\\整理\\PM\\2018_all\\'
input_path = 'D:\\毕业论文程序\\气象数据\\筛除字符串\\2018_all\\'
data= pd.read_excel(input_path+"2018_all.xlsx", index_col='日期')

# 后
#data = pd.read_excel('D:\\雨雪+2018_new_pm_aod.xlsx',index_col='日期')
print('样本总量', len(data.index))
print(data.isnull().sum())
print('所有特征非空总数:', data.isnull().sum().sum())

#null = pd.DataFrame(data.isnull().sum())
#null.to_excel('D:\\总体缺失值统计.xlsx')