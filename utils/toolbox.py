from config import setting


class Logging(object):
    """功能模块: 获取不同格式日志器"""

    @staticmethod
    def default_logger():
        import logging
        logger = logging.getLogger('default')
        if len(logger.handlers) < 2:  # 避免日志重复打印的情况
            logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')

            handler_file = logging.FileHandler(
                filename=setting.BASE_DIR + "\\config\\logging.log",  # log文件名
                mode='a',  # 写入模式“w”或“a”
                encoding='utf-8'
            )
            handler_file.setFormatter(formatter)
            logger.addHandler(handler_file)

            handler_console = logging.StreamHandler()
            handler_console.setLevel(logging.INFO)
            handler_console.setFormatter(formatter)
            logger.addHandler(handler_console)

        return logger


def count_time(method="class"):
    """
    功能函数：统计函数或方法的运行时间，在函数或方法上方加@count_time("class")或@count_time("func")
    """
    import datetime
    def count_time_decorator_outer(func):
        if method == "class":
            def count_time_decorator_inner(self, *args, **kwargs):
                start_time = datetime.datetime.now()  # 程序开始时间
                result = func(self, *args, **kwargs)
                over_time = datetime.datetime.now()  # 程序结束时间
                total_time = datetime.datetime(2020, 1, 1, 0, 0, 0, 0) + (over_time - start_time)
                str_title = '【报时】{}类{}()方法共计运行'.format(str(self.__class__.__name__), str(func.__name__))
                if total_time.minute < 1:
                    str_time = "{}秒".format(round((over_time - start_time).total_seconds(), 2))
                elif total_time.hour < 1:
                    str_time = '{}分{}秒'.format(total_time.minute, total_time.second)
                elif total_time.day < 2:
                    str_time = '{}小时{}分'.format(total_time.hour, total_time.minute)
                else:
                    str_time = '{}天{}小时'.format(total_time.day - 1, total_time.hour)
                Logging.default_logger().info(str_title + str_time)
                return result
        else:
            def count_time_decorator_inner(*args, **kwargs):
                start_time = datetime.datetime.now()  # 程序开始时间
                result = func(*args, **kwargs)
                over_time = datetime.datetime.now()  # 程序结束时间
                total_time = (over_time - start_time).total_seconds()
                total_time = datetime.datetime(2020, 1, 1, 0, 0, 0, 0) + (over_time - start_time)
                str_title = '【报时】{}()函数共计运行'.format(str(func.__name__))
                if total_time.minute < 1:
                    str_time = "{}秒".format(round((over_time - start_time).total_seconds(), 2))
                elif total_time.hour < 1:
                    str_time = '{}分{}秒'.format(total_time.minute, total_time.second)
                elif total_time.day < 2:
                    str_time = '{}小时{}分'.format(total_time.hour, total_time.minute)
                else:
                    str_time = '{}天{}小时'.format(total_time.day - 1, total_time.hour)
                Logging.default_logger().info(str_title + str_time)
                return result

        return count_time_decorator_inner

    return count_time_decorator_outer



if __name__ == '__main__':
    MysqlConnHelper()
