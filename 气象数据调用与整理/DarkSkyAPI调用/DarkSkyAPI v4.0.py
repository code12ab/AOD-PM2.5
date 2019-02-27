# -*- coding: utf-8 -*-
# 时间    : 2019/1/25 10:28
# 作者    : xcl
# 版本    ：v3.0

from darksky import forecast  # DarkSkyAPI
import time  # 年度时间范围生成
from datetime import datetime as dt  # 时间戳日期转换
import pandas as pd  # BDS
# import datetime

# 文件格式设置
pd.set_option('display.width', 6666)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大列，None为显示所有列

# 参数设置
year_days = 365  # 365
date_start = 2018000
API_KEY = "a5fc93a6781f6d55e7899ae443acd876"
coordinate_file_path = "F:\\毕业论文程序\\MODIS\\坐标\\"
output_file_path = "F:\\毕业论文程序\\气象数据\\数据\\"  # 气象数据输出路径
error_information_path = "F:\\毕业论文程序\\气象数据\\报错\\"  # 报错信息输出路径
time_out = 30  # 超时设置,10秒太短

# 批量导入监测站坐标
# JCZ_file = pd.read_excel("监测站坐标toDarkSkyAPI.xlsx")
JCZ_file = pd.read_excel(coordinate_file_path+"剩余.xlsx")  # 监测站坐标toDarkSkyAPI
JCZ = []
for i in range(len(JCZ_file)):
    exec('JCZ%s = [JCZ_file["经度"][i],JCZ_file["纬度"][i],JCZ_file["城市"][i]+"-"+JCZ_file["监测点名称"][i]]' % i)
    exec("JCZ.append(JCZ%s)" % i)  # exec可以执行字符串指令
jcz_list = []
for jcz in JCZ:
    JCZ_V0 = API_KEY, jcz[1], jcz[0], jcz[2]  # API_KEY,纬度,经度,监测站,注意格式是先"纬度"后"经度"
    jcz_list.append(JCZ_V0)

# 一年日期
time_list = []
date_int = []
for j in range(year_days):
    date_start += 1
    date = str(date_start)  # 如2018123
    date = time.strptime(date, '%Y%j')
    date = date[0], date[1], date[2]
    time_list.append(date)

# 基本信息
print("监测站个数:", len(jcz_list), "天数:", len(time_list),
      "即" + str(time_list[0]) + "至" + str(time_list[-1]))

# 主程序
global t


def get_outcome(date_time):
    # 定义气象数据获取函数,增加了语言lang=["zh"]
    monitoring_station = forecast(*MonitoringStation, time=date_time, timeout=time_out, lang=["zh"])  # 超时报错设置
    darksky_outcome = monitoring_station['hourly']["data"]  # 输出一天24小时的数据,调用一次API
    # 第一天0时至23时
    # print(coordinate[3], monitoring_station['hourly']["data"]) 数据内容
    # 输出到文件
    outcome.append(darksky_outcome)
    return outcome


# 监测站循环
for coordinate in jcz_list:
    MonitoringStation = coordinate[0:3]  # API_KEY、纬度、经度
    outcome = []
    error = []
    # 一年循环
    for time in time_list:
        # noinspection PyBroadException
        try:
            t = dt(time[0], time[1], time[2], 00).isoformat()
            get_outcome(t)
            # 进度
            print("完成:%s" % coordinate[3], "时间:%s" % t)
        except Exception as e:
            print(t, "报错")
            error.append(t)  # 保存报错日期
    # print("old", error)
    # 报错日期循环
    print("接下来执行报错日期数据重新获取")
    while len(error) != 0:
        error_update = []
        print("%s 未获取数据的天数:" % coordinate[3], len(error))
        for error_time in error:
            # print(error_time)
            print("重新获取%s" % coordinate[3], error_time)
            # noinspection PyBroadException
            try:
                get_outcome(error_time)
                print("重新获取成功")
            except Exception as e:
                print("重新获取失败,稍后重新获取")
                error_update.append(error_time)
        error = error_update
    df = []
    for item in outcome:
        item = eval(str(item))
        item = pd.DataFrame(item)
        df.append(item)
    if len(df) != 0:
        df_output = pd.concat(df, sort=True)
        df_output['time'] = df_output['time'].map(lambda x: dt.fromtimestamp(x))  # datetime.datetime
        df_output = df_output.sort_values("time", ascending=True)
        df_output = df_output.set_index('time')
        df_output.to_excel(output_file_path+"%s.xlsx" % coordinate[3])
    if len(error) != 0:  # 空列表不输出,代码经过修改已经没有"error"列表了,以防万一保存了该部分代码
        error = pd.DataFrame(error)
        error.columns = ["Index", '日期']
        error.to_excel(error_information_path+"%s报错.xlsx" % coordinate[3])

print("完成啦")
