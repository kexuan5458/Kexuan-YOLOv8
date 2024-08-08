import json
from ultralytics import YOLO
import cv2
import os

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

root_dir = './runs/obb/yolov8s-obb_60e'
input_weight_file = root_dir + '/weights/best.pt'
Output_file_path = './runs/obb/yolov8s-obb_60e/yolov8s-obb_60e.json' # Path to json file

# Load the YOLOv8 model
model = YOLO(input_weight_file)
predictions = []
# Path to the folder containing images
Image_folder = '/data/v8OBB/test/images'

for filename in os.listdir(Image_folder):
    if filename.endswith(('.jpg', '.jpeg', '.png')):  # Filter image files
        # Read the image
        img_path = os.path.join(Image_folder, filename)
        img = cv2.imread(img_path)

        # Perform object detection on the image
        results = model.predict(img)

        # Process detection results
        for r in results:
          # xyxyxyxy is used to get the oriented bounding boxes in the correct format
          obbs = r.obb.xyxyxyxy.cpu().numpy()
          scores = r.obb.conf.cpu().numpy()
          classes = r.obb.cls.cpu().numpy()
          for obb, score, cls in zip(obbs, scores, classes):
            # print("OBB Data:", obb)  # 印出實際的OBB數據
            # print("Length of OBB Data:", len(obb))
            cls = int(cls)
            points = [[float(point[0]), float(point[1])] for point in obb]
            predicts_object = {
                "sample_token": filename,
                "points": points,
                "name": CATEGORY_ID_TO_NAME.get(cls, "unknown"),
                "score": float(score)
            }
            predictions.append(predicts_object)
        
with open(Output_file_path, "w") as outfile:
        json.dump(predictions, outfile, indent=2)
# Save the bounding box information to a JSON file
print(f"Bounding box information saved to {Output_file_path}")
