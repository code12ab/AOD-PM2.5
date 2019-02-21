# -*- coding: utf-8 -*-
# 时间    : 2019/1/25 10:28
# 作者    : xcl
# 使用情况：2019/2/8

from darksky import forecast  # DarkSkyAPI
import time  # 时间转换
from datetime import datetime as dt  # 日期转换
import pandas as pd  # BDS
import datetime

# 文件格式设置
pd.set_option('display.width', 6666)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大列，None为显示所有列


# 参数设置
year_days = 365
date_start = 2018000
API_KEY = "*"

# 批量导入监测站坐标
JCZ_file = pd.read_excel("监测站坐标to气象.xlsx")
JCZ = []
for i in range(len(JCZ_file)):
    exec('JCZ%s = [JCZ_file["经度"][i],JCZ_file["纬度"][i],JCZ_file["城市"][i]+"-"+JCZ_file["监测点名称"][i]]' % i)
    exec("JCZ.append(JCZ%s)" % i)  # exec可以执行字符串指令
jcz_list = []
# 第一天中午12点起到第二天中午12点结束,需再次验证
for jcz in JCZ:
    JCZ_V0 = API_KEY, jcz[1], jcz[0], jcz[2]  # API_KEY,纬度,经度,监测站
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
output_file_path = "C:\\Users\\寻常鹿\\Desktop\\气象数据\\数据\\"  # 气象数据输出路径
error_information_path = "C:\\Users\\寻常鹿\\Desktop\\气象数据\\报错\\"  # 报错信息输出路径
global t
schedule_whole = 0
for coordinate in jcz_list:
    BOSTON = coordinate[0:3]  # 纬度、经度
    outcome = []
    error = []
    schedule_current = 0
    for time in time_list:
        schedule_whole += 1
        schedule_current += 1
        # noinspection PyBroadException
        try:
            t = dt(time[0], time[1], time[2], 00).isoformat()
            boston = forecast(*BOSTON, time=t, timeout=30)  # 超时报错设置
            DarkSky_outcome = boston['hourly']["data"]  # 输出一天24小时的数据,调用一次API
            # print(coordinate[3], boston['hourly']["data"]) 数据内容
            # 输出到文件
            outcome.append(DarkSky_outcome)
            # 进度
            print("完成:%s" % coordinate[3], "时间:%s" % str(time[0]) + "-" + str(time[1]) + "-" + str(time[2]),
                  "监测站进度:%.2f%%" % (schedule_current / 365 * 100),
                  "总进度:%.2f%%" % (100 * schedule_whole / (len(jcz_list) * 365)))
        except Exception as e:
            print(t, "报错")
            error.append(t)
    count = 0
    df = []
    for item in outcome:
        count += 1
        item = eval(str(item))
        item = pd.DataFrame(item)
        df.append(item)
    if len(df) != 0:
        df_output = pd.concat(df, sort=True)
        df_output['time'] = df_output['time'].map(lambda x: datetime.datetime.fromtimestamp(x))
        df_output = df_output.set_index('time')
        df_output.to_excel(output_file_path+"%s.xlsx" % coordinate[3])
    if len(error) != 0:  # 空列表不输出
        error = pd.DataFrame(error)
        error.to_excel(error_information_path+"%s报错.xlsx" % coordinate[3])
