from config import setting
import pandas as pd
from xgboost import XGBClassifier
import itertools
from sklearn.externals import joblib
import datetime


class CreateFeature(object):
    def __init__(self):
        pass

    def load_train_sample(self):
        df_train = pd.read_csv(setting.BASE_DIR + "\data_model\data\sensor_train.csv")
        return df_train

    def load_test_sample(self):
        df_test = pd.read_csv(setting.BASE_DIR + "\data_model\data\sensor_test.csv")
        return df_test

    def create_startmark_endmark_linenum_feature(self, df):
        start_mark_list = []
        end_mark_list = []
        line_num_list = []
        last_fragment_id = -1
        line_num = 1
        for fragment_id in df["fragment_id"]:
            if last_fragment_id != fragment_id:
                start_mark_list.append(1)
                end_mark_list.append(1)
                line_num = 1
                line_num_list.append(line_num)
            else:
                start_mark_list.append(0)
                end_mark_list.append(0)
                line_num += 1
                line_num_list.append(line_num)

            last_fragment_id = fragment_id
        end_mark_list.append(1)
        end_mark_list = end_mark_list[1:]

        df["fragment_start_mark"] = start_mark_list
        df["fragment_end_mark"] = end_mark_list
        df["fragment_line_num"] = line_num_list
        return df

    def create_timepoint_diff_feature(self, df):
        df["time_point_diff"] = df["time_point"].diff().fillna(0)
        return df

    def create_feature(self, df):
        df = self.create_startmark_endmark_linenum_feature(df)
        df = self.create_timepoint_diff_feature(df)
        return df

    def derive_feature(self, df):
        def derive_mean_feature(df_groupby, col, day):
            return df_groupby[col].rolling(day).mean()

        to_derive_column_list = [column for column in df.columns if
                                 column not in ["fragment_id", "time_point", "behavior_id"]]

        # 加减乘数特征衍生

        column_sets = itertools.product(to_derive_column_list, to_derive_column_list)
        for col1, col2 in column_sets:
            print(col1, col2)
            df[col1 + ":+:" + col2] = df[col1] + df[col2]
            df[col1 + ":-:" + col2] = df[col1] - df[col2]
            df[col1 + ":*:" + col2] = df[col1] * df[col2]
            df[col1 + ":/:" + col2] = df[col1] / (df[col2] + 10)

        # 均值特征衍生
        for col in to_derive_column_list:
            for day in [2, 4, 6, 8, 10]:
                df[col + "_{}_mean".format(day)] = df[["fragment_id", col]].groupby("fragment_id").apply(
                    derive_mean_feature, col, day).reset_index(drop=True)
        df = df.fillna(0)
        return df

    def create_train_val_test_feature(self, df):
        from sklearn.model_selection import train_test_split
        X = df.drop("behavior_id", axis=1).values
        y = df["behavior_id"].values
        X_train_val, X_test, y_train_val, y_test = train_test_split(X, y, test_size=0.2, random_state=10086)
        X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.2, random_state=10087)
        return X_train, X_val, y_train, y_val, X_test, y_test

    def run(self):
        # 构造特征
        df = self.load_train_sample()
        df = self.create_feature(df)
        df = self.derive_feature(df)

        # 切分训练验证测试集
        X_train, X_val, y_train, y_val, X_test, y_test = self.create_train_val_test_feature(df)
        return X_train, X_val, y_train, y_val, X_test, y_test


class XgboostModeling(object):
    def __init__(self, X_train=None, X_val=None, y_train=None, y_val=None, X_test=None, y_test=None):
        self.X_train = X_train
        self.X_val = X_val
        self.y_train = y_train
        self.y_val = y_val
        self.X_test = X_test
        self.y_test = y_test

    def initialize_model(self):
        self.xgb_clf = XGBClassifier(objective="multi:softmax", num_class=19, n_jobs=4)

    def load_model(self):
        self.xgb_clf = joblib.load(setting.BASE_DIR + "/data_model/model/xgboost_{}.pkl".format(
            datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")))

    def save_model(self):
        joblib.dump(self.xgb_clf, setting.BASE_DIR + "/data_model/model/xgboost_{}.pkl".format(
            datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")))

    def train(self):
        self.xgb_clf.fit(self.X_train,
                         self.y_train,
                         eval_set=[(self.X_train, self.y_train), (self.X_val, self.y_val)],
                         eval_metric='mlogloss',
                         early_stopping_rounds=10)

        self.save_model()
