# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/9/1 17:43


# 库
import pandas as pd
import numpy as np
import os
import time, datetime

input_path = 'D:\\毕业论文程序\\NDVI\\2018_线性填充\\'
output_path = 'D:\\毕业论文程序\\时空特征\\2018\\'
jcz_file = 'D:\\毕业论文程序\\MODIS\\坐标\\站点列表-2018.11.08起_152.xlsx'
jcz_data = pd.read_excel(jcz_file, sheet_name='station152')
jcz_data['监测点'] = jcz_data['城市']+'-'+jcz_data['监测点名称']


input_list = os.listdir(input_path)


for file in input_list:
    print(file)

    data = pd.read_excel(input_path+file)
    # 转换
    data['日期'] = data['日期'].map(lambda x: str(x)[0:10])  # 去掉换行符
    data = data.set_index('日期')
    # 生成
    data['tm_mon'] = data.index.map(lambda x: time.strptime(x, '%Y-%m-%d').tm_mon)
    data['tm_mday'] = data.index.map(lambda x: time.strptime(x, '%Y-%m-%d').tm_mday)
    data['tm_wday'] = data.index.map(lambda x: time.strptime(x, '%Y-%m-%d').tm_wday)
    data['tm_yday'] = data.index.map(lambda x: time.strptime(x, '%Y-%m-%d').tm_yday)
    data['tm_week'] = data.index.map(lambda x: datetime.datetime(time.strptime(x, '%Y-%m-%d').tm_year,
                                                                 time.strptime(x, '%Y-%m-%d').tm_mon,
                                                                 time.strptime(x, '%Y-%m-%d').tm_mday).isocalendar()[1])

    data_ts = data[['tm_mon', 'tm_mday', 'tm_wday', 'tm_yday', 'tm_week']]

    name = file.replace('.xlsx', '')
    id_nub = jcz_data[jcz_data['监测点']==name]['id_order'].values[0]

    # 创建
    data_ts['id'] = id_nub
    # 字符串
    for cccc in data_ts.columns:
        data_ts[cccc] = data_ts[cccc].map(lambda x: str(x))
    # 存
    data_ts.to_excel(output_path + file)


