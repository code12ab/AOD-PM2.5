# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/21 8:21


# 库
import pandas as pd
# import numpy as np
import os

# 路径
input_path = "d:\\毕业论文程序\\气溶胶光学厚度\\空间转换模块\\Terra\\"
output_path = "d:\\毕业论文程序\\气溶胶光学厚度\\空间转换模块\\Terra\\多年合一\\"
file_name = os.listdir(input_path+"2014\\")  # 获取文件名

for name in file_name:
    data_2014 = pd.read_excel(input_path+'2014\\'+name, index_col="日期")
    data_2015 = pd.read_excel(input_path + '2015\\' + name, index_col="日期")
    data_2016 = pd.read_excel(input_path + '2016\\' + name, index_col="日期")
    data_2017 = pd.read_excel(input_path + '2017\\' + name, index_col="日期")
    data_2018 = pd.read_excel(input_path + '2018\\' + name, index_col="日期")
    data_full = pd.concat([data_2014, data_2015, data_2016, data_2017, data_2018], axis=0)
    data_full.to_excel(output_path+name)
    print(name, "完成")