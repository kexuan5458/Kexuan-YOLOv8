import json
import os

# Load the original JSON file
input_json_file = '/home/ee904/Repo/yolov8/test.json'
with open(input_json_file, 'r') as f:
    original_data = json.load(f)

myDict = {}
images = []
categories = []

# List to store converted bounding box information
converted_data = []

# Iterate through the original data
for box_info in original_data["annotations"]:
    
    # Extract box information
    points_lst = box_info["bbox"] # box coordinates in (left_top_x, left_top_y, width, height) format
    points_lst.append(box_info["angle"])

    # Append converted bounding box information to the list
    converted_data.append({
        "id": box_info["id"],
        "image_id": box_info["image_id"],
        "category_id": box_info["category_id"],
        "bbox": points_lst,
        "angle": box_info["angle"],
        "area": box_info["area"],
        "iscrowd": 0
    })


categories = original_data["categories"]
myDict["categories"] = categories
images = original_data["images"]
myDict["images"] = images
annotations = converted_data
myDict["annotations"] = annotations


# Save the converted bounding box information to a new JSON file
output_json_file = './coco_angle_converted.json'
with open(output_json_file, "w") as outfile:
    json.dump(myDict, outfile)

print(f"Converted bounding box information saved to {output_json_file}")
