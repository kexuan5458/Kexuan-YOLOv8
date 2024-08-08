import os
import json
from PIL import Image

# Category ID to name mapping (replace with your actual category names)
CATEGORY_ID_TO_NAME = {
    0: "car",
    1: "van",
    2: "bus",
    3: "truck",
    4: "motorbike",
    5: "bicycle",
    6: "pedestrian",
    7: "group_of_pedestrians",
    # Add other category mappings here
}

def convert_coordinates(x_center, y_center, width, height, img_width, img_height):
    # back to non-normalized values
    x_center *= img_width
    y_center *= img_height
    width *= img_width
    height *= img_height
    
    x1 = x_center - width / 2
    y1 = y_center - height / 2
    x2 = x_center + width / 2
    y2 = y_center - height / 2
    x3 = x_center + width / 2
    y3 = y_center + height / 2
    x4 = x_center - width / 2
    y4 = y_center + height / 2

    return [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]

def process_label_file(label_file, img_folder):
    # label_file = '/labels/xxxxx.txt'
    filename = os.path.splitext(os.path.basename(label_file))[0]
    img_path = os.path.join(img_folder, f"{filename}.png")
    img = Image.open(img_path)
    img_width, img_height = img.size        # 1152*1152

    with open(label_file, 'r') as file:
        lines = file.readlines()

    annotations = []
    for line in lines:
        parts = line.strip().split()
        # the class label, bounding box coordinates (x, y, width, height)
        class_id = int(parts[0])
        x_center = float(parts[1])
        y_center = float(parts[2])
        width = float(parts[3])
        height = float(parts[4])

        points = convert_coordinates(x_center, y_center, width, height, img_width, img_height)
        annotation = {
            "sample_token": f"{filename}.png",
            "points": points,
            "name": CATEGORY_ID_TO_NAME.get(class_id, "unknown"),
            # "scores": 0.0  # Placeholder for scores
        }
        annotations.append(annotation)

    return annotations

def process_obb_label_file(label_file, img_folder):
    # label_file = '/test/labels/xxxxx.txt'
    filename = os.path.splitext(os.path.basename(label_file))[0]    # 'xxxxx'
    img_path = os.path.join(img_folder, f"{filename}.png")
    img = Image.open(img_path)
    img_width, img_height = img.size

    with open(label_file, 'r') as file:
        lines = file.readlines()
    annotations = []
    for line in lines:
        parts = line.strip().split()
        # the class label, x1, y1, x2, y2, x3, y3, x4, y4
        class_id = int(parts[0])
        points = [[float(parts[1]), float(parts[2])], 
                  [float(parts[3]), float(parts[4])], 
                  [float(parts[5]), float(parts[6])], 
                  [float(parts[7]), float(parts[8])]]
        points = [[x * img_width, y * img_height] for x, y in points]
        annotation = {
            "sample_token": f"{filename}.png",
            "points": points,
            "name": CATEGORY_ID_TO_NAME.get(class_id, "unknown")
        }
        annotations.append(annotation)
    return annotations

def process_folder(labels_folder, img_folder, output_file):
    all_annotations = []
    for filename in os.listdir(labels_folder):
        if filename.endswith('.txt'):
            label_path = os.path.join(labels_folder, filename)
            # annotations = process_label_file(label_path, img_folder)
            annotations = process_obb_label_file(label_path, img_folder)
            all_annotations.extend(annotations)

    with open(output_file, 'w') as file:
        json.dump(all_annotations, file, indent=2)


labels_folder = '/data/v8OBB/test/labels'
img_folder = '/data/v8OBB/test/images/'
output_file = '/data/v8OBB/test/GT_annotations.json'

process_folder(labels_folder, img_folder, output_file)