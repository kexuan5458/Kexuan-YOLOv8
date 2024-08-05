'''
First step: TRAIN the model
Second step: using YOLO_convert_json.py to generate bounding_boxes_data_converted.json (specified format)
'''
import json
import os

root_dir = './runs/detect/yolov8s_50e'
# Load the original JSON file
input_json_file = root_dir + '/bounding_boxes_data.json'
with open(input_json_file, 'r') as f:
    original_data = json.load(f)

# List to store converted bounding box information
converted_data = []

# Iterate through the original data
for filename, boxes_info in original_data.items():
    for box_info in boxes_info:
        # Extract box information
        sample_token = filename # sample_token = os.path.splitext(filename)[0]
        
        xywh_points = box_info['box_coordinates'] # box coordinates in (left_top_x, left_top_y, width, height) format
        points_lst = []
        points_lst.append([float(xywh_points[0]), float(xywh_points[1])])
        points_lst.append([float(xywh_points[0]+xywh_points[2]), float(xywh_points[1])])
        points_lst.append([float(xywh_points[0]+xywh_points[2]), float(xywh_points[1]+xywh_points[3])])
        points_lst.append([float(xywh_points[0]), float(xywh_points[1]+xywh_points[3])])
        
        name = box_info['class']
        score = box_info['confidence']

        # Append converted bounding box information to the list
        converted_data.append({
            "sample_token": sample_token,
            "points": points_lst,
            "name": name,
            "scores": score
        })

# Save the converted bounding box information to a new JSON file
output_json_file = root_dir + '/bounding_boxes_data_converted.json'
with open(output_json_file, 'w') as f:
    # json.dump(converted_data, f, indent=2)
    json.dump(converted_data, f)

print(f"Converted bounding box information saved to {output_json_file}")
