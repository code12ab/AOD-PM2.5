# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/10/3 18:02


# 库
import pandas as pd
import numpy as np
import os

input_path = 'D:\\雨雪+2018_new_pm_aod.xlsx'
data = pd.read_excel(input_path, index_col='日期')

data = data[data['AOD_0']<= 2]
df1 = data[['AOD_0', 'PM25', 'tm_mon']]
print(len(data.index))
df2 = df1.groupby('tm_mon').mean()
df3 = df1.groupby('tm_mon').median()
df4 = df1.groupby('tm_mon').max()
df5 = df1.groupby('tm_mon').min()

writer = pd.ExcelWriter('df2.xlsx')
numb = 0
for methods_output in [df2, df3,df4,df5]:
    numb = numb+1
    methods_output.to_excel(writer,sheet_name="sheet_%s" % numb)
writer.save()
