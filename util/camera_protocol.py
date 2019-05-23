import cv2
from script import *


def rtmp_camera(rtmp_url):
    try:
        cap = cv2.VideoCapture(rtmp_url)
        return cap
    except Exception as e:
        pass


def nvr_camera(camera_name, camera_pwd, camera_ip):
    try:
        nvr_ip = camera_ip.split("_")[0]
        channel = camera_ip.split("_")[1]
        cap = cv2.VideoCapture(
            f"rtsp://{camera_name}:{camera_pwd}@{nvr_ip}:554/cam/realmonitor?channel={channel}&subtype=0")
        return cap
    except Exception as e:
        logger_script.info(f'||| {camera_ip} nvr_camera Error set camera ip')


def rtsp_camera(camera_name, camera_pwd, camera_ip, channel=1):
    cap = cv2.VideoCapture(f"rtsp://{camera_name}:{camera_pwd}@{camera_ip}//Streaming/Channels/{channel}")
    return cap

