# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/7/18 9:58

import pandas as pd
import numpy as np
from scipy import stats
import numpy as np
data = pd.read_excel("Dental_2390022.xls")

miaoshu = data.describe()
#miaoshu.to_excel("描述统计.xls")

for i in range(len(data["DFMT"])):
    if data['DFMT'][i] != 0:
        data['DFMT'][i] = 1

for i in range(len(data["DFMT"])):
    if data['DepCat'][i] != 7:
        data['DepCat'][i] = 0
    else:
        data['DepCat'][i] = 1

#print(data)
ttfc = stats.levene(data["DFMT"][data["DepCat"]==1],data["DFMT"][data["DepCat"]==0])
ttest_b = stats.ttest_ind(data["DFMT"][data["DepCat"]==1],data["DFMT"][data["DepCat"]==0], equal_var = False)
print("方差检验",ttfc,"\n","t检验",ttest_b)

jiaocha = pd.pivot_table(data,values = 'DFMT',index = ['DepCat'],aggfunc=len)
print(jiaocha)

# 交叉表格

#jiaocha = pd.pivot_table(data,values = 'DFMT',index = ['DepCat'],aggfunc=len)
#print(jiaocha)
#ttest1 = stats.ttest_ind(data["DFMT"][data["DepCat"]==4],data["DFMT"][data["DepCat"]==6])
#ttest2 = stats.ttest_ind(data["DFMT"][data["DepCat"]==4],data["DFMT"][data["DepCat"]==7])
#ttest3 = stats.ttest_ind(data["DFMT"][data["DepCat"]==6],data["DFMT"][data["DepCat"]==7])
#print(ttest1,ttest2,ttest3,sep="\n")

# 置信区间
#x = data["DFMT"][data["DepCat"]==6]
#interval=stats.t.interval(0.95,len(x)-1,x.mean(),x.std())
#print(interval)


################################################Q22222222222222