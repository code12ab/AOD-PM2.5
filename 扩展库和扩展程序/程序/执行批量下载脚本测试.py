# -*- coding: utf-8 -*-
# 时间    : 2019/1/21 14:44
# 作者    : xcl
'''
请使用CMD运行MODIS_download.py
'''



import os
p=os.popen('cd Desktop')
p=os.popen('cd MODIS')
p=os.popen('python MODIS_download_script_from_NASA.py -s https://ladsweb.modaps.eosdis.nasa.gov/archive/orders/501297347/ -d E:\\temp\\modis_download -t 0199091A-1D26-11E9-A7F5-C3B17C49A85D')

