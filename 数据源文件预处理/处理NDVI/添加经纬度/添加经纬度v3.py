# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/18 9:39

import pandas as pd
import numpy as np
from osgeo import gdal

# 路径
hdf = "C:\\Users\\iii\\Desktop\\MYD13A2.A2019121.h26v03.006.2019137234541.hdf"
# 读取
in_ds = gdal.Open(hdf)
# 重投影
datasets = in_ds.GetSubDatasets()
gdal.Warp('D:/reprojection02.tif', datasets[0][0], dstSRS='EPSG:4326')   # 等经纬度投影, 即地理坐标系投影GCS_WGS_1984
# gdal.Warp('D:/reprojection02.tif', datasets[0][0], dstSRS='EPSG:32649')  # 该投影方式无法与经纬度对标
# print(datasets[0][0])  # 1 km 16 days NDVI
root_ds = None

# dataset = gdal.Open(hdf)
gdal.AllRegister()
dataset = gdal.Open('D:\\reprojection02.tif')

adfGeoTransform = dataset.GetGeoTransform()

# print(dir(dataset))
# 左上角地理坐标
# print(adfGeoTransform[0])
# print(adfGeoTransform[3])
data = dataset.GetRasterBand(1).ReadAsArray() * 0.0001  # 1km edvi 转化行后
# print(data, data.shape)
nXSize = dataset.RasterXSize  # 列数
nYSize = dataset.RasterYSize  # 行数
print("行数:", nYSize, "列数:", nXSize)
arrSlope_x = []  # 用于存储每个像素的（X，Y）坐标
arrSlope_y = []
for i in range(nYSize):
    x_sheet = []
    y_sheet = []
    for j in range(nXSize):
        px = adfGeoTransform[0] + i * adfGeoTransform[1] + j * adfGeoTransform[2]
        py = adfGeoTransform[3] + i * adfGeoTransform[4] + j * adfGeoTransform[5]
        x_sheet.append(px)
        y_sheet.append(py)
    x_sheet = np.array(x_sheet)
    y_sheet = np.array(y_sheet)
    arrSlope_x.append(x_sheet)
    arrSlope_y.append(y_sheet)
arrSlope_x = pd.DataFrame(arrSlope_x)
arrSlope_y = pd.DataFrame(arrSlope_y)
x_out = pd.concat([arrSlope_x], axis=0)
y_out = pd.concat([arrSlope_y], axis=0)
data_out = pd.DataFrame(data)

sheet_name = ["KNN", "ewm", "IDW", "Iterative"]
sheet_name_count = 0  # 为什么显示without usage ?  因为下面如果if为false则..
#writer = pd.ExcelWriter('xy_out.xlsx')
# x_out.to_excel(writer, sheet_name="x")
# y_out.to_excel(writer, sheet_name="y")
# data_out.to_excel(writer, sheet_name="data")
#writer.save()
x_out.to_csv("x.csv")
y_out.to_csv("y.csv")
data_out.to_csv("data.csv")

