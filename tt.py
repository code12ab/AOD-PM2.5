# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/7 11:10


# 库
import pandas as pd
import copy
from pandas import DataFrame
import numpy as np
left1 = DataFrame({'group_val2':[3.5,7]},index=['a2','b2'])
right1 = DataFrame({'group_val2':[3.5,7]},index=['a1','b1'])




d = pd.concat([left1,right1],axis=1, sort=False)
c = pd.concat([left1,right1],axis=0, sort=False)



b = copy.deepcopy(d)
b = d.copy()
d.columns = ["xxx", "xxsdsa"]
print(b.index, d.index)