# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/7/31 9:02
import keras
from keras.layers import Input, Embedding, LSTM, Dense
from keras.models import Model

# 标题输入：接收一个含有 100 个整数的序列，每个整数在 1 到 10000 之间。
# 注意我们可以通过传递一个 `name` 参数来命名任何层。
main_input = Input(shape=(100,), dtype='int32', name='main_input')
# Embedding 层将输入序列编码为一个稠密向量的序列，每个向量维度为 512。
x = Embedding(output_dim=512, input_dim=10000, input_length=100)(main_input)

##########################上下变量虽然融合到一个模型但是是各自由各自的权重，因此需要添加共享层。见收藏夹

# LSTM 层把向量序列转换成单个向量，它包含整个序列的上下文信息
lstm_out = LSTM(32)(x)
#插入辅助损失，使得即使在模型主损失很高的情况下，LSTM 层和 Embedding 层都能被平稳地训练。
auxiliary_output = Dense(1, activation='sigmoid', name='aux_output')(lstm_out)

#  LSTM 层的输出作为辅助输入数据
auxiliary_input = Input(shape=(5,), name='aux_input')
x = keras.layers.concatenate([lstm_out, auxiliary_input])

# 堆叠多个全连接网络层
x = Dense(64, activation='relu')(x)
x = Dense(64, activation='relu')(x)
x = Dense(64, activation='relu')(x)

# 最后添加主要的逻辑回归层
main_output = Dense(1, activation='sigmoid', name='main_output')(x)

#定义一个具有两个输入和两个输出的模型
model = Model(inputs=[main_input, auxiliary_input], outputs=[main_output, auxiliary_output])

#编译模型，给辅助损失aux_output分配0.2权重
model.compile(optimizer='rmsprop',
              loss={'main_output': 'binary_crossentropy', 'aux_output': 'binary_crossentropy'},
              loss_weights={'main_output': 1., 'aux_output': 0.2})


#=================================================================================================================
# 标题输入：接收一个含有 100 个整数的序列，每个整数在 1 到 10000 之间。
# 注意我们可以通过传递一个 `name` 参数来命名任何层。
main_input2 = Input(shape=(100,), dtype='int32', name='main_input2')
x2 = Embedding(output_dim=512, input_dim=10000, input_length=100)(main_input2)
lstm_out2 = LSTM(32)(x2)
auxiliary_output2 = Dense(1, activation='sigmoid', name='aux_output2')(lstm_out2)
auxiliary_input2 = Input(shape=(5,), name='aux_input2')
x2 = keras.layers.concatenate([lstm_out2, auxiliary_input2])
x2 = Dense(64, activation='relu')(x2)
x2 = Dense(64, activation='relu')(x2)
x2 = Dense(64, activation='relu')(x2)
main_output2 = Dense(1, activation='sigmoid', name='main_output2')(x2)
model2 = Model(inputs=[main_input2, auxiliary_input2], outputs=[main_output2, auxiliary_output2])
model2.compile(optimizer='rmsprop',
              loss={'main_output2': 'binary_crossentropy', 'aux_output2': 'binary_crossentropy'},
              loss_weights={'main_output2': 1., 'aux_output2': 0.2})

r1 = model.output[0]
r2 = model.output[1]
r3 = model2.output[0]
r4 = model2.output[1]
############################ 获取编译后模型的输出，输出是一个list，包含两个tensor。
print(r1.__class__)
x3 = keras.layers.concatenate([r1,r2])  # 合并编译后的tensor；获得模型1
x3 = Dense(64, activation='relu')(x3)

xxx = keras.layers.concatenate([r3,r4])  # 合并编译后的tensor；获得模型2
xxx = Dense(64, activation='relu')(xxx)

xres = keras.layers.concatenate([x3, xxx])  # 合并

xres = Dense(64, activation='relu')(xres)
xres = Dense(64, activation='relu')(xres)
xres = Dense(64, activation='sigmoid')(xres)


model = Model(inputs=[main_input,auxiliary_input,main_input2,auxiliary_input2], outputs=xres)
model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
##########################  之后添加预测层即可


print(model.summary())




########################### 后续添加 共享层 见论文。

shared_lstm = LSTM(64)
print(shared_lstm.__class__)

########################## 没有和模型连接在一起 ， 直接和层连接在一起了