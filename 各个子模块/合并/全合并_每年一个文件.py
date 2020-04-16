# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/9/1 19:55


# 库
import pandas as pd
import numpy as np
import os
'''=============================================================================================================================='''
# 读
for year in [2008,2009,2010,2011,2012,2013,2014,2015,2016,2017]:
    input1_aod = 'D:\\毕业论文程序\\气溶胶光学厚度\\插值模块\\Res\\%s\\' % year
    input2_sky = 'D:\\毕业论文程序\\气象数据\\插值模块\\Res\\%s\\' % year  # ‘Res’以前是‘原日期’
    input3_ts = 'D:\\毕业论文程序\\建模数据\\时空特征\\%s\\' % year
    input4_t1 = 'D:\\毕业论文程序\\建模数据\\时滞\\\%s\\' % year
    # input5_ndvi = 'D:\\毕业论文程序\\NDVI\\插值模块\\Res\\%s\\' % year
    input5_ndvi = 'D:\\毕业论文程序\\NDVI\\%s\\' % year

    input6_pm = 'D:\\毕业论文程序\\污染物浓度\\插值模块\\Res\\%s\\' % year

    file_list = os.listdir(input6_pm)
    listout = []
    for file in file_list:
        data1 = pd.read_excel(input1_aod + file)
        data1['日期'] = data1['日期'].map(lambda x: str(x)[0:10])
        data2 = pd.read_excel(input2_sky + file)
        data2['日期'] = data2['日期'].map(lambda x: str(x)[0:10])
        data3 = pd.read_excel(input3_ts + file)
        data3['日期'] = data3['日期'].map(lambda x: str(x)[0:10])
        data4 = pd.read_excel(input4_t1 + file)
        data4['日期'] = data4['日期'].map(lambda x: str(x)[0:10])
        data5 = pd.read_excel(input5_ndvi + file)
        data5['日期'] = data5['日期'].map(lambda x: str(x)[0:10])
        data6 = pd.read_excel(input6_pm + file)
        data6['日期'] = data6['日期'].map(lambda x: str(x)[0:10])

        data_concat1 = pd.merge(data1, data2, how='right', on='日期')
        data_concat2 = pd.merge(data3, data4, how='right', on='日期')
        data_concat3 = pd.merge(data5, data6, how='right', on='日期')
        print(data_concat3.head(5))

        data_concat4 = pd.merge(data_concat1, data_concat2, how='left', on='日期')
        data_merge = pd.merge(data_concat3, data_concat4, how='right', on='日期')

        listout.append(data_merge)
        # print(data_merge)

    dataout = pd.concat(listout,axis =0,sort = True)

    dataout['precipAccumulation_T1'] = dataout['precipAccumulation_T1'].fillna(0.00)
    dataout['precipIntensity_T1'] = dataout['precipIntensity_T1'].fillna(0.00)
    dataout['precipAccumulation'] = dataout['precipAccumulation'].fillna(0.00)
    dataout['precipIntensity'] = dataout['precipIntensity'].fillna(0.00)
    dataout['ozone'] = dataout['ozone'].fillna(0.00)
    dataout = dataout.set_index('日期')
    dataout.to_excel('D:\\毕业论文程序\\08到17年\\输入特征_原始\\%s.xlsx' % year)  # 另存放到项目里的文件中 ‘08-17年’
