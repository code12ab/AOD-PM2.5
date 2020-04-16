# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/9/1 19:28


# 库
import pandas as pd
import numpy as np
import os

# 路径
years = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]  # 08有
for year in years:
    aod_path = 'D:\\毕业论文程序\\气溶胶光学厚度\\插值模块\\Res\\%s\\' % year
    # darksky_path = 'D:\\毕业论文程序\\气象数据\\插值模块\\原日期\\2018\\'
    darksky_path = 'D:\\毕业论文程序\\气象数据\\插值模块\\Res\\%s\\' % year
    # out_path = 'D:\\毕业论文程序\\建模数据\\时滞\\2018_不补全\\'
    out_path = 'D:\\毕业论文程序\\建模数据\\时滞\\%s\\' % year

    file_list = os.listdir(aod_path)

    for file in file_list:
        data_sky = pd.read_excel(darksky_path + file)
        data_aod = pd.read_excel(aod_path + file)
        data_aod["日期"] = data_aod["日期"].map(lambda x: str(x)[0:10])
        data_sky["日期"] = data_sky["日期"].map(lambda x: str(x)[0:10])  # 有一个多了个空格

        data = pd.merge(left=data_aod, right=data_sky,  on='日期', how="right")
        # data = pd.concat([data_aod,data_sky])
        # print(data_aod["日期"][1],data_sky["日期"][1])
        print(data.head(3))
        # T - 1
        data = data.set_index('日期')
        for ccc in data.columns:
            data[ccc] = data[ccc].shift(periods=1, axis=0)
        """
        if len(data.index) == 365:
            for ddd in data.columns:
                data.loc['2018-01-01', ddd] = float(data[ddd].mean())
        """
        data.columns = [x+"_T1" for x in data.columns]
        data = data.drop(data.index[0], axis=0)
        data.to_excel(out_path + file)
