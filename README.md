### intrusion_detection
- 越界检测，目前只针对行人进入设定区域检测
- environment : ubuntu18.04+Rabbitmq
- 支持rtsp协议的网络相机

1.pip3 install -r requirements.txt

2.Downloads yolov3.weights

-这里使用darknet原作者的模型，需要训练自己的模型可以参考
[darknet训练yolov3](https://github.com/Jeffer-hua/network-train-function/tree/master/yolov3_darknet)
```bash
wget https://pjreddie.com/media/files/yolov3.weights
mv yolov3.weights model/.
wget https://github.com/pjreddie/darknet/blob/master/data/coco.names
mv coco.names model/.
wget https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg
mv yolov3.cfg model/.
```
3.Modify param
```bash
vim model/yolov3.cfg
# 修改如下
# Testing
batch=1
subdivisions=1
# Training
#batch=64
#subdivisions=16

vim conf/config_setting.py
# 修改如下
```
4.Running
```bash
# 消费者
python3 intrusion_customer.py
# 生产者
python3 intrusion_produce.py

```
5.Todo
>script to draw region
>
>append new function to detection all objection , like vibe
>
