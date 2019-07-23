# -*- coding: utf-8 -*-
# 作者：xcl
# 时间：2019/6/18  20:14

from keras.models import Sequential, Model
from keras import layers, Input
import keras
import numpy as np
import pandas as pd
############ 199
'''
input_tensor = Input(shape=(32,))
dense = layers.Dense(32, activation="relu")
output_tensor = dense(input_tensor)


############ 199
seq_model = Sequential()
seq_model.add(layers.Dense(32, activation="relu", input_shape=(64, )))
seq_model.add(layers.Dense(32, activation="relu"))
seq_model.add(layers.Dense(10, activation="softmax"))

input_tensor = Input(shape=(64, ))
x = layers.Dense(32, activation="relu")(input_tensor)
x = layers.Dense(32, activation="relu")(x)
output_tensor = layers.Dense(10, activation="softmax")(x)

model = Model(input_tensor, output_tensor)
model.summary()
print(x)
'''

text_vocabulary_size = 10000
question_vocabulary_size = 10000
answer_vocabulary_size = 22

text_input = Input(shape=(None,), dtype="int32", name="text")

embedded_text = layers.Embedding(text_vocabulary_size, 64)(text_input)

encoded_text = layers.LSTM(32)(embedded_text)

question_input = Input(shape=(None,), dtype="int32", name="question")

embedded_question =layers.Embedding(question_vocabulary_size, 32)(question_input)

encoded_question = layers.LSTM(16)(embedded_question)

concatenated = layers.concatenate([encoded_text, encoded_question], axis=-1)

answer = layers.Dense(answer_vocabulary_size, activation="softmax")(concatenated)

model = Model([text_input, question_input], answer)
model.compile(optimizer="rmsprop", loss="categorical_crossentropy", metrics=["acc"])



##################      输入数据

num_samples = 1000
max_length = 100

text = np.random.randint(1, text_vocabulary_size, size=(num_samples, max_length))  # 1000个样本 每个100维度
question = np.random.randint(1, question_vocabulary_size, size=(num_samples, max_length))

answer = np.random.randint(answer_vocabulary_size, size=(num_samples))  # 1000个 数字
print(answer)
answer = keras.utils.to_categorical(answer, answer_vocabulary_size)

model.fit([text, question], answer, epochs=1, batch_size=128)

c = model.predict([text, question])
print(c)
c = pd.DataFrame(c)
c.to_excel("c_123.xlsx")