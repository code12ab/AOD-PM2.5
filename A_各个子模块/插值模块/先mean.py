# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/9/11 16:22


# 库
import pandas as pd
import numpy as np
import os

# 路径
input_file_path_Aqua = "D:\\毕业论文程序\\气溶胶光学厚度\\空间转换模块\\Aqua\\2018_日期补全\\"
input_file_path_Terra = "D:\\毕业论文程序\\气溶胶光学厚度\\空间转换模块\\Terra\\2018_日期补全\\"
mean_output_file_path = "D:\\毕业论文程序\\气溶胶光学厚度\\插值模块\\Mean\\2018\\"
input_file_names = os.listdir(input_file_path_Aqua)  # 文件名列表
saved_list = os.listdir(mean_output_file_path)

for input_file_name in input_file_names:
    if input_file_name in saved_list:
        print("已经完成%s" % input_file_name)
        #continue
    print("========正在计算%s========" % input_file_name)
    # 读取
    data_Aqua = pd.read_excel(input_file_path_Aqua + input_file_name)
    data_Terra = pd.read_excel(input_file_path_Terra + input_file_name)
    if len(data_Aqua.index) >= len(data_Terra.index):
        data_merge_AT = pd.merge(
            data_Aqua,
            data_Terra,
            how='right',
            on=["日期"])
    else:
        data_merge_AT = pd.merge(
            data_Aqua,
            data_Terra,
            how='left',
            on=["日期"])
    data_merge_AT = data_merge_AT.set_index('日期')
    print(data_merge_AT.columns)
    for area_numb in range(0, 17):
        d1 = data_merge_AT[['AOD_%s_x' % area_numb, "AOD_%s_y" % area_numb]]
        d2 = d1.mean(1)
        data_merge_AT["AOD_%s" % area_numb] = d2
        # print(data_merge_AT[["AOD_%s" % area_numb,'AOD_%s_x' % area_numb,'AOD_%s_y' % area_numb]])
        data_merge_AT.drop(['AOD_%s_x' %
                           area_numb, "AOD_%s_y" %
                           area_numb], inplace=True, axis=1)

    data_merge_AT.to_excel(mean_output_file_path+input_file_name)