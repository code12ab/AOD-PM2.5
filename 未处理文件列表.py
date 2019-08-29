# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/7 11:10


# 库
import pandas as pd
import os

# 路径
merge_output_file_path = "D:\\毕业论文程序\\气象数据\\数据\\逐时\\2017\\"
JCZ_info = pd.read_excel("D:\\毕业论文程序\\MODIS\\坐标\\监测站坐标.xlsx", sheet_name="汇总")  # 152个
JCZ_info["监测站"] = JCZ_info["城市"] + "-" + JCZ_info["监测点名称"]
# 已经输出
saved_list = os.listdir(merge_output_file_path)

jcz_152 = pd.read_excel("D:\\毕业论文程序\\MODIS\\坐标\\站点列表-2018.11.08起_152.xlsx", sheet_name="station152")
jcz_152["监测站名称_152"] = jcz_152["城市"] + "-" + jcz_152["监测点名称"]

null_list = []
for item in jcz_152["监测站名称_152"]:
    if item+".xlsx" not in saved_list:
        null_list.append(item)
print(null_list)