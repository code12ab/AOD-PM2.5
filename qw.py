# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/25 15:49


# 库
import pandas as pd
import numpy as np

import datetime
import datetime

end_time = 1525104000
d = datetime.datetime.fromtimestamp(end_time)  # 时间戳转换成字符串日期时间
str1 = d.strftime("%Y-%m-%d %H:%M:%S.%f")
print(d)  # 2018-05-01 00:00:00
print(str1) # 2018-05-01 00:00:00.000000