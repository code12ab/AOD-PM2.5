# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/10/6 18:57


# 库
import pandas as pd
import numpy as np
import os, time

# 字符类型的时间
def get_sjc(x):
    x = str(x)
    timeArray = time.strptime(x, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp  # 1381419600


df1 = pd.read_excel('d:\\雨雪+2018_new_pm_aod_interpolate - 副本.xlsx')
df2 = pd.read_excel('d:\\id+x+y+aod+pm.xlsx')

df3 = pd.merge(df1,df2,how='left',on='id')
df3['经度'] = df3['经度'].fillna(method='pad')
df3['纬度'] = df3['纬度'].fillna(method='pad')
df3["tstamps"] = df3['日期'].map(lambda x:get_sjc(x))
df3 = df3.set_index('日期')
df3 = df3.dropna()
df3.to_excel('D:\\GW-R.xlsx')