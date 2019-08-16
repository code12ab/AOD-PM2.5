# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/7/15 13:02

# 库
import gdal, osr


def array2raster(newRasterfn, rasterOrigin, xsize, ysize, array):
    """
    newRasterfn: 输出tif路径
    rasterOrigin: 原始栅格数据路径
    xsize: x方向像元大小
    ysize: y方向像元大小
    array: 计算后的栅格数据
    """
    cols = array.shape[1]
    rows = array.shape[0]
    originX = rasterOrigin[0]  # 起始像元经度
    originY = rasterOrigin[1]
    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Float32)
    # 括号中两个0表示起始像元的行列号从(0,0)开始
    outRaster.SetGeoTransform((originX, xsize, 0, originY, 0, ysize))
    # 获取数据集第一个波段，是从1开始，不是从0开始
    outband = outRaster.GetRasterBand(1)
    outband.WriteArray(array)
    outRasterSRS = osr.SpatialReference()
    # 代码4326表示WGS84坐标
    outRasterSRS.ImportFromEPSG(4326)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()


ds = gdal.Open('C:\\Users\\iii\\Desktop\\MYD13A2.A2019121.h26v03.006.2019137234541.hdf')

subdatasets = ds.GetSubDatasets()
ndvi_ds = gdal.Open(subdatasets[0][0]).ReadAsArray()

dst_filename = "D:/DATA/try.tif"
xsize = 0.0025
ysize = 0.0025


array2raster(dst_filename, [90, 75], xsize, ysize, ndvi_ds)