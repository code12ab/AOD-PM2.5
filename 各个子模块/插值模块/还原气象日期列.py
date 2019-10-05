# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/9/13 16:42


# 库
import pandas as pd
import numpy as np
import os

inputPath = 'd:\\毕业论文程序\\气象数据\\插值模块\\Res\\2018\\'
outputPath = 'd:\\毕业论文程序\\气象数据\\插值模块\\原日期\\2018\\'

oldIndexPath = 'd:\\毕业论文程序\\气象数据\\筛除字符串\\2018_不补全\\'

fileList = os.listdir(inputPath)

for file in fileList:
    data_merge = pd.read_excel(inputPath+file)
    data_index = pd.read_excel(oldIndexPath+file)[['日期']]

    dataOut = pd.merge(data_index, data_merge,
                       how='left',
                        on='日期')
    dataOut = dataOut.set_index('日期')
    dataOut.to_excel(outputPath+file)
    print(file)