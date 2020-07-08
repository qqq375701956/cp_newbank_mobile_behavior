import datetime
import os

import tensorflow as tf

from config import setting
from utils.toolbox import Logging


class LstmModel(object):
    def __init__(self):
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            try:
                # 设置GPU 显存占用为按需分配
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)  # 设置TensorFlow按需申请显存资源
                logical_gpus = tf.config.experimental.list_logical_devices('GPU')
                print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
            except RuntimeError as e:
                # 异常处理
                print(e)

    def initialize_lstm_model(self):
        """构建lstm模型架构"""
        model = tf.keras.Sequential([
            tf.keras.layers.LSTM(100, activation='tanh', use_bias=True, return_sequences=True, input_shape=(61, 7)),
            tf.keras.layers.LSTM(400, activation='tanh', use_bias=True, return_sequences=True),
            tf.keras.layers.LSTM(200, activation='tanh', use_bias=True, return_sequences=True),
            tf.keras.layers.LSTM(100, activation='tanh', use_bias=True, return_sequences=True),
            tf.keras.layers.LSTM(50, activation='tanh', use_bias=True, return_sequences=True),
            tf.keras.layers.LSTM(20, activation='tanh', use_bias=True, return_sequences=True),
            tf.keras.layers.LSTM(19, return_sequences=False)
        ])

        model.compile(loss="mse",
                      # loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),  # 交叉熵损失
                      optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.001), metrics=['accuracy'])

        Logging.default_logger().info("已成功初始化模型")
        return model

    def save_model(self, model):
        model.save(os.path.join(setting.BASE_DIR, "./data_model/model/model_lstm{}.h5".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))))
        Logging.default_logger().info("已成功保存模型")

    def load_model(self):
        model = tf.keras.models.load_model("D:/qt_ch_a_stock_RE_data_model/model/model_similar_category.h5")
        Logging.default_logger().info("已成功加载模型")
        return model