# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/30 14:11


# 库
import pandas as pd
import numpy as np
import os

# 路径
merge_output_file_path = "D:\\毕业论文程序\\气象数据\\插值模块\\Merge\\2018\\"
saved_list = os.listdir(merge_output_file_path)


null_list = []
for item in saved_list:

    try:
        pd.read_excel(merge_output_file_path+item, sheet_name="Iterative")
    except Exception as e:
        null_list.append(item)




print(len(null_list))