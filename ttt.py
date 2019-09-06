# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/9/5 9:02


# 库
import pandas as pd
import numpy as np
import os

a = [[1,np.nan],[np.nan,2],[10,10]]

a = pd.DataFrame(a)

a.columns = ["x", "y"]
print(a)
b = a.mean(1)

print(b)