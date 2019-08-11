# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/7 11:10


# 库
import copy
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import numpy as np
from fancyimpute import KNN, IterativeImputer
import os


# 地理距离公式
def geo_distance(lng1_df, lat1_df, lng2_df, lat2_df):
    lng1_df, lat1_df, lng2_df, lat2_df = map(radians, [lng1_df, lat1_df, lng2_df, lat2_df])
    d_lon = lng2_df - lng1_df
    d_lat = lat2_df - lat1_df
    a = sin(d_lat / 2) ** 2 + cos(lat1_df) * cos(lat2_df) * sin(d_lon / 2) ** 2
    dis = 2 * asin(sqrt(a)) * 6371.393 * 1000  # 地球半径
    return dis  # 输出结果的单位为“米”


# 路径
input_file_path_pollution = "D:\\毕业论文程序\\污染物浓度\\整理\\全部污染物\\多年合一\\"
merge_output_file_path = "D:\\毕业论文程序\\污染物浓度\\插值模块\\Merge\\多年合一\\"
JCZ_info = pd.read_excel("D:\\毕业论文程序\\MODIS\\坐标\\监测站坐标.xlsx", sheet_name="汇总")
JCZ_info["监测站"] = JCZ_info["城市"] + "-" + JCZ_info["监测点名称"]
input_file_names = os.listdir(input_file_path_pollution)  # 文件名列表, **.xlsx

for input_file_name in input_file_names:
    # 读取数据源
    data_pollution = pd.read_excel(input_file_path_pollution + input_file_name)
    data_pollution = data_pollution.set_index('日期')
    # del data_pollution["监测站"]  # 删除字符串,便于计算


    data_pollution_to_IDW = copy.deepcopy(data_pollution)
    name = str(input_file_name).replace(".xlsx", "")  # 定义相关变量
    lng1 = JCZ_info[JCZ_info["监测站"] == name]["经度"]
    lat1 = JCZ_info[JCZ_info["监测站"] == name]["纬度"]


    merge_list = []
    for pollution_Iterative in ["PM25", "PM10", "SO2", "NO2", "O3", "CO"]:
        concat_list = []
        numb = 0
        for item in JCZ_info["监测站"]:  # 不同于气溶胶插值方法
            if item != name:
                lng_2 = JCZ_info[JCZ_info["监测站"] == item]["经度"]
                lat_2 = JCZ_info[JCZ_info["监测站"] == item]["纬度"]
                dis_2 = geo_distance(lng1, lat1, lng_2, lat_2)  # 两站地理距离
                if dis_2 <= 50000:  # 合并距离内的临近监测站
                    data_to_add_in_to_Iterative = pd.read_excel(input_file_path_pollution + item + ".xlsx")
                    data_to_add_in_to_Iterative = data_to_add_in_to_Iterative.set_index("日期")
                    data_to_Iterative_concat = data_to_add_in_to_Iterative[pollution_Iterative]
                    data_to_Iterative_concat = pd.DataFrame(data_to_Iterative_concat)
                    data_to_Iterative_concat.columns = [pollution_Iterative + "_add%s" % numb]
                    concat_list.append(data_to_Iterative_concat)
                    numb += 1
        if len(concat_list) > 0:  # 合并本身与临近
            data_to_Iterative = pd.concat(concat_list, axis=1, sort=False)
            data_to_Iterative = pd.concat([data_pollution[pollution_Iterative], data_to_Iterative], axis=1, sort=False)
        else:
            data_to_Iterative = data_pollution[pollution_Iterative].copy()
            data_to_Iterative = pd.DataFrame(data_to_Iterative)
            data_to_Iterative.columns = [pollution_Iterative]   # 本身
        data_pollution_Iterative_to_merge = IterativeImputer(max_iter=10).fit_transform(data_to_Iterative)
        data_pollution_Iterative_to_merge = pd.DataFrame(data_pollution_Iterative_to_merge)
        data_pollution_Iterative_to_merge = data_pollution_Iterative_to_merge.set_index(data_to_Iterative.index)
        data_pollution_Iterative_to_merge.columns = data_to_Iterative.columns
        print(data_pollution_Iterative_to_merge)
        for numb_del in range(numb):
            del data_pollution_Iterative_to_merge[pollution_Iterative + "_add%s" % numb_del]
            print("删除")
        merge_list.append(data_pollution_Iterative_to_merge)
        #print(merge_list)
    data_pollution_Iterative = pd.concat(merge_list, axis=1, sort=False)
    #print(data_pollution_Iterative)    # 只有一列CO

    data_pollution_Iterative.replace(0, np.nan, inplace=True)

    # 合并相同方法的结果

    data_pollution_Iterative = data_pollution_Iterative.set_index(data_pollution.index)
    data_pollution_Iterative.columns = data_pollution.columns

