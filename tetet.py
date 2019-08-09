# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/9 1:26


# 库
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import numpy as np
from fancyimpute import KNN, IterativeImputer
import os
# 路径
def geo_distance(lng1, lat1, lng2, lat2):
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    d_lon = lng2 - lng1
    d_lat = lat2 - lat1
    a = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
    dis = 2 * asin(sqrt(a)) * 6371.393 * 1000  # 地球半径
    return dis  # 输出结果的单位为“米”


input_file_path_pollution = "D: \\毕业论文程序\\污染物浓度\\整理\\全部污染物\\"
merge_output_file_path = "D:\\毕业论文程序\\气象数据\\插值模块\\Merge\\2018\\"
mean_output_file_path = "D:\\毕业论文程序\\气象数据\\插值模块\\Mean\\2018\\"
xytodis = pd.read_excel("D:\\毕业论文程序\\气溶胶光学厚度\\插值模块\\xytodis.xlsx")  # 17个区域的投影坐标

JCZ_info = pd.read_excel("D:\\毕业论文程序\\MODIS\\坐标\\监测站坐标.xlsx", sheet_name="汇总")
JCZ_info["监测站"] = JCZ_info["城市"]+"-"+JCZ_info["监测点名称"]
input_file_names = os.listdir(input_file_path_pollution)  # 文件名列表, **.xlsx

for input_file_name in input_file_names:
    # 读取
    data_pollution = pd.read_excel(input_file_path_pollution + input_file_name)
    # 获取监测站名
    name = str(input_file_name).replace(".xlsx", "")
    # 删除字符串,便于计算
    del data_pollution["监测站"]

    data_pollution = data_pollution.set_index('日期')

    def get_IDW(input_data):
        for pollution in ["PM25", "PM10", "SO2", "NO2", "O3", "CO"]:
            data_1 = input_data[pollution]
            # for count_1 in range(len(input_data.index)):
            for indx in input_data.index:
                res_list= []
                weight_list = []
                # if pd.isnull(data_1.iloc[count_1][pollution]):
                if pd.isnull(data_1[pollution][indx]):
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
                                res = (dis_1/weight_sum) * data_to_add_in[pollution][indx]
                                res_list.append(res)
                    res_output = np.sum(np.array(res_list))
                    try:
                        data_1[pollution][indx] = res_output
                    except Exception as e:
                        print("缺失严重, 插值未定义:", e)
    get_IDW(data_pollution)