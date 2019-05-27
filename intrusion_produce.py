# !/usr/bin/python3
# -*- coding:utf-8 -*-
import pika
import multiprocessing as mp
import pickle
import time
import numpy as np
from util.camera_protocol import *
from conf.config_setting import *
from conf.config_function import detection_timer, logging_handle
from util.manage_floder import manage_dir


class ImgHandler(object):
    def __init__(self, username, password, host, queue_name):
        '''
        rtsp 协议取流handler定义
        :param username: rabbitmq name
        :param password: rabbitmq password
        :param host: rabbitmq ip
        :param queue_name: rabbitmq queue name
        '''
        self.username = username
        self.password = password
        self.host = host
        self.queue_name = queue_name
        self.channel, self.connection = self.load_channel()

    def load_channel(self):
        try:
            user_pwd = pika.PlainCredentials(self.username, self.password)
            # 创建连接对象
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, credentials=user_pwd))
            # 创建频道对象
            channel = connection.channel()
            # 切换到指定的队列,如果不存在则创建
            channel.queue_declare(queue=self.queue_name, durable=True)
            return channel, connection
        except Exception as e:
            logger_intrusion.info(f'[INFO] produce load_channel error.')
            return False

    def upload_img(self, data):
        '''
        multiprocessing upload image
        :param data: upload data
        :return:
        '''
        try:
            self.channel.basic_publish(exchange='',
                                       routing_key=self.queue_name,
                                       body=str(data),
                                       properties=pika.BasicProperties(delivery_mode=2,  # make message persistent
                                                                       ))
        except Exception as e:
            logger_intrusion.info(f'[INFO] upload_img error.')

    def keep_alive(self):
        # on time seed heartbeat
        try:
            self.connection.process_data_events()
        except Exception as e:
            self.channel, self.connection = self.load_channel()


def producer_intrusion(queue, CAMERA_NAME, CAMERA_PWD, camera_ip, camera_type):
    '''
    python producer queue to put data
    :param queue_intrusion: python queue name
    :param camera_name: camera info(username)
    :param camera_pwd: camera info(password)
    :param camera_id: camera info(system mysql id)
    :param camera_url: camera info(ip)
    :return:
    '''
    # Init camera cap
    if camera_type == "rtsp":
        cap = rtsp_camera(CAMERA_NAME, CAMERA_PWD, camera_ip)
    elif camera_type == "nvr":
        cap = nvr_camera(CAMERA_NAME, CAMERA_PWD, camera_ip)
    else:
        cap = rtmp_camera(camera_ip)
    while True:
        is_opened, frame = cap.read()
        detection_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if is_opened:
            # put frame,detection_time,camera_id python queue
            queue.put((frame, detection_time, camera_ip))
        else:
            # if get frame failed,put None
            queue.put((None, None, None))
            cap = rtsp_camera(CAMERA_NAME, CAMERA_PWD, camera_ip)
            logger_intrusion.info(f'[INFO] {camera_ip} customer_intrusion put queue error.')
        # keep 1 frame in queue,queue.qsize=2
        queue.get() if queue.qsize() > 1 else None


def customer_intrusion(queue, ori_data, num_camera):
    '''
        python customer queue to get data
        :param queue_intrusion: python queue name
        :param num_face_camera: sleep fps
        :return:
        '''
    # Init RabbitMQ to put image
    img_mq = ImgHandler(V_INTRUSION_MQ["username"], V_INTRUSION_MQ["password"], V_INTRUSION_MQ["host"],
                        V_INTRUSION_MQ["queue_name"])
    while True:
        # seed heartbeat to keep communication
        img_mq.keep_alive()
        # for python queue get data
        (frame, detection_time, camera_ip) = queue.get()
        if isinstance(frame, np.ndarray):
            data = {
                "frame": pickle.dumps(frame),
                "camera_ip": camera_ip,
                "ori_data": ori_data,
                "detection_time": detection_time
            }
            img_mq.upload_img(data)
            # control detection time
            time.sleep(num_camera * INTRUSION_FPS)


def run():  # mutil camera
    # A time to wait rabbitmq running
    # time.sleep(60)
    process_intrusion = []

    if CAMERA_POINT_LIST:
        # make image dir
        is_dir = manage_dir(CAMERA_IP_LIST, ICV_IMG_PATH, IMG_NAME_DICT)
        if is_dir:
            num_camera = len(CAMERA_IP_LIST)
            queue_list = [mp.Queue(maxsize=2) for _ in CAMERA_IP_LIST]
            for queue, camera_ip, camera_type, ori_data in zip(queue_list, CAMERA_IP_LIST, CAMERA_TYPE_LIST,
                                                               ori_data_list):
                process_intrusion.append(
                    mp.Process(target=producer_intrusion,
                               args=(queue, CAMERA_NAME, CAMERA_PWD, camera_ip, camera_type)))
                process_intrusion.append(
                    mp.Process(target=customer_intrusion,
                               args=(queue, ori_data, num_camera)))

        [process.start() for process in process_intrusion]
        [process.join() for process in process_intrusion]


if __name__ == '__main__':
    logger_intrusion = logging_handle(LOGGING_PATH_DICT["intrusion"])
    run()
