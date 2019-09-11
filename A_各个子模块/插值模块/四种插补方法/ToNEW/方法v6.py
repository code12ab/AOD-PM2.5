# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/9/11 11:18


"""
KNN可以和IDW合并
"""

# 库
from multiprocessing import Process  # 多线程,提高CPU利用率
import copy
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import numpy as np
from fancyimpute import KNN, IterativeImputer  # 方法创建新的数据框,不覆盖原始数据
import os,time
import numba
# 路径
input_file_path_pollution = "D:\\毕业论文程序\\气溶胶光学厚度\\插值模块\\Mean\\2018\\"
merge_output_file_path = "D:\\毕业论文程序\\气溶胶光学厚度\\插值模块\\Merge\\Aqua\\2018\\"
# 监测点坐标
JCZ_info = pd.read_excel("D:\\毕业论文程序\\MODIS\\坐标\\监测站坐标.xlsx", sheet_name="汇总")  # 152个
JCZ_info["监测站"] = JCZ_info["城市"] + "-" + JCZ_info["监测点名称"]
# 已经输出
saved_list = os.listdir(merge_output_file_path)


def get4method(xx152):
    # 地理距离
    def geo_distance(lng1_df, lat1_df, lng2_df, lat2_df):
        lng1_df, lat1_df, lng2_df, lat2_df = map(radians, [lng1_df, lat1_df, lng2_df, lat2_df])
        d_lon = lng2_df - lng1_df
        d_lat = lat2_df - lat1_df
        a = sin(d_lat / 2) ** 2 + cos(lat1_df) * cos(lat2_df) * sin(d_lon / 2) ** 2
        dis = 2 * asin(sqrt(a)) * 6371.393 * 1000  # 地球半径
        return dis  # 输出结果的单位为“米”

    # 监测站
    jcz_152 = pd.read_excel("D:\\毕业论文程序\\MODIS\\坐标\\站点列表-2018.11.08起_152.xlsx", sheet_name=xx152)
    jcz_152["监测站名称_152"] = jcz_152["城市"] + "-" + jcz_152["监测点名称"]
    for input_file_name in jcz_152["监测站名称_152"]:
        input_file_name = input_file_name + ".xlsx"
        if input_file_name in saved_list:
            print("已经完成:", input_file_name, xx152)
            # continue
        print("========正在计算%s========" % input_file_name)
        # 读取数据源
        data_pollution = pd.read_excel(input_file_path_pollution + input_file_name)
        data_pollution = data_pollution.set_index('日期')

        # 定义经纬度
        data_pollution_to_IDW = copy.deepcopy(data_pollution)
        name = str(input_file_name).replace(".xlsx", "")  # 定义相关变量
        lng1 = JCZ_info[JCZ_info["监测站"] == name]["经度"]
        lat1 = JCZ_info[JCZ_info["监测站"] == name]["纬度"]
        # 局部
        # 最近邻KNN,是使用K行都具有全部特征的样本,使用其他特征的均方差进行加权,判断最接近的时间点.
        merge_list2 = []  # 同一监测站,不同污染物
        for pol in data_pollution.columns:
            data_knn_raw = copy.deepcopy(data_pollution[[pol]])
            data_knn_raw = data_knn_raw.reset_index()
            numb1 = 0
            weight_list = []
            null_idx = data_pollution[pol][data_pollution[pol].isnull().values == True].index.tolist()
            list_idw_out2 = []
            for item_idw in JCZ_info["监测站"]:  # 获取距离,定义权重
                if item_idw != name:
                    lng2 = JCZ_info[JCZ_info["监测站"] == item_idw]["经度"]
                    lat2 = JCZ_info[JCZ_info["监测站"] == item_idw]["纬度"]
                    dis_1 = geo_distance(lng1, lat1, lng2, lat2)  # 两站地理距离
                    if dis_1 <= 200000:
                        data_knnadd = pd.read_excel(input_file_path_pollution+item_idw+'.xlsx')
                        data_knnadd = data_knnadd[[pol, '日期']]
                        data_knnadd.columns = [pol + "add_%s" % numb1, '日期']
                        if data_knnadd[pol + "add_%s" % numb1].sum() == 0:
                            continue
                        else:
                            weight_list.append((1 / dis_1))
                            data_knn_raw = pd.merge(data_knn_raw, data_knnadd, how='left', on='日期')
                            data_knnadd = data_knnadd.set_index('日期')  # 为了下一行

                            list_idw_out1 = [(1 / dis_1) * data_knnadd[pol + "add_%s" % numb1][j] for j in null_idx]
                            list_idw_out2.append(list_idw_out1)  # 给列表 添加： 距离*观测
                numb1 += 1
            list_idw_out3 = np.array(list_idw_out2)
            arrar01 = np.array([j/j for j in list_idw_out3])  # nan 1 矩阵
            list_nan = np.isnan(arrar01)
            arrar01[list_nan] = 0  # 0 1 矩阵
            arrayw = arrar01.T * weight_list  # 0 1 权重列表
            arrayw = arrayw.sum(1)
            list_idw_out3[np.isnan(list_idw_out3)] = 0  # 距离 * 数据 矩阵 替换nan为0
            idw_output1 = list_idw_out3.T.sum(1)
            idw_output2 = idw_output1 / arrayw  # idw结果
            idw_output2 = pd.DataFrame(idw_output2, index= null_idx, columns=[pol])
            data_pollution_to_IDW[pol][data_pollution[pol].isnull()] = idw_output2[pol]  # 插入
            # KNN计算部分
            data_knn_raw = data_knn_raw.set_index('日期')
            if pol+'add_0' in data_knn_raw.columns:
                print('============================================')
                data_pollution_KNN = KNN(k=30).fit_transform(data_knn_raw)
                data_pollution_KNN = pd.DataFrame(data_pollution_KNN)
                data_pollution_KNN.columns = data_knn_raw.columns
            else:
                data_pollution_KNN = copy.deepcopy(data_knn_raw)
            for numb_del2 in data_pollution_KNN.columns:
                if 'add' in numb_del2:
                    del data_pollution_KNN[numb_del2]
            merge_list2.append(data_pollution_KNN)
        data_darksky_weather_KNN_1 = pd.concat(merge_list2, axis=1, sort=True)

get4method('样例1')
