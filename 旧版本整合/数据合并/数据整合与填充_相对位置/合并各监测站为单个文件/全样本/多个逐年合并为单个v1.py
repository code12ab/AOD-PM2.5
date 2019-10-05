# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/6/28 0:33


# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/6/27 19:10

# -*- coding: utf-8 -*-
# 日期: 2019/6/27 14:47
# 作者: xcl
# 工具：PyCharm


import pandas as pd
import numpy as np
import os

data_2014 = pd.read_excel("D:\\毕业论文程序\\整合数据\\汇总为单个文件_逐年\\自身与相邻站点PM_AOD_T-1_2014.xlsx", index_col="日期")
data_2015 = pd.read_excel("D:\\毕业论文程序\\整合数据\\汇总为单个文件_逐年\\自身与相邻站点PM_AOD_T-1_2015.xlsx", index_col="日期")
data_2016 = pd.read_excel("D:\\毕业论文程序\\整合数据\\汇总为单个文件_逐年\\自身与相邻站点PM_AOD_T-1_2016.xlsx", index_col="日期")
data_2017 = pd.read_excel("D:\\毕业论文程序\\整合数据\\汇总为单个文件_逐年\\自身与相邻站点PM_AOD_T-1_2017.xlsx", index_col="日期")
data_2018 = pd.read_excel("D:\\毕业论文程序\\整合数据\\汇总为单个文件_逐年\\自身与相邻站点PM_AOD_T-1_2018.xlsx", index_col="日期")

output_file_path = "D:\\毕业论文程序\\整合数据\\汇总为单个文件_全样本\\"


data_res = pd.concat([data_2014, data_2015, data_2016, data_2017, data_2018], sort=True, axis=0)