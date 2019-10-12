# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/10/4 7:37


# 库

from scipy import interpolate
import pandas as pd
import copy
import numpy as np

#ind = 'D:\\毕业论文程序\\气象数据\\筛除字符串\\2018\\威海-山大分校.xlsx'

input_path = 'D:\\雨雪+2018_new_pm_aod_interpolate-副本.xlsx'
df1 = pd.read_excel(input_path, index_col='日期')

df2 = df1.groupby('id').mean()
df3 = df1.groupby('id').median()
df4 = df1.groupby('id').max()
df5 = df1.groupby('id').min()

writer = pd.ExcelWriter('df2.xlsx')
numb = 0
for methods_output in [df2, df3,df4,df5]:
    numb = numb+1
    methods_output.to_excel(writer,sheet_name="sheet_%s" % numb)
writer.save()
