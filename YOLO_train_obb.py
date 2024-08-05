from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import yaml
import pandas as pd
import numpy as np
from clearml import Task
task = Task.init(project_name="YOLO experiments", task_name="train1")
'''
tensorboard --logdir /home/ee904/Repo/yolov8/runs/detect/yolov8s-obb_60e
'''

model = YOLO("yolov8s-obb.pt")
dict_classes = model.model.names


data = {'train' :  '/data/v8OBB/test/images',
        'val' :  '/data/v8OBB/valid/images',
        'test' :  '/data/v8OBB/test/images',
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
model.train(data='/home/ee904/Repo/yolov8/Radiate_train_n_2.yaml', imgsz=1152, epochs=60, batch=8, name='yolov8s-obb_60e')
##### Training.
# results = model.train(
#    data='pothole_v8.yaml',
#    imgsz=1152,
#    epochs=60,
#    batch=8,
#    name='yolov8n_v8_60e'
# )