     # -*- coding: utf-8 -*-
# 作者：xcl
# 时间：2019/6/20  17:49 

from keras.models import Sequential, Model
from keras import layers, Input
import keras
import numpy as np
import pandas as pd


# 读取
data = pd.read_excel("测试用数据.xlsx")
# 设置变量

independent = ["AOD值", 'cloudCover', 'dewPoint', 'humidity', 'precipAccumulation', 'precipIntensity', 'pressure',
               'temperature', 'uvIndex', 'visibility', 'windSpeed', 'windBearing']
T_1 =["AOD值-t-1", 'cloudCover-t-1', 'dewPoint-t-1', 'humidity-t-1', 'precipAccumulation-t-1', 'precipIntensity-t-1', 'pressure-t-1',
               'temperature-t-1', 'uvIndex-t-1', 'visibility-t-1', 'windSpeed-t-1', 'windBearing-t-1', "日均PM2.5-t-1"]
PM_list = ["A1-日均PM2.5-MEAN-t-1", "A2-日均PM2.5-MEAN-t-1", "A3-日均PM2.5-MEAN-t-1", "A4-日均PM2.5-MEAN-t-1",
           "A5-日均PM2.5-MEAN-t-1", "A6-日均PM2.5-MEAN-t-1", "A7-日均PM2.5-MEAN-t-1", "A8-日均PM2.5-MEAN-t-1",
           "B1-日均PM2.5-MEAN-t-1", "B2-日均PM2.5-MEAN-t-1", "B3-日均PM2.5-MEAN-t-1", "B4-日均PM2.5-MEAN-t-1",
           "B5-日均PM2.5-MEAN-t-1", "B6-日均PM2.5-MEAN-t-1", "B7-日均PM2.5-MEAN-t-1", "B8-日均PM2.5-MEAN-t-1"
        ]
dependent = ["日均PM2.5"]
independent = list(set(independent) | set(T_1))  # 合集
#independent = list(set(independent) | set(PM_list))  # 合集




#############################  模型建立部分

text_vocabulary_size = len(data[independent].columns)
question_vocabulary_size = len(data[PM_list].columns)
answer_vocabulary_size = 1

text_input = Input(shape=(None,), name="text")
embedded_text = layers.Embedding(text_vocabulary_size, 64)(text_input)
encoded_text = layers.LSTM(32)(embedded_text)

question_input = Input(shape=(None,), name="question")
embedded_question = layers.Embedding(question_vocabulary_size, 64)(question_input)
encoded_question = layers.LSTM(16)(embedded_question)

concatenated = layers.concatenate([encoded_text, encoded_question], axis=-1)
#concatenated = layers.concatenate([embedded_question, embedded_text], axis=-1)
answer = layers.Dense(56, activation="softmax")(concatenated)

model = Model([text_input, question_input], answer)
model.compile(optimizer="rmsprop", loss="categorical_crossentropy", metrics=["acc"])



##################      输入数据

text = data[PM_list] # 1000个样本 每个100维度
question = data[independent]
answer = data[dependent] # 1000个 数字
answer = keras.utils.to_categorical(answer, answer_vocabulary_size)

model.fit([text, question], answer, epochs=1, batch_size=128)

pre_all = model.predict([text, question])
pre_all = pd.DataFrame(pre_all)
pre_all.to_excel("pre_all.xlsx")