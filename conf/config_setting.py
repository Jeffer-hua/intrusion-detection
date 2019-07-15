import os

# code path,修改为自己的路劲
ICV_INSTALL_PATH = "/opt/intrusion_detection"
# save result image path ,修改为自己的路劲
ICV_IMG_PATH = '/home/oem/img'
# network camera IP, 修改为自己的IP
CAMERA_IP_LIST = ["192.168.1.100"]
CAMERA_TYPE_LIST = ["rtsp"]
# region points ,修改为自己检测区域的坐标,顺时针
CAMERA_POINT_LIST = [[[10, 10], [1200, 10], [1200, 900], [10, 900]]]
# 相机设置,修改为自己的配置
CAMERA_NAME = "admin"
CAMERA_PWD = "!QAZ2wsx3edc"
# rabbitmq设置,修改为自己的设置
V_INTRUSION_MQ = {
    "host": 'localhost',
    "username": "rabbitmq",  # mq用户名
    "password": "rabbitmq",  # mq密码
    "queue_name": "vision_intrusion"
}
# 识别帧率
INTRUSION_FPS = 2
# logging 存放位置
LOGGING_PATH_DICT = {
    "intrusion": os.path.join(ICV_INSTALL_PATH, "./intrusion.log")
}

# 图片文件名
IMG_NAME_DICT = {
    "intrusion_res_name": "intrusion_result",
    "intrusion_bp_name": "intrusion_backup",
}

# 模型路劲
MODE_PATH_DICT = {
    "intrusion": {
        "model_weights": os.path.join(ICV_INSTALL_PATH, "model/yolov3.weights"),
        "model_label": os.path.join(ICV_INSTALL_PATH, "model/coco.names"),
        "model_cfg": os.path.join(ICV_INSTALL_PATH, "model/yolov3.cfg")
    },
}
