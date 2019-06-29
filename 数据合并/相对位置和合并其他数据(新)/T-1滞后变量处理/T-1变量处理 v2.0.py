# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/6/27 18:59


import pandas as pd
import numpy as np
import os

for year in range(2013,2019):
    input_file_path = "D:\\毕业论文程序\\整合数据\\自身与相邻站点PM_AOD\\%s\\" % year
    outpu_file_path = "D:\\毕业论文程序\\整合数据\\自身与相邻站点PM_AOD_T-1\\%s\\" % year
    input_file_name = os.listdir(input_file_path)  # 文件名列表
    print("文件个数:"+str(len(input_file_name)))


    for file_name in input_file_name:
        print("处理监测站:"+file_name)
        data = pd.read_excel(input_file_path + file_name)
        data = data.set_index("日期")
        # t-1
        for ccc in data.columns:
            data["%s-t-1" % ccc] = data[ccc].shift(periods=1, axis=0)  # 下移动 列移动
        # 补0
        for cx_name_2 in data.columns:
            data[cx_name_2] = data[cx_name_2].fillna(0)
        # 删除无用列
        del data["监测站-t-1"]
        # 存
        data.to_excel(outpu_file_path+file_name)
