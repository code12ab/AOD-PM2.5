# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/10/5 21:36


# 库
import pandas as pd
import numpy as np
import os

input_path = 'D:\\ID.xlsx'
df1 = pd.read_excel(input_path)

# 读
ts = 'D:\\毕业论文程序\\建模数据\\时空特征\\2018\\'
coordinate_file_path = "D:\\毕业论文程序\\MODIS\\坐标\\"
JCZ_file = pd.read_excel(coordinate_file_path +
                         "监测站坐标toDarkSkyAPI.xlsx")  # 监测站坐标toDarkSkyAPI
JCZ = []
for i in range(len(JCZ_file)):
    exec(
        'JCZ%s = [JCZ_file["经度"][i],JCZ_file["纬度"][i],JCZ_file["城市"][i]+"-"+JCZ_file["监测点名称"][i]]' %
        i)
    exec("JCZ.append(JCZ%s)" % i)  # exec可以执行字符串指令


file_list = os.listdir(ts)
listout = []
for file in file_list:
    data6 = pd.read_excel(ts + file)
    listout.append([data6['id'][0],file.replace('.xlsx','')])


print(JCZ)
print(listout)

df_id = pd.DataFrame(listout,columns=['id','监测点'])
df_xy = pd.DataFrame(JCZ,columns=['经度','纬度','监测点'])

res = pd.merge(df_id,df_xy,how='left', on='监测点')
print(res)

out = pd.merge(res,df1,how='left', on='id')

out.to_excel('d:\\id+x+y+aod+pm.xlsx')