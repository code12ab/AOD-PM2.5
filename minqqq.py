# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/6 16:59

# 库
import pandas as pd
import numpy as np
import os

# -*- coding: utf-8 -*-
# 时间    : 2019/1/31 11:12
# 作者    : xcl

from pyhdf.SD import SD, SDC
import os, gdal
import pandas as pd

hdf = "C:\\Users\\iii\\Desktop\\MYD13A2.A2019121.h26v03.006.2019137234541.hdf"


hdf = SD(hdf, SDC.READ)

print(hdf.datasets())

data = hdf.select('1 km 16 days NDVI')
attr = hdf.attributes(full=1)
attNames = attr.keys()

print(attNames)
t = attr['ArchiveMetadata.0']
print(t[0])

import osr
proj = osr.SpatialReference()
proj.ImportFromEPSG(4326)
proj.ExportToWkt()

print(proj)

hdf.SetProjection(proj)