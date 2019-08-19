# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/19 0:58


# 库
import pandas as pd
import numpy as np

a = [[-1,3,4,5],[-1,-1,123,412],[-1,-1,23,-1]]
a= pd.DataFrame(a)
print(a)
print(np.min(a))