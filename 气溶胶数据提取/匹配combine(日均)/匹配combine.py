# -*- coding: utf-8 -*-
# 日期: 2019/3/6 17:53
# 作者: xcl
# 工具：PyCharm

import pandas as pd
import numpy as np
import os

input_file_path = "D:\\毕业论文程序\\气溶胶光学厚度\\Terra\\2018\\"
input_file_name = os.listdir(input_file_path)  # 文件名列表

i = 0
for file_name in input_file_name:
    i += 1
    # 读取数据
    try:
        Terra_AOD = "D:\\毕业论文程序\\气溶胶光学厚度\\Terra\\2018\\"+file_name
        Aqua_AOD = "D:\\毕业论文程序\\气溶胶光学厚度\\Aqua\\2018\\"+file_name

        output_name = Terra_AOD.replace("D:\\毕业论文程序\\气溶胶光学厚度\\Terra\\2018\\", "")
        output_name = output_name.replace(".xlsx", "")

        Terra_AOD = pd.read_excel(Terra_AOD, index_col="日期")
        Aqua_AOD = pd.read_excel(Aqua_AOD, index_col="日期")

        # 合并数据
        data = pd.merge(Terra_AOD, Aqua_AOD, right_on='日期', left_index=True, how='outer')
        # print(data.isnull().sum())  # 空值检查

        # 处理残缺值
        # 删除AOD值为空的数据
        '''
        indexs = list(data[np.isnan(data['AOD值_x'])].index)  # 获取AOD值为空的数据的索引
        data = data.drop(indexs)  # 删除
        indexs = list(data[np.isnan(data['AOD值_y'])].index)  # 获取AOD值为空的数据的索引
        data = data.drop(indexs)  # 删除
        '''
        # 输出文件
        data["监测站"] = data["监测站_x"]
        data["AOD值"] = (data["AOD值_x"]+data["AOD值_y"])*0.5  # 数值 + 空值 = 空值
        data = data.drop(["监测站_x", "监测站_y", "AOD值_x", "AOD值_y"], axis=1)
        data.to_excel("D:\\毕业论文程序\\气溶胶光学厚度\\combine\\2018\\%s.xlsx" % output_name)
        print("进度:%.2f%%" % float(100*i/len(input_file_name)))
    except Exception as e:
        print("跳过原因:", e)
