import json
from ultralytics import YOLO
import cv2
import os

root_dir = './runs/detect/yolov8s_100e_crop2'
input_weight_file = root_dir + '/weights/best.pt'
# Load the YOLOv8 model
model = YOLO(input_weight_file)

# Path to the folder containing images
folder_path = '/data/v8_crop/test/images'

# Dictionary to store bounding box information for each image
bounding_boxes_data = {}

# Iterate through each image in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(('.jpg', '.jpeg', '.png')):  # Filter image files
        # Read the image
        img_path = os.path.join(folder_path, filename)
        img = cv2.imread(img_path)

        # Perform object detection on the image
        results = model.predict(img)

        # List to store bounding box information for the current image
        image_boxes = []

        # Process detection results
        for r in results:
            boxes = r.boxes
            for box in boxes:
                b = box.xywh[0]  # get box coordinates in (left_top_x, left_top_y, width, height) format, 
                # box.xywh : tensor([[545.8571, 933.0884,  20.8210,  24.2227]], device='cuda:0')
                # box.xywh[0] : tensor([545.8571, 933.0884,  20.8210,  24.2227], device='cuda:0')
                c = box.cls
                r = box.conf
                class_label = model.names[int(c)]
                box_coordinates = [float(coord) for coord in b]
                # print(box_coordinates)  # [545, 933, 20, 24]
                # print(type(box_coordinates)) # <class 'list'>

                # Append bounding box information to the list
                image_boxes.append({
                    'class': class_label,
                    'box_coordinates': [float(coord) for coord in b],
                    'confidence': float(r)
                })

        # Save bounding box information for the current image in the dictionary
        bounding_boxes_data[filename] = image_boxes

# Save the bounding box information to a JSON file
output_json_file = root_dir + '/bounding_boxes_data.json'
with open(output_json_file, 'w') as f:
    json.dump(bounding_boxes_data, f, indent=4)

print(f"Bounding box information saved to {output_json_file}")
