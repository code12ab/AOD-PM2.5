# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2020/3/10 11:10


# 库
import pandas as pd

import numpy as np
from fancyimpute import KNN, IterativeImputer
import os
# 输入端路径
input_file_path = "D:\\毕业论文程序\\NDVI\\空间转换模块\\Terra插补效率\\"
xytodis = pd.read_excel("D:\\毕业论文程序\\NDVI\\插值模块\\xytodis.xlsx")  # 17个区域的投影坐标
# 输出端
merge_output_file_path = "D:\\毕业论文程序\\NDVI\\插值模块\\Merge\\2018插补效率\\"
null_output_path = "D:\\毕业论文程序\\NDVI\\插值模块\\制造的缺失值\\"


input_file_names = os.listdir(input_file_path)  # 文件名列表
# 空间局部公式: 不存在插值为1*nan=nan的插值结果;只存在nan*nan=nan -> 因为使用的插值数据已经筛选为'>0'的部分.
def get_IDW(input_data):
    list_to_concat = []
    for count in range(len(input_data.index)):
        data_to_add = pd.DataFrame(list(input_data.iloc[count]))  # 把某一行 转换成 列表 从而把行转化成 df中的列,不会修改原数据
        data_to_dis = pd.concat([data_to_add, xytodis], axis=1)  # 坐标和某一行合并
        # 这里使用简单合并的原因: 每行格式都是一致的,AOD0-16完美对应xytodis
        # print(data_to_dis, input_data.iloc[count], "================================", sep="\n")
        data_to_dis.columns = ["value", "index", "longitude", "latitude"]
        # 对这一行进行操作 对每一行输出一下
        for count_2 in range(len(data_to_dis["value"])):
            res_list = []
            weight_list = []
            if pd.isnull(data_to_dis.iloc[count_2]['value']):
                data_to_weight = data_to_dis[data_to_dis["value"] > 0]
                if len(data_to_weight["value"]) > 0:
                    # 先求权重
                    for item in range(len(data_to_weight["value"])):
                        dx = 1 * (data_to_weight.iloc[item]["longitude"] -
                                  data_to_dis.iloc[count_2]['longitude'])
                        dy = 1 * (data_to_weight.iloc[item]["latitude"] -
                                  data_to_dis.iloc[count_2]['latitude'])
                        weight_dis = 1 / ((dx * dx + dy * dy) ** 0.5)
                        # weight = inf ?
                        weight_list.append(weight_dis)
                    weight_sum = np.sum(np.array(weight_list))
                    # 计算结果
                    for item in range(len(data_to_weight["value"])):
                        dx = 1 * (data_to_weight.iloc[item]["longitude"] -
                                  data_to_dis.iloc[count_2]['longitude'])
                        dy = 1 * (data_to_weight.iloc[item]["latitude"] -
                                  data_to_dis.iloc[count_2]['latitude'])
                        weight_dis = 1 / ((dx * dx + dy * dy) ** 0.5)
                        res = (weight_dis/weight_sum) * data_to_weight.iloc[item]["value"]
                        res_list.append(res)
                    res_output = np.sum(np.array(res_list))  # 插补的数值
                    try:
                        data_to_dis.loc[count_2, 'value'] = res_output  # 进行插补
                    except Exception as e:
                        print("缺失严重, 插值未定义:", e)
        data_to_dis = data_to_dis.drop(["latitude", "longitude"], axis=1)   # 删除无用列
        data_to_dis = data_to_dis.drop(["index"], axis=1)
        list_to_concat.append(data_to_dis.T)  # 添加,行转化为列,合并中最终数据.
    data_last = pd.concat(list_to_concat)
    return data_last


import random

for input_file_name in input_file_names:
    print("========正在计算%s========" % input_file_name)
    # 读取
    data_input = pd.read_excel(input_file_path + input_file_name)
    # 删除字符串,便于计算
    # del data_input["监测站"]  # ndvi中没有。
    data_input = data_input.set_index('日期')

    # 处理AQUA，制造 缺失值
    saveA = list()
    for columname in data_input.columns:
        if columname != "日期":
            if columname != "监测站":
                # loc 是某列为空的行坐标
                loc = data_input[columname][data_input[columname].isnull().values == False].index.tolist()
                # 筛选个数
                c1 = int(len(loc) * 0.25)
                # 筛选出样本
                slice1 = random.sample(loc, c1)
                # print(data_input[columname][0])
                # print(slice1)
                # 保存 变空之前 的 变量位置和数值
                exec('save_a_%s = list()' % columname)
                for nub in slice1:
                    # print(data_input[columname][nub])
                    # print((columname, nub, data_input[columname][nub]))
                    exec('save_a_%s.append((columname, nub, data_input[columname][nub]))' % columname)
                    # exec("JCZ.append(JCZ%s)" % i)
                    # 下一行，修改成缺失值
                    data_input[columname][nub] = np.nan
                    # print(data_input[columname][nub])
                exec('saveA.append(save_a_%s)' % columname)
    
    # 保存编号
    sA = pd.DataFrame(saveA)  # A没意义了 懒得继续改了
    sA.to_excel(null_output_path + "%s" % input_file_name)

    # 时间局部：KNN
    # 最近邻估算，使用两行都具有观测数据的特征的均方差来对样本进行加权。然后用加权的结果进行特征值填充
    # 相当于A0D17个点为特征进行近邻,则参数K为时间,即时间上最近的16行按特征的均方差进行加权，即哪个时间点的权重大一些
    data_input_KNN = KNN(k=7).fit_transform(data_input)
    data_input_KNN = pd.DataFrame(data_input_KNN)  # 结果中有许多零值,应为空值

    # 时间全局: 平滑,常用于股市
    data_input_ewm = pd.DataFrame.ewm(
        self=data_input,
        com=0.8,
        ignore_na=False,
        adjust=True).mean()  # 参数设置不同

    # 空间局部: IDW
    data_input_IDW = get_IDW(data_input)

    # 空间全局: 迭代函数法,缺失特征作为y，其他特征作为x
    data_input_Iterative = IterativeImputer(
        max_iter=10).fit_transform(data_input)
    data_input_Iterative = pd.DataFrame(data_input_Iterative)

    # 对结果的0值取np.nan
    data_input_KNN.replace(0, np.nan, inplace=True)
    data_input_ewm.replace(0, np.nan, inplace=True)
    data_input_IDW.replace(0, np.nan, inplace=True)
    data_input_Iterative.replace(0, np.nan, inplace=True)

    # 合并相同方法的结果
    data_input_KNN = data_input_KNN.set_index(data_input.index)
    data_input_KNN.columns = data_input.columns
    data_input_KNN["日期合并用"] = data_input_KNN.index
    data_input_ewm = data_input_ewm.set_index(data_input.index)
    data_input_ewm.columns = data_input.columns
    data_input_ewm["日期合并用"] = data_input_ewm.index
    data_input_IDW = data_input_IDW.set_index(data_input.index)
    data_input_IDW.columns = data_input.columns
    data_input_IDW["日期合并用"] = data_input_IDW.index
    data_input_Iterative = data_input_Iterative.set_index(data_input.index)
    data_input_Iterative.columns = data_input.columns
    data_input_Iterative["日期合并用"] = data_input_Iterative.index

    # 合并不同方法下的A/T为一个文件
    sheet_name = ["KNN", "ewm", "IDW", "Iterative"]
    sheet_name_count = 0  # 为什么显示without usage ?  因为下面如果if为false则..
    writer = pd.ExcelWriter(merge_output_file_path+'%s.xlsx' % (input_file_name.replace(".xlsx", "")))
    for methods_output in [data_input_KNN, data_input_ewm, data_input_IDW, data_input_Iterative]:
        methods_output.to_excel(writer, sheet_name=sheet_name[sheet_name_count])
        sheet_name_count = 1 + sheet_name_count
    writer.save()



