# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2020/3/16 23:25


# 库
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt


file_input = "D:\\硕士\\论文 项目 报销\\论文\\正在写的论文\\毕业论文之MODIS04_3KM_AOD\\AOD-PM2.5批注\\退修 地理学报\\图片文件\\数据.xlsx"

data = pd.read_excel(file_input, sheet_name="监测站-MAE作图")



# 30 points between [0, 0.2) originally made using np.random.rand(30)*.2
pts0 = np.array(data['DP-DNN'])
pts1 = np.array(data.MNN)
pts2 = np.array(data["MI-NN"])
pts3 = np.array(data["LSTM"])
pts4 = np.array(data["GWR"])
pts5 = np.array(data['B-OLSR'])
pts6 = np.array(data["EN"])
# Now let's make two outlier points which are far away from everything.

# If we were to simply plot pts, we'd lose most of the interesting
# details due to the outliers. So let's 'break' or 'cut-out' the y-axis
# into two portions - use the top (ax) for the outliers, and the bottom
# (ax2) for the details of the majority of our data
f, (ax, ax2) = plt.subplots(2, 1, sharex=True)

# plot the same data on both axes
ax.plot(pts0)
ax2.plot(pts0)
ax.plot(pts1)
ax2.plot(pts1)
ax.plot(pts2)
ax2.plot(pts2)
ax.plot(pts3)
ax2.plot(pts3)
ax.plot(pts4)
ax2.plot(pts4)
ax.plot(pts5)
ax2.plot(pts5)
ax.plot(pts6)
ax2.plot(pts6)

# zoom-in / limit the view to different portions of the data
ax.set_ylim(7, 39)  # 异常值区域
ax2.set_ylim(.30, .60)  # 正常值

# hide the spines between ax and ax2
ax.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax.xaxis.tick_top()
ax.tick_params(labeltop='off')  # don't put tick labels at the top
ax2.xaxis.tick_bottom()

# This looks pretty good, and was fairly painless, but you can get that
# cut-out diagonal lines look with just a bit more work. The important
# thing to know here is that in axes coordinates, which are always
# between 0-1, spine endpoints are at these locations (0,0), (0,1),
# (1,0), and (1,1).  Thus, we just need to put the diagonals in the
# appropriate corners of each of our axes, and so long as we use the
# right transform and disable clipping.
d = .015  # how big to make the diagonal lines in axes coordinates
# arguments to pass to plot, just so we don't keep repeating them
kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
ax.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

# What's cool about this is that now if we vary the distance between
# ax and ax2 via f.subplots_adjust(hspace=...) or plt.subplot_tool(),
# the diagonal lines will move accordingly, and stay right at the tips
# of the spines they are 'breaking'
ax.legend(['A simple line'])
plt.xlabel('实验次数')
plt.ylabel('MAE' ,ha='center')





plt.show()
