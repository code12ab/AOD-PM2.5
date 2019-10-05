# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/7 18:54

# 库
import pandas as pd
import numpy as np
import math
from numpy import array
import os
from sklearn import linear_model
from sklearn.linear_model import LinearRegression

Merge_output_file_path = "D:\\毕业论文程序\\污染物浓度\\插值模块\\Merge\\多年合一\\"
res_output_path = "D:\\毕业论文程序\\污染物浓度\\插值模块\\Res\\多年合一\\"
raw_data_file_path = r"D:\毕业论文程序\污染物浓度\整理\全部污染物\\多年合一\\"
input_file_names = os.listdir(Merge_output_file_path)  # 文件名列表
for input_file_name in input_file_names:
    print(input_file_name)
    # 读取插补数据
    data_KNN = pd.read_excel(
        Merge_output_file_path +
        input_file_name,
        sheet_name="KNN")
    data_ewm = pd.read_excel(
        Merge_output_file_path +
        input_file_name,
        sheet_name="ewm")
    data_IDW = pd.read_excel(
        Merge_output_file_path +
        input_file_name,
        sheet_name="IDW")
    data_Iterative = pd.read_excel(
        Merge_output_file_path +
        input_file_name,
        sheet_name="Iterative")
    # 原始数据
    data_raw = pd.read_excel(raw_data_file_path + input_file_name)

    # 结果列表
    res = []
    for column_name in ["PM25", "PM10", "SO2", "NO2", "O3", "CO"]:
        d1 = data_KNN[["日期", column_name]]
        d2 = data_ewm[["日期", column_name]]
        d3 = data_IDW[["日期", column_name]]
        d4 = data_Iterative[["日期", column_name]]
        d0 = data_raw[["日期", column_name]]
        # 合并时间插补
        data_Time = pd.merge(d1,
                             d2,
                             how='left',
                             on=["日期"])  # 列名: 日期,KNN,ewm
        data_Time.columns = ["日期", "KNN", "ewm"]
        # 合并空间插补
        data_Station = pd.merge(
            d3,
            d4,
            how='left',
            on=["日期"])  # 列名: 日期,IDW,Iterative
        data_Station.columns = ["日期", "IDW", "Iterative"]
        # 合并时空插补
        data_T_S = pd.merge(
            data_Time,
            data_Station,
            how='left',
            on=["日期"])  # 列名: 日期,KNN,ewm,IDW,Iterative
        # 合并时空插补,4种和真实数据
        data_aod_contain0 = pd.merge(
            d0,
            data_T_S,
            how='left',
            on=["日期"])  # 列名: 日期,'column_name',KNN,ewm,IDW,Iterative

        data_aod_contain0 = data_aod_contain0.set_index("日期")
        data_aod = data_aod_contain0[data_aod_contain0[column_name] > 0]
        # data_aod_to_weight = data_aod.dropna()  # 用非空值计算更合理
        #
        # 如果都不为空则不用回归

        # 情况1 都是不空的
        data_aod_0null = data_aod[(data_aod['KNN'] > 0) & (data_aod['KNN'] > 0) & (data_aod['KNN'] > 0) & (data_aod['KNN'] > 0)]

        # 情况2 都是空值的: 基本不存在,基本都使用ewm插值完了
        data_aod_4null = data_aod[pd.isnull(data_aod['KNN']) & pd.isnull(data_aod['ewm']) & pd.isnull(data_aod['IDW']) & pd.isnull(data_aod['Iterative'])]

        # 情况3 三种空值
        data_aod_3null_1 = data_aod[(data_aod['KNN'] > 0) & pd.isnull(data_aod['ewm']) & pd.isnull(data_aod['IDW']) & pd.isnull(data_aod['Iterative'])]
        data_aod_3null_2 = data_aod[pd.isnull(data_aod['KNN']) & (data_aod['ewm'] > 0) & pd.isnull(data_aod['IDW']) & pd.isnull(data_aod['Iterative'])]
        data_aod_3null_3 = data_aod[pd.isnull(data_aod['KNN']) & pd.isnull(data_aod['ewm']) & (data_aod['IDW'] > 0) & pd.isnull(data_aod['Iterative'])]
        data_aod_3null_4 = data_aod[pd.isnull(data_aod['KNN']) & pd.isnull(data_aod['ewm']) & pd.isnull(data_aod['IDW']) & (data_aod['Iterative'] > 0)]

        # 情况4 两种空值
        data_aod_2null_1 = data_aod[(data_aod['KNN'] > 0) & (data_aod['ewm'] > 0) & pd.isnull(data_aod['IDW']) & pd.isnull(data_aod['Iterative'])]
        data_aod_2null_2 = data_aod[(data_aod['KNN'] > 0) & pd.isnull(data_aod['ewm']) & (data_aod['IDW'] > 0) & pd.isnull(data_aod['Iterative'])]
        data_aod_2null_3 = data_aod[(data_aod['KNN'] > 0) & pd.isnull(data_aod['ewm']) & pd.isnull(data_aod['IDW']) & (data_aod['Iterative'] > 0)]
        data_aod_2null_4 = data_aod[pd.isnull(data_aod['KNN']) & (data_aod['ewm'] > 0) & (data_aod['IDW'] > 0) & pd.isnull(data_aod['Iterative'])]
        data_aod_2null_5 = data_aod[pd.isnull(data_aod['KNN']) & (data_aod['ewm'] > 0) & pd.isnull(data_aod['IDW']) & (data_aod['Iterative'] > 0)]
        data_aod_2null_6 = data_aod[pd.isnull(data_aod['KNN']) & pd.isnull(data_aod['ewm']) & (data_aod['IDW'] > 0) & (data_aod['Iterative'] > 0)]

        # 情况5 一种空值
        data_aod_1null_1 = data_aod[(data_aod['KNN'] > 0) & (data_aod['ewm'] > 0) & (data_aod['IDW'] > 0) & pd.isnull(data_aod['Iterative'])]
        data_aod_1null_2 = data_aod[(data_aod['KNN'] > 0) & (data_aod['ewm'] > 0) & pd.isnull(data_aod['IDW']) & (data_aod['Iterative'] > 0)]
        data_aod_1null_3 = data_aod[(data_aod['KNN'] > 0) & pd.isnull(data_aod['ewm']) & (data_aod['IDW'] > 0) & (data_aod['Iterative'] > 0)]
        data_aod_1null_4 = data_aod[pd.isnull(data_aod['KNN']) & (data_aod['ewm'] > 0) & (data_aod['IDW'] > 0) & (data_aod['Iterative'] > 0)]




        # 下面是含零的分割 ============================================================================================================================================

        # 情况1 都是不空的
        data_aod_contain0_0null = data_aod_contain0[(data_aod_contain0['KNN'] > 0) & (data_aod_contain0['KNN'] > 0) & (data_aod_contain0['KNN'] > 0) & (data_aod_contain0['KNN'] > 0)]
        # 情况2 都是空值的: 基本不存在,基本都使用ewm插值完了
        data_aod_contain0_4null = data_aod_contain0[pd.isnull(data_aod_contain0['KNN']) & pd.isnull(data_aod_contain0['ewm']) & pd.isnull(data_aod_contain0['IDW']) & pd.isnull(data_aod_contain0['Iterative'])]
        # 情况3 三种空值
        data_aod_contain0_3null_1 = data_aod_contain0[(data_aod_contain0['KNN'] > 0) & pd.isnull(data_aod_contain0['ewm']) & pd.isnull(data_aod_contain0['IDW']) & pd.isnull(data_aod_contain0['Iterative'])]
        data_aod_contain0_3null_2 = data_aod_contain0[pd.isnull(data_aod_contain0['KNN']) & (data_aod_contain0['ewm'] > 0) & pd.isnull(data_aod_contain0['IDW']) & pd.isnull(data_aod_contain0['Iterative'])]
        data_aod_contain0_3null_3 = data_aod_contain0[pd.isnull(data_aod_contain0['KNN']) & pd.isnull(data_aod_contain0['ewm']) & (data_aod_contain0['IDW'] > 0) & pd.isnull(data_aod_contain0['Iterative'])]
        data_aod_contain0_3null_4 = data_aod_contain0[pd.isnull(data_aod_contain0['KNN']) & pd.isnull(data_aod_contain0['ewm']) & pd.isnull(data_aod_contain0['IDW']) & (data_aod_contain0['Iterative'] > 0)]
        # 情况4 两种空值
        data_aod_contain0_2null_1 = data_aod_contain0[(data_aod_contain0['KNN'] > 0) & (data_aod_contain0['ewm'] > 0) & pd.isnull(data_aod_contain0['IDW']) & pd.isnull(data_aod_contain0['Iterative'])]
        data_aod_contain0_2null_2 = data_aod_contain0[(data_aod_contain0['KNN'] > 0) & pd.isnull(data_aod_contain0['ewm']) & (data_aod_contain0['IDW'] > 0) & pd.isnull(data_aod_contain0['Iterative'])]
        data_aod_contain0_2null_3 = data_aod_contain0[(data_aod_contain0['KNN'] > 0) & pd.isnull(data_aod_contain0['ewm']) & pd.isnull(data_aod_contain0['IDW']) & (data_aod_contain0['Iterative'] > 0)]
        data_aod_contain0_2null_4 = data_aod_contain0[pd.isnull(data_aod_contain0['KNN']) & (data_aod_contain0['ewm'] > 0) & (data_aod_contain0['IDW'] > 0) & pd.isnull(data_aod_contain0['Iterative'])]
        data_aod_contain0_2null_5 = data_aod_contain0[pd.isnull(data_aod_contain0['KNN']) & (data_aod_contain0['ewm'] > 0) & pd.isnull(data_aod_contain0['IDW']) & (data_aod_contain0['Iterative'] > 0)]
        data_aod_contain0_2null_6 = data_aod_contain0[pd.isnull(data_aod_contain0['KNN']) & pd.isnull(data_aod_contain0['ewm']) & (data_aod_contain0['IDW'] > 0) & (data_aod_contain0['Iterative'] > 0)]
        # 情况5 一种空值
        data_aod_contain0_1null_1 = data_aod_contain0[(data_aod_contain0['KNN'] > 0) & (data_aod_contain0['ewm'] > 0) & (data_aod_contain0['IDW'] > 0) & pd.isnull(data_aod_contain0['Iterative'])]
        data_aod_contain0_1null_2 = data_aod_contain0[(data_aod_contain0['KNN'] > 0) & (data_aod_contain0['ewm'] > 0) & pd.isnull(data_aod_contain0['IDW']) & (data_aod_contain0['Iterative'] > 0)]
        data_aod_contain0_1null_3 = data_aod_contain0[(data_aod_contain0['KNN'] > 0) & pd.isnull(data_aod_contain0['ewm']) & (data_aod_contain0['IDW'] > 0) & (data_aod_contain0['Iterative'] > 0)]
        data_aod_contain0_1null_4 = data_aod_contain0[pd.isnull(data_aod_contain0['KNN']) & (data_aod_contain0['ewm'] > 0) & (data_aod_contain0['IDW'] > 0) & (data_aod_contain0['Iterative'] > 0)]


        print(data_aod_contain0_2null_5.index)
        print(data_aod_contain0_2null_5)
        # 分组没毛病===================================================================================================================


        # 毛病在 aod非空的点 数据不够建模
        # 上面把1000行拆成了 = 250行+250行+250行+250行
        # 去 aod污染物 > 0的行
        """
        for item_1 in [data_aod_0null, data_aod_4null, data_aod_3null_1, data_aod_3null_2, data_aod_3null_3, data_aod_3null_4,
                       data_aod_2null_1, data_aod_2null_2, data_aod_2null_3, data_aod_2null_4, data_aod_2null_5, data_aod_2null_6,
                       data_aod_1null_1, data_aod_1null_2, data_aod_1null_3, data_aod_1null_4]:
            if len(item_1) > 0:
                linreg = LinearRegression()
                linreg.fit(item_1[["KNN", "ewm", "IDW", 'Iterative']], item_1[column_name])
                print(linreg.intercept_)
                print(linreg.coef_)
                print(item_1)
         """

        for item_1 in [[data_aod_contain0_0null, data_aod_0null],
                       [data_aod_contain0_4null, data_aod_4null],
                       [data_aod_contain0_3null_1, data_aod_3null_1],[data_aod_contain0_3null_2,data_aod_3null_2],[data_aod_contain0_3null_3,data_aod_3null_3],[data_aod_contain0_3null_4,data_aod_3null_4],
                       [data_aod_contain0_2null_1, data_aod_2null_1],[data_aod_contain0_2null_2, data_aod_2null_2],[data_aod_contain0_2null_3, data_aod_2null_3],[data_aod_contain0_2null_4, data_aod_2null_4],
                       [data_aod_contain0_2null_5, data_aod_2null_5],[data_aod_contain0_2null_6, data_aod_2null_6],
                       [data_aod_contain0_1null_1, data_aod_1null_1],[data_aod_contain0_1null_2, data_aod_1null_2],[data_aod_contain0_1null_3, data_aod_1null_3],[data_aod_contain0_1null_4, data_aod_1null_4]]:
            if len(item_1[1]) > 0:
                linreg = LinearRegression()
                linreg.fit(item_1[1][["ewm", 'Iterative']], item_1[1][column_name])  # 区分情况不一定都要用四个变量
                #print(linreg.intercept_)
                #print(linreg.coef_)
                #if len(item_1[0]) > len(item_1[1]):
                for idx in item_1[0].index:
                    #print(idx)
                    if item_1[0][column_name][idx] == np.nan:
                        item_1[0][column_name][idx] = 0.1 * item_1[1]["ewm"][idx]
                        print("chabu", item_1[0][column_name][idx])

'''         问题在于，筛选出来用于train的数据，是空的。所以应该自己构造空值，参考易，抹除原有。这部分内容可以放到后期。
'''