# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/9/19 20:10


# 库
import pandas as pd
import numpy as np
import os


s = map(int,input().split())
def all_list(arr):
    result = {}
    for i in set(arr):
        result[i] = arr.count(i)
    return result
res = all_list(s)














# a,b,b,c,a,a,b,a,c