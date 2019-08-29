# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/29 14:55


# 库
import pandas as pd
import numpy as np


a = [[np.nan,np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan,np.nan],[np.nan,np.nan,np.nan,np.nan]]
a = pd.DataFrame(a)
a[a.shape[1]%2][a.shape[0]%2] = float(0.00)

print(a)

print(11//2)