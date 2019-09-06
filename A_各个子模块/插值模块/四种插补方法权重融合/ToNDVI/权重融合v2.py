# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/7 18:54

# 库
import pandas as pd
import numpy as np
import math
from numpy import array
import os


# 定义熵值法函数
def cal_weight(x):
    # 标准化
    x = x.apply(lambda x: ((x - np.min(x)) / (np.max(x) - np.min(x))))

    # 求k
    rows = x.index.size  # 行
    cols = x.columns.size  # 列
    k = 1.0 / math.log(rows)

    lnf = [[None] * cols for i in range(rows)]

    # 矩阵计算--
    # 信息熵
    # p=array(p)
    x = array(x)
    lnf = [[None] * cols for i in range(rows)]
    lnf = array(lnf)
    for i in range(0, rows):
        for j in range(0, cols):
            if x[i][j] == 0:
                lnfij = 0.0
            else:
                p = x[i][j] / x.sum(axis=0)[j]
                lnfij = math.log(p) * p * (-k)
            lnf[i][j] = lnfij
    lnf = pd.DataFrame(lnf)
    E = lnf

    # 计算冗余度
    d = 1 - E.sum(axis=0)
    # 计算各指标的权重
    w = [[None] * 1 for i in range(cols)]
    for j in range(0, cols):
        wj = d[j] / sum(d)
        w[j] = wj
        # 计算各样本的综合得分,用最原始的数据

    w = pd.DataFrame(w)
    return w


mean_output_file_path = "D:\\毕业论文程序\\NDVI\\插值模块\\Mean\\2018\\"
res_output_path = "d:\\毕业论文程序\\NDVI\\插值模块\\Res\\2018\\"
input_file_names = os.listdir(mean_output_file_path)  # 文件名列表
saved_list = os.listdir(res_output_path)
for input_file_name in input_file_names:
    if input_file_name in saved_list:
        continue
    print(input_file_name)

    # 读取
    data_KNN = pd.read_excel(
        mean_output_file_path +
        input_file_name,
        sheet_name="KNN")
    data_ewm = pd.read_excel(
        mean_output_file_path +
        input_file_name,
        sheet_name="ewm")
    data_IDW = pd.read_excel(
        mean_output_file_path +
        input_file_name,
        sheet_name="IDW")
    data_Iterative = pd.read_excel(
        mean_output_file_path +
        input_file_name,
        sheet_name="Iterative")
    if str(data_KNN.set_index('日期').stack().max()) == "nan" and str(data_ewm.set_index('日期').stack().max()) == "nan"\
            and str(data_IDW.set_index('日期').stack().max()) == "nan"\
            and str(data_Iterative.set_index('日期').stack().max()) == "nan":
        data_KNN = data_KNN.set_index('日期')
        data_KNN = data_KNN.fillna(0.00)
        data_KNN.to_excel(res_output_path + input_file_name)
        continue
    # 结果列表
    res = []
    for area_numb in range(0, 1):
        d1 = data_KNN[["日期", 'NDVI_%s' % area_numb]]
        d2 = data_ewm[["日期", 'NDVI_%s' % area_numb]]

        if len(data_KNN.index) > len(data_ewm):
            data_Time = pd.merge(d1,
                                 d2,
                                 how='left',
                                 on=["日期"])
        else:
            data_Time = pd.merge(d1,
                                 d2,
                                 how='right',
                                 on=["日期"])

        d3 = data_IDW[["日期", 'NDVI_%s' % area_numb]]
        d4 = data_Iterative[["日期", 'NDVI_%s' % area_numb]]
        if len(data_Iterative.index) > len(data_IDW.index):
            data_Station = pd.merge(
                d3,
                d4,
                how='right',
                on=["日期"])
        else:
            data_Station = pd.merge(
                d3,
                d4,
                how='left',
                on=["日期"])

        if len(data_Time.index) > len(data_Station.index):
            data_NDVI = pd.merge(
                data_Time,
                data_Station,
                how='left',
                on=["日期"])
        else:
            data_NDVI = pd.merge(
                data_Time,
                data_Station,
                how='right',
                on=["日期"])
        data_NDVI.columns = ["日期", "KNN", "ewm", "IDW", "Iterative"]
        # print(data_NDVI)
        # data_NDVI.columns : 日期 NDVI_0_x_x NDVI_0_y_x NDVI_0_x_y NDVI_0_y_y
        data_NDVI = data_NDVI.set_index("日期")
        data_NDVI_to_weight = data_NDVI.dropna()  # 用非空值计算更合理
        if len(data_NDVI_to_weight.index) > 0:
            w = cal_weight(data_NDVI_to_weight)  # 调用cal_weight
            w.index = data_NDVI.columns
            w.columns = ['weight']
            # print(input_file_name, w)
        else:
            morethan0_list = []
            for cname in data_NDVI.columns:
                if data_NDVI[cname].max() > 0:
                    morethan0_list.append(cname)
            null_list = []
            for noin_name in data_NDVI.columns:
                if noin_name not in morethan0_list:
                    null_list.append(noin_name)

            # 空白w, 仅有一列可用, 修复bug
            w_null = pd.DataFrame(index=['KNN','ewm','IDW','Iterative'],columns=['weight'])
            # print(w_null)
            data_NDVI_to_weight = data_NDVI[morethan0_list]
            w_def = cal_weight(data_NDVI_to_weight)  # 调用cal_weight
            w_def.index = [morethan0_list]
            w_def.columns = ['weight']
            # print(input_file_name, w_def)
            w_def = w_def.reset_index()
            w_null = w_null.reset_index()
            w_def.rename(columns={'level_0': 'method', 'weight': 'weight_def'}, inplace=True)
            w_null.rename(columns={'index': 'method', 'weight': 'weight_null'}, inplace=True)
            # print(w_def,w_null)
            w123 = pd.merge(w_null,w_def,how='left', on=['method'])
            w123 = w123.fillna(0.00)
            w123['weight'] = w123['weight_null'] + w123['weight_def']
            w = pd.DataFrame(w123['weight'])
            # print(w,"============")

        '''
        value_weight= data_NDVI["KNN"] * w.weight[0] + data_NDVI["ewm"] * \
            w.weight[1] + data_NDVI["IDW"] * w.weight[2] + data_NDVI["Iterative"] * w.weight[3]
        # print(data_NDVI.isnull().sum())
        '''
        value_weight_list = []
        for loc in range(len(data_NDVI.index)):
            # 四种方法均不缺失
            if pd.notnull(
                data_NDVI["KNN"][loc]) and pd.notnull(
                data_NDVI["ewm"][loc]) and pd.notnull(
                data_NDVI["IDW"][loc]) and pd.notnull(
                    data_NDVI["Iterative"][loc]):
                value_weight = data_NDVI["KNN"][loc] * w.weight[0] + data_NDVI["ewm"][loc] * w.weight[1] +\
                    data_NDVI["IDW"][loc] * w.weight[2] + data_NDVI["Iterative"][loc] * w.weight[3]
            # 某一种缺失
            elif pd.isnull(data_NDVI["KNN"][loc]) and pd.notnull(data_NDVI["ewm"][loc]) and pd.notnull(data_NDVI["IDW"][loc]) and \
                    pd.notnull(data_NDVI["Iterative"][loc]):
                value_weight = data_NDVI["ewm"][loc] * (w.weight[1] / (w.weight[1] + w.weight[2] + w.weight[3])) + \
                    data_NDVI["IDW"][loc] * (w.weight[2] / (w.weight[1] + w.weight[2] + w.weight[3])) +\
                    data_NDVI["Iterative"][loc] * (w.weight[3] / (w.weight[1] + w.weight[2] + w.weight[3]))
            elif pd.notnull(data_NDVI["KNN"][loc]) and pd.isnull(data_NDVI["ewm"][loc]) and pd.notnull(data_NDVI["IDW"][loc]) and \
                    pd.notnull(data_NDVI["Iterative"][loc]):
                value_weight = data_NDVI["KNN"][loc] * (w.weight[0] / (w.weight[0] + w.weight[2] + w.weight[3])) +\
                    data_NDVI["IDW"][loc] * (w.weight[2] / (w.weight[0] + w.weight[2] + w.weight[3])) +\
                    data_NDVI["Iterative"][loc] * (w.weight[3] / (w.weight[0] + w.weight[2] + w.weight[3]))
            elif pd.notnull(data_NDVI["KNN"][loc]) and pd.notnull(data_NDVI["ewm"][loc]) and pd.isnull(data_NDVI["IDW"][loc]) and \
                    pd.notnull(data_NDVI["Iterative"][loc]):
                value_weight = data_NDVI["KNN"][loc] * (
                    w.weight[0] / (w.weight[0] + w.weight[1] + w.weight[3])) + \
                    data_NDVI["ewm"][loc] * (
                    w.weight[1] / (w.weight[0] + w.weight[1] + w.weight[3])) + \
                    data_NDVI["Iterative"][loc] * (
                    w.weight[3] / (w.weight[0] + w.weight[1] + w.weight[3]))
            elif pd.notnull(data_NDVI["KNN"][loc]) and pd.notnull(data_NDVI["ewm"][loc]) and pd.notnull(data_NDVI["IDW"][loc]) and \
                    pd.isnull(data_NDVI["Iterative"][loc]):
                value_weight = data_NDVI["KNN"][loc] * (
                    w.weight[0] / (w.weight[0] + w.weight[1] + w.weight[2])) + \
                    data_NDVI["ewm"][loc] * (
                    w.weight[1] / (w.weight[0] + w.weight[1] + w.weight[2])) + \
                    data_NDVI["IDW"][loc] * (
                    w.weight[2] / (w.weight[0] + w.weight[1] + w.weight[2]))
            # 两种缺失
            elif pd.isnull(data_NDVI["KNN"][loc]) and pd.isnull(data_NDVI["ewm"][loc]) and pd.notnull(data_NDVI["IDW"][loc]) and \
                    pd.notnull(data_NDVI["Iterative"][loc]):
                value_weight = data_NDVI["IDW"][loc] * (w.weight[2] / (w.weight[2] + w.weight[3])) + \
                    data_NDVI["Iterative"][loc] * (w.weight[3] / (w.weight[2] + w.weight[3]))
            elif pd.isnull(data_NDVI["KNN"][loc]) and pd.notnull(data_NDVI["ewm"][loc]) and pd.isnull(data_NDVI["IDW"][loc]) and \
                    pd.notnull(data_NDVI["Iterative"][loc]):
                value_weight = data_NDVI["ewm"][loc] * (w.weight[1] / (w.weight[1] + w.weight[3])) + \
                    data_NDVI["Iterative"][loc] * (w.weight[3] / (w.weight[1] + w.weight[3]))
            elif pd.isnull(data_NDVI["KNN"][loc]) and pd.notnull(data_NDVI["ewm"][loc]) and pd.notnull(data_NDVI["IDW"][loc]) and \
                    pd.isnull(data_NDVI["Iterative"][loc]):
                value_weight = data_NDVI["ewm"][loc] * (w.weight[1] / (w.weight[1] + w.weight[2])) + \
                    data_NDVI["IDW"][loc] * (w.weight[2] / (w.weight[1] + w.weight[2]))
            elif pd.notnull(data_NDVI["KNN"][loc]) and pd.isnull(data_NDVI["ewm"][loc]) and pd.isnull(data_NDVI["IDW"][loc]) and \
                    pd.notnull(data_NDVI["Iterative"][loc]):
                value_weight = data_NDVI["KNN"][loc] * (w.weight[0] / (w.weight[0] + w.weight[3])) + \
                    data_NDVI["Iterative"][loc] * (w.weight[3] / (w.weight[0] + w.weight[3]))
            elif pd.notnull(data_NDVI["KNN"][loc]) and pd.isnull(data_NDVI["ewm"][loc]) and pd.notnull(data_NDVI["IDW"][loc]) and \
                    pd.isnull(data_NDVI["Iterative"][loc]):
                value_weight = data_NDVI["KNN"][loc] * (w.weight[0] / (w.weight[0] + w.weight[2])) + \
                    data_NDVI["IDW"][loc] * (w.weight[2] / (w.weight[0] + w.weight[2]))
            elif pd.notnull(data_NDVI["KNN"][loc]) and pd.notnull(data_NDVI["ewm"][loc]) and pd.isnull(data_NDVI["IDW"][loc]) and \
                    pd.isnull(data_NDVI["Iterative"][loc]):
                value_weight = data_NDVI["KNN"][loc] * (w.weight[0] / (w.weight[0] + w.weight[1])) + \
                    data_NDVI["IDW"][loc] * (w.weight[1] / (w.weight[0] + w.weight[1]))
            # 三种缺失
            elif pd.notnull(data_NDVI["KNN"][loc]) and pd.isnull(data_NDVI["ewm"][loc]) and pd.isnull(data_NDVI["IDW"][loc]) and \
                    pd.isnull(data_NDVI["Iterative"][loc]):
                value_weight = data_NDVI["KNN"][loc] * w.weight[0]
            elif pd.isnull(data_NDVI["KNN"][loc]) and pd.notnull(data_NDVI["ewm"][loc]) and pd.isnull(data_NDVI["IDW"][loc]) and \
                    pd.isnull(data_NDVI["Iterative"][loc]):
                value_weight = data_NDVI["ewm"][loc] * w.weight[1]
            elif pd.isnull(data_NDVI["KNN"][loc]) and pd.isnull(data_NDVI["ewm"][loc]) and pd.notnull(data_NDVI["IDW"][loc]) and \
                    pd.isnull(data_NDVI["Iterative"][loc]):
                value_weight = data_NDVI["IDW"][loc] * w.weight[2]
            elif pd.isnull(data_NDVI["KNN"][loc]) and pd.isnull(data_NDVI["ewm"][loc]) and pd.isnull(data_NDVI["IDW"][loc]) and \
                    pd.notnull(data_NDVI["Iterative"][loc]):
                value_weight = data_NDVI["Iterative"][loc] * w.weight[3]
            else:
                value_weight = np.nan
            value_weight_list.append(value_weight)
            # print(value_weight)
        value_weight_list = pd.DataFrame(value_weight_list)
        value_weight_list = value_weight_list.set_index(data_NDVI.index)
        value_weight_list.columns = ["NDVI_%s" % area_numb]
        connect_data = pd.merge(
            data_NDVI,
            value_weight_list,
            left_index=True,
            right_index=True)
        connect_data = connect_data.drop(
            columns=["KNN", "ewm", "IDW", "Iterative"])
        res.append(connect_data)

    if len(res) > 0:
        res_data = pd.concat(res, sort=False, axis=1)
        for cname in ['NDVI_0']:
            if cname not in res_data.columns:
                res_data[cname] = np.nan
        res_data = res_data.fillna(0.00)
        res_data.to_excel(res_output_path + input_file_name)
        # print("已输出:" + "%s" % input_file_name)
