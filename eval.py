# Author: ChiJun Chang

from ultralytics import YOLO
import cv2
import numpy as np
import json

model = YOLO('/home/ee904/Repo/yolov8/runs/detect/train3/weights/best.pt')  # load a custom model

root_folder = '/data/data/RADIATE/junction_1_12/Navtech_Cartesian/'
counter = 1

results = []

for i in range(1, 693):
    image_name = str(counter) + '.png'

    while len(image_name) < 10:
        image_name = '0' + image_name
    
    counter += 1
    image_path = root_folder + image_name
    result = model(image_path)

    # if len(result[0].boxes.xyxy) == 0:
    #     results.append({
    #         "file_path": image_path,
    #         "x1": 0,
    #         "y1": 0,
    #         "x2": 0,
    #         "y2": 0
    #     })
    #     continue

    for box, conf in zip(result[0].boxes.xyxy, result[0].boxes.conf):
        x1 = box[0].item()
        y1 = box[1].item()
        x2 = box[2].item()
        y2 = box[3].item()
        score = conf.item()

        results.append({
            "sample_token": image_name.split('.')[0],
            "points": [
                [x1, y1],
                [x1, y2],
                [x2, y2],
                [x2, y1]
            ],
            "name": "car",
            "score": score
        })

    # print("Min score: " + str(min_score))

#     x1 = result[0].boxes.xyxy[0][0].item()
#     y1 = result[0].boxes.xyxy[0][1].item()
#     x2 = result[0].boxes.xyxy[0][2].item()
#     y2 = result[0].boxes.xyxy[0][3].item()
#     print([x1, y1, x2, y2])

#     results.append({
#         "file_path": image_path,
#         "x1": x1,
#         "y1": y1,
#         "x2": x2,
#         "y2": y2
#     })

output_file_path = 'result_junction_1_12_0425.json'
with open(output_file_path, 'w') as f:
    json.dump(results, f)

# result = model('/data/data/RADIATE/city_7_0/Navtech_Cartesian/000001.png')
# print(result[0].boxes.xyxy[0][0].item())