# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/10/10 14:56


# 库
import pandas as pd
import numpy as np
import os
import random

list1 = []
list2 = []
list3 = []

for i in range(0,100):
    a = random.uniform(27, 31)
    b = random.uniform(0.91, 1.21)

    list1.append(a)
    list2.append(b)


for i in range(0,100):
    mean = np.average(list1)
    c = random.uniform((mean+3*np.std(list1))**2, (mean+8*np.std(list1))**2)
    list3.append(c)
list4 = []
list4.append(list1)
list4.append(list2)
list4.append(list3)

df = pd.DataFrame(list4)
df.to_excel('test.xlsx')


print(np.average(list1))
print(np.average(list2))
print(np.average(list3))