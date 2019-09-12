# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/9/12 11:11


# 库
import pandas as pd
import numpy as np
import os
a= [[np.nan,1],[np.nan,1]]

a = pd.DataFrame(a)
print(a)
print(a[0].sum())
print(a[0].isnull().sum())
print(len(a[0].index))