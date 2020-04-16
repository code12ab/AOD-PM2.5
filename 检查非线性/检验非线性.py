# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2020/3/19 1:14


# 库
import pandas as pd
import numpy as np
import os




input_path = "C:\\Users\\iii\\Desktop\\北京-古城.xlsx"
input_path = 'D:\\毕业论文程序\\污染物浓度\\整理\\PM\\2018_new\\北京-古城.xlsx'
data = pd.read_excel(input_path)
def Pettitt_change_point_detection(inputdata):
    inputdata = np.array(inputdata)
    n = inputdata.shape[0]
    k = range(n)
    inputdataT = pd.Series(inputdata)
    r = inputdataT.rank()
    Uk = [2 * np.sum(r[0:x]) - x * (n + 1) for x in k]
    Uka = list(np.abs(Uk))
    U = np.max(Uka)
    K = Uka.index(U)
    pvalue = 2 * np.exp((-6 * (U**2)) / (n**3 + n**2))
    if pvalue <= 0.05:
        change_point_desc = '显著'
    else:
        change_point_desc = '不显著'
    #  Pettitt_result = {'突变点位置':K,'突变程度':change_point_desc}
    return K ,change_point_desc # ,Pettitt_result


#c = Pettitt_change_point_detection(data["相关系数"])
c = Pettitt_change_point_detection(data["PM25"])

print(c)


#length = len(data["相关系数"])
length = len(data["PM25"])

locations = []
for i in range(0, length, 1):
    pos, result = Pettitt_change_point_detection(data["PM25"][i:i+365])
    #pos, result = Pettitt_change_point_detection(data["相关系数"][i:i+152])
    if result == "显著":
        locations.append(pos+i)

print(set(locations))