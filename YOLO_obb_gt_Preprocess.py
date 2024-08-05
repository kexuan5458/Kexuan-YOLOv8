import os
import json
import numpy as np
import argparse
import math

def rotate_point(px, py, cx, cy, angle):
    """
    Rotate point (px, py) around (cx, cy) by angle in radians.
    """
    s, c = np.sin(angle), np.cos(angle)
    px -= cx
    py -= cy
    new_x = px * c - py * s + cx
    new_y = px * s + py * c + cx
    return new_x, new_y

def coco_to_yolo_obb(coco_annotation_path, output_path):
    with open(coco_annotation_path) as f:
        coco_data = json.load(f)

    yolo_obb_annotations = []

    for annotation in coco_data['annotations']:
        class_index = annotation['category_id']
        x, y, width, height = annotation['bbox']
        angle = annotation['angle']  # Angle in degrees
        
        # Convert angle to radians for rotation
        angle_rad = math.radians(-angle)
        
        # Calculate the center of the bounding box
        cx, cy = x + width / 2, y + height / 2
        
        # Calculate the four corners of the bounding box before rotation
        corners = [
            (x, y),
            (x + width, y),
            (x + width, y + height),
            (x, y + height)
        ]
        
        # Rotate the corners around the center
        rotated_corners = [rotate_point(px, py, cx, cy, angle_rad) for px, py in corners]
        
        # Flatten the list of tuples
        flattened_corners = [coord for point in rotated_corners for coord in point]
        
        yolo_obb_annotations.append([class_index] + flattened_corners)
    
    # Save to file in the required format
    with open(output_path, 'w') as f:
        for annotation in yolo_obb_annotations:
            annotation_str = ' '.join(map(str, annotation))
            f.write(f"{annotation_str}\n")

# Usage
# init params
parser = argparse.ArgumentParser()
parser.add_argument("--folder", help="test folder with radiate dataset",
                    default='city_1_0',
                    type=str)
args = parser.parse_args()
root_dir = '/data/RADIATE'
folder = args.folder
annotation_name = folder + '_coco_annotations.json'

coco_annotation_path = annotation_name
output_path = 'path_to_output_yolo_obb.txt'
coco_to_yolo_obb(coco_annotation_path, output_path)
