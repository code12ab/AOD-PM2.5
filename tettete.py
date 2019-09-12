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
input_file_path_pollution = "D:\\毕业论文程序\\气象数据\\筛除字符串\\2018_不补全\\"
merge_output_file_path = "D:\\毕业论文程序\\气象数据\\插值模块\\Merge\\2018\\"
# 监测点坐标
JCZ_info = pd.read_excel("D:\\毕业论文程序\\MODIS\\坐标\\监测站坐标.xlsx", sheet_name="汇总")  # 152个
JCZ_info["监测站"] = JCZ_info["城市"] + "-" + JCZ_info["监测点名称"]
# 已经输出
saved_list = os.listdir(merge_output_file_path)


def get4method(xx152):
    # 地理距离

    # 监测站
    jcz_152 = pd.read_excel("D:\\毕业论文程序\\MODIS\\坐标\\站点列表-2018.11.08起_152.xlsx", sheet_name=xx152)
    jcz_152["监测站名称_152"] = jcz_152["城市"] + "-" + jcz_152["监测点名称"]
    for input_file_name in jcz_152["监测站名称_152"]:
        print(input_file_name)
        input_file_name = input_file_name + ".xlsx"
        data_pollution = pd.read_excel(input_file_path_pollution + input_file_name)
        data_pollution = data_pollution.set_index('日期')
        name = str(input_file_name).replace(".xlsx", "")  # 定义相关变量
        # 全局: 迭代回归,缺失特征作为y,其他特征作为x
        merge_list = []  # 同一监测站,不同污染物
        for darksky_weather_Iterative in data_pollution.columns:
            # 合并部分
            numb = 0
            data_darksky_weather_to_Iterative = copy.deepcopy(data_pollution[[darksky_weather_Iterative]])
            data_darksky_weather_to_Iterative = data_darksky_weather_to_Iterative.reset_index()
            if data_darksky_weather_to_Iterative[darksky_weather_Iterative].sum() == 0 \
                    or data_darksky_weather_to_Iterative[darksky_weather_Iterative].isnull().sum() == 0:
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
                        if data_to_add_in_to_Iterative[darksky_weather_Iterative].sum() == 0 \
                                or data_to_add_in_to_Iterative[darksky_weather_Iterative].isnull().sum() == \
                                len(data_to_add_in_to_Iterative.index):
                            continue
                        else:
                            data_to_Iterative_concat = data_to_add_in_to_Iterative[[darksky_weather_Iterative, '日期']]
                            data_to_Iterative_concat.columns = [darksky_weather_Iterative + "_add%s" % numb, '日期']  # 如果有五个临近, 则NDVI1-NDVI5
                            data_darksky_weather_to_Iterative = pd.merge(data_darksky_weather_to_Iterative,
                                                                        data_to_Iterative_concat,
                                                                        how='left',
                                                                        on='日期')
                            numb += 1  # 添加了列则增加计数
                            # print(len(data_darksky_weather_to_Iterative.columns))
                data_darksky_weather_to_Iterative = data_darksky_weather_to_Iterative.set_index('日期')
                # 迭代部分
                if numb >= 1:  # 至少两个非空列才可以计算
                    data_darksky_weather_Iterative_to_merge = IterativeImputer(
                        max_iter=1).fit_transform(data_darksky_weather_to_Iterative)
                    pd.DataFrame(data_darksky_weather_Iterative_to_merge).to_excel('tets1.xlsx')
                    data_darksky_weather_to_Iterative.to_excel('test2.xlsx')
                    data_darksky_weather_Iterative_to_merge = pd.DataFrame(
                        data_darksky_weather_Iterative_to_merge, columns=data_darksky_weather_to_Iterative.columns)  # 格式转换
                    data_darksky_weather_Iterative_to_merge = data_darksky_weather_Iterative_to_merge.set_index(
                        data_darksky_weather_to_Iterative.index)  # ok
                    # print(len(data_darksky_weather_Iterative_to_merge.columns))

                else:
                    data_darksky_weather_Iterative_to_merge = copy.deepcopy(data_darksky_weather_to_Iterative)
                for numb_del in data_darksky_weather_Iterative_to_merge.columns:
                    if 'add' in numb_del:
                        del data_darksky_weather_Iterative_to_merge[numb_del]  # 至此, 只剩下一列特征列
            # 插补后的该监测点的气象特征列, 仅一列, 循环添加其他特征
                merge_list.append(data_darksky_weather_Iterative_to_merge)
        data_darksky_weather_Iterative_1 = pd.concat(merge_list, axis=1, sort=False)
        print('[Iterative]Finished')

        # 对结果的0值取np.nan
        data_darksky_weather_Iterative_1.replace(0, np.nan, inplace=True)

        # 合并相同方法的结果

        data_pollution_Iterative = data_darksky_weather_Iterative_1.set_index(data_pollution.index)
        data_pollution_Iterative.columns = data_pollution.columns
        data_pollution_Iterative.to_excel('test3.xlsx')

if __name__ == '__main__':
    print('=====主进程=====')

    p1 = Process(target=get4method, args=("样例1",))
    p2 = Process(target=get4method, args=('样例2',))
    p3 = Process(target=get4method, args=('样例3',))
    p4 = Process(target=get4method, args=('样例4',))
    #p5 = Process(target=get4method, args=('样例5',))
    #p6 = Process(target=get4method, args=('样例6',))

    p3.start()

