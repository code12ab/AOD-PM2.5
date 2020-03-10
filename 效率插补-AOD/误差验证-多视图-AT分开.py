# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/7 18:54

# 库
import pandas as pd
import numpy as np
import math
from numpy import array
import os
# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/7 18:54

# 库
import pandas as pd
import numpy as np
import math
from numpy import array
import os

resA_output_path = "D:\\毕业论文程序\\气溶胶光学厚度\\插值模块\\Merge\\Aqua\\2018插补效率\\"  # 制造空值后的插补结果
resT_output_path = "D:\\毕业论文程序\\气溶胶光学厚度\\插值模块\\Merge\\Terra\\2018插补效率\\"  # 制造空值后的插补结果

null_output_path = "D:\\毕业论文程序\\气溶胶光学厚度\\插值模块\\制造的缺失值\\"  # 制造出来的空值的，真实值。
# input_file_path_Aqua = "D:\\毕业论文程序\\气溶胶光学厚度\\空间转换模块\\Aqua插补效率\\2018\\"  # 插补前数据
# input_file_path_Terra = "D:\\毕业论文程序\\气溶胶光学厚度\\空间转换模块\\Terra插补效率\\2018\\"
input_file_names = os.listdir(resA_output_path)  # 文件名列表
for input_file_name in input_file_names:
    # 插值后AT
    data_resA = pd.read_excel(resA_output_path + input_file_name)
    data_resT = pd.read_excel(resT_output_path + input_file_name)
    # 制造出来的空值的，真实值
    data_null_Aqua = pd.read_excel(null_output_path + "Aqua\\" + input_file_name, index_col='Unnamed: 0')
    data_null_Terra = pd.read_excel(null_output_path + "Terra\\" + input_file_name, index_col='Unnamed: 0')  # 第一列空列，处理一下
    # 原始数据，只是换个文件夹放置
    # data_origin_Terra = pd.read_excel(input_file_path_Terra + input_file_name)  # 插补前
    # data_origin_Aqua = pd.read_excel(input_file_path_Aqua + input_file_name)
    data_resA['日期'] = data_resA['日期'].map(lambda x: x.replace(" ",""))
    data_resT['日期'] = data_resT['日期'].map(lambda x: x.replace(" ",""))
    # data_origin_Terra['日期'] = data_origin_Terra['日期'].map(lambda x: x.replace(" ",""))
    # data_origin_Aqua['日期'] = data_origin_Aqua['日期'].map(lambda x: x.replace(" ", ""))
    # print(data_res)
    # print(data_null.isnull())
    error1 = list()
    defeat_A = 0
    for columname in data_null_Aqua.columns:
        if columname != "日期":
            if columname != "监测站":
                # loc 是某列为空的行坐标，这里由于前一个步骤中被转置了，
                # loc 对应的是AOD0到AOD16
                # print(columname)
                loc_t = data_null_Aqua[columname][data_null_Aqua[columname].isnull().values == False].index.tolist()
                # print(loc_t)
                for numb1 in loc_t:
                    if numb1 != 0:  # 此时为 aod_0  # ！=0 时为其他即，aods
                        # 原真实值。 Colu列→源数据第几行；numb（loc-t）第几行即AODx]
                        # print(data_null_Aqua[columname][numb1])
                        c_null = data_null_Aqua[columname][numb1].replace("(","").replace(")","").replace("'","").replace(" ","").split(",")
                        # c_null = data_null_Terra[columname][numb1]
                        # print(c_null)
                        c_null = list(c_null)  # 转化格式完毕
                        # print(c_origin[1])
                        # print(c_origin[1].__class__)
                        # 先 日期 ， 后 aod 变量
                        # print(data_origin_Aqua[data_origin_Aqua['日期'] == c_null[1]][c_null[0]].values[0])  # 提出数值
                        c_chabu = data_resA[data_resA['日期'] == c_null[1]][c_null[0]].values[0]
                        if c_chabu > 0:
                            c_res1 = float(c_null[2])  # 观测值终值 相当于真实值
                            e1 = abs(c_chabu - c_res1) / c_res1
                            error1.append(e1)
                            # print(e1)
                        else:
                            print(c_chabu)
    for columname in data_null_Terra.columns:
        if columname != "日期":
            if columname != "监测站":
                # loc 是某列为空的行坐标，这里由于前一个步骤中被转置了，
                # loc 对应的是AOD0到AOD16
                # print(columname)
                loc_t = data_null_Terra[columname][data_null_Terra[columname].isnull().values == False].index.tolist()
                # print(loc_t)
                for numb1 in loc_t:
                    if numb1 != 0:  # 此时为 aod_0  # ！=0 时为其他即，aods
                        # 原真实值。 Colu列→源数据第几行；numb（loc-t）第几行即AODx]
                        # print(data_null_Aqua[columname][numb1])
                        c_null = data_null_Terra[columname][numb1].replace("(","").replace(")","").replace("'","").replace(" ","").split(",")
                        # c_null = data_null_Terra[columname][numb1]
                        # print(c_null)
                        c_null = list(c_null)  # 转化格式完毕
                        # print(c_origin[1])
                        # print(c_origin[1].__class__)
                        # 先 日期 ， 后 aod 变量
                        # print(data_origin_Aqua[data_origin_Aqua['日期'] == c_null[1]][c_null[0]].values[0])  # 提出数值
                        c_chabu = data_resT[data_resT['日期'] == c_null[1]][c_null[0]].values[0]
                        if c_chabu > 0:
                            c_res1 = float(c_null[2])  # 观测值终值 相当于真实值
                            e1 = abs(c_chabu - c_res1) / c_res1
                            error1.append(e1)
                            # print(e1)
                        else:
                            print(c_chabu)
print('RE', np.average(error1))
print(np.std(error1))
    # print(data_null_Terra.columns)
    # print(data_res.head(3))
    # print(data_res['日期'][1].__class__)
    # print(data_res['日期'][1])
    # print(data_res[data_res['日期'] == '2018-01-01 ']['AOD_0'])  # 日期后面多了个空格
    # lng2 = JCZ_info[JCZ_info["监测站"] == item_idw]["经度"]


