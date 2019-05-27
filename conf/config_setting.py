import os

ICV_INSTALL_PATH = "/opt/icv_client"
ICV_IMG_PATH = '/home/oem/img'

CAMERA_IP_LIST = ["192.168.1.100"]
CAMERA_TYPE_LIST = ["rtsp"]
CAMERA_POINT_LIST = [[[51, 439], [859, 538], [1077, 544], [1070, 627], [70, 483]]]

V_INTRUSION_MQ = {
    "host": 'localhost',
    "username": "rabbitmq",  # mq用户名
    "password": "rabbitmq",  # mq密码
    "queue_name": "vision_intrusion"
}

INTRUSION_FPS = 2
# 海康相机设置
CAMERA_NAME = "admin"
CAMERA_PWD = "admin123"
# logging 存放位置
LOGGING_PATH_DICT = {
    "intrusion": os.path.join(ICV_INSTALL_PATH, "logging/intrusion.log")
}

# 图片文件名
IMG_NAME_DICT = {
    "intrusion_res_name": "intrusion_result",
    "intrusion_bp_name": "intrusion_backup",
}

# 模型路劲
MODE_PATH_DICT = {
    "intrusion": {
        "model_weights": os.path.join(ICV_INSTALL_PATH, "model/intrusion/yolov3.weights"),
        "model_label": os.path.join(ICV_INSTALL_PATH, "model/intrusion/coco.names"),
        "model_cfg": os.path.join(ICV_INSTALL_PATH, "model/intrusion/yolov3.cfg")
    },
}

SAVE_ORI_INTRUSION_IMG = True
