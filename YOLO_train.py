from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import yaml
import pandas as pd
import numpy as np
from clearml import Task
task = Task.init(project_name="YOLO experiments", task_name="train6")
'''
tensorboard --logdir /home/ee904/Repo/yolov8/runs/detect/yolov8s_100e_GoodAndBad
'''
# training
# model = YOLO("yolov8s.pt")

# Resume training
model = YOLO("/home/ee904/Repo/yolov8/runs/detect/yolov8s_100e_GoodAndBad5/weights/last.pt")
dict_classes = model.model.names


data = {'train' :  '/data/v8_crop/train/images',
        'val' :  '/data/v8_crop/val/images',
        'test' :  '/data/v8_crop/test/images',
        'nc': 8,
        'names': ['car', 'van', 'bus', 'truck', 'motorbike', 'bicycle', 'pedestrian', 'group_of_pedestrians']
        }

# overwrite the data to the .yaml file
# with open('/home/ee904/Repo/yolov8/Radiate_train_n_1.yaml', 'w') as f:
#     yaml.dump(data, f)

# # read the content in .yaml file
# with open('/home/ee904/Repo/yolov8/Radiate_train_n_1.yaml', 'r') as f:
#     hamster_yaml = yaml.safe_load(f)

#　original image size: 1152 * 1152
model.train(data='/home/ee904/Repo/yolov8/Radiate_train_s_1.yaml', 
            imgsz=1152, 
            epochs=100, 
            batch=-1, 
            name='yolov8s_100e_GoodAndBad', 
            val=False)
##### Training.
# results = model.train(
#    data='pothole_v8.yaml',
#    imgsz=1152,
#    epochs=60,
#    batch=8,
#    name='yolov8n_v8_50e'
# )