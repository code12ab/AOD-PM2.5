# -*- coding: utf-8 -*-
# 日期: 2019/4/14 16:03
# 作者: xcl
# 工具：PyCharm


'''
import pandas as pd  # BDS
data = "C:\\Users\\Administrator.SC-201902221855\\Desktop\\Data\\airquality.csv"
data = pd.read_csv(data)
print(data.head(15))
print(data.columns)

import pandas as pd
data_aod = "F:\\毕业论文程序\\气溶胶光学厚度\\日均\\"
data111 = pd.read_excel(data_aod + "北京-东四.xlsx")
data111 = data111.set_index('日期')
data111['AOD值'] = data111['AOD值'].fillna(0)
data222 = pd.read_excel(data_aod + "北京-定陵.xlsx")
data222['AOD值'] = data222['AOD值'].fillna(0)
data222 = data222.set_index('日期')
data333 = pd.DataFrame()
data333["xxxx"] = data111["AOD值"] + data222["AOD值"]
print(data333)

#data333.to_excel("tadasd3.xlsx")


# 不行 空行直接加 即便索引一只 但是空行+数字 = 无结果
'''

import pandas as pd


