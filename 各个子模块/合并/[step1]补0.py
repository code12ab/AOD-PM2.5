# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/9/2 14:18


# 库
import pandas as pd
import numpy as np
import os
for year in [2008,2009,2010,2011,2012,2013,2014,2015,2016,2017]:
    input_file = 'D:\\毕业论文程序\\08到17年\\输入特征_原始\\%s.xlsx' % year

    data = pd.read_excel(input_file, index_col='日期')

    data['sunTime'] = (data['sunsetTime'] - data['sunriseTime']) / 3600
    data['sunTime_T1'] = (data['sunsetTime_T1'] - data['sunriseTime_T1']) / 3600
    data = data[(data['sunTime'] > 7.00) & (data['sunTime_T1'] > 7.00)]

    data_rainsonw = data[(data['precipIntensity_T1'] > 0) | (data['precipIntensity'] > 0) |
                         (data['precipIntensityMax'] > 0) | (data['precipIntensityMax_T1'] > 0) |
                         (data['precipAccumulation'] > 0) | (data['precipAccumulation_T1'] > 0)]
    # data_rainsonw.to_excel('d:\\全2018_雨雪.xlsx')  # 只有发生雨雪天时候的数据

    data['precipIntensity'] = data['precipIntensity'].fillna(0.00)
    data['precipIntensity_T1'] = data['precipIntensity_T1'].fillna(0.00)
    data['precipIntensityMax'] = data['precipIntensityMax'].fillna(0.00)
    data['precipIntensityMax_T1'] = data['precipIntensityMax_T1'].fillna(0.00)
    data['precipAccumulation'] = data['precipAccumulation'].fillna(0.00)
    data['precipAccumulation_T1'] =data['precipAccumulation_T1'].fillna(0.00)
    # data.to_excel('d:\\雨雪+2018_new_pm.xlsx')  # 雨雪填充为0后的全部, 这是原输出文件名
    data.to_excel('D:\\毕业论文程序\\08到17年\\输入特征_补零再单位转换\\%s.xlsx' % year)

    data = data[(data['precipIntensity_T1']==0) &
                (data['precipIntensity_T1']==0) &
                (data['precipIntensityMax']==0) &
                (data['precipIntensityMax_T1']==0) &
                (data['precipAccumulation']==0) &
                (data['precipAccumulation_T1']==0)]
    # 无雨雪的文件
    del data['precipIntensity']
    del data['precipIntensity_T1']
    del data['precipIntensityMax']
    del data['precipIntensityMax_T1']
    del data['precipAccumulation']
    del data['precipAccumulation_T1']


