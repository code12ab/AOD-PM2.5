# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/7/3 10:35



import pandas as pd

import datetime  # 程序耗时

# 开始计算耗时
start_time = datetime.datetime.now()
# 读取
data = pd.read_excel("测试用数据.xlsx")
coordinate_file_path = "D:\\毕业论文程序\\MODIS\\坐标\\"
JCZ_file = pd.read_excel(coordinate_file_path + "监测站坐标toDarkSkyAPI.xlsx", sheet_name="汇总")  # 监测站坐标toDarkSkyAPI
datajcz = JCZ_file["城市"]
print(datajcz.shape)


xni = pd.get_dummies(datajcz)
#print(xni)
print(xni.shape)
from sklearn import preprocessing
enc = preprocessing.OneHotEncoder()
c = enc.fit(xni)  # 这里一共有4个数据，3种特征
array = enc.transform(xni).toarray()  # 这里使用一个新的数据来测试
#print(array)  # [[ 1  0  0  1  0  0  0  0  1]]

array = pd.DataFrame(array)
print(array.shape[1])
