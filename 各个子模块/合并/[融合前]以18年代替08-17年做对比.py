# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2020/3/30 21:26


# 库
import pandas as pd
import numpy as np
import os
years = [2008,2009,2010,2011,2012,2013,2014,2015,2016,2017]


for year in years:
    '''
    input_path = 'D:\\毕业论文程序\\NDVI\\插值模块\\2018_线性填充\\'
    input_path2 = 'D:\\毕业论文程序\\气溶胶光学厚度\\插值模块\\Res\\%s\\' % year
    output_path = 'D:\\毕业论文程序\\NDVI\\%s\\' % year
    '''
    input_path = 'D:\\毕业论文程序\\污染物浓度\\插值模块\\Res\\2018_new\\'  # 输入文件
    input_path2 = 'D:\\毕业论文程序\\气溶胶光学厚度\\插值模块\\Res\\2017\\'  # 文件名列表而已
    output_path = 'D:\\毕业论文程序\\污染物浓度\\插值模块\\Res\\%s\\' % year  # 输出位置
    input_file = os.listdir(input_path2)

    for file_name in input_file:
        data_out = pd.read_excel(input_path+file_name)
        data_out['日期'] = data_out['日期'].map(lambda x: x.replace("2018","%s" % year))

        print(data_out.head(3))
        data_out.to_excel(output_path+file_name)