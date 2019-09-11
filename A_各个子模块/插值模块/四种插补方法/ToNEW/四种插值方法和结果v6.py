# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/7 11:10

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
import os
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
            continue
        #  print("========正在计算%s========" % input_file_name)
        # 读取数据源
        data_pollution = pd.read_excel(input_file_path_pollution + input_file_name)
        data_pollution = data_pollution.set_index('日期')

        # 时间: 平滑,常用于股市;创建新的数据框,不会覆盖原始数据
        print('======%s:开始进行时间特性捕捉======' % input_file_name.replace('.xlsx', ''))
        data_pollution_ewm_mid = pd.DataFrame.ewm(
            self=data_pollution,
            com=0.5,
            ignore_na=True,
            adjust=True).mean()
        data_pollution_ewm = copy.deepcopy(data_pollution)  # 避免覆盖原始数据
        for columname in data_pollution_ewm.columns:
            if data_pollution[columname].count() != len(data_pollution):
                loc = data_pollution[columname][data_pollution[columname].isnull().values == True].index.tolist()
                for nub in loc:
                    data_pollution_ewm.loc[nub, columname] = data_pollution_ewm_mid.loc[nub, columname]

        print('[ewm]Finished')

        # 定义经纬度
        data_pollution_IDW = copy.deepcopy(data_pollution)
        name = str(input_file_name).replace(".xlsx", "")  # 定义相关变量
        lng1 = JCZ_info[JCZ_info["监测站"] == name]["经度"]
        lat1 = JCZ_info[JCZ_info["监测站"] == name]["纬度"]

        # 全局: 迭代回归,缺失特征作为y,其他特征作为x
        print('======%s:开始进行全局规律性捕捉======' % input_file_name.replace('.xlsx', ''))
        merge_list = []  # 同一监测站,不同污染物
        for darksky_weather_Iterative in data_pollution.columns:
            # 合并部分
            numb = 0
            data_darksky_weather_to_Iterative = copy.deepcopy(data_pollution[[darksky_weather_Iterative]])
            data_darksky_weather_to_Iterative = data_darksky_weather_to_Iterative.reset_index()
            if data_darksky_weather_to_Iterative[darksky_weather_Iterative].sum() == 0:
                data_darksky_weather_to_Iterative = data_darksky_weather_to_Iterative.set_index('日期')
                merge_list.append(data_darksky_weather_to_Iterative)
            else:
                # 如果 该特征不是全空,则合并
                for item in JCZ_info["监测站"]:  # 不同于气溶胶插值方法
                    if item != name:
                        # 添加的文件
                        data_to_add_in_to_Iterative = pd.read_excel(
                            input_file_path_pollution + item + ".xlsx")
                        # 添加的列名, 若要添加的列全空则跳过
                        if data_to_add_in_to_Iterative[darksky_weather_Iterative].sum() == 0:
                            continue
                        else:
                            data_to_Iterative_concat = data_to_add_in_to_Iterative[[darksky_weather_Iterative, '日期']]
                            data_to_Iterative_concat.columns = [darksky_weather_Iterative + "_add%s" % numb, '日期']  # 如果有五个临近, 则NDVI1-NDVI5
                            data_darksky_weather_to_Iterative = pd.merge(data_darksky_weather_to_Iterative,
                                                                        data_to_Iterative_concat,
                                                                        how='left',
                                                                        on='日期')
                            numb += 1  # 添加了列则增加计数
                        data_darksky_weather_to_Iterative = data_darksky_weather_to_Iterative.set_index('日期')
                # 迭代部分
                if numb >= 1:  # 至少两个非空列才可以计算
                    data_darksky_weather_Iterative_to_merge = IterativeImputer(
                        max_iter=30).fit_transform(data_darksky_weather_to_Iterative)
                    data_darksky_weather_Iterative_to_merge = pd.DataFrame(
                        data_darksky_weather_Iterative_to_merge, columns=data_darksky_weather_to_Iterative.columns)  # 格式转换
                    data_darksky_weather_Iterative_to_merge = data_darksky_weather_Iterative_to_merge.set_index(
                        data_darksky_weather_to_Iterative.index)  # ok
                else:
                    data_darksky_weather_Iterative_to_merge = copy.deepcopy(data_darksky_weather_to_Iterative)
                for numb_del in data_darksky_weather_Iterative_to_merge.columns:
                    if 'add' in numb_del:
                        del data_darksky_weather_Iterative_to_merge[numb_del]  # 至此, 只剩下一列特征列
            # 插补后的该监测点的气象特征列, 仅一列, 循环添加其他特征
                merge_list.append(data_darksky_weather_Iterative_to_merge)
        data_darksky_weather_Iterative_1 = pd.concat(merge_list, axis=1, sort=False)
        print('[Iterative]Finished')

        # 局部 + 空间
        # 最近邻KNN,是使用K行都具有全部特征的样本,使用其他特征的均方差进行加权,判断最接近的时间点.
        print('======%s:开始进行空间特性和局部相关性捕捉======' % input_file_name.replace('.xlsx', ''))
        merge_list2 = []  # 同一监测站,不同污染物
        for pol in data_pollution_IDW.columns:
            data_knn_raw = copy.deepcopy(data_pollution_IDW[[pol]])
            data_knn_raw = data_knn_raw.reset_index()
            numb1 = 0
            weight_list = []
            null_idx = data_pollution_IDW[pol][data_pollution_IDW[pol].isnull().values == True].index.tolist()
            list_idw_out2 = []
            for item_idw in JCZ_info["监测站"]:  # 获取距离,定义权重
                if item_idw != name:
                    lng2 = JCZ_info[JCZ_info["监测站"] == item_idw]["经度"]
                    lat2 = JCZ_info[JCZ_info["监测站"] == item_idw]["纬度"]
                    dis_1 = geo_distance(lng1, lat1, lng2, lat2)  # 两站地理距离
                    if dis_1 <= 200000:
                        data_knnadd = pd.read_excel(input_file_path_pollution + item_idw + '.xlsx')
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
            arrar01 = np.array([j / j for j in list_idw_out3])  # nan 1 矩阵
            list_nan = np.isnan(arrar01)
            arrar01[list_nan] = 0  # 0 1 矩阵
            arrayw = arrar01.T * weight_list  # 0 1 权重列表
            arrayw = arrayw.sum(1)
            list_idw_out3[np.isnan(list_idw_out3)] = 0  # 距离 * 数据 矩阵 替换nan为0
            idw_output1 = list_idw_out3.T.sum(1)
            idw_output2 = idw_output1 / arrayw  # idw结果
            idw_output2 = pd.DataFrame(idw_output2, index=null_idx, columns=[pol])
            data_pollution_IDW[pol][data_pollution_IDW[pol].isnull()] = idw_output2[pol]  # 插入

            # KNN计算部分
            data_knn_raw = data_knn_raw.set_index('日期')
            if pol + 'add_0' in data_knn_raw.columns:
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
        print('[IDW]Finished')

        # 对结果的0值取np.nan
        data_darksky_weather_KNN_1.replace(0, np.nan, inplace=True)
        data_pollution_ewm.replace(0, np.nan, inplace=True)
        data_pollution_IDW.replace(0, np.nan, inplace=True)
        data_darksky_weather_Iterative_1.replace(0, np.nan, inplace=True)

        # 合并相同方法的结果
        data_pollution_KNN = data_darksky_weather_KNN_1.set_index(data_pollution.index)
        data_pollution_KNN.columns = data_pollution.columns
        data_pollution_ewm = data_pollution_ewm.set_index(data_pollution.index)
        data_pollution_ewm.columns = data_pollution.columns
        data_pollution_IDW = data_pollution_IDW.set_index(data_pollution.index)
        data_pollution_IDW.columns = data_pollution.columns
        data_pollution_Iterative = data_darksky_weather_Iterative_1.set_index(data_pollution.index)
        data_pollution_Iterative.columns = data_pollution.columns

        # 合并不同方法为一个文件
        sheet_name = ["KNN", "ewm", "IDW", "Iterative"]
        sheet_name_count = 0
        writer = pd.ExcelWriter(merge_output_file_path + '%s.xlsx' % (input_file_name.replace(".xlsx", "")))
        for methods_output in [data_pollution_KNN, data_pollution_ewm, data_pollution_IDW, data_pollution_Iterative]:
            methods_output.to_excel(writer, sheet_name=sheet_name[sheet_name_count])
            sheet_name_count = 1 + sheet_name_count
        writer.save()


if __name__ == '__main__':
    print('=====主进程=====')

    p1 = Process(target=get4method, args=("样例1",))
    p2 = Process(target=get4method, args=('样例2',))
    p3 = Process(target=get4method, args=('样例3',))
    p4 = Process(target=get4method, args=('样例4',))
    #p5 = Process(target=get4method, args=('样例5',))
    #p6 = Process(target=get4method, args=('样例6',))

    p1.start()
    p2.start()
    p3.start()
    #p4.start()
    #p5.start()
    #p6.start()

    #p6.join()  # 依次检测是否完成, 完成才会执行join下面的代码
    #p5.join()
    p4.join()
    p3.join()
    p2.join()
    p1.join()

    # 自动关机
    print("程序已完成," + str(60) + '秒后将会关机')
    print('关机')
    # os.system('shutdown -s -f -t 60')
