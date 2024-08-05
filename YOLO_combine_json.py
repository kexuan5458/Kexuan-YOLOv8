import json
import os
import sys

root_dir = '/home/ee904/Repo/yolov8/JSON'
# Load the original JSON file
first_json_file = os.path.join(root_dir, 'combined_json_file.json')
second_json_file = os.path.join(root_dir, 'snow_1_0_GT.json')
with open(first_json_file, 'r') as f1:
    first_data = json.load(f1)
with open(second_json_file, 'r') as f2:
    second_data = json.load(f2)

# Combine dictionaries' entries together
combined_list = []
# Add entries from dict1
for entry in first_data:
    combined_list.append(entry)
# Add entries from dict2
for entry in second_data:
    combined_list.append(entry)

with open('/home/ee904/Repo/yolov8/JSON/combined_json_file.json', 'w') as f:
    json.dump(combined_list, f)