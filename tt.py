# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/7 11:10


# 库
import pandas as pd
import numpy as np

data_pollution = pd.DataFrame(np.arange(12).reshape(4,3), index=list('abcd'), columns=list('xyz'))
df2 = pd.DataFrame(np.arange(12).reshape(4,3), index=list('abcd'), columns=list('xyz'))
data_pollution.x = np.nan
data_pollutionX = data_pollution.copy()
for columname in data_pollution.columns:
    if data_pollution[columname].count() != len(data_pollution):
        loc = data_pollution[columname][data_pollution[columname].isnull().values == True].index.tolist()
        for nub in loc:
            data_pollutionX[columname][nub] = df2[columname][nub]

print(data_pollution)
print(data_pollutionX)