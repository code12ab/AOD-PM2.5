# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2020/3/13 15:45


# 库
import pandas as pd
import numpy as np
import os
from math import radians, cos, sin, asin, sqrt
from scipy.stats import ttest_rel

def geo_distance(lng1, lat1, lng2, lat2):
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    d_lon = lng2 - lng1
    d_lat = lat2 - lat1
    a = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
    dis = 2 * asin(sqrt(a)) * 6371.393 * 1000  # 地球半径
    return dis  # 输出结果的单位为“米”

JCZ_info = pd.read_excel("D:\\毕业论文程序\\MODIS\\坐标\\监测站坐标.xlsx", sheet_name="汇总")
JCZ_info["监测站"] = JCZ_info["城市"] + "-" + JCZ_info["监测点名称"]

input_path = 'D:\\毕业论文程序\\污染物浓度\\插值模块\\Res\\2018_new\\'
out_path = 'D:\\毕业论文程序\\非线性检验\\各自\\'
out_path2 = 'D:\\毕业论文程序\\非线性检验\\汇总\\'

file_name_list = os.listdir(input_path)  # 文件名
# 接受拒绝统计表
ar = list()
# 距离和结果列表
for name in file_name_list:
    res = list()
    data0 = pd.read_excel(input_path + name, index_col="日期")
    name = name.replace(".xlsx","")
    lng1 = JCZ_info[JCZ_info["监测站"] == name]["经度"]
    lat1 = JCZ_info[JCZ_info["监测站"] == name]["纬度"]
    n = 0
    reject = 0
    accept = 0
    for name2 in file_name_list:
        if name2 != name:
            n += 1
            data1 = pd.read_excel(input_path + name2, index_col="日期")
            name2 = name2.replace(".xlsx", "")
            lng2 = JCZ_info[JCZ_info["监测站"] == name2]["经度"]
            lat2 = JCZ_info[JCZ_info["监测站"] == name2]["纬度"]
            # print(lng2)
            d1 = geo_distance(lng1, lat1, lng2, lat2)
            # print(name,name2,d1)
            # print("============================================================")
            # print("Null Hypothesis:mean(s1)=mean(s2)，α=0.05")
            ttest, pval = ttest_rel(data0['PM25'], data1['PM25'])
            # print(pval)
            if pd.isna(pval):
                # print(pval)
                pval = 0.000
            if pval < 0.05:
                reject += 1
                # print(n, "Reject the Null Hypothesis.")
                res.append((name2, pval, d1))
            else:
                accept += 1
                # print(n, "Accept the Null Hypothesis.")
                res.append((name2, pval, d1))

    res = pd.DataFrame(res)
    # res = res.fillna(res.median())
    print(res.head(3))
    res.columns = ['监测站', "P值", "地理距离"]  # 重命名

    res.to_excel(out_path + name + ".xlsx")
    ar.append((name, reject, accept))

ar = pd.DataFrame(ar)
ar.columns = ["监测站",'拒绝次数', '接受次数']
ar.to_excel(out_path2 + "汇总.xlsx")