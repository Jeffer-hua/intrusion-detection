import time
import logging


def detection_timer(func):
    def call_func(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        stop_time = time.time()
        print('detection time is %s' % round((stop_time - start_time), 4))

    return call_func


def logging_handle(logging_path):
    # 日志定义
    logger_handle = logging.getLogger(__name__)
    logger_handle.setLevel(level=logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler = logging.FileHandler(logging_path)
    file_handler.setFormatter(formatter)
    logger_handle.addHandler(file_handler)

    return logger_handle
