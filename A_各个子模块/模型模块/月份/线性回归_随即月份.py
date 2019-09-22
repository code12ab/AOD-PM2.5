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
# 不标准化
data_out = pd.concat([data_dummies, data_to_std], join='outer', axis=1)
data_test = data_out[(data_out['tm_mon'] == "3") |
                     (data_out['tm_mon'] == "6") |
                     (data_out['tm_mon'] == "9")]
data_train = data_out[(data_out['tm_mon'] == "1") |
                      (data_out['tm_mon'] == "2") |
                      (data_out['tm_mon'] == '4') |

                      (data_out['tm_mon'] == '5') |
                      (data_out['tm_mon'] == '7') |
                      (data_out['tm_mon'] == '8') |
                      (data_out['tm_mon'] == '10') |
                      (data_out['tm_mon'] == '11') |
                      (data_out['tm_mon'] == '12')]
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


error_AME = []
error_MSE = []
error_RE = []
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
