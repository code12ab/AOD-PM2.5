# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2020/03/20 23:09


# 库
import pandas as pd
# import numpy as np
import os

# 路径
# input_path = "d:\\毕业论文程序\\气溶胶光学厚度\\空间转换模块\\Aqua\\2018_日期补全\\"
# output_path = "d:\\毕业论文程序\\气溶胶光学厚度\\空间转换模块\\Aqua\\2018_all\\"
# input_path = "d:\\毕业论文程序\\NDVI\\DATA\\MOD2018\\"
# output_path = "d:\\毕业论文程序\\NDVI\\DATA\\MODALL\\"
# input_path ='D:\\毕业论文程序\\污染物浓度\\整理\\PM\\2018_日期补全\\'
# output_path ='D:\\毕业论文程序\\污染物浓度\\整理\\PM\\2018_all\\'

# 路径
input_path = 'D:\\毕业论文程序\\污染物浓度\\整理\\PM\\2018_new\\'
output_path = 'D:\\毕业论文程序\\污染物浓度\\空间自相关\\'
coordinate_file_path = "D:\\毕业论文程序\\MODIS\\坐标\\"
# 批量导入监测站坐标
JCZ_file = pd.read_excel(coordinate_file_path +
                         "监测站坐标toDarkSkyAPI.xlsx",
                         sheet_name="汇总")  # 监测站坐标toDarkSkyAPI
JCZ = []
for i in range(len(JCZ_file)):
    exec(
        'JCZ%s = [JCZ_file["经度"][i],JCZ_file["纬度"][i],JCZ_file["城市"][i]+"-"+JCZ_file["监测点名称"][i]]' %
        i)
    exec("JCZ.append(JCZ%s)" % i)  # exec可以执行字符串指令
print(JCZ)

# 批量读取PM站
# 共358天
for day in range(358):
    print(day)  # 第一天
    day_list = list()
    num = 0
    for name in JCZ:
        data_pm = pd.read_excel(input_path + name[2] + ".xlsx")
        # print(data_pm['日期'][1].__class__)
        # print(data_pm.iloc[day].values[1],name[0],name[1],name[2], num)
        cun = [data_pm.iloc[day].values[1],name[0],name[1],name[2], num]
        # print(cun)
        day_list.append(cun)
        num += 1
    data_cun = pd.DataFrame(day_list)
    data_cun =data_cun.fillna(method='ffill')
    data_cun =data_cun.fillna(method='pad')

    data_cun.columns = ["PM", "经度", "纬度", "监测点", "编号"]
    data_cun.to_excel(output_path + str(day) + ".xls")