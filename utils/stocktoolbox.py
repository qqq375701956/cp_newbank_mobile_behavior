import datetime


def _is_newstock(df):
    """是否仅上市一天的新股"""
    # 传入：该股票所有的数据，可以是day级，分时级的k线df数据
    return True if df.groupby("date").count().shape[0] == 1 else False


def _is_subnewstock(df, list_day=10):
    """是否为上市不足n个交易日的次新股"""
    # 传入：该股票所有的数据，可以是day级，分时级的k线df数据
    return True if df.groupby("date").count().shape[0] < list_day else False


def drop_data_afterlist(df, list_day, drop_day=15):
    """删除股票在刚上市的n个交易日的数据"""
    # 传入：该股票所有的数据，可以是day级，分时级的k线df数据
    # 获取上市后第n天的日期
    cut_time = (datetime.datetime.strptime(list_day, '%Y-%m-%d') + datetime.timedelta(days=drop_day)).strftime(
        "%Y-%m-%d")
    # 如果数据的时间都大于这个时间，则直接全部返回
    if df["date"].iloc[0] > cut_time:
        return df
    # 否则就截取大于该时间的数据返回
    else:
        df = df[df["date"] > cut_time]
    return df
