# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/6 20:32

import math
from darksky.api import DarkSky, DarkSkyAsync
from darksky.types import languages, units, weather

API_KEY = "ea6ba6d12b5619189b54f10275557872"


# Synchronous way
darksky = DarkSky(API_KEY)