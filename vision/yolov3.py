import cv2
import numpy as np


class Detection_YOLOV3(object):
    def __init__(self, model_weights, label_path, model_config):
        self.conf_threshold = 0.6
        self.nms_threshold = 0.4
        self.input_width = 608
        self.input_height = 608
        self.classes = self.init_label_name(label_path)
        self.net = self.init_net(model_weights, model_config)

    def init_label_name(self, label_path):
        with open(label_path, 'rt') as f:
            classes = f.read().rstrip('\n').split('\n')
        return classes

    def init_net(self, model_weights, model_config):
        net = cv2.dnn.readNetFromDarknet(model_config, model_weights)
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        return net

    def get_outputs_names(self, net):
        layersNames = net.getLayerNames()
        # Get the names of the output layers, i.e. the layers with unconnected outputs
        return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    def get_objection_info(self, frame, outs):
        r_confidences_list = []
        r_boxes_list = []
        frame_height = frame.shape[0]
        frame_width = frame.shape[1]
        class_index_list = []
        confidences_list = []
        boxes_list = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_index = np.argmax(scores)
                confidence = scores[class_index]
                if confidence > self.conf_threshold and class_index == 0:
                    center_x = int(detection[0] * frame_width)
                    center_y = int(detection[1] * frame_height)
                    width = int(detection[2] * frame_width)
                    height = int(detection[3] * frame_height)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    class_index_list.append(class_index)
                    confidences_list.append(float(confidence))
                    boxes_list.append([left, top, width, height])
        indices = cv2.dnn.NMSBoxes(boxes_list, confidences_list, self.conf_threshold, self.nms_threshold)
        for i in indices:
            i = i[0]
            box = boxes_list[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            # class_index_list[i]:label
            # confidences_list[i]:socer
            r_boxes_list.append([left, top, width, height])
        return r_boxes_list

    def update(self, frame):
        blob = cv2.dnn.blobFromImage(frame, 1 / 255, (self.input_width, self.input_height), [0, 0, 0], 1, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.get_outputs_names(self.net))
        boxes_list = self.get_objection_info(frame, outs)
        return boxes_list



