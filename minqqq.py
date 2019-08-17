# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/16 23:53

import pandas as pd
from osgeo import gdal

# 路径
hdf = "C:\\Users\\iii\\Desktop\\MYD13A2.A2019121.h26v03.006.2019137234541.hdf"
# 读取
in_ds = gdal.Open(hdf)
# 重投影
datasets = in_ds.GetSubDatasets()
gdal.Warp('D:/reprojection02.tif', datasets[0][0], dstSRS='EPSG:4326')   # 等经纬度投影, 即地理坐标系投影GCS_WGS_1984
#gdal.Warp('D:/reprojection02.tif', datasets[0][0], dstSRS='EPSG:32649')
# print(datasets[0][0])  # 1 km 16 days NDVI
root_ds = None

# dataset = gdal.Open(hdf)
gdal.AllRegister()
dataset = gdal.Open('D:\\reprojection02.tif')

adfGeoTransform = dataset.GetGeoTransform()

print(dir(dataset))
# 左上角地理坐标
# print(adfGeoTransform[0])
# print(adfGeoTransform[3])
data = dataset.GetRasterBand(1).ReadAsArray()  #  1km edvi 转化行后
print(data, data.shape)
nXSize = dataset.RasterXSize  # 列数
nYSize = dataset.RasterYSize  # 行数
print("行数:", nYSize, "列数:", nXSize)

for i in range(nYSize):
    arrSlopeX = []  # 用于存储每个像素的（X，Y）坐标
    arrSlopeY = []

    for j in range(nXSize):
        px = adfGeoTransform[0] + i * adfGeoTransform[1] + j * adfGeoTransform[2]
        py = adfGeoTransform[3] + i * adfGeoTransform[4] + j * adfGeoTransform[5]
        col = [px, py]

        arrSlopeX.append(px)
        arrSlopeY.append(py)

arrSlopeX = pd.DataFrame(arrSlopeX)
arrSlopeY = pd.DataFrame(arrSlopeY)
arrSlopeY.to_excel("yy.xlsx")
arrSlopeX.to_excel("xx.xlsx")
