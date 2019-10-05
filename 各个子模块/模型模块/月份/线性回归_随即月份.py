# -*- coding: utf-8 -*-
# 日期: 2019/3/18 9:26
# 作者: xcl
# 工具：PyCharm


from sklearn.linear_model import LinearRegression
from sklearn.utils import shuffle

import numpy as np
from sklearn.utils import check_random_state
from sklearn.ensemble import AdaBoostRegressor
import pandas as pd
from sklearn.model_selection import KFold
import random
# 读取
input_path = 'D:\\雨雪+2018_new_pm_aod.xlsx'
data_all = pd.read_excel(input_path, index_col='日期')
"""
del data_all['pressure_T1']
del data_all['pressure']
"""
data_all = data_all.dropna()
# 打乱
data_all = shuffle(data_all, random_state=1027)

data_ts_df = data_all[['tm_mon', 'tm_mday',
                       'tm_wday', 'tm_yday', 'tm_week', 'id']]
# 虚拟变量
for ccc in data_ts_df.columns:
    data_ts_df[ccc] = data_ts_df[ccc].map(lambda x: str(x))
data_get_dummies1 = pd.get_dummies(data_ts_df[['tm_mon']], drop_first=True)
print(data_get_dummies1.columns)
data_get_dummies2 = pd.get_dummies(data_ts_df[['tm_mday']], drop_first=True)
data_get_dummies3 = pd.get_dummies(data_ts_df[['id']], drop_first=True)
data_dummies = pd.concat([data_get_dummies1,
                          data_get_dummies2,
                          data_get_dummies3,
                          data_ts_df[['tm_mon']]],
                         axis=1)
list1 = []
for ccc in data_dummies.columns:
    # print(ccc)
    if ccc != 'tm_mon':
        list1.append(ccc)

# 去掉无用列
data_to_std = data_all.drop(
    ['tm_mon', 'tm_mday', 'tm_wday', 'tm_yday', 'tm_week', 'id'], axis=1)

# 标准化
"""
data_to_std2 = MinMaxScaler().fit_transform(data_to_std)
data_to_std2 = pd.DataFrame(data_to_std2)
data_to_std2 = data_to_std2.set_index(data_to_std.index)
data_to_std2.columns = data_to_std.columns
data_out = pd.concat([data_dummies, data_to_std2], join='outer', axis=1)
"""
error_AME = []
error_MSE = []
error_RE = []
for t_numb in range(0, 10):
    data_ts_df = data_all[['tm_mon', 'tm_mday',
                           'tm_wday', 'tm_yday', 'tm_week', 'id']]
    # 虚拟变量
    for ccc in data_ts_df.columns:
        data_ts_df[ccc] = data_ts_df[ccc].map(lambda x: str(x))
    data_get_dummies1 = pd.get_dummies(data_ts_df[['tm_mon']], drop_first=True)
    # print(data_get_dummies1.columns)
    data_get_dummies2 = pd.get_dummies(data_ts_df[['tm_mday']], drop_first=True)
    data_get_dummies3 = pd.get_dummies(data_ts_df[['id']], drop_first=True)
    data_dummies = pd.concat([data_get_dummies1,
                              data_get_dummies2,
                              data_get_dummies3,
                              data_ts_df[['tm_mon']]],
                             axis=1)
    list1 = []
    for ccc in data_dummies.columns:
        # print(ccc)
        if ccc != 'tm_mon':
            list1.append(ccc)

    # 去掉无用列
    data_to_std = data_all.drop(
        ['tm_mon', 'tm_mday', 'tm_wday', 'tm_yday', 'tm_week', ], axis=1)

    # 不标准化
    data_out = pd.concat([data_dummies, data_to_std], join='outer', axis=1)
    # 划分
    idlist = list(range(1, 13))
    slice1 = random.sample(idlist, 4)  # 从list中随机获取5个元素，作为一个片断返回
    slice2 = []
    for idx in idlist:
        if idx not in slice1:
            idx = str(idx)
            slice2.append(idx)
    slice1 = [str(j) for j in slice1]

    data_test = data_out[data_out["tm_mon"].isin(slice1)]
    data_train = data_out[data_out["tm_mon"].isin(slice2)]
    # 不标准化
    data_out = pd.concat([data_dummies, data_to_std], join='outer', axis=1)

    # 自变量列
    independent = [
                   'AOD_0',
                   'tm_mon_10',
                   'tm_mon_11',
                   'tm_mon_12',
                   'tm_mon_2',
                   'tm_mon_3',
                   'tm_mon_4',
                   'tm_mon_5',
                   'tm_mon_6',
                   'tm_mon_7',
                   'tm_mon_8',
                   'tm_mon_9',
                   'AOD_0_T1',
                   'cloudCover_T1',
                   'dewPoint_T1',
                   'humidity_T1',
                   'sunTime_T1',
                   'visibility_T1',
                   'windSpeed_T1',
                   'temperature_T1',
                   'pressure_T1',
                   'precipIntensity_T1',
                   'precipAccumulation_T1',
                   'NDVI_0',
                   'cloudCover',
                   'dewPoint',
                   'humidity',
                   'sunTime',
                   'visibility',
                   'windBearing',
                   'windGust',
                   'windSpeed',
                   'apparentTemperature',
                   'temperature',
                   'tempMM',
                   'tempHL',
                   'atempMM',
                   'atempHL',
                   'pressure',
                   'precipIntensity',
                   'precipAccumulation',
                   'AOD_1',
                   'AOD_2',
                   'AOD_3',
                   'AOD_4',
                   'AOD_5',
                   'AOD_6',
                   'AOD_7',
                   'AOD_8',
                   'AOD_9',
                   'AOD_10',
                   'AOD_11',
                   'AOD_12',
                   'AOD_13',
                   'AOD_14',
                   'AOD_15',
                   'AOD_16', ]
    for clo in data_get_dummies3.columns:
        independent.append(clo)
    # 因变量
    dependent = ["PM25"]

    # 打乱
    data = shuffle(data_out)


    # k折分组



    # 参数设置
    mlp = LinearRegression(fit_intercept=True)
    rng = check_random_state(0)
    # 划分
    x_train = data_train[independent].values
    x_test = data_test[independent].values
    y_train = data_train[dependent].values.ravel()
    y_test = data_test[dependent].values.ravel()
    ensemble = AdaBoostRegressor(base_estimator=mlp, learning_rate=0.001,
                                 loss='linear').fit(x_train, y_train)
    res = ensemble.predict(x_test)
    # print(res, y_test)
    # 格式转换
    res = pd.DataFrame(res)
    y_test = pd.DataFrame(y_test)
    # 相同索引方便合并
    res.index = y_test.index
    data_pred = pd.concat([res, y_test], axis=1)
    data_pred.columns = ["pre", "true"]
    # 计算误差AME
    e_AME = abs(data_pred["pre"] - data_pred["true"]).mean()
    e_RE = abs(data_pred["pre"] - data_pred["true"]).div(data_pred["true"]).mean()
    # print("AME误差:", e)
    e_MSE = ((data_pred["pre"] - data_pred["true"])**2).mean()
    error_AME.append(e_AME)
    error_MSE.append(e_MSE)
    error_RE.append(e_RE)
print(
        "交叉验证后的平均AME误差值:",
        np.average(error_AME),
        "\n",
        "预测结果的标准差",
        np.std(error_AME))
print(
        "交叉验证后的平均MSE误差值:",
        np.average(error_MSE),
        "\n",
        "预测结果的标准差",
        np.std(error_MSE))
print(
        "交叉验证后的平均RE误差值:",
        np.average(error_RE),
        "\n",
        "预测结果的标准差",
        np.std(error_RE))
