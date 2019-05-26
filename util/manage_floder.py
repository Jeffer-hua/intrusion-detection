import time
import os


def manage_dir(camera_id_list, icv_img_path, function_name_dict):
    localtime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    try:
        # 安全着装结果图片当天文件夹
        for camera_id in camera_id_list:
            if not os.path.exists(
                    os.path.join(icv_img_path, str(camera_id), localtime, function_name_dict["dress_res_name"])):
                os.makedirs(
                    os.path.join(icv_img_path, str(camera_id), localtime, function_name_dict["dress_res_name"]))
        # 安全着装原始图片当天文件夹
        for camera_id in camera_id_list:
            if not os.path.exists(
                    os.path.join(icv_img_path, str(camera_id), localtime, function_name_dict["dress_bp_name"])):
                os.makedirs(
                    os.path.join(icv_img_path, str(camera_id), localtime, function_name_dict["dress_bp_name"]))
        # 越界结果图片当天文件夹
        for camera_id in camera_id_list:
            if not os.path.exists(
                    os.path.join(icv_img_path, str(camera_id), localtime, function_name_dict["intrusion_res_name"])):
                os.makedirs(
                    os.path.join(icv_img_path, str(camera_id), localtime, function_name_dict["intrusion_res_name"]))
        # 越界原始图片当天文件夹
        for camera_id in camera_id_list:
            if not os.path.exists(
                    os.path.join(icv_img_path, str(camera_id), localtime, function_name_dict["intrusion_bp_name"])):
                os.makedirs(
                    os.path.join(icv_img_path, str(camera_id), localtime, function_name_dict["intrusion_bp_name"]))

        # 车牌识别结果图片当天文件夹
        for camera_id in camera_id_list:
            if not os.path.exists(
                    os.path.join(icv_img_path, str(camera_id), localtime, function_name_dict["car_res_name"])):
                os.makedirs(
                    os.path.join(icv_img_path, str(camera_id), localtime, function_name_dict["car_res_name"]))
        # 车牌识别原始图片当天文件夹
        for camera_id in camera_id_list:
            if not os.path.exists(
                    os.path.join(icv_img_path, str(camera_id), localtime, function_name_dict["car_bp_name"])):
                os.makedirs(
                    os.path.join(icv_img_path, str(camera_id), localtime, function_name_dict["car_bp_name"]))

        # 人脸识别背景图片当天文件夹
        for camera_id in camera_id_list:
            if not os.path.exists(
                    os.path.join(icv_img_path, str(camera_id), localtime, function_name_dict["face_back_name"])):
                os.makedirs(
                    os.path.join(icv_img_path, str(camera_id), localtime, function_name_dict["face_back_name"]))
        # 人脸识别人脸图片当天文件夹
        for camera_id in camera_id_list:
            if not os.path.exists(
                    os.path.join(icv_img_path, str(camera_id), localtime, function_name_dict["face_snap_name"])):
                os.makedirs(
                    os.path.join(icv_img_path, str(camera_id), localtime, function_name_dict["face_snap_name"]))
        return True
    except Exception as e:
        # logger_script.info(f'[INFO] manage_dir error.')
        return False
