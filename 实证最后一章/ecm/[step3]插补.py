# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2020/3/31 22:04


# 库
import pandas as pd
import numpy as np
import os

input_data = 'D:\\硕士\\论文 项目 报销\\论文\\' \
             '正在写的论文\\毕业论文之MODIS04_3KM_AOD\\AOD-PM2.5批注\\实证研究章\\建模用.xlsx'
input_data = 'D:\\硕士\\论文 项目 报销\\论文\\' \
             '正在写的论文\\毕业论文之MODIS04_3KM_AOD\\AOD-PM2.5批注\\实证研究章\\建模用 - 去掉几个变量.xlsx'

input_data = 'C:\\Users\\iii\\Desktop\\汇总ecm.xlsx'
input_data = 'D:\\硕士\\论文 项目 报销\\论文\\正在写的论文\\毕业论文之MODIS04_3KM_AOD\\AOD-PM2.5批注\\实证研究章\\协整关系0412多变量\\汇总ecm_fill.xlsx'
data = pd.read_excel(input_data, index_col='date')  # 日期全

data2 = data.interpolate()
# data2 = data2.fillna('bfill')
# data2 = data2.fillna('pad')
#
# print(pd.isna(data2).sum())

# data2.to_excel('D:\\硕士\\论文 项目 报销\\论文\\正在写的论文\\毕业论文之MODIS04_3KM_AOD\\AOD-PM2.5批注\\实证研究章\\建模用2-插补后.xlsx')

# data3 = data.dropna()
# data3.to_excel('D:\\硕士\\论文 项目 报销\\论文\\正在写的论文\\毕业论文之MODIS04_3KM_AOD\\AOD-PM2.5批注\\实证研究章\\建模用2-删除法.xlsx')

print(pd.isna(data2).sum().sum())


data2.to_excel('C:\\Users\\iii\\Desktop\\汇总ecm_fill.xlsx')
