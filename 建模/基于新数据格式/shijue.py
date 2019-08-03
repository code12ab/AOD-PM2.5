# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/7/31 21:56
import keras
from keras.layers import Input, Embedding, LSTM, Dense
from keras.models import Model

# 定义共享模型
'''
factor_input = Input(shape=(None,))
factor_x = Embedding(output_dim=100000, input_dim=64)(factor_input)
share_layers = LSTM(64)
out = share_layers(factor_x)
res_x = Model(factor_input, out)


factor_input_1 = Input(shape=(27,))
factor_input_2 = Input(shape=(13,))
out_1 = res_x(factor_input_1)
out_2 = res_x(factor_input_2)
out_concat = keras.layers.concatenate([out_1, out_2])

out = Dense(1, activation="sigmoid")(out_concat)
res_model = Model([factor_input_1, factor_input_2], out)

'''

'''
# xiayige

#This returns a tensor
inputs = Input(shape=(784,))

#a Layer instance is callable on a tensor , and returns a tensor
x = Dense(64 , activation='relu')(inputs)
x = Dense(64,activation='relu')(x)
predictions = Dense(10,activation='softmax')(x)

model = Model(inputs=inputs,outputs=predictions)
model.compile(optimizer='rmsprop',loss='categorical_crossentropy',metrics=['accuracy'])

factor_input_1 = Input(shape=(784,))
factor_input_2 = Input(shape=(784,))
out1 = model(factor_input_1)
out2 = model(factor_input_2)
out_concat = keras.layers.concatenate([out1, out2])
out = Dense(1, activation="sigmoid")(out_concat)
res_model = Model([factor_input_1, factor_input_2], out)
print(res_model.summary())
print(out.__class__)

'''




factor_input_1 = Input(shape=(12,))
factor_input_2 = Input(shape=(4,))
factor_input = keras.layers.concatenate([factor_input_1, factor_input_2])
x = Dense(64 , activation='relu')(factor_input)
predictions = Dense(10,activation='softmax')(x)

#model = Model(inputs=[factor_input_1, factor_input_2],outputs=predictions)
#model.compile(optimizer='rmsprop',loss='categorical_crossentropy',metrics=['accuracy'])


factor_input_3 = Input(shape=(12,))
factor_input_4 = Input(shape=(4,))
factor_input = keras.layers.concatenate([factor_input_3, factor_input_4])
x2 = Dense(64 , activation='relu')(factor_input)
predictions2 = Dense(10,activation='softmax')(x2)

#model2 = Model(inputs=[factor_input_3, factor_input_4],outputs=predictions2)
#model2.compile(optimizer='rmsprop',loss='categorical_crossentropy',metrics=['accuracy'])

#res = keras.layers.concatenate([model.output, model2.output])
res = keras.layers.concatenate([predictions,predictions2])
xres = Dense(1, activation='sigmoid')(res)
model = Model(inputs=[factor_input_1,factor_input_2,factor_input_3,factor_input_4], outputs=xres)

model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
print(model.summary())

print(model.__class__)
print(xres.__class__)