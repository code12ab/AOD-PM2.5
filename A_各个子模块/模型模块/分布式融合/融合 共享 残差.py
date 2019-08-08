# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/7/31 9:02
import keras
from keras.layers import Input, Embedding, LSTM, Dense
from keras.models import Model

# 定义共享模型
factor_input = Input(shape=(56,))
factor_x = Embedding(output_dim=512,input_dim=10000)(factor_input)
share_layers = LSTM(64)
out = share_layers(factor_x)
res_x = Model(factor_input, out)############
factor_input_1 = Input(shape=(27,))
factor_input_2 = Input(shape=(13,))
###########
out_1 = res_x(factor_input_1)
out_2 = res_x(factor_input_2)
#############
out_concat = keras.layers.concatenate([out_1, out_2])

out = Dense(1, activation="sigmoid")(out_concat)
res_model = Model([factor_input_1, factor_input_2], out)

print(res_model.summary())
print(out_1.__class__)
print(res_model.__class__)
print(out_1.__class__)

print(out_concat.__class__)





'''
# 定义共享模型
factor_input = Input(shape=(56,))
factor_x = Embedding(output_dim=512,input_dim=10000)(factor_input)
share_layers = LSTM(64)
out = share_layers(factor_x)
res_x = Model(factor_input, out)############
factor_input_1 = Input(shape=(27,))
factor_input_2 = Input(shape=(13,))
###########
#out_1 = res_x(factor_input_1)
out_2 = res_x(factor_input_2)
out_1 = Embedding(output_dim=512,input_dim=10000)(factor_input_1)
out_1 = share_layers(out_1)
#############
out_concat = keras.layers.concatenate([out_1, out_2])

out = Dense(1, activation="sigmoid")(out_concat)
res_model = Model([factor_input_1, factor_input_2], out)
print(res_model.summary())
print(out_1.__class__)



'''













# 主
main_input1 = Input(shape=(100,), dtype='int32', name='main_input1')
main_x1 = Embedding(output_dim=512, input_dim=10000, input_length=100)(main_input1)
# 辅
aux_input1 = Input(shape=(100,), dtype='int32', name='aux_input1')
aux_x1 = Embedding(output_dim=512, input_dim=10000, input_length=100)(aux_input1)
# 定义一个共享层
share_layers = LSTM(64)
main_out1 = share_layers(main_x1)
aux_out1 = share_layers(aux_x1)

# 合并主辅
output_x1 = keras.layers.concatenate([main_x1, aux_x1])
output_x1 = Dense(64, activation='relu')(output_x1)
output_x1 = Dense(1, activation='sigmoid')(output_x1)
model1 = Model(inputs=[main_input1, aux_input1], outputs=output_x1)


#print(model.summary())

# 主22222222222222======================================================================
main_input2 = Input(shape=(100,), dtype='int32', name='main_input2')
main_x2 = Embedding(output_dim=512, input_dim=10000, input_length=100)(main_input2)

# 辅
aux_input2 = Input(shape=(100,), dtype='int32', name='aux_input2')
aux_x2 = Embedding(output_dim=512, input_dim=10000, input_length=100)(aux_input2)

# 定义一个共享层
share_layers = LSTM(64)

main_out2 = share_layers(main_x2)
aux_out2 = share_layers(aux_x2)

output_x2 = keras.layers.concatenate([main_x2, aux_x2])
output_x2 = Dense(64, activation='relu')(output_x2)
output_x2 = Dense(1, activation='sigmoid')(output_x2)
model2 = Model(inputs=[main_input2, aux_input2], outputs=output_x2)
model2.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])

r1 = model1.output
r2 = model2.output
#x3 = keras.layers.concatenate([model1,model2])
x3 = keras.layers.concatenate([r1,r2])  # 合并编译后的tensor；获得模型1
x3 = Dense(64, activation='relu')(x3)
xres = Dense(64, activation='sigmoid')(x3)
model = Model(inputs=[main_input1,aux_input1,main_input2,aux_input2], outputs=xres)

model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
#print(model.summary())