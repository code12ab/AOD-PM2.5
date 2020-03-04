# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/10/11 20:38


# 库
from mgwr.gwr import GWR
import pandas as pd
import random
import os
import datetime
import copy
import numpy as np
from mgwr.sel_bw import Sel_BW

input_path = 'D:\\data - 副本.xlsx'
data_all = pd.read_excel(input_path, index_col='日期')
# 预设
data_all = data_all.dropna()
data_ts_df = data_all[['tm_mon', 'id']]
# 虚拟变量
for ccc in data_ts_df.columns:
    data_ts_df[ccc] = data_ts_df[ccc].map(lambda x: str(x))
data_get_dummies1 = pd.get_dummies(data_ts_df[['tm_mon']], drop_first=True)
data_get_dummies3 = pd.get_dummies(data_ts_df[['id']], drop_first=True)
data_dummies = pd.concat([data_get_dummies1,
                          data_get_dummies3,
                          data_ts_df[['tm_mon']],
                          data_ts_df[['id']]],
                         axis=1)
# 去掉不标准化列
data_to_std = data_all.drop(['tm_mon', 'id' ], axis=1)
# 标准化
data_std = copy.deepcopy(data_to_std)
mean_pm = data_std['PM25'].mean()
std_pm = data_std['PM25'].std()

for col in data_std:
    mean = data_std[col].mean()
    std = data_std[col].std()
    data_std[col] = data_std[col].map(lambda x:(x-mean)/std)
# 标准化后的数据矩阵
data_out = pd.concat([data_dummies, data_std], join='outer', axis=1)
# 标准化前的数据矩阵
data_out2 = pd.concat([data_dummies, data_to_std], join='outer', axis=1)  # 标准化前的真实值
# 格式
data_out['tm_mon'] = data_out['tm_mon'].map(lambda x: int(x))
# 耗时
time_list = []


# 整体选择一个最优带宽
# AOD
aod0 = np.array(data_out.AOD_0).reshape((-1, 1))
# AODs
aod1 = np.array(data_out.AOD_1).reshape((-1, 1))
aod2 = np.array(data_out.AOD_2).reshape((-1, 1))
aod3 = np.array(data_out.AOD_3).reshape((-1, 1))
aod4 = np.array(data_out.AOD_4).reshape((-1, 1))
aod5 = np.array(data_out.AOD_5).reshape((-1, 1))
aod6 = np.array(data_out.AOD_6).reshape((-1, 1))
aod7 = np.array(data_out.AOD_7).reshape((-1, 1))
aod8 = np.array(data_out.AOD_8).reshape((-1, 1))
aod9 = np.array(data_out.AOD_9).reshape((-1, 1))
aod10 = np.array(data_out.AOD_10).reshape((-1, 1))
aod11 = np.array(data_out.AOD_11).reshape((-1, 1))
aod12 = np.array(data_out.AOD_12).reshape((-1, 1))
aod13 = np.array(data_out.AOD_13).reshape((-1, 1))
aod14 = np.array(data_out.AOD_14).reshape((-1, 1))
aod15 = np.array(data_out.AOD_15).reshape((-1, 1))
aod16 = np.array(data_out.AOD_16).reshape((-1, 1))
# 气象
cloudCover = np.array(data_out.cloudCover).reshape((-1, 1))
dewPoint = np.array(data_out.dewPoint).reshape((-1, 1))
humidity = np.array(data_out.humidity).reshape((-1, 1))
sunTime = np.array(data_out.sunTime).reshape((-1, 1))
tempMM = np.array(data_out.tempMM).reshape((-1, 1))
tempHL = np.array(data_out.tempHL).reshape((-1, 1))
atempMM = np.array(data_out.atempMM).reshape((-1, 1))
atempHL = np.array(data_out.atempHL).reshape((-1, 1))
visibility = np.array(data_out.visibility).reshape((-1, 1))
windGust = np.array(data_out.windGust).reshape((-1, 1))
windSpeed = np.array(data_out.windSpeed).reshape((-1, 1))
windBearing = np.array(data_out.windBearing).reshape((-1, 1))
apparentTemperature = np.array(data_out.apparentTemperature).reshape((-1, 1))
temperature = np.array(data_out.temperature).reshape((-1, 1))
pressure = np.array(data_out.pressure).reshape((-1, 1))
precipIntensity = np.array(data_out.precipIntensity).reshape((-1, 1))
precipAccumulation = np.array(data_out.precipAccumulation).reshape((-1, 1))
# 时滞
aod0_T1 = np.array(data_out.AOD_0_T1).reshape((-1, 1))
cloudCover_T1 = np.array(data_out.cloudCover_T1).reshape((-1, 1))
dewPoint_T1 = np.array(data_out.dewPoint_T1).reshape((-1, 1))
humidity_T1 = np.array(data_out.humidity_T1).reshape((-1, 1))
sunTime_T1 = np.array(data_out.sunTime_T1).reshape((-1, 1))
visibility_T1 = np.array(data_out.visibility_T1).reshape((-1, 1))
windSpeed_T1 = np.array(data_out.windSpeed_T1).reshape((-1, 1))
temperature_T1 = np.array(data_out.temperature_T1).reshape((-1, 1))
pressure_T1 = np.array(data_out.pressure_T1).reshape((-1, 1))
precipIntensity_T1 = np.array(data_out.precipIntensity_T1).reshape((-1, 1))
precipAccumulation_T1 = np.array(data_out.precipAccumulation_T1).reshape((-1, 1))
# NDVI
ndvi = np.array(data_out.NDVI_0).reshape((-1, 1))
# 时间节点
mon = np.array(data_out.tm_mon).reshape((-1, 1))
# 设置
coords = list(zip(data_out['经度'], data_out['纬度']))
# x = np.hstack([aod0, ndvi, aod0_T1])
x = np.hstack(
    [aod0, aod1, aod2, aod3, aod4, aod5, aod6, aod7, aod8,
     aod9,
     aod10, aod11, aod12, aod13, aod14, aod15, aod16,
     cloudCover, dewPoint, humidity, sunTime, tempMM, tempHL, atempMM,
     atempHL, visibility,
     windGust, windSpeed, windBearing, apparentTemperature, temperature, pressure,
     precipIntensity, precipAccumulation,
     aod0_T1, cloudCover_T1, dewPoint_T1, humidity_T1, sunTime_T1, visibility_T1,
     windSpeed_T1,
     temperature_T1, pressure_T1, precipIntensity_T1, precipAccumulation_T1,
     ndvi, mon])
y = np.array(data_out.PM25).reshape((-1, 1))

# bw
# bw = Sel_BW(coords, y, x).search(criterion='AICc')
bw = 1096
# ==================================================================================

for method in ['tm_mon', 'id']:
    # 误差
    MAE_list = []
    RE_list = []
    MSE_list = []
    for t_numb in range(0, 1):  # 实验次数
        # 划分
        if method == "tm_mon":
            idlist = list(range(1, 13))
            slice1 = random.sample(idlist, 3)  # 从list中随机获取3个元素，作为一个片断返回
            slice2 = []
            for idx in idlist:
                if idx not in slice1:
                    idx = str(idx)
                    slice2.append(idx)
            slice1 = [str(j) for j in slice1]
        else:
            idlist = list(range(1, 153))
            slice1 = random.sample(idlist, 38)  # 从list中随机获取3个元素，作为一个片断返回
            slice2 = []
            for idx in idlist:
                if idx not in slice1:
                    idx = str(idx)
                    slice2.append(idx)
            slice1 = [str(j) for j in slice1]

        # 划分不标准化下的训练集测试集, 用于检验
        data_test2 = data_out2[data_out2["%s" % method].isin(slice1)]
        # print(data_test2.PM25)  # 这才是真实值
    
        # 划分标准化后的训练集测试集, 用于训练
        data_test = data_out[data_out["%s" % method].isin(slice1)]
        data_train = data_out[data_out["%s" % method].isin(slice2)]
    
        # 训练坐标
        coords_train = list(zip(data_train['经度'], data_train['纬度']))
        # 验证坐标
        coords_test = list(zip(data_test['经度'], data_test['纬度']))
        coords_test = np.array(coords_test)
        # 训练
        # AOD
        aod0_train = np.array(data_train.AOD_0).reshape((-1, 1))
        # AODs
        aod1_train = np.array(data_train.AOD_1).reshape((-1, 1))
        aod2_train = np.array(data_train.AOD_2).reshape((-1, 1))
        aod3_train = np.array(data_train.AOD_3).reshape((-1, 1))
        aod4_train = np.array(data_train.AOD_4).reshape((-1, 1))
        aod5_train = np.array(data_train.AOD_5).reshape((-1, 1))
        aod6_train = np.array(data_train.AOD_6).reshape((-1, 1))
        aod7_train = np.array(data_train.AOD_7).reshape((-1, 1))
        aod8_train = np.array(data_train.AOD_8).reshape((-1, 1))
        aod9_train = np.array(data_train.AOD_9).reshape((-1, 1))
        aod10_train = np.array(data_train.AOD_10).reshape((-1, 1))
        aod11_train = np.array(data_train.AOD_11).reshape((-1, 1))
        aod12_train = np.array(data_train.AOD_12).reshape((-1, 1))
        aod13_train = np.array(data_train.AOD_13).reshape((-1, 1))
        aod14_train = np.array(data_train.AOD_14).reshape((-1, 1))
        aod15_train = np.array(data_train.AOD_15).reshape((-1, 1))
        aod16_train = np.array(data_train.AOD_16).reshape((-1, 1))
        # 气象
        cloudCover_train = np.array(data_train.cloudCover).reshape((-1, 1))
        dewPoint_train = np.array(data_train.dewPoint).reshape((-1, 1))
        humidity_train = np.array(data_train.humidity).reshape((-1, 1))
        sunTime_train = np.array(data_train.sunTime).reshape((-1, 1))
        tempMM_train = np.array(data_train.tempMM).reshape((-1, 1))
        tempHL_train = np.array(data_train.tempHL).reshape((-1, 1))
        atempMM_train = np.array(data_train.atempMM).reshape((-1, 1))
        atempHL_train = np.array(data_train.atempHL).reshape((-1, 1))
        visibility_train = np.array(data_train.visibility).reshape((-1, 1))
        windGust_train = np.array(data_train.windGust).reshape((-1, 1))
        windSpeed_train = np.array(data_train.windSpeed).reshape((-1, 1))
        windBearing_train = np.array(data_train.windBearing).reshape((-1, 1))
        apparentTemperature_train = np.array(data_train.apparentTemperature).reshape((-1, 1))
        temperature_train = np.array(data_train.temperature).reshape((-1, 1))
        pressure_train = np.array(data_train.pressure).reshape((-1, 1))
        precipIntensity_train = np.array(data_train.precipIntensity).reshape((-1, 1))
        precipAccumulation_train = np.array(data_train.precipAccumulation).reshape((-1, 1))
        # 时滞
        aod0_T1_train = np.array(data_train.AOD_0_T1).reshape((-1, 1))
        cloudCover_T1_train = np.array(data_train.cloudCover_T1).reshape((-1, 1))
        dewPoint_T1_train = np.array(data_train.dewPoint_T1).reshape((-1, 1))
        humidity_T1_train = np.array(data_train.humidity_T1).reshape((-1, 1))
        sunTime_T1_train = np.array(data_train.sunTime_T1).reshape((-1, 1))
        visibility_T1_train = np.array(data_train.visibility_T1).reshape((-1, 1))
        windSpeed_T1_train = np.array(data_train.windSpeed_T1).reshape((-1, 1))
        temperature_T1_train = np.array(data_train.temperature_T1).reshape((-1, 1))
        pressure_T1_train = np.array(data_train.pressure_T1).reshape((-1, 1))
        precipIntensity_T1_train = np.array(data_train.precipIntensity_T1).reshape((-1, 1))
        precipAccumulation_T1_train = np.array(data_train.precipAccumulation_T1).reshape((-1, 1))
        # NDVI
        ndvi_train = np.array(data_train.NDVI_0).reshape((-1, 1))
        # 时间节点
        mon_train =np.array(data_train.tm_mon).reshape((-1,1))
    
    
        # 验证
        # AOD
        aod0_test = np.array(data_test.AOD_0).reshape((-1, 1))
        # AODs
        aod1_test = np.array(data_test.AOD_1).reshape((-1, 1))
        aod2_test = np.array(data_test.AOD_2).reshape((-1, 1))
        aod3_test = np.array(data_test.AOD_3).reshape((-1, 1))
        aod4_test = np.array(data_test.AOD_4).reshape((-1, 1))
        aod5_test = np.array(data_test.AOD_5).reshape((-1, 1))
        aod6_test = np.array(data_test.AOD_6).reshape((-1, 1))
        aod7_test = np.array(data_test.AOD_7).reshape((-1, 1))
        aod8_test = np.array(data_test.AOD_8).reshape((-1, 1))
        aod9_test = np.array(data_test.AOD_9).reshape((-1, 1))
        aod10_test = np.array(data_test.AOD_10).reshape((-1, 1))
        aod11_test = np.array(data_test.AOD_11).reshape((-1, 1))
        aod12_test = np.array(data_test.AOD_12).reshape((-1, 1))
        aod13_test = np.array(data_test.AOD_13).reshape((-1, 1))
        aod14_test = np.array(data_test.AOD_14).reshape((-1, 1))
        aod15_test = np.array(data_test.AOD_15).reshape((-1, 1))
        aod16_test = np.array(data_test.AOD_16).reshape((-1, 1))
        # 气象
        cloudCover_test = np.array(data_test.cloudCover).reshape((-1, 1))
        dewPoint_test = np.array(data_test.dewPoint).reshape((-1, 1))
        humidity_test = np.array(data_test.humidity).reshape((-1, 1))
        sunTime_test = np.array(data_test.sunTime).reshape((-1, 1))
        tempMM_test = np.array(data_test.tempMM).reshape((-1, 1))
        tempHL_test = np.array(data_test.tempHL).reshape((-1, 1))
        atempMM_test = np.array(data_test.atempMM).reshape((-1, 1))
        atempHL_test = np.array(data_test.atempHL).reshape((-1, 1))
        visibility_test = np.array(data_test.visibility).reshape((-1, 1))
        windGust_test = np.array(data_test.windGust).reshape((-1, 1))
        windSpeed_test = np.array(data_test.windSpeed).reshape((-1, 1))
        windBearing_test = np.array(data_test.windBearing).reshape((-1, 1))
        apparentTemperature_test = np.array(data_test.apparentTemperature).reshape((-1, 1))
        temperature_test = np.array(data_test.temperature).reshape((-1, 1))
        pressure_test = np.array(data_test.pressure).reshape((-1, 1))
        precipIntensity_test = np.array(data_test.precipIntensity).reshape((-1, 1))
        precipAccumulation_test = np.array(data_test.precipAccumulation).reshape((-1, 1))
        # 时滞
        aod0_T1_test = np.array(data_test.AOD_0_T1).reshape((-1, 1))
        cloudCover_T1_test = np.array(data_test.cloudCover_T1).reshape((-1, 1))
        dewPoint_T1_test = np.array(data_test.dewPoint_T1).reshape((-1, 1))
        humidity_T1_test = np.array(data_test.humidity_T1).reshape((-1, 1))
        sunTime_T1_test = np.array(data_test.sunTime_T1).reshape((-1, 1))
        visibility_T1_test = np.array(data_test.visibility_T1).reshape((-1, 1))
        windSpeed_T1_test = np.array(data_test.windSpeed_T1).reshape((-1, 1))
        temperature_T1_test = np.array(data_test.temperature_T1).reshape((-1, 1))
        pressure_T1_test = np.array(data_test.pressure_T1).reshape((-1, 1))
        precipIntensity_T1_test = np.array(data_test.precipIntensity_T1).reshape((-1, 1))
        precipAccumulation_T1_test = np.array(data_test.precipAccumulation_T1).reshape((-1, 1))
        # NDVI
        ndvi_test = np.array(data_test.NDVI_0).reshape((-1, 1))
        # 时间节点
        mon_test =np.array(data_test.tm_mon).reshape((-1, 1))
    
    
        # 训练
        """
    
        x_train = np.hstack([aod0_train,
                             ndvi_train,  aod0_T1_train])
        x_train = np.hstack([aod0_train, cloudCover_train, humidity_train,
                             windSpeed_train, windBearing_train,
                             temperature_train, pressure_train,
                             ndvi_train,  aod0_T1_train])

        """

        x_train = np.hstack([aod0_train,aod1_train,aod2_train,aod3_train,aod4_train, aod5_train, aod6_train, aod7_train, aod8_train, aod9_train,
                             aod10_train, aod11_train, aod12_train, aod13_train, aod14_train, aod15_train, aod16_train,
                             cloudCover_train, dewPoint_train, humidity_train, sunTime_train, tempMM_train, tempHL_train, atempMM_train, atempHL_train, visibility_train,
                             windGust_train, windSpeed_train, windBearing_train, apparentTemperature_train, temperature_train, pressure_train, precipIntensity_train, precipAccumulation_train,
                             aod0_T1_train, cloudCover_T1_train, dewPoint_T1_train, humidity_T1_train, sunTime_T1_train, visibility_T1_train, windSpeed_T1_train,
                             temperature_T1_train, pressure_T1_train, precipIntensity_T1_train, precipAccumulation_T1_train,
                             ndvi_train, mon_train])
        # 验证
        """
        x_test = np.hstack([aod0_test,
                            ndvi_test,  aod0_T1_test])

        x_test = np.hstack([aod0_test, cloudCover_test, humidity_test,
                            windSpeed_test, windBearing_test,
                            temperature_test, pressure_test,
                            ndvi_test,  aod0_T1_test])
        """
        x_test = np.hstack([aod0_test,aod1_test,aod2_test,aod3_test,aod4_test, aod5_test, aod6_test, aod7_test, aod8_test, aod9_test,
                            aod10_test, aod11_test, aod12_test, aod13_test, aod14_test, aod15_test, aod16_test,
                            cloudCover_test, dewPoint_test, humidity_test, sunTime_test, tempMM_test, tempHL_test, atempMM_test, atempHL_test, visibility_test,
                            windGust_test, windSpeed_test, windBearing_test, apparentTemperature_test, temperature_test, pressure_test, precipIntensity_test, precipAccumulation_test,
                            aod0_T1_test, cloudCover_T1_test, dewPoint_T1_test, humidity_T1_test, sunTime_T1_test, visibility_T1_test, windSpeed_T1_test,
                            temperature_T1_test, pressure_T1_test, precipIntensity_T1_test, precipAccumulation_T1_test,
                            ndvi_test, mon_test])

        # 训练
        y_train = np.array(data_train.PM25).reshape((-1, 1))
        # 验证
        y_test = np.array(data_test.PM25).reshape((-1, 1))
        # 计算耗时
        starttime = datetime.datetime.now()
    
        # 测试 自动BW Golden section search CV - adaptive bisquare
        # bw = Sel_BW(coords_train, y_train, x_train).search(criterion='AICc')

        # 坐标导致了奇异矩阵；当BW=900时,解决了这一问题
        model = GWR(coords_train, y_train, x_train, bw=bw, fixed=False, kernel='bisquare')
        results = model.fit()
    
        # 耗时
        endtime = datetime.datetime.now()
        t_gap = endtime - starttime
        time_list.append(t_gap.seconds)
        # 预测
        res = model.predict(coords_test, x_test)
    
        # 误差
        res2 = pd.DataFrame(res.predy, index=data_test2.index, columns=['PM25'])
        res2.PM25 = res2.PM25.map(lambda x: x*std_pm + mean_pm)
        # 真实值
        datares = res2 - data_test2[['PM25']]  # 预测-真实
        # print(datares)
        datares.PM25 = datares.PM25.map(lambda x: abs(x))
        data_predt = pd.concat([datares, data_test2.PM25], axis=1)  # 标准化后真值变化了 需要修改
    
        data_predt.columns = ["差值", '真']
        data_predt['差值'] = data_predt['差值'].map(lambda x: abs(x))
        data_predt['百分误'] = data_predt['差值'].div(data_predt["真"])
        data_predt['差值2'] = data_predt['差值'].map(lambda x: x ** 2)
    
        MAE = np.average(data_predt['差值'])
        RE = np.average(data_predt['百分误'])
        MSE = np.average(data_predt['差值2'])
        print('第%s次实验, mae:' % t_numb, np.average(data_predt['差值']))
        print('第%s次实验, re:' % t_numb, np.average(data_predt['百分误']))
        print('第%s次实验, mse:' % t_numb, np.average(data_predt['差值2']))
        MSE_list.append(MSE)
        RE_list.append(RE)
        MAE_list.append(MAE)
    
    print('mae', np.average(MAE_list))
    print('re', np.average(RE_list))
    print('mse', np.average(MSE_list))
    
    a = []
    a.append(MAE_list)
    a.append(RE_list)
    a.append(MSE_list)
    
    a = pd.DataFrame(a)
    a.to_excel('GWR_%s_标准化.xlsx' % method)
print('平均耗时', np.average(time_list))
print('总耗时', np.sum(time_list))

print(bw)
# os.system('shutdown -s -f -t 60')

