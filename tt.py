# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/7 11:10


# 库

import numpy as np


# 地理距离公式
a = [np.nan,1.0,np.nan]
d = [1,np.nan,np.nan]
d2 = [np.nan,np.nan,np.nan]

l = []


c = [a,d,d2]

import pandas as pd
import copy
c = pd.DataFrame(c)



e = c[c==1].sum().sum()
print(e)