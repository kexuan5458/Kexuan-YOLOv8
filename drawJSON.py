# Use the same color setting with Ian Peng
import cv2
import numpy as np
from collections import defaultdict
from shapely.geometry import Polygon
import json

def group_by_key(detections, key):
    groups = defaultdict(list)
    for detection in detections:
        groups[detection[key]].append(detection)
    return groups

gt_file = '/data/v8/test/GT_annotations.json'
# pred_file = '/home/ee904/Repo/yolov8/runs/detect/yolov8s_50e2/yolov8s_50e2.json'
# gt_file = '/home/ee904/Repo/yolov8/RADIATE_Test.json'
pred_file = '/home/ee904/Repo/yolov8/runs/obb/yolov8s-obb_60e/yolov8s-obb_60e.json'
gt = []
predictions = []

with open(pred_file) as f:
    predictions = json.load(f)
with open(gt_file) as f:
    gt = json.load(f)
grouped_gt = group_by_key(gt, "sample_token")
grouped_predictions = group_by_key(predictions, "sample_token")

from copy import copy
cv2.namedWindow('I', cv2.WINDOW_NORMAL)
colors = {'car': (255, 0, 255),         # pink
          'van': (50, 255, 0),          # green
          'bus': (255, 77, 64),         # orange
          'truck': (0, 0, 255),         # blue
          'motorbike': (18, 237, 233),  # ocean blue
          'bicycle': (173, 143, 255),   # lavender
          'pedestrian': (168, 126, 0),  # mud color
          'group_of_pedestrians': (255, 255,0)} # yellow

# Iterate through each sample_token
sample_token_count = 0
for sample_token in grouped_gt:
    # print("sample_token_count = ", sample_token_count)
    # Create a blank image (or load the actual image corresponding to the sample_token)
    image = cv2.imread(f"/data/v8/test/images/" + sample_token, 1)

    canvas = np.zeros((1152, 1152, 3), dtype=np.uint8)  # Change dimensions as needed
    image_copy = canvas.copy()
    image = cv2.addWeighted(image, 0.8, image, 0, 0)
    gt_image = copy(image)
    predict_image = copy(image)
    # sample_token_count += 1
    
    # Draw prediction boxes
    for box in grouped_predictions.get(sample_token, []):
        points = np.array(box["points"], dtype=np.int32)
        if (box['name'] == 'car') or (box['name'] == 'van') or (box['name'] == 'bus') or (box['name'] == 'truck'):
            cv2.polylines(image, [points], isClosed=True, color=(255, 255, 0), thickness=2)      # light blue
        else:
            # cv2.polylines(image, [points], isClosed=True, color=colors[box['name']], thickness=2)
            cv2.polylines(image, [points], isClosed=True, color=(0, 255, 0), thickness=2)   # pred bbox+image (green)





    # Draw ground truth boxes in white and purple
    for box in grouped_gt.get(sample_token, []):
        points = np.array(box["points"], dtype=np.int32)
        if (box['name'] == 'car') or (box['name'] == 'van') or (box['name'] == 'bus') or (box['name'] == 'truck'):
            cv2.fillPoly(image_copy, [points], color=(0, 0, 255))      # red
        else:
            cv2.fillPoly(image_copy, [points], color=(52, 147, 235))   # gt bbox+image  (orange)
        # cv2.polylines(gt_image, [points], isClosed=True, color=(255, 255, 255), thickness=2)    # gt bbox+image
    
    # cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)
    image = cv2.addWeighted(image_copy, 0.4, image, 0.8, 0)
    # Display the image
    cv2.imshow(f'Image', image)
    cv2.imwrite(f'/home/ee904/Repo/yolov8/runs/detect/yolov8s_50e2/drawJSON/{sample_token}', image)
    key = cv2.waitKey(500)
    if key == ord('q'):
        break