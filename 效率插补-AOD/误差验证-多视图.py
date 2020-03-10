# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/7 18:54

# 库
import pandas as pd
import numpy as np
import math
from numpy import array
import os

res_output_path = "D:\\毕业论文程序\\气溶胶光学厚度\\插值模块\\Res\\2018插补效率\\"
null_output_path = "D:\\毕业论文程序\\气溶胶光学厚度\\插值模块\\制造的缺失值\\"

input_file_names = os.listdir(res_output_path)  # 文件名列表
for input_file_name in input_file_names:
    # print(input_file_name)
    data_res = pd.read_excel(res_output_path + input_file_name)
    data_null_Aqua = pd.read_excel(null_output_path + "Auqa\\" + input_file_name)
    data_null_Terra = pd.read_excel(null_output_path + "Terra\\" + input_file_name)

    # print(data_null.isnull())
    for columname in data_null.columns:
        if columname != "日期":
            if columname != "监测站":
                # loc 是某列为空的行坐标，这里由于前一个步骤中被转置了，
                # loc 对应的是AOD0到AOD16
                # print(columname)
                loc = data_null[columname][data_null[columname].isnull().values == False].index.tolist()
                print(loc)
    # print(data_res.head(3))
    # print(data_res['日期'][1].__class__)
    # print(data_res['日期'][1])
    # print(data_res[data_res['日期'] == '2018-01-01 ']['AOD_0'])  # 日期后面多了个空格
    # lng2 = JCZ_info[JCZ_info["监测站"] == item_idw]["经度"]

    break