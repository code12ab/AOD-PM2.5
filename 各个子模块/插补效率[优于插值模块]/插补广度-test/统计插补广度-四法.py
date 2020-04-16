# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2020/3/11 10:05


# 库
import pandas as pd
import numpy as np
import os

null0_knn =list()
null1_knn = list()
null2_knn = list()
null3_knn = list()
null4_knn = list()

null0_ewm = list()
null1_ewm = list()
null2_ewm = list()
null3_ewm = list()
null4_ewm = list()

null0_idw = list()
null1_idw = list()
null2_idw = list()
null3_idw = list()
null4_idw = list()

null0_iter = list()
null1_iter = list()
null2_iter = list()
null3_iter = list()
null4_iter = list()
# 路径
# input_path = "d:\\毕业论文程序\\气溶胶光学厚度\\空间转换模块\\Aqua\\2018_日期补全\\"
# output_path = "d:\\毕业论文程序\\气溶胶光学厚度\\空间转换模块\\Aqua\\2018_all\\"
# input_path = "d:\\毕业论文程序\\NDVI\\DATA\\MOD2018\\"
# output_path = "d:\\毕业论文程序\\NDVI\\DATA\\MODALL\\"
# input_path ='D:\\毕业论文程序\\污染物浓度\\整理\\PM\\2018_日期补全\\'
# output_path ='D:\\毕业论文程序\\污染物浓度\\整理\\PM\\2018_all\\'

input_path1 = "d:\\毕业论文程序\\气溶胶光学厚度\\插值模块\\Merge\\2018\\"
input_path2 = "d:\\毕业论文程序\\NDVI\\插值模块\\Merge\\2018\\"
input_path3 = "d:\\毕业论文程序\\气象数据\\插值模块\\Merge\\2018\\"  # 还有时间滞后
input_path4 = "d:\\毕业论文程序\\污染物浓度\\插值模块\\Merge\\2018_new\\"

input_file_names = os.listdir(input_path1)  # 文件名列表, **.xlsx

for name in input_file_names:
    data1_knn = pd.read_excel(input_path1 + name, index_col="日期",sheet_name='KNN')
    data1_ewm = pd.read_excel(input_path1 + name, index_col="日期",sheet_name='ewm')
    data1_idw = pd.read_excel(input_path1 + name, index_col="日期",sheet_name='IDW')
    data1_iter = pd.read_excel(input_path1 + name, index_col="日期",sheet_name='Iterative')

    data2_knn = pd.read_excel(input_path2 + name, index_col="日期",sheet_name='KNN')
    data2_ewm = pd.read_excel(input_path2 + name, index_col="日期",sheet_name='ewm')
    data2_idw = pd.read_excel(input_path2 + name, index_col="日期",sheet_name='IDW')
    data2_iter = pd.read_excel(input_path2 + name, index_col="日期",sheet_name='Iterative')

    data3_knn = pd.read_excel(input_path3 + name, index_col="日期", sheet_name='KNN')
    data3_ewm = pd.read_excel(input_path3 + name, index_col="日期", sheet_name='ewm')
    data3_idw = pd.read_excel(input_path3 + name, index_col="日期", sheet_name='IDW')
    data3_iter = pd.read_excel(input_path3 + name, index_col="日期", sheet_name='Iterative')

    data4_knn = pd.read_excel(input_path4 + name, index_col="日期", sheet_name='KNN')
    data4_ewm = pd.read_excel(input_path4 + name, index_col="日期", sheet_name='ewm')
    data4_idw = pd.read_excel(input_path4 + name, index_col="日期", sheet_name='IDW')
    data4_iter = pd.read_excel(input_path4 + name, index_col="日期", sheet_name='Iterative')
    # print(name)
    # print(len(data3_iter.index)*len(data3_iter.columns))  # 一共多少数据量
    # print(data3_iter.isnull().sum().sum())  # 多列需要俩sum()

    # KNN 部分
    queshi0_knn = data1_knn['AOD_0'].isnull().sum().sum() / (len(data1_knn.index) * len(data1_knn.columns))
    del data1_knn['AOD_0']
    queshi1_knn = data1_knn.isnull().sum().sum() / (len(data1_knn.index) * len(data1_knn.columns))
    queshi2_knn = data2_knn.isnull().sum().sum() / (len(data2_knn.index) * len(data2_knn.columns))
    # queshi3_knn = data3_knn.isnull().sum().sum() / (len(data3_knn.index) * len(data3_knn.columns))
    queshi3_knn = data3_knn.isnull().sum().sum() / (365 * 26)  #
    queshi4_knn = data4_knn.isnull().sum().sum() / (len(data4_knn.index) * len(data4_knn.columns))

    null0_knn.append(queshi0_knn)
    null1_knn.append(queshi1_knn)
    null2_knn.append(queshi2_knn)
    null3_knn.append(queshi3_knn)
    null4_knn.append(queshi4_knn)
    # ewm
    queshi0_ewm = data1_ewm['AOD_0'].isnull().sum().sum() / (len(data1_ewm.index) * len(data1_ewm.columns))
    del data1_ewm['AOD_0']
    queshi1_ewm = data1_ewm.isnull().sum().sum() / (len(data1_ewm.index) * len(data1_ewm.columns))
    queshi2_ewm = data2_ewm.isnull().sum().sum() / (len(data2_ewm.index) * len(data2_ewm.columns))
    # queshi3_ewm = data3_ewm.isnull().sum().sum() / (len(data3_ewm.index) * len(data3_ewm.columns))
    queshi3_ewm = data3_ewm.isnull().sum().sum() / (365 * 26)
    queshi4_ewm = data4_ewm.isnull().sum().sum() / (len(data4_ewm.index) * len(data4_ewm.columns))

    null0_ewm.append(queshi0_ewm)
    null1_ewm.append(queshi1_ewm)
    null2_ewm.append(queshi2_ewm)
    null3_ewm.append(queshi3_ewm)
    null4_ewm.append(queshi4_ewm)
    # idw
    queshi0_idw = data1_idw['AOD_0'].isnull().sum().sum() / (len(data1_idw.index) * len(data1_idw.columns))
    del data1_idw['AOD_0']
    queshi1_idw = data1_idw.isnull().sum().sum() / (len(data1_idw.index) * len(data1_idw.columns))
    queshi2_idw = data2_idw.isnull().sum().sum() / (len(data2_idw.index) * len(data2_idw.columns))
    # queshi3_idw = data3_idw.isnull().sum().sum() / (len(data3_idw.index) * len(data3_idw.columns))
    queshi4_idw = data4_idw.isnull().sum().sum() / (len(data4_idw.index) * len(data4_idw.columns))
    queshi3_idw = data3_idw.isnull().sum().sum() / (365 * 26)

    null0_idw.append(queshi0_idw)
    null1_idw.append(queshi1_idw)
    null2_idw.append(queshi2_idw)
    null3_idw.append(queshi3_idw)
    null4_idw.append(queshi4_idw)
    # iter 部分
    queshi0_iter = data1_iter['AOD_0'].isnull().sum().sum() / (len(data1_iter.index) * len(data1_iter.columns))
    del data1_iter['AOD_0']
    queshi1_iter = data1_iter.isnull().sum().sum() / (len(data1_iter.index) * len(data1_iter.columns))
    queshi2_iter = data2_iter.isnull().sum().sum() / (len(data2_iter.index) * len(data2_iter.columns))
    # queshi3_iter = data3_iter.isnull().sum().sum() / (len(data3_iter.index) * len(data3_iter.columns))
    queshi4_iter = data4_iter.isnull().sum().sum() / (len(data4_iter.index) * len(data4_iter.columns))
    queshi3_iter = data3_iter.isnull().sum().sum() / (365 * 26)

    null0_iter.append(queshi0_iter)
    null1_iter.append(queshi1_iter)
    null2_iter.append(queshi2_iter)
    null3_iter.append(queshi3_iter)
    null4_iter.append(queshi4_iter)
    print("完成:", name)
print("knn→AOD:", np.average(null0_knn), 'AODs', np.average(null1_knn),"NDVI:", np.average(null2_knn),
      "气象:", np.average(null3_knn), "PM:", np.average(null4_knn))
print("ewm→AOD:", np.average(null0_ewm), 'AODs', np.average(null1_ewm),"NDVI:", np.average(null2_ewm),
      "气象:", np.average(null3_ewm), "PM:", np.average(null4_ewm))
print("idw→AOD:", np.average(null0_idw), 'AODs', np.average(null1_idw),"NDVI:", np.average(null2_idw),
      "气象:", np.average(null3_idw), "PM:", np.average(null4_idw))
print("iter→AOD:", np.average(null0_iter), 'AODs', np.average(null1_iter),"NDVI:", np.average(null2_iter),
      "气象:", np.average(null3_iter), "PM:", np.average(null4_iter))

'''
由于气象不是每个人文件都符合 365天*26变量，所以把分母修改成365*26.
'''
'''
这里气象插补结果很好，是因为逐时模块好用了，darksky修复了逐时数据能调用出来了。
'''
'''
之X前X使用的不包含逐时插值。前一次调用中逐时模块也是缺失的。
'''