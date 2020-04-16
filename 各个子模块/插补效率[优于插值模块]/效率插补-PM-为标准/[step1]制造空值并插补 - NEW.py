# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/7 11:10

"""
更新 trt,except
"""

# 库
from multiprocessing import Process  # 多线程,提高CPU利用率
import copy
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import numpy as np
from fancyimpute import KNN, IterativeImputer  # 方法创建新的数据框,不覆盖原始数据
import os
from scipy.interpolate import interp1d

# 路径
null_output_path = "D:\\毕业论文程序\\污染物浓度\\插值模块\\制造的缺失值\\"  # 2018
input_file_path_pollution = "D:\\毕业论文程序\\污染物浓度\\整理\\全部污染物\\2018插补效率\\"
merge_output_file_path = "D:\\毕业论文程序\\污染物浓度\\插值模块\\Merge\\2018插补效率\\"
JCZ_info = pd.read_excel("D:\\毕业论文程序\\MODIS\\坐标\\监测站坐标.xlsx", sheet_name="北京")  # 152个
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

    # 空间局部: 难以插值是因为大部分地区及其临近地区同一污染物值可能会一同缺失.
    def get_IDW(input_data):
        for pollution in ["PM25"]:  # 确定污染物列
            for indx in input_data.index:  # 获取索引
                res_list = []
                weight_list = []
                if pd.isnull(input_data[pollution][indx]):  # 开始循环
                    for item_idw in JCZ_info["监测站"]:  # 获取距离,定义权重
                        if item_idw != name:
                            lng2 = JCZ_info[JCZ_info["监测站"] == item_idw]["经度"]
                            lat2 = JCZ_info[JCZ_info["监测站"] == item_idw]["纬度"]
                            dis_1 = geo_distance(lng1, lat1, lng2, lat2)  # 两站地理距离
                            if dis_1 <= 50000:
                                data_to_add_in_1 = pd.read_excel(input_file_path_pollution + item_idw + ".xlsx")
                                data_to_add_in_1 = data_to_add_in_1.set_index("日期")  # 需要日期为索引,方便下面添加
                                if indx in data_to_add_in_1.index and pd.notnull(data_to_add_in_1[pollution][indx]):
                                    weight_list.append(dis_1)
                    weight_sum = np.sum(np.array(weight_list))  # 总距离,权重分母
                    for item_idw_2 in JCZ_info["监测站"]:  # 分配权重
                        if item_idw_2 != name:
                            lng2 = JCZ_info[JCZ_info["监测站"] == item_idw_2]["经度"]
                            lat2 = JCZ_info[JCZ_info["监测站"] == item_idw_2]["纬度"]
                            dis_1 = geo_distance(lng1, lat1, lng2, lat2)  # 两站地理距离
                            if dis_1 <= 50000:
                                data_to_add_in = pd.read_excel(input_file_path_pollution + item_idw_2 + ".xlsx")
                                data_to_add_in = data_to_add_in.set_index("日期")  # 需要日期为索引,方便下面添加
                                if indx in data_to_add_in.index and pd.notnull(data_to_add_in[pollution][indx]):
                                    res = (dis_1 / weight_sum) * data_to_add_in[pollution][indx]
                                    res_list.append(res)
                                    # print("已添加单元格插值:", res)
                    res_output = np.sum(np.array(res_list))  # 上下公式结果若为nan,并不会报错.会让最后的插值为nan.
                    try:
                        input_data[pollution][indx] = res_output
                    except Exception as e:
                        print("缺失严重, 插值未定义:", e)
        print("[IDW]Finished.")
        return input_data

    # 监测站
    jcz_152 = pd.read_excel("D:\\毕业论文程序\\MODIS\\坐标\\站点列表-2018.11.08起_152.xlsx", sheet_name=xx152)
    jcz_152["监测站名称_152"] = jcz_152["城市"] + "-" + jcz_152["监测点名称"]
    error_list = []
    import random
    for input_file_name in jcz_152["监测站名称_152"]:
        input_file_name = input_file_name + ".xlsx"
        # if input_file_name in saved_list:
            # print("已经完成:", input_file_name, xx152)
            # continue
        print("========正在计算%s========" % input_file_name)
        try:
            # 读取数据源
            data_pollution = pd.read_excel(input_file_path_pollution + input_file_name)
            data_pollution = data_pollution.set_index('日期')

            # 处理AQUA，制造 缺失值
            saveA = list()
            for columname in data_pollution.columns:
                if columname != "日期":
                    if columname != "监测站":
                        # loc 是某列为空的行坐标
                        loc = data_pollution[columname][
                            data_pollution[columname].isnull().values == False].index.tolist()
                        # 筛选个数
                        c1 = int(len(loc) * 0.25)
                        # 筛选出样本
                        slice1 = random.sample(loc, c1)
                        # print(data_darksky_weather[columname][0])
                        # print(slice1)
                        # 保存 变空之前 的 变量位置和数值
                        exec('save_a_%s = list()' % columname)
                        for nub in slice1:
                            # print(data_darksky_weather[columname][nub])
                            # print((columname, nub, data_darksky_weather[columname][nub]))
                            exec('save_a_%s.append((columname, nub, data_pollution[columname][nub]))' % columname)
                            # exec("JCZ.append(JCZ%s)" % i)
                            # 下一行，修改成缺失值
                            data_pollution[columname][nub] = np.nan
                            # print(data_darksky_weather[columname][nub])
                        exec('saveA.append(save_a_%s)' % columname)

            # 保存编号
            sA = pd.DataFrame(saveA)
            sA.to_excel(null_output_path + "%s" % input_file_name)
            # 局部：局部局部局部局部局部局部局部局部局部局部局部局部局部局部局部局部最近邻KNN,使用其他监测点同一个特征的均方差进行加权,判断最接近的时间点.
            # 局部！合并部分！局部局部局部局部局部局部局部局部局部局部
            name2 = str(input_file_name).replace(".xlsx", "")  # 定义相关变量
            lng1 = JCZ_info[JCZ_info["监测站"] == name2]["经度"]
            lat1 = JCZ_info[JCZ_info["监测站"] == name2]["纬度"]
            merge_list_KNN = []  # 同一监测站,不同污染物
            for darksky_weather_KNN in ['PM25']:
                # 合并部分
                numb2 = 0
                data_darksky_weather_to_KNN = copy.deepcopy(data_pollution[[darksky_weather_KNN]])
                data_darksky_weather_to_KNN = data_darksky_weather_to_KNN.reset_index()
                for item in JCZ_info["监测站"]:  # 不同于气溶胶插值方法
                    if item != name2:
                        lng2 = JCZ_info[JCZ_info["监测站"] == item]["经度"]
                        lat2 = JCZ_info[JCZ_info["监测站"] == item]["纬度"]
                        dis_1 = geo_distance(lng1, lat1, lng2, lat2)  # 两站地理距离
                        if dis_1 > 0: # <=
                            # 添加的文件
                            data_to_add_in_to_KNN = pd.read_excel(
                                input_file_path_pollution + item + ".xlsx")
                            # 添加的列名
                            data_to_KNN_concat = data_to_add_in_to_KNN[[darksky_weather_KNN, '日期']]
                            data_to_KNN_concat.columns = [darksky_weather_KNN + "_add%s" % numb2,
                                                                '日期']  # 如果有五个临近, 则NDVI1-NDVI5

                            data_darksky_weather_to_KNN = pd.merge(data_darksky_weather_to_KNN,
                                                                         data_to_KNN_concat,
                                                                         how='left',
                                                                         on='日期')
                            data_darksky_weather_to_KNN = data_darksky_weather_to_KNN.set_index('日期')
                    numb2 += 1
                # 迭代部分
                count_2 = 0
                for value_1 in data_darksky_weather_to_KNN.sum():
                    if value_1 != 0:
                        count_2 += 1
                if count_2 > 1:  # 至少两个非空列才可以计算
                    data_darksky_weather_KNN_to_merge = KNN(k=7).fit_transform(data_darksky_weather_to_KNN)
                    # data_darksky_weather_KNN_to_merge = IterativeImputer(max_iter=100).fit_transform(data_darksky_weather_to_KNN)
                else:
                    data_darksky_weather_KNN_to_merge = copy.deepcopy(
                        data_darksky_weather_to_KNN)
                data_darksky_weather_KNN_to_merge = pd.DataFrame(
                    data_darksky_weather_KNN_to_merge)  # 格式转换
                data_darksky_weather_KNN_to_merge = data_darksky_weather_KNN_to_merge.set_index(
                    data_darksky_weather_to_KNN.index)  # ok
                if len(data_darksky_weather_KNN_to_merge.columns) < len(
                        data_darksky_weather_to_KNN.columns):
                    reset_col_name_list_KNN = []  # 对非nan列先命名
                    for col_name in data_darksky_weather_to_KNN.columns:
                        if np.max(data_darksky_weather_to_KNN[col_name]) > 0:
                            reset_col_name_list_KNN.append(col_name)
                    data_darksky_weather_KNN_to_merge.columns = reset_col_name_list_KNN

                    for col_name in data_darksky_weather_to_KNN.columns:  # 对缺失的nan列补充
                        if col_name not in data_darksky_weather_KNN_to_merge.columns:
                            # 补全缺失nan列
                            data_darksky_weather_KNN_to_merge[col_name] = np.nan
                else:
                    data_darksky_weather_KNN_to_merge.columns = data_darksky_weather_to_KNN.columns  # 重设列名
                for numb_del in data_darksky_weather_KNN_to_merge.columns:
                    if 'add' in numb_del:
                        del data_darksky_weather_KNN_to_merge[numb_del]

                # 插补后的该监测点的气象特征列, 仅一列, 循环添加其他特征
                merge_list_KNN.append(data_darksky_weather_KNN_to_merge)
            data_darksky_weather_KNN_1 = pd.concat(
                merge_list_KNN, axis=1, sort=False)
            # 对结果的0值取np.nan
            # data_pollution_KNN = KNN(k=7).fit_transform(data_pollution)
            # data_pollution_KNN = pd.DataFrame(data_pollution_KNN)

            # 时间全局: 平滑,常用于股市;创建新的数据框,不会覆盖原始数据
            data_pollution_ewm_mid = pd.DataFrame.ewm(
                self=data_pollution,
                com=0.8,
                ignore_na=True,
                adjust=True).mean()
            # data_pollution_ewm_mid = data_pollution.interpolate()  # 23%[时间视图33→19]
            # 替换空白处
            data_pollution_ewm = copy.deepcopy(data_pollution)  # 避免覆盖原始数据
            for columname in data_pollution_ewm.columns:
                if data_pollution[columname].count() != len(data_pollution):
                    loc = data_pollution[columname][data_pollution[columname].isnull().values == True].index.tolist()
                    for nub in loc:
                        data_pollution_ewm[columname][nub] = data_pollution_ewm_mid[columname][nub]
            #########################################################################################################################################
            #########################################################################################################################################
            #########################################################################################################################################

            # 空间
            data_pollution_to_IDW = copy.deepcopy(data_pollution)
            name = str(input_file_name).replace(".xlsx", "")  # 定义相关变量
            lng1 = JCZ_info[JCZ_info["监测站"] == name]["经度"]
            lat1 = JCZ_info[JCZ_info["监测站"] == name]["纬度"]
            # 空间局部: IDW,反距离插值
            data_pollution_IDW = get_IDW(data_pollution_to_IDW)
            # 空间全局: 迭代回归,缺失特征作为y,其他特征作为x
            merge_list = []  # 同一监测站,不同污染物
            for darksky_weather_Iterative in ['PM25']:
                # 合并部分
                numb = 0
                data_darksky_weather_to_Iterative = copy.deepcopy(data_pollution[[darksky_weather_Iterative]])
                data_darksky_weather_to_Iterative = data_darksky_weather_to_Iterative.reset_index()
                for item in JCZ_info["监测站"]:  # 不同于气溶胶插值方法
                    if item != name:
                        # 添加的文件
                        data_to_add_in_to_Iterative = pd.read_excel(
                            input_file_path_pollution + item + ".xlsx")
                        # 添加的列名
                        data_to_Iterative_concat = data_to_add_in_to_Iterative[[darksky_weather_Iterative, '日期']]
                        data_to_Iterative_concat.columns = [darksky_weather_Iterative + "_add%s" % numb,
                                                            '日期']  # 如果有五个临近, 则NDVI1-NDVI5

                        data_darksky_weather_to_Iterative = pd.merge(data_darksky_weather_to_Iterative,
                                                                     data_to_Iterative_concat,
                                                                     how='left',
                                                                     on='日期')
                        data_darksky_weather_to_Iterative = data_darksky_weather_to_Iterative.set_index('日期')
                    numb += 1
                # 迭代部分
                count_1 = 0
                for value_1 in data_darksky_weather_to_Iterative.sum():
                    if value_1 != 0:
                        count_1 += 1
                if count_1 > 1:  # 至少两个非空列才可以计算
                    data_darksky_weather_Iterative_to_merge = IterativeImputer(
                        max_iter=100).fit_transform(data_darksky_weather_to_Iterative)
                else:
                    data_darksky_weather_Iterative_to_merge = copy.deepcopy(
                        data_darksky_weather_to_Iterative)
                data_darksky_weather_Iterative_to_merge = pd.DataFrame(
                    data_darksky_weather_Iterative_to_merge)  # 格式转换
                data_darksky_weather_Iterative_to_merge = data_darksky_weather_Iterative_to_merge.set_index(
                    data_darksky_weather_to_Iterative.index)  # ok
                if len(data_darksky_weather_Iterative_to_merge.columns) < len(
                        data_darksky_weather_to_Iterative.columns):
                    reset_col_name_list = []  # 对非nan列先命名
                    for col_name in data_darksky_weather_to_Iterative.columns:
                        if np.max(data_darksky_weather_to_Iterative[col_name]) > 0:
                            reset_col_name_list.append(col_name)
                    data_darksky_weather_Iterative_to_merge.columns = reset_col_name_list

                    for col_name in data_darksky_weather_to_Iterative.columns:  # 对缺失的nan列补充
                        if col_name not in data_darksky_weather_Iterative_to_merge.columns:
                            # 补全缺失nan列
                            data_darksky_weather_Iterative_to_merge[col_name] = np.nan
                else:
                    data_darksky_weather_Iterative_to_merge.columns = data_darksky_weather_to_Iterative.columns  # 重设列名
                for numb_del in data_darksky_weather_Iterative_to_merge.columns:
                    if 'add' in numb_del:
                        del data_darksky_weather_Iterative_to_merge[numb_del]

                # 插补后的该监测点的气象特征列, 仅一列, 循环添加其他特征
                merge_list.append(data_darksky_weather_Iterative_to_merge)
            data_darksky_weather_Iterative_1 = pd.concat(
                merge_list, axis=1, sort=False)
            # 对结果的0值取np.nan
            # data_pollution_KNN.replace(0, np.nan, inplace=True)
            data_darksky_weather_KNN_1.replace(0, np.nan, inplace=True)  # 新
            data_pollution_ewm.replace(0, np.nan, inplace=True)
            data_pollution_IDW.replace(0, np.nan, inplace=True)
            data_darksky_weather_Iterative_1.replace(0, np.nan, inplace=True)

            # 合并相同方法的结果
            # data_pollution_KNN = data_pollution_KNN.set_index(data_pollution.index)
            # data_pollution_KNN.columns = data_pollution.columns
            data_pollution_KNN = data_darksky_weather_KNN_1.set_index(data_pollution.index)  # 新
            data_pollution_KNN.columns = data_pollution.columns  # 新

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
        except Exception as e:
            print(input_file_name, "发生错误:", e)
            error_list.append(input_file_name)

        if len(error_list) != 0:
            error_list = pd.DataFrame(error_list)
            error_list.to_excel(xx152+".xlsx")


if __name__ == '__main__':
    print('=====主进程=====')

    p1 = Process(target=get4method, args=("北京1",))
    p2 = Process(target=get4method, args=('北京2',))
    p3 = Process(target=get4method, args=('北京3',))
    p4 = Process(target=get4method, args=('北京4',))
    p5 = Process(target=get4method, args=('北京5',))
    p6 = Process(target=get4method, args=('北京6',))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()

    p6.join()  # 依次检测是否完成, 完成才会执行join下面的代码
    p5.join()
    p4.join()
    p3.join()
    p2.join()
    p1.join()

    # 自动关机
    print("程序已完成," + str(60) + '秒后将会关机')
    print('关机')
    # os.system('shutdown -s -f -t 60')
