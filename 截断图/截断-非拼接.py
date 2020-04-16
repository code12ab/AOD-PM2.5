# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2020/3/17 0:10


# 库
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager
from brokenaxes import brokenaxes
import numpy as np


file_input = "D:\\硕士\\论文 项目 报销\\论文\\正在写的论文\\毕业论文之MODIS04_3KM_AOD\\AOD-PM2.5批注\\退修 地理学报\\图片文件\\数据.xlsx"
myfont = font_manager.FontProperties(fname=r'C:\Windows\Fonts\simsun.ttc')

data = pd.read_excel(file_input, sheet_name="监测站-RE")
pts0 = np.array(data['DP-DNN'])
pts1 = np.array(data.MNN)
pts2 = np.array(data["MI-NN"])
pts3 = np.array(data["LSTM"])
pts4 = np.array(data["GWR"])
pts5 = np.array(data['B-OLSR'])
pts6 = np.array(data["EN"])

# 横坐标
x0 = np.arange(0,100)
x1 = np.arange(0,100)
x2 = np.arange(0,100)
x3 = np.arange(0,100)
x4 = np.arange(0,100)
x5 = np.arange(0,100)
x6 = np.arange(0,100)

# 图的大小
fig = plt.figure(dpi=300)

# 切切切

# bax = brokenaxes(xlims=((0, .1), (.4, .7)), ylims=((-1, .7), (.79, 1)), hspace=.05, despine=False)
bax1 = brokenaxes(ylims=((0.3, 1),(6.5,6.8), (8.4, 8.9)))  # hspace 间隔图上显示大小
bax1.plot(x0, pts0,label='DP-DNN')
bax1.plot(x1, pts1,label='MNN')
bax1.plot(x2, pts2,label='MI-NN')
bax1.plot(x3, pts3,label='LSTM')
bax1.plot(x4, pts4,label='GWR')
bax1.plot(x5, pts5,label='B-OLSR')
bax1.plot(x6, pts6,label='EN')

bax1.legend(loc='center left', bbox_to_anchor=(0.2, 1.12),ncol=3)
bax1.set_xlabel('实验次数',fontproperties=myfont)
bax1.set_ylabel('RE')


plt.show()