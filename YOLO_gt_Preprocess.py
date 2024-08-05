'''
First step: using convert_annotation.py to generate xxxxxx_x_x_coco_annotations.json
Second step: using YOLO_gt_Preprocess.py to generate xxxxxx_x_x_GT.json (bbox has been rotated)
'''
import os
import json
import numpy as np
import argparse
import math

# init params
parser = argparse.ArgumentParser()
parser.add_argument("--folder", help="test folder with radiate dataset",
                    default='city_1_0',
                    type=str)
args = parser.parse_args()
root_dir = '/data/RADIATE'
folder = args.folder
annotation_name = folder + '_coco_annotations.json'
class_list = ['car', 'van', 'truck', 'bus', 'motorbike', 'bicycle', 'pedestrian', 'group of pedestrian']

# left top width height angle

def rotate_rectangle(left, top, width, height, angle):
    theta = math.radians(-angle)  # 將角度轉換為弧度
    # 計算矩形中心點
    center_x = left + width / 2
    center_y = top + height / 2
    
    # 計算矩形的四個頂點相對於中心點的坐標
    dx = np.array([-width / 2, width / 2, width / 2, -width / 2])
    dy = np.array([-height / 2, -height / 2, height / 2, height / 2])
    
    # 構建旋轉矩陣
    R = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
    
    # 計算旋轉後的四個頂點的相對(於原點)座標
    rotated_dx_dy = np.dot(R, np.vstack((dx, dy)))
    
    # 相對座標加上中心點的絕對座標
    rotated_points = rotated_dx_dy + np.array([[center_x], [center_y]])
    
    # 將四個頂點坐標轉換成列表形式並返回
    rotated_bbox = [[rotated_points[0, i], rotated_points[1, i]] for i in range(4)]
    
    return rotated_bbox

def gen_corners(bbox, angle):
    theta = np.deg2rad(-angle)
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta), np.cos(theta)]])
    points = np.array([[bbox[0], bbox[1]],
                       [bbox[0] + bbox[2], bbox[1]],
                       [bbox[0] + bbox[2], bbox[1] + bbox[3]],
                       [bbox[0], bbox[1] + bbox[3]]]).T

    cx = bbox[0] + bbox[2] / 2
    cy = bbox[1] + bbox[3] / 2
    T = np.array([[cx], [cy]])

    points = points - T
    rotated_points = np.matmul(R, points) + T
    # return rotated_points.T  
    rotated_bbox = [[rotated_points[0, i], rotated_points[1, i]] for i in range(4)]
    
    return rotated_bbox

for file in root_dir:
  annotation_path = os.path.join(root_dir, folder, annotation_name)
  # annotation_path = os.path.join(root_dir, 'city_1_1_coco_annotations.json')
  with open(annotation_path, 'r') as f_annotation:
      dataset_dicts = json.load(f_annotation)

  json_output = []

  # for data in (dataset_dicts):
  #   ["annotations"]["annotations"]
    # Loading annotation
  for anno in dataset_dicts["annotations"]:
    x1, y1, w, h = anno["bbox"] # [x,y,width,height]
    cx = x1 + w/2
    cy = y1 + h/2
    theta = anno["angle"]
    cls = anno["category_id"]
    imgID = anno["image_id"]
    bbox_list = [x1, y1, w, h]
    
    points = rotate_rectangle(x1, y1, w, h, theta)
    # points = gen_corners(bbox_list, theta)

    # output json
    gt = {}
    gt['sample_token'] = dataset_dicts["images"][imgID]["file_name"]
    gt['points'] = points
    gt['name'] = class_list[cls]
    json_output.append(gt)

  jsonFile = open(f"./JSON/{folder}_GT.json", "w")
  json.dump(json_output, jsonFile)