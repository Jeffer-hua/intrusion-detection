#!/usr/bin/python3
# -*- coding:utf-8 -*-
import pika
import time
import pickle
from vision.yolov3 import Detection_YOLOV3
from util.data_trans import send_data
import cv2
import json
import numpy as np
from util.pts_in_box import isin_multipolygon
from util.label_image import object_draw
from conf.config_setting import *
from conf.config_function import detection_timer, logging_handle


class DetectionHandler(object):
    def __init__(self, username, password, host, queue_name, logger_intrusion, init_image):
        '''
        安全着装handler定义
        :param username: rabbitmq name
        :param password: rabbitmq password
        :param host: rabbitmq ip
        :param queue_name: rabbitmq queue name
        :param logger_intrusion: logging
        '''
        self.username = username
        self.password = password
        self.host = host
        self.queue_name = queue_name
        self.logger_intrusion = logger_intrusion
        # Init intrusion function
        self.fn = Detection_YOLOV3(MODE_PATH_DICT["intrusion"]["model_weights"],
                                   MODE_PATH_DICT["intrusion"]["model_label"],
                                   MODE_PATH_DICT["intrusion"]["model_cfg"])
        self.fn.update(init_image)
        # Init RabbitMQ server
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
            logger_intrusion.info(f'[INFO] intrusion load_channel error.')
            return False

    def keep_alive(self):
        # on time seed heartbeat
        self.connection.process_data_events()

    def detection(self):
        """消费，接收消息..."""
        self.channel.basic_consume(
            queue=self.queue_name,
            # 回调函数
            consumer_callback=self.callback,
            no_ack=True
        )
        self.channel.start_consuming()

    # @detection_timer
    def callback(self, ch, method, properties, body):
        # body : RabbitMQ消息队列中传递的消息
        # seed heartbeat to keep communication
        self.keep_alive()
        # define queue message
        data = eval(body.decode("utf-8"))
        frame = pickle.loads(data["frame"])
        camera_id = data["camera_id"]
        detection_time = data["detection_time"]
        ori_data = data["ori_data"]
        camera_pts = json.loads(ori_data)
        ori_data = np.array(camera_pts)
        # 保证图片完整性,cv2中image格式为np
        if isinstance(frame, np.ndarray):
            # yolo_v3 output data
            boxes_list = self.fn.update(frame)
            # data process to box_info
            if len(boxes_list) > 0:
                back_name = "{}.jpg".format(str(time.time()).replace(".", ""))
                # folder now day name
                localtime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                intrusion_backup_path = os.path.join(ICV_IMG_PATH, str(camera_id), localtime,
                                                     IMG_NAME_DICT["intrusion_bp_name"],
                                                     back_name)
                # save origin image to train
                if SAVE_ORI_INTRUSION_IMG:
                    cv2.imwrite(intrusion_backup_path, frame)
                for boxes in boxes_list:
                    is_box = isin_multipolygon([int(boxes[0] + boxes[2]), int(boxes[1] + boxes[3])], ori_data.tolist(),
                                               contain_boundary=True)
                    if is_box:
                        show_green_box = False
                        status_type = "异常"
                        message_id = MESSAGE_ID_DICT["intrusion"]["wrong"]
                    else:
                        show_green_box = True
                        status_type = "正常"
                        message_id = MESSAGE_ID_DICT["intrusion"]["ok"]
                    show_img = object_draw(boxes, frame.copy(), show_green_box)
                    show_img = cv2.drawContours(show_img, [ori_data], -1, (0, 255, 255), 3)
                    img_name = "{}.jpg".format(str(time.time()).replace(".", ""))

                    intrusion_result_path = os.path.join(ICV_IMG_PATH, str(camera_id), localtime,
                                                         IMG_NAME_DICT["intrusion_res_name"],
                                                         img_name)
                    intrusion_save_path = os.path.split(intrusion_result_path)[0]
                    if not os.path.exists(intrusion_save_path):
                        os.makedirs(intrusion_save_path)

                    cv2.imwrite(intrusion_result_path, show_img)
                    # API to send result
                    try:
                        data = {"camera_id": camera_id,
                                "intrusion_result_path": intrusion_result_path,
                                "detection_time": detection_time,
                                "message_id": message_id,
                                "status_type": status_type}
                        file = {"file": open(intrusion_result_path, "rb").read()}
                        is_send = send_data(data, file, SERVER_URL_DICT["intrusion_result"])
                        if not is_send:
                            logger_intrusion.info(f'[INFO] {camera_id} {detection_time} intrusion is_send error.')
                    except Exception as e:
                        logger_intrusion.info(f'[INFO] {camera_id} {detection_time} intrusion is_send error.')


if __name__ == '__main__':
    # A time to wait rabbitmq running
    time.sleep(60)
    init_image = cv2.imread(os.path.join(ICV_INSTALL_PATH, "model", "intrusion", "test.jpg"))
    logger_intrusion = logging_handle(LOGGING_PATH_DICT["intrusion"])
    detection_mq = DetectionHandler(INTRUSIONMQ_PARAMS["username"], INTRUSIONMQ_PARAMS["password"],
                                    INTRUSIONMQ_PARAMS["host"],
                                    INTRUSIONMQ_PARAMS["queue_name"], logger_intrusion, init_image)
    detection_mq.detection()
