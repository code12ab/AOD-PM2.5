# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2020/3/10 13:54


# 库
import pandas as pd
import numpy as np
import math
from numpy import array
import os

chabu_output_path = "D:\\毕业论文程序\\气象数据\\插值模块\\Merge\\2018插补效率\\"  # 制造空值后的插补结果
null_output_path = "D:\\毕业论文程序\\气象数据\\插值模块\\制造的缺失值\\"  # 制造出来的空值的，真实值。
input_file_names = os.listdir(chabu_output_path)  # 文件名列表
total = 0  # 只有一个变量，那么制造的空值矩阵必定没有空格在。
defeat1 = 0
defeat2 = 0
defeat3 = 0
defeat4 = 0
for input_file_name in input_file_names:
    # 插值后AT
    data_chabu_knn = pd.read_excel(chabu_output_path + input_file_name, sheet_name ='KNN')
    data_chabu_ewm = pd.read_excel(chabu_output_path + input_file_name, sheet_name ='ewm')
    data_chabu_idw = pd.read_excel(chabu_output_path + input_file_name, sheet_name ='IDW')
    data_chabu_iter = pd.read_excel(chabu_output_path + input_file_name, sheet_name ='Iterative')

    # 制造出来的空值的，真实值
    data_null_Aqua = pd.read_excel(null_output_path + input_file_name, index_col='Unnamed: 0')
    data_null_Terra = pd.read_excel(null_output_path + input_file_name, index_col='Unnamed: 0')  # 第一列空列，处理一下
    # 原始数据，只是换个文件夹放置
    # data_origin_Terra = pd.read_excel(input_file_path_Terra + input_file_name)  # 插补前
    # data_origin_Aqua = pd.read_excel(input_file_path_Aqua + input_file_name)
    # print(str(data_chabu['日期'][0])[0:11])
    data_chabu_knn['日期'] = data_chabu_knn['日期'].map(lambda x: str(x)[0:11].replace(" ",""))
    data_chabu_ewm['日期'] = data_chabu_ewm['日期'].map(lambda x: str(x)[0:11].replace(" ",""))
    data_chabu_idw['日期'] = data_chabu_idw['日期'].map(lambda x: str(x)[0:11].replace(" ",""))
    data_chabu_iter['日期'] = data_chabu_iter['日期'].map(lambda x: str(x)[0:11].replace(" ",""))

    # print(data_true['日期'])
    # data_origin_Terra['日期'] = data_origin_Terra['日期'].map(lambda x: x.replace(" ",""))
    # data_origin_Aqua['日期'] = data_origin_Aqua['日期'].map(lambda x: x.replace(" ", ""))
    # print(data_res)
    # print(data_null.isnull())
    error1 = list()
    error2 = list()
    error3 = list()
    error4 = list()
    error1_mae = list()
    error2_mae = list()
    error3_mae = list()
    error4_mae = list()
    for columname in data_null_Terra.columns:
        if columname != "日期":
            if columname != "监测站":
                # loc 是某列为空的行坐标，这里由于前一个步骤中被转置了，
                # loc 对应的是AOD0到AOD16
                # print(columname)
                loc_t = data_null_Terra[columname][data_null_Terra[columname].isnull().values == False].index.tolist()
                # print(loc_t)
                for numb1 in loc_t:
                    if numb1 >= 0:  # 此时为 aod_0  # ！=0 时为其他即，aods
                        total += 1
                        # 原真实值。 Colu列→源数据第几行；numb（loc-t）第几行即AODx]
                        # print(data_null_Aqua[columname][numb1])
                        c_null = data_null_Terra[columname][numb1].replace("(","").replace(")","").replace("'","").replace(" ","").replace("Timestamp","")\
                            .replace("00:00:00", "").split(",")
                        # c_null = data_null_Terra[columname][numb1]
                        # print(c_null)
                        c_null = list(c_null)  # 转化格式完毕
                        # print(c_origin[1])
                        # print(c_origin[1].__class__)
                        # 先 日期 ， 后 aod 变量
                        # print(data_origin_Aqua[data_origin_Aqua['日期'] == c_null[1]][c_null[0]].values[0])  # 提出数值
                        c_chabu_knn = data_chabu_knn[data_chabu_knn['日期'] == c_null[1]][c_null[0]].values[0]
                        # print(c_chabu_knn)
                        c_chabu_ewm = data_chabu_ewm[data_chabu_ewm['日期'] == c_null[1]][c_null[0]].values[0]
                        c_chabu_idw = data_chabu_idw[data_chabu_idw['日期'] == c_null[1]][c_null[0]].values[0]
                        c_chabu_iter = data_chabu_iter[data_chabu_iter['日期'] == c_null[1]][c_null[0]].values[0]
                        c_true = float(c_null[2])  # 制造的空值的真实值
                        c_chabu_knn = float(c_chabu_knn)
                        if c_chabu_knn >= 0 and c_true > 0:
                            e1 = abs(c_chabu_knn - c_true) / c_true
                            e1_mae = abs(c_chabu_knn - c_true)
                            error1_mae.append(e1_mae)
                            error1.append(e1)
                        else:
                            defeat1 += 1

                        if c_chabu_ewm > 0 and c_true > 0:
                            e2 = abs(c_chabu_ewm - c_true) / c_true
                            e2_mae = abs(c_chabu_ewm - c_true)
                            error2_mae.append(e2_mae)
                            error2.append(e2)
                        else:
                            defeat2 += 1

                        if c_chabu_idw > 0 and c_true > 0:
                            e3 = abs(c_chabu_idw - c_true) / c_true
                            e3_mae = abs(c_chabu_idw - c_true)
                            error3_mae.append(e3_mae)
                            error3.append(e3)
                        else:
                            defeat3 += 1

                        if c_chabu_iter > 0 and c_true > 0:
                            e4 = abs(c_chabu_iter - c_true) / c_true
                            e4_mae = abs(c_chabu_iter - c_true)
                            error4_mae.append(e4_mae)
                            error4.append(e4)
                        else:
                            defeat4 += 1
print('RE', np.average(error1), np.average(error2), np.average(error3), np.average(error4))
print('maE', np.average(error1_mae), np.average(error2_mae), np.average(error3_mae), np.average(error4_mae))
# print(np.std(error1))
print("失败", defeat1/total, defeat2/total, defeat3/total, defeat4/total,)
# print(data_null_Terra.columns)
# print(data_res.head(3))
# print(data_res['日期'][1].__class__)
# print(data_res['日期'][1])
# print(data_res[data_res['日期'] == '2018-01-01 ']['AOD_0'])  # 日期后面多了个空格
# lng2 = JCZ_info[JCZ_info["监测站"] == item_idw]["经度"]


