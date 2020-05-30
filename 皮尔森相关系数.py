# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2020/4/26 11:20


# 库
import pandas as pd
import numpy as np
import os
import math
y =[700,650,900,950,1100,1150,1200,1400,1550,1500]
x1=[800,1000,1200,1400,1600,1800,2000,2200,2400,2600]
x2=[8100,10090,12730,14250,16930,18760,20520,22010,24350,26860]

def pearson(vector1, vector2):
    n = len(vector1)
    #simple sums
    sum1 = sum(float(vector1[i]) for i in range(n))
    sum2 = sum(float(vector2[i]) for i in range(n))
    #sum up the squares
    sum1_pow = sum([pow(v, 2.0) for v in vector1])
    sum2_pow = sum([pow(v, 2.0) for v in vector2])
    #sum up the products
    p_sum = sum([vector1[i]*vector2[i] for i in range(n)])
    #分子num，分母den
    num = p_sum - (sum1*sum2/n)
    den = math.sqrt((sum1_pow-pow(sum1, 2)/n)*(sum2_pow-pow(sum2, 2)/n))
    if den == 0:
        return 0.0
    return num/den

print(pearson(y, x2))