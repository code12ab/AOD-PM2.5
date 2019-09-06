# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/21 10:24


# 库
import pandas as pd
import numpy as np
from osgeo import gdal
import os
# 路径
hdf_input = "e:\\NDVI\\MOD2018\\"
file_name = os.listdir(hdf_input)
# 输出
tif_output_path = "E:\\NDVI\\TIF\\MOD2018\\"
ndvi_raw_output_path = "E:\\NDVI\\NDVI_RAW\\MOD2018\\"
x_output_path = "E:\\NDVI\\X\\MOD2018\\"
y_output_path = "E:\\NDVI\\Y\\MOD2018\\"
# 检查重复
saved_file_list = os.listdir(ndvi_raw_output_path)
saved_file_list = map(lambda x: str(x).replace(".csv", ".hdf"), [x for x in saved_file_list])  # map, lambda
# 转换格式
for name in file_name:
    if name in saved_file_list:
        continue
    # 读取
    in_ds = gdal.Open(hdf_input+name)
    save_name = str(name).replace(".hdf", "")
    # 重投影
    datasets = in_ds.GetSubDatasets()
    gdal.Warp(tif_output_path+'%s.tif' % save_name, datasets[0][0], dstSRS='EPSG:4326')   # 等经纬度投影, 即地理坐标系投影GCS_WGS_1984
    # gdal.Warp('D:/reprojection02.tif', datasets[0][0], dstSRS='EPSG:32649')  # 该投影方式无法与经纬度对标
    # print(datasets[0][0])  # 1 km 16 days NDVI
    root_ds = None
    # 计算 经纬度
    gdal.AllRegister()
    dataset = gdal.Open(tif_output_path+'%s.tif' % save_name)
    adfGeoTransform = dataset.GetGeoTransform()
    # print(dir(dataset))
    # 左上角地理坐标
    # print(adfGeoTransform[0])
    # print(adfGeoTransform[3])
    data = dataset.GetRasterBand(1).ReadAsArray() * 0.0001  # 1km edvi 转化行后
    # print(data, data.shape)
    nXSize = dataset.RasterXSize  # 列数
    nYSize = dataset.RasterYSize  # 行数
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
    # 存
    x_out.to_csv(x_output_path+"%s.csv" % save_name)
    y_out.to_csv(y_output_path+"%s.csv" % save_name)
    data_out.to_csv(ndvi_raw_output_path+"%s.csv" % save_name)
    print("行数:", nYSize, "列数:", nXSize, "已保存")
