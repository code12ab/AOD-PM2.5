# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/9/1 19:55


# 库
import pandas as pd
import numpy as np
import os
'''=============================================================================================================================='''
# 读
year = 2017
input1_aod = 'D:\\毕业论文程序\\建模数据\\气溶胶\\%s\\' % year
input2_sky = 'D:\\毕业论文程序\\建模数据\\气象\\%s\\' % year
input3_ts = 'D:\\毕业论文程序\\建模数据\\时空特征\\%s\\' % year
input4_t1 = 'D:\\毕业论文程序\\建模数据\\时滞\\%s\\' % year
input5_ndvi = 'D:\\毕业论文程序\\建模数据\\NDVI\\%s\\' % year
input6_pm = 'D:\\毕业论文程序\\建模数据\\污染物\\%s\\' % year

outpath1 = 'D:\\毕业论文程序\\建模数据_合并\\%s\\气溶胶\\' % year
outpath2 = 'D:\\毕业论文程序\\建模数据_合并\\%s\\气象\\' % year
outpath3 = 'D:\\毕业论文程序\\建模数据_合并\\%s\\时空特征\\' % year
outpath4 = 'D:\\毕业论文程序\\建模数据_合并\\%s\\时滞\\' % year
outpath5 = 'D:\\毕业论文程序\\建模数据_合并\\%s\\NDVI\\' % year
outpath6 = 'D:\\毕业论文程序\\建模数据_合并\\%s\\污染物' % year
file_list = os.listdir(input1_aod)
print(file_list)
list1 = []
list2 = []
list3 = []
list4 = []
list5 = []
list6 = []
for file in file_list:
    data1 = pd.read_excel(input1_aod + file)
    data2 = pd.read_excel(input2_sky + file)
    data3 = pd.read_excel(input3_ts + file)
    data4 = pd.read_excel(input4_t1 + file)
    data5 = pd.read_excel(input5_ndvi + file)
    data6 = pd.read_excel(input6_pm + file)

    list1.append(data1)
    list2.append(data2)
    list3.append(data3)
    list4.append(data4)
    list5.append(data5)
    list6.append(data6)

out1 = pd.concat(list1, axis=0, sort=True)
out2 = pd.concat(list2, axis=0, sort=True)
out3 = pd.concat(list3, axis=0, sort=True)
out4 = pd.concat(list4, axis=0, sort=True)
out5 = pd.concat(list5, axis=0, sort=True)
out6 = pd.concat(list6, axis=0, sort=True)

out1.to_excel(outpath1 + "气溶胶.xlsx")
out2.to_excel(outpath2 + "气象.xlsx")
out3.to_excel(outpath3 + "时空特征.xlsx")
out4.to_excel(outpath4 + "时滞.xlsx")
out5.to_excel(outpath5 + "NDVI.xlsx")
out6.to_excel(outpath6 + "污染物.xlsx")
