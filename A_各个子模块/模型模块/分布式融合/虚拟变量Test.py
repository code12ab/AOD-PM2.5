# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/9/3 19:50


# 库
import pandas as pd
import numpy as np
import os



a  = [[1,2,3,2,142],[2,1,2,3,111],[3,3,1,1,221]]

a = pd.DataFrame(a)
for ccc in a.columns:
    a[ccc] = a[ccc].map(lambda x : str(x))

b = pd.get_dummies(a, drop_first=True)

print(b, len(b.columns))