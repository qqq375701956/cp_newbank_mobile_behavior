# 构造均线，区间高低价等常用数据特征
# 不作为数据获取项目使用，而是作为接口提供其他项目使用
import os
import pandas as pd
from config import setting
from utils.toolbox import Logging


class CreateAverageData(object):
    def __init__(self):
        pass

    def create_close_average_data(self, df_k_data):
        """构造收盘价10, 20, 30, 60, 120, 250均线"""
        if "close" not in df_k_data.columns:
            Logging.default_logger().warning("没有{}这一列".format("close"))
            return df_k_data

        for interval in [10, 20, 30, 60, 120, 250]:
            df_k_data["close_avg_" + str(interval)] = df_k_data[["close"]].rolling(interval).mean()
        return df_k_data

    def create_volume_average_data(self, df_k_data):
        """构造交易量5, 10, 30均线"""
        if "volume" not in df_k_data.columns:
            Logging.default_logger().warning("没有{}这一列".format("volume"))
            return df_k_data

        for interval in [5, 10, 30]:
            df_k_data["volume_avg_" + str(interval)] = df_k_data[["volume"]].rolling(interval).mean()
        return df_k_data

    def create_close_top_high_low_data(self, df_k_data):
        """构造区间最高最低价数据"""
        for column in ["close", "high", "low"]:
            if column not in df_k_data.columns:
                Logging.default_logger().warning("没有{}这一列".format(column))
                return df_k_data

        # 构造收盘价区间最高最低价数据
        for interval in [10, 20, 30, 60, 120, 250]:
            df_k_data["close_max_" + str(interval)] = df_k_data[["close"]].rolling(interval).max()
            df_k_data["close_min_" + str(interval)] = df_k_data[["close"]].rolling(interval).min()

        # 构造high的区间最高价数据
        for interval in [10, 20, 30, 60, 120, 250]:
            df_k_data["high_max_" + str(interval)] = df_k_data[["high"]].rolling(interval).max()

        # 构造low的区间最低价数据
        for interval in [10, 20, 30, 60, 120, 250]:
            df_k_data["low_min_" + str(interval)] = df_k_data[["low"]].rolling(interval).min()

        return df_k_data
