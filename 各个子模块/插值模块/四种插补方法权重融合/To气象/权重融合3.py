# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/9/12 11:11

# 库
import pandas as pd
import numpy as np
import math
import os
from sklearn.preprocessing import MinMaxScaler
min_max_sacler = MinMaxScaler()

for year in [2008,2009,2010,2011,2012,2013,2014,2015,2016,2017]:
    input_file_path = "D:\\毕业论文程序\\气象数据\\插值模块\\Merge\\%s\\" % year
    res_output_path = "D:\\毕业论文程序\\气象数据\\插值模块\\Res\\%s\\" % year
    file_list = os.listdir(input_file_path)
    for input_file in file_list:
        data_KNN = pd.read_excel(
            input_file_path +
            input_file,
            sheet_name="KNN",
            index_col='日期')
        data_ewm = pd.read_excel(
            input_file_path +
            input_file,
            sheet_name="ewm",
            index_col='日期')
        data_IDW = pd.read_excel(
            input_file_path +
            input_file,
            sheet_name="IDW",
            index_col='日期')
        data_Iterative = pd.read_excel(
            input_file_path +
            input_file,
            sheet_name="Iterative",
            index_col='日期')
        # 每个监测站
        res = []
        for col in data_Iterative.columns:
            w_list = []
            data_concat = pd.concat([data_KNN[[col]], data_ewm[[col]], data_IDW[[
                                    col]], data_Iterative[[col]]], axis=1)
            """
            data_concat.columns = ['KNN_%s' % col,
                                   'ewm_%s' % col,
                                   'IDW_%s' % col,
                                   'Iterative_%s' % col]
            """
            data_concat.columns = ['KNN',
                                   'ewm',
                                   'IDW',
                                   'Iterative']
            # 权重部分
            KNN_std = pd.DataFrame(min_max_sacler.fit_transform(data_KNN[[col]]))
            KNN_std = KNN_std.set_index(data_KNN.index)
            KNN_std.columns = [col]
            KNN_sum = KNN_std[KNN_std[col] > 0].sum()
            KNN_n = len(KNN_std[KNN_std[col] >= 0])
            KNN_pi1 = KNN_std[KNN_std[col] > 0][col].map(lambda x: (
                x / KNN_sum) * math.log((x / KNN_sum), math.e)).sum()
            if KNN_n > 0:
                KNN_e = KNN_pi1 * (-1) * math.log((1 / (KNN_n)), math.e)
                KNN_e = float(KNN_e)
            else:
                KNN_e = 0

            ewm_std = pd.DataFrame(min_max_sacler.fit_transform(data_ewm[[col]]))
            ewm_std = ewm_std.set_index(data_ewm.index)
            ewm_std.columns = [col]
            ewm_sum = ewm_std[ewm_std[col] > 0].sum()
            ewm_n = len(ewm_std[ewm_std[col] >= 0])
            ewm_pi1 = ewm_std[ewm_std[col] > 0][col].map(lambda x: (
                x / ewm_sum) * math.log((x / ewm_sum), math.e)).sum()
            if ewm_n > 0:
                ewm_e = ewm_pi1 * (-1) * math.log((1 / (ewm_n)), math.e)
                ewm_e = float(ewm_e)
            else:
                ewm_e = 0

            IDW_std = pd.DataFrame(min_max_sacler.fit_transform(data_IDW[[col]]))
            IDW_std = IDW_std.set_index(data_IDW.index)
            IDW_std.columns = [col]
            IDW_sum = IDW_std[IDW_std[col] > 0].sum()
            IDW_n = len(IDW_std[IDW_std[col] >= 0])
            IDW_pi1 = IDW_std[IDW_std[col] > 0][col].map(lambda x: (
                x / IDW_sum) * math.log((x / IDW_sum), math.e)).sum()
            if IDW_n > 0:
                IDW_e = IDW_pi1 * (-1) * math.log((1 / (IDW_n)), math.e)
                IDW_e = float(IDW_e)
            else:
                IDW_e = 0

            Iterative_std = pd.DataFrame(
                min_max_sacler.fit_transform(data_Iterative[[col]]))
            Iterative_std = Iterative_std.set_index(data_Iterative.index)
            Iterative_std.columns = [col]
            Iterative_sum = Iterative_std[Iterative_std[col] > 0].sum()
            Iterative_n = len(Iterative_std[Iterative_std[col] >= 0])
            Iterative_pi1 = Iterative_std[Iterative_std[col] > 0][col].map(
                lambda x: (x / Iterative_sum) * math.log((x / Iterative_sum), math.e)).sum()
            if Iterative_n > 0:
                Iterative_e = Iterative_pi1 * \
                    (-1) * math.log((1 / (Iterative_n)), math.e)
                Iterative_e = float(Iterative_e)
            else:
                Iterative_e = 0
            # 添加
            w_sum = KNN_e + ewm_e + IDW_e + Iterative_e
            w1 = (1 - KNN_e) / (4 - w_sum)
            w2 = (1 - ewm_e) / (4 - w_sum)
            w3 = (1 - IDW_e) / (4 - w_sum)
            w4 = (1 - Iterative_e) / (4 - w_sum)
            w_list.append(w1)
            w_list.append(w2)
            w_list.append(w3)
            w_list.append(w4)
            print('权重总和', np.array(w_list).sum())
            value_weight_list = []
            for loc in range(len(data_concat.index)):
                # 四种方法均不缺失
                if pd.notnull(
                        data_concat["KNN"][loc]) and pd.notnull(
                        data_concat["ewm"][loc]) and pd.notnull(
                        data_concat["IDW"][loc]) and pd.notnull(
                        data_concat["Iterative"][loc]):
                    value_weight = data_concat["KNN"][loc] * w_list[0] + data_concat["ewm"][loc] * w_list[1] + \
                        data_concat["IDW"][loc] * w_list[2] + data_concat["Iterative"][loc] * w_list[3]
                # 某一种缺失
                elif pd.isnull(data_concat["KNN"][loc]) and pd.notnull(data_concat["ewm"][loc]) and pd.notnull(
                        data_concat["IDW"][loc]) and \
                        pd.notnull(data_concat["Iterative"][loc]):
                    value_weight = data_concat["ewm"][loc] * (w_list[1] / (w_list[1] + w_list[2] + w_list[3])) + \
                        data_concat["IDW"][loc] * (w_list[2] / (w_list[1] + w_list[2] + w_list[3])) + \
                        data_concat["Iterative"][loc] * (w_list[3] / (w_list[1] + w_list[2] + w_list[3]))
                elif pd.notnull(data_concat["KNN"][loc]) and pd.isnull(data_concat["ewm"][loc]) and pd.notnull(
                        data_concat["IDW"][loc]) and \
                        pd.notnull(data_concat["Iterative"][loc]):
                    value_weight = data_concat["KNN"][loc] * (w_list[0] / (w_list[0] + w_list[2] + w_list[3])) + \
                        data_concat["IDW"][loc] * (w_list[2] / (w_list[0] + w_list[2] + w_list[3])) + \
                        data_concat["Iterative"][loc] * (w_list[3] / (w_list[0] + w_list[2] + w_list[3]))
                elif pd.notnull(data_concat["KNN"][loc]) and pd.notnull(data_concat["ewm"][loc]) and pd.isnull(
                        data_concat["IDW"][loc]) and \
                        pd.notnull(data_concat["Iterative"][loc]):
                    value_weight = data_concat["KNN"][loc] * (
                        w_list[0] / (w_list[0] + w_list[1] + w_list[3])) + \
                        data_concat["ewm"][loc] * (
                        w_list[1] / (w_list[0] + w_list[1] + w_list[3])) + \
                        data_concat["Iterative"][loc] * (
                        w_list[3] / (w_list[0] + w_list[1] + w_list[3]))
                elif pd.notnull(data_concat["KNN"][loc]) and pd.notnull(data_concat["ewm"][loc]) and pd.notnull(
                        data_concat["IDW"][loc]) and \
                        pd.isnull(data_concat["Iterative"][loc]):
                    value_weight = data_concat["KNN"][loc] * (
                        w_list[0] / (w_list[0] + w_list[1] + w_list[2])) + \
                        data_concat["ewm"][loc] * (
                        w_list[1] / (w_list[0] + w_list[1] + w_list[2])) + \
                        data_concat["IDW"][loc] * (
                        w_list[2] / (w_list[0] + w_list[1] + w_list[2]))
                # 两种缺失
                elif pd.isnull(data_concat["KNN"][loc]) and pd.isnull(data_concat["ewm"][loc]) and pd.notnull(
                        data_concat["IDW"][loc]) and \
                        pd.notnull(data_concat["Iterative"][loc]):
                    value_weight = data_concat["IDW"][loc] * (w_list[2] / (w_list[2] + w_list[3])) + \
                        data_concat["Iterative"][loc] * (w_list[3] / (w_list[2] + w_list[3]))
                elif pd.isnull(data_concat["KNN"][loc]) and pd.notnull(data_concat["ewm"][loc]) and pd.isnull(
                        data_concat["IDW"][loc]) and \
                        pd.notnull(data_concat["Iterative"][loc]):
                    value_weight = data_concat["ewm"][loc] * (w_list[1] / (w_list[1] + w_list[3])) + \
                        data_concat["Iterative"][loc] * (w_list[3] / (w_list[1] + w_list[3]))
                elif pd.isnull(data_concat["KNN"][loc]) and pd.notnull(data_concat["ewm"][loc]) and pd.notnull(
                        data_concat["IDW"][loc]) and \
                        pd.isnull(data_concat["Iterative"][loc]):
                    value_weight = data_concat["ewm"][loc] * (w_list[1] / (w_list[1] + w_list[2])) + \
                        data_concat["IDW"][loc] * (w_list[2] / (w_list[1] + w_list[2]))
                elif pd.notnull(data_concat["KNN"][loc]) and pd.isnull(data_concat["ewm"][loc]) and pd.isnull(
                        data_concat["IDW"][loc]) and \
                        pd.notnull(data_concat["Iterative"][loc]):
                    value_weight = data_concat["KNN"][loc] * (w_list[0] / (w_list[0] + w_list[3])) + \
                        data_concat["Iterative"][loc] * (w_list[3] / (w_list[0] + w_list[3]))
                elif pd.notnull(data_concat["KNN"][loc]) and pd.isnull(data_concat["ewm"][loc]) and pd.notnull(
                        data_concat["IDW"][loc]) and \
                        pd.isnull(data_concat["Iterative"][loc]):
                    value_weight = data_concat["KNN"][loc] * (w_list[0] / (w_list[0] + w_list[2])) + \
                        data_concat["IDW"][loc] * (w_list[2] / (w_list[0] + w_list[2]))
                elif pd.notnull(data_concat["KNN"][loc]) and pd.notnull(data_concat["ewm"][loc]) and pd.isnull(
                        data_concat["IDW"][loc]) and \
                        pd.isnull(data_concat["Iterative"][loc]):
                    value_weight = data_concat["KNN"][loc] * (w_list[0] / (w_list[0] + w_list[1])) + \
                        data_concat["IDW"][loc] * (w_list[1] / (w_list[0] + w_list[1]))
                # 三种缺失
                elif pd.notnull(data_concat["KNN"][loc]) and pd.isnull(data_concat["ewm"][loc]) and pd.isnull(
                        data_concat["IDW"][loc]) and \
                        pd.isnull(data_concat["Iterative"][loc]):
                    value_weight = data_concat["KNN"][loc] * w_list[0]
                elif pd.isnull(data_concat["KNN"][loc]) and pd.notnull(data_concat["ewm"][loc]) and pd.isnull(
                        data_concat["IDW"][loc]) and \
                        pd.isnull(data_concat["Iterative"][loc]):
                    value_weight = data_concat["ewm"][loc] * w_list[1]
                elif pd.isnull(data_concat["KNN"][loc]) and pd.isnull(data_concat["ewm"][loc]) and pd.notnull(
                        data_concat["IDW"][loc]) and \
                        pd.isnull(data_concat["Iterative"][loc]):
                    value_weight = data_concat["IDW"][loc] * w_list[2]
                elif pd.isnull(data_concat["KNN"][loc]) and pd.isnull(data_concat["ewm"][loc]) and pd.isnull(
                        data_concat["IDW"][loc]) and \
                        pd.notnull(data_concat["Iterative"][loc]):
                    value_weight = data_concat["Iterative"][loc] * w_list[3]
                else:
                    value_weight = np.nan
                value_weight_list.append(value_weight)
            value_weight_list = pd.DataFrame(value_weight_list)
            value_weight_list = value_weight_list.set_index(data_concat.index)
            value_weight_list.columns = [col]
            connect_data = pd.merge(
                data_concat,
                value_weight_list,
                left_index=True,
                right_index=True)
            connect_data = connect_data.drop(
                columns=["KNN", "ewm", "IDW", "Iterative"])
            res.append(connect_data)

        if len(res) > 0:
            res_data = pd.concat(res, sort=False, axis=1)
            for cname in data_KNN.columns:
                if cname not in res_data.columns:
                    res_data[cname] = np.nan
            res_data = res_data.fillna(0.00)
            res_data.replace(0, np.nan, inplace=True)

            res_data.to_excel(res_output_path + input_file)
