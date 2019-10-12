# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/1 21:51

import keras
from keras.layers import Input, Embedding, LSTM, Dense, concatenate, core, add
from keras.models import Model
# 模块
# 当日天气模块
# 时滞天气模块
# 其他空气污染物模块
# 时空元属性模块
# 整体影响模块


# 第一个模块 当日天气模块
#
# 输入层
Meteorology_input = Input(shape=(12,), name="Meteorology_input")
AODs_input = Input(shape=(17,), name="AODs_input")
# 因素融合层
meteorology_concat = concatenate([Meteorology_input, AODs_input])
# 全连接层
meteorology_x = Dense(24, activation=keras.layers.advanced_activations.ELU(alpha=1.0),
                      kernel_regularizer=keras.regularizers.l2(0.1), name="FullConnectionMA_1")(meteorology_concat)
# 残差层
meteorology_residual_connection = Dense(24, activation=keras.layers.advanced_activations.ELU(alpha=1.0),
                                        kernel_regularizer=keras.regularizers.l2(0.1),
                                        name="ResidualConnectionMA")(meteorology_x)
meteorology_residual_connection = Dense(24, activation=keras.layers.advanced_activations.ELU(alpha=1.0),
                                        kernel_regularizer=keras.regularizers.l2(0.1),
                                        name="FullConnectionMA_RC")(meteorology_residual_connection)
meteorology_residual_connection = add([meteorology_x, meteorology_residual_connection], name="ResidualConnectionMA_Add")
# 全连接层
meteorology_x = Dense(3, activation=keras.layers.advanced_activations.ELU(alpha=1.0),
                      kernel_regularizer=keras.regularizers.l2(0.1),
                      name="FullConnectionMA_2")(meteorology_residual_connection)
# Dropout
meteorology_y = core.Dropout(rate=0.5, name="Meteorology_Module")(meteorology_x)
# 模型层
model_meteorology = Model(inputs=[Meteorology_input, AODs_input], outputs=meteorology_y)


######################################################################################################################
# 第二个模块 时滞天气模块

Weather_input = Input(shape=(12,), name="Weather_input")  # 只添加新的因素即可
# AODs_input = Input(shape=(17,), name="AODs_input")
# 因素融合层
weather_concat = concatenate([Weather_input, AODs_input])
# 全连接层
weather_x = Dense(24, activation=keras.layers.advanced_activations.ELU(alpha=1.0),
                  kernel_regularizer=keras.regularizers.l2(0.1), name="FullConnectionWA_1")(weather_concat)
# 残差层
weather_residual_connection = Dense(24, activation=keras.layers.advanced_activations.ELU(alpha=1.0),
                                    kernel_regularizer=keras.regularizers.l2(0.1),
                                    name="ResidualConnectionWA")(weather_x)
weather_residual_connection = Dense(24, activation=keras.layers.advanced_activations.ELU(alpha=1.0),
                                    kernel_regularizer=keras.regularizers.l2(0.1),
                                    name="FullConnectionWAForRC")(weather_residual_connection)
weather_residual_connection = add([weather_x, weather_residual_connection], name="ResidualConnectionWA_Add")
# 全连接层
weather_x = Dense(3, activation=keras.layers.advanced_activations.ELU(alpha=1.0),
                  kernel_regularizer=keras.regularizers.l2(0.1),
                  name="FullConnectionWA_2")(weather_residual_connection)
# Dropout
weather_y = core.Dropout(rate=0.5, name="Weather_Module")(weather_x)  # use `rate` instead of `keep_prob`. r=1-p.

# 模型层
model_weather = Model(inputs=[Weather_input, AODs_input], outputs=weather_y)


######################################################################################################################
# 第三个模块 其他空气污染物模块
# 输入层
OtherPollution_input = Input(shape=(15,))
# 因素融合层
otherpollution_concat = concatenate([OtherPollution_input, AODs_input])
# 全连接层
otherpollution_x = Dense(24, activation=keras.layers.advanced_activations.ELU(alpha=1.0),
                         kernel_regularizer=keras.regularizers.l2(0.1),
                         name="FullConnectionOPA_1")(otherpollution_concat)
# 残差层
otherpollution_residual_connection = Dense(24, activation=keras.layers.advanced_activations.ELU(alpha=1.0),
                                           kernel_regularizer=keras.regularizers.l2(0.1),
                                           name="ResidualConnectionOPA")(otherpollution_x)
otherpollution_residual_connection = Dense(24, activation=keras.layers.advanced_activations.ELU(alpha=1.0),
                                           kernel_regularizer=keras.regularizers.l2(0.1),
                                           name="FullConnectionOPA_RC")(otherpollution_residual_connection)
otherpollution_residual_connection = add([otherpollution_x, otherpollution_residual_connection],
                                         name="ResidualConnectionOPA_Add")
# 全连接层
otherpollution_x = Dense(3, activation=keras.layers.advanced_activations.ELU(alpha=1.0),
                         kernel_regularizer=keras.regularizers.l2(0.1),
                         name="FullConnectionOPA_2")(otherpollution_residual_connection)
# Dropout
otherpollution_y = core.Dropout(rate=0.5, name="OtherPollution_Module")(otherpollution_x)
# 模型层
model_otherpollution = Model(inputs=[OtherPollution_input, AODs_input], outputs=otherpollution_y)


######################################################################################################################
# 第四个模块 时空元属性模块
# 输入层
TimeStation_input = Input(shape=(12,), name="TimeStation_input")
# 编码层, 该层之前需要自己对数据提前独特编码
embedded_timestation = Embedding(input_dim=12, output_dim=64)(TimeStation_input)  # 参数设置 ?
encoded_text = LSTM(32)(embedded_timestation)
# 因素融合层
timestation_concat = concatenate([encoded_text, AODs_input])
# 全连接层
timestation_x = Dense(24, activation=keras.layers.advanced_activations.ELU(alpha=1.0),
                      kernel_regularizer=keras.regularizers.l2(0.1),
                      name="FullConnectionOTSA_1")(timestation_concat)
# 残差层
timestation_residual_connection = Dense(24, activation=keras.layers.advanced_activations.ELU(alpha=1.0),
                                        kernel_regularizer=keras.regularizers.l2(0.1),
                                        name="ResidualConnectionTSA")(timestation_x)
timestation_residual_connection = Dense(24, activation=keras.layers.advanced_activations.ELU(alpha=1.0),
                                        kernel_regularizer=keras.regularizers.l2(0.1),
                                        name="FullConnectionTSA_RC")(timestation_residual_connection)
timestation_residual_connection = add([timestation_x, timestation_residual_connection],
                                      name="ResidualConnectionTSA_Add")
# 全连接层
timestation_x = Dense(3, activation=keras.layers.advanced_activations.ELU(alpha=1.0),
                      kernel_regularizer=keras.regularizers.l2(0.1),
                      name="FullConnectionTSA_2")(timestation_residual_connection)
# Dropout
timestation_y = core.Dropout(rate=0.5, name="TimeStation_Module")(timestation_x)
# 模型层
model_timestation = Model(inputs=[TimeStation_input, AODs_input], outputs=timestation_y)


######################################################################################################################
# 第五个模块 时空元属性模块
# 整体影响模块
# 因素融合层
allin_concat = concatenate([Meteorology_input, Weather_input, OtherPollution_input, TimeStation_input, AODs_input])
# 全连接层
allin_x = Dense(24, activation=keras.layers.advanced_activations.ELU(alpha=1.0),
                kernel_regularizer=keras.regularizers.l2(0.1),
                name="FullConnectionAIA_1")(allin_concat)
# 残差层
allin_residual_connection = Dense(24, activation=keras.layers.advanced_activations.ELU(alpha=1.0),
                                  kernel_regularizer=keras.regularizers.l2(0.1),
                                  name="ResidualConnectionAIA")(allin_x)
allin_residual_connection = Dense(24, activation=keras.layers.advanced_activations.ELU(alpha=1.0),
                                  kernel_regularizer=keras.regularizers.l2(0.1),
                                  name="FullConnectionAIA_RC")(allin_residual_connection)
allin_residual_connection = add([allin_x, allin_residual_connection], name="ResidualConnectionAIA_Add")
# 全连接层
allin_x = Dense(3, activation=keras.layers.advanced_activations.ELU(alpha=1.0),
                kernel_regularizer=keras.regularizers.l2(0.1),
                name="FullConnectionAIA_2")(allin_residual_connection)
# Dropout
allin_y = core.Dropout(rate=0.5, name="AllIn_Module")(allin_x)
# 模型层
model_allin = Model(inputs=[Meteorology_input, Weather_input, OtherPollution_input, TimeStation_input, AODs_input],
                    outputs=allin_y)


#####################
# 最后的融合
# 捕捉的影响的融合层
res_concat = concatenate([model_meteorology.output, model_weather.output, model_otherpollution.output,
                          model_timestation.output, model_allin.output])
# 全连接层
res_x = Dense(24, activation=keras.layers.advanced_activations.ELU(alpha=1.0),
              kernel_regularizer=keras.regularizers.l2(0.1), name="ResFullConnectionResModelForLast")(res_concat)
# 残差连接层
res_residual_connection = Dense(24, activation=keras.layers.advanced_activations.ELU(alpha=1.0),
                                kernel_regularizer=keras.regularizers.l2(0.1),
                                name="ResidualConnectionLast")(res_x)
res_residual_connection = Dense(24, activation=keras.layers.advanced_activations.ELU(alpha=1.0),
                                kernel_regularizer=keras.regularizers.l2(0.1),
                                name="FullConnectionLast_RC")(res_residual_connection)
res_residual_connection = add([res_x, res_residual_connection], name="ResidualConnectionLast_Add")
# 全连接层
res_x = Dense(3, activation=keras.layers.advanced_activations.ELU(alpha=1.0),
              kernel_regularizer=keras.regularizers.l2(0.1),
              name="FullConnectionLast_2")(res_residual_connection)
# Dropout
res_y = core.Dropout(rate=0.5, name="Res_Module")(res_x)
# sigmoid 最终融合结果
res_outcome = Dense(1, activation="sigmoid", kernel_regularizer=keras.regularizers.l2(0.1),
                    name="sigmoid_FC")(res_y)
# 编译最终模型
model_last = Model(inputs=[Meteorology_input, Weather_input, OtherPollution_input, TimeStation_input, AODs_input],
                   outputs=res_outcome)
model_last.compile(loss="mse", optimizer="adam", metrics=["accuracy"])

#print(model_last.summary())

#########################################

yaml_string = model_last.to_yaml()
with open("model_save_file.yaml", "w") as f:
    f.write(yaml_string)  # 将模型转为yaml文件后的字符串写入本地
# 读取模型网络结构