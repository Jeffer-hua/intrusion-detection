import cv2


def rtsp_camera(camera_name, camera_pwd, camera_ip, channel=1):
    cap = cv2.VideoCapture(f"rtsp://{camera_name}:{camera_pwd}@{camera_ip}//Streaming/Channels/{channel}")
    return cap
