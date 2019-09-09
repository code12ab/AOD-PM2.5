# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/7 11:10

'''
bug
'''
# 库
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import numpy as np
from fancyimpute import KNN, IterativeImputer
import os
# 路径
# 地理距离公式
def geo_distance(lng1, lat1, lng2, lat2):
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    d_lon = lng2 - lng1
    d_lat = lat2 - lat1
    a = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
    dis = 2 * asin(sqrt(a)) * 6371.393 * 1000  # 地球半径
    return dis  # 输出结果的单位为“米”

input_file_path_pollution = "D:\\毕业论文程序\\污染物浓度\\整理\\全部污染物\\多年合一\\"
merge_output_file_path = "D:\\毕业论文程序\\污染物浓度\\插值模块\\Merge\\多年合一\\"


JCZ_info = pd.read_excel("D:\\毕业论文程序\\MODIS\\坐标\\监测站坐标.xlsx", sheet_name="汇总")
JCZ_info["监测站"] = JCZ_info["城市"]+"-"+JCZ_info["监测点名称"]
input_file_names = os.listdir(input_file_path_pollution)  # 文件名列表, **.xlsx

for input_file_name in input_file_names:
    # 读取
    KNN_list = []
    ewm_list = []
    IDW_list = []
    Iterative_list = []
    data_pollution = pd.read_excel(input_file_path_pollution + input_file_name)
    # 删除字符串,便于计算
    # del data_pollution["监测站"]
    data_pollution = data_pollution.set_index('日期')
# 时间局部：KNN
    # 最近邻估算，使用两行都具有观测数据的特征的均方差来对样本进行加权。然后用加权的结果进行特征值填充
    # 相当于A0D17个点为特征进行近邻,则参数K为时间,即时间上最近的7行按特征的均方差进行加权，即哪个时间点的权重大一些
    data_pollution_KNN = KNN(k=7).fit_transform(data_pollution)
    data_pollution_KNN = pd.DataFrame(data_pollution_KNN)  # 结果中有许多零值,应为空值

    # 时间全局: 平滑,常用于股市
    data_pollution_ewm_mid = pd.DataFrame.ewm(
        self=data_pollution,
        com=0.5,
        ignore_na=True,
        adjust=True).mean()
    data_pollution_ewm = data_pollution.copy()  # 区别于气溶胶插值方法
    for columname in data_pollution_ewm.columns:
        if data_pollution[columname].count() != len(data_pollution):
            loc = data_pollution[columname][data_pollution[columname].isnull().values == True].index.tolist()
            for nub in loc:
                data_pollution_ewm[columname][nub] = data_pollution_ewm_mid[columname][nub]
    for pollution in ["PM25", "PM10", "SO2", "NO2", "O3", "CO"]:


        # 空间局部: IDW
        name = str(input_file_name).replace(".xlsx", "")  # 定义相关变量

        def get_IDW(input_data):
            # data_1 = input_data[pollution]  # 单一某污染物列
            # for count_1 in range(len(input_data.index)):
            for indx in input_data.index:
                res_list = []
                weight_list = []
                # if pd.isnull(data_1.iloc[count_1][pollution]):
                if pd.isnull(input_data[pollution][indx]):
                    lng1 = JCZ_info[JCZ_info["监测站"] == name]["经度"]
                    lat1 = JCZ_info[JCZ_info["监测站"] == name]["纬度"]
                    for item in JCZ_info["监测站"]:
                        if item != name:
                            lng2 = JCZ_info[JCZ_info["监测站"] == item]["经度"]
                            lat2 = JCZ_info[JCZ_info["监测站"] == item]["纬度"]
                            dis_1 = geo_distance(lng1, lat1, lng2, lat2)  # 两站地理距离
                            if dis_1 < 50000:
                                weight_list.append(dis_1)
                    weight_sum = np.sum(np.array(weight_list))
                    for item in JCZ_info["监测站"]:
                        if item != name:
                            lng2 = JCZ_info[JCZ_info["监测站"] == item]["经度"]
                            lat2 = JCZ_info[JCZ_info["监测站"] == item]["纬度"]
                            dis_1 = geo_distance(lng1, lat1, lng2, lat2)  # 两站地理距离
                            if dis_1 < 50000:
                                data_to_add_in = pd.read_excel(input_file_path_pollution+item+".xlsx")
                                if indx in data_to_add_in.index:
                                    res = (dis_1/weight_sum) * data_to_add_in[pollution][indx]
                                    res_list.append(res)
                    res_output = np.sum(np.array(res_list))
                    try:
                        input_data[pollution][indx] = res_output
                    except Exception as e:
                        print("缺失严重, 插值未定义:", e)
            return input_data

        data_pollution_IDW = get_IDW(data_pollution.copy())

        # 空间全局: 迭代函数法,缺失特征作为y，其他特征作为x
        concat_list = []
        for item in JCZ_info["监测站"]:    # 不同于气溶胶插值方法
            if item != name:
                lng_1 = JCZ_info[JCZ_info["监测站"] == name]["经度"]
                lat_1 = JCZ_info[JCZ_info["监测站"] == name]["纬度"]
                lng_2 = JCZ_info[JCZ_info["监测站"] == item]["经度"]
                lat_2 = JCZ_info[JCZ_info["监测站"] == item]["纬度"]
                dis_2 = geo_distance(lng_1, lat_1, lng_2, lat_2)  # 两站地理距离
                if dis_2 < 50000:
                    data_to_add_in_to_Iterative = pd.read_excel(input_file_path_pollution + item + ".xlsx")
                    data_to_add_in_to_Iterative = data_to_add_in_to_Iterative.set_index("日期")
                    concat_list.append(data_to_add_in_to_Iterative[pollution])
        if len(concat_list) > 0:
            data_to_Iterative = pd.concat(concat_list, axis=1, sort=False)
            data_to_Iterative = pd.concat([data_pollution[pollution], data_to_Iterative], axis=1, sort=False)
        else:
            data_to_Iterative = data_pollution[pollution].copy()
        data_pollution_Iterative = IterativeImputer(max_iter=10).fit_transform(data_to_Iterative)
        data_pollution_Iterative = pd.DataFrame(data_pollution_Iterative)
        print(data_to_Iterative.columns)
        print(data_pollution.columns)
        # del data_pollution_Iterative

    # 对结果的0值取np.nan
    data_pollution_KNN.replace(0, np.nan, inplace=True)
    data_pollution_ewm.replace(0, np.nan, inplace=True)
    data_pollution_IDW.replace(0, np.nan, inplace=True)
    data_pollution_Iterative.replace(0, np.nan, inplace=True)

    # 合并相同方法的结果
    data_pollution_KNN = data_pollution_KNN.set_index(data_pollution.index)
    data_pollution_KNN.columns = data_pollution.columns
    # data_pollution_KNN["日期合并用"] = data_pollution_KNN.index
    data_pollution_ewm = data_pollution_ewm.set_index(data_pollution.index)
    data_pollution_ewm.columns = data_pollution.columns
    # data_pollution_ewm["日期合并用"] = data_pollution_ewm.index
    data_pollution_IDW = data_pollution_IDW.set_index(data_pollution.index)
    data_pollution_IDW.columns = data_pollution.columns
    # data_pollution_IDW["日期合并用"] = data_pollution_IDW.index
    data_pollution_Iterative = data_pollution_Iterative.set_index(data_pollution.index)
    data_pollution_Iterative.columns = data_pollution.columns
    # data_pollution_Iterative["日期合并用"] = data_pollution_Iterative.index

    #KNN_list.append(data_pollution_KNN)
    #ewm_list.append(data_pollution_ewm)
    IDW_list.append(data_pollution_IDW)
    Iterative_list.append(data_pollution_Iterative)

    data_pollution_IDW_save = pd.concat(IDW_list, axis=1, sort=False)
    #data_pollution_KNN_save = pd.concat(KNN_list, axis=1, sort=False)
    #data_pollution_ewm_save = pd.concat(ewm_list, axis=1, sort=False)
    data_pollution_Iterative_save = pd.concat(Iterative_list, axis=1, sort=False)
    # 合并不同方法为一个文件
    sheet_name = ["KNN", "ewm", "IDW", "Iterative"]
    sheet_name_count = 0  # 为什么显示without usage ?  因为: 上面如果if为false则..
    writer = pd.ExcelWriter(merge_output_file_path+'%s.xlsx' % (input_file_name.replace(".xlsx", "")))
    for methods_output in [data_pollution_KNN, data_pollution_ewm, data_pollution_IDW_save, data_pollution_Iterative_save]:
        methods_output.to_excel(writer, sheet_name=sheet_name[sheet_name_count])
        sheet_name_count = 1 + sheet_name_count
    writer.save()
