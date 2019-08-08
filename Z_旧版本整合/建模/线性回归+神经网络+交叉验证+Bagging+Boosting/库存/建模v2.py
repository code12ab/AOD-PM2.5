# -*- coding: utf-8 -*-
# 日期: 2019/3/7 10:21
# 作者: xcl
# 工具：PyCharm


import os
import pandas as pd
import numpy as np

from scipy import stats  # t检验
from sklearn.model_selection import train_test_split, cross_val_score, cross_validate  # 交叉验证所需的函数
from sklearn.model_selection import KFold,LeaveOneOut,LeavePOut,ShuffleSplit  # 交叉验证所需的子集划分方法
from sklearn.model_selection import StratifiedKFold,StratifiedShuffleSplit  # 分层分割
from sklearn.model_selection import GroupKFold,LeaveOneGroupOut, LeavePGroupsOut, GroupShuffleSplit  # 分组分割
from sklearn.model_selection import TimeSeriesSplit  # 时间序列分割
from sklearn import datasets  # 自带数据集
from sklearn import svm  # SVM算法
from sklearn import preprocessing  # 预处理模块
from sklearn.metrics import recall_score  # 模型度量
from sklearn.linear_model import LogisticRegression  # 逻辑回归模型
# OLS
import statsmodels.api as sm  # OLS模型
from statsmodels.stats.outliers_influence import summary_table  # OLS模型
# 多元线性回归
from sklearn import linear_model  # 线性回归模型
from sklearn.linear_model import LinearRegression  # 线性回归模型
from sklearn.metrics import mean_absolute_error, mean_squared_error  # 线性回归 评估误差
# 岭回归
from sklearn.linear_model import Ridge, RidgeCV


input_file_path = "F:\\毕业论文程序\\整合数据\\各地区\\combine\\"
input_file_name = os.listdir(input_file_path)  # 文件名列表

list_outcome = []
for file_name in input_file_name:
    #print(file_name)
    # 读取数据
    input_file = "F:\\毕业论文程序\\整合数据\\各地区\\combine\\"+file_name
    data = pd.read_excel(input_file)
    # print(data.isnull().sum())  # 空值检查

    # 删除PM2.5为空的数据
    data = data[data["PM2.5浓度"] > 0]
    # 删除部分自变量
    data = data.drop(["监测站", "windGust", "windBearing"], axis=1)
    # print(data[["windBearing", "windSpeed"]])

    for key in data.columns:
        data['%s' % key] = data['%s' % key].fillna(0)


    # 划分自变量与因变量
    y_data = data.iloc[:, 2]
    # print(y_data)
    x_data = data.iloc[:, 5:]
    # print(y_data, x_data)
    # print(x_data.columns)
    # 划分测试集,每次运行都随机划分
    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, train_size=0.7, test_size=0.3, random_state=0)
    # 划分结果
    # print("自变量---源数据:", x_data.shape, ";  训练集:", x_train.shape, ";  测试集:", x_test.shape)
    # print("因变量---源数据:", y_data.shape, ";  训练集:", y_train.shape, ";  测试集:", y_test.shape)


    # 线性回归模型,OLS
    '''
    # 普通最小二乘法
    # 未进行湿度-垂直订正,直接进行了回归;模型结果：R方约.85;p值仅有一半变量通过
    # 增加常数项目
    x_train = sm.add_constant(x_train)
    x_test = sm.add_constant(x_test)
    regr = sm.OLS(y_train, x_train)
    res = regr.fit()
    st, data, ss2 = summary_table(res, alpha=0.05)
    print(res.summary())  # p值 R方
    # 模型残差
    # print(res.resid)
    # 训练样本预测值
    # print(res.fittedvalues)
    # 测试样本预测
    # print(res.predict(x_test))
    # 误差简单算例
    a = res.predict(x_test)  # 测试集预测
    b = y_test
    c = a-b  # 差值
    c = abs(c)
    d = c.sum()/len(c)  # 相对误差
    # 模型系数
    print(res.params)
    '''
    # 线性回归模型,LinearRegression

    # 多元线性回归回归没有使用最小二乘法
    # lr = LinearRegression(fit_intercept=True, normalize=False)
    lr = LinearRegression(normalize=True)
    lr.fit(x_train, y_train)
    res = lr.fit(x_train, y_train)
    # lr.get_params(), 模型参数,如是否标准化
    # 回归系数
    # print(lr.coef_)
    # 对测试集数据预测
    y_pred = lr.predict(x_test)
    # print(y_pred-y_test)
    lr_score = lr.score(x_train, y_train, sample_weight=None)  # 样本权重 sample_weight=
    # print("R^2", lr_score)
    # 评估模型
    EE = mean_absolute_error(y_test, y_pred)
    EE2 = mean_squared_error(y_test, y_pred)
    #print("R^2", lr_score, "平均绝对误差：", EE, "均方误差", EE2)
    # 交叉验证 CV
    scores = cross_val_score(lr, x_data, y_data, cv=5)  # cv为迭代次数。
    # print(scores)  # 打印输出每次准确度
    '''
    print(file_name.replace(".xlsx", ""), "R^2", lr_score, "平均绝对误差：", EE, "均方误差", EE2,
          "Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    '''
    outcome = file_name.replace(".xlsx", ""), "R^2", lr_score, "平均绝对误差：", EE, "均方误差", EE2,\
        "Accuracy", "%0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)
    print(outcome)
    list_outcome.append(outcome)










    # 岭回归,Ridge,RidgeCV
    '''
    clf = Ridge(alpha=1, fit_intercept=True, normalize=True)
    # clf = Ridge(alpha=0.88, copy_X=False, fit_intercept=True, max_iter=None, normalize=True, solver='auto', tol=0.001)
    clf.fit(x_train, y_train)
    # print('系数：', clf.coef_, "\n", "截距：", clf.intercept_)
    # 预测
    y_pred = clf.predict(x_test)
    # print(y_pred-y_test)
    # score为拟合优度
    clf.score(x_train, y_train)
    # 岭回归的交叉验证,CV
    clf = RidgeCV(alphas=[0.01, 0.001, .01, 0.5, 1.0], fit_intercept=True, normalize=True)  # 参数为列表形式,调整最优参数
    clf = RidgeCV(alphas=[0.01, 0.001, .01, 0.5, 1.0], fit_intercept=True, normalize=True, cv=10,
                  gcv_mode="auto", scoring=None)  # 参数为列表形式,调整最优参数
    clf.fit(x_train, y_train)
    # print('系数矩阵:\n', clf.coef_)
    print('交叉验证最佳alpha值', clf.alpha_)  # 返回最优的alpha值
    # 预测
    y_pred = clf.predict(x_test)
    # print(y_pred-y_test)
    # 误差
    EE = mean_absolute_error(y_test, y_pred)
    print("平均绝对误差：", EE)
    scores = cross_val_score(clf, x_data, y_data, cv=10)  # 样本CV处理
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))  # 获取置信区间(均值和方差):0.29和0.90
    '''
    # SVM,不适用于连续变量
    '''
    # clf = svm.SVC(kernel='linear', C=1).fit(x_train, y_train)
    # print('准确率：', clf.score(x_test, y_test))  # 计算测试集的度量值（准确率）
    '''

    # 线性回归模型
    # 进行湿度-垂直订正
    # 尚未进行

    # 地理加权回归模型
    # R语言


    # 多阶段模型
    # 尚未进行


list_outcome = pd.DataFrame(list_outcome)
list_outcome.to_excel("list.xlsx")