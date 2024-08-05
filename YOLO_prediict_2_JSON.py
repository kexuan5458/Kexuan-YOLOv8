import os
import json
from ultralytics import YOLO
'''
Author by JiaWen Liao
Given an image folder, an output json file path, and a model weight
Output: A json file to specified path.
This Json file can be visualized by "drawJSON.py" in the folder 'My_CenterNet/radiate_sdk'
'''

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

def sort_key(path):
    filename = os.path.basename(path)
    x_value = int(filename.split(".")[0])
    return x_value

def generateJSON(Image_folder, Output_file_path, weight_path):
    model = YOLO(weight_path)
    predictions = []
    Image_file_list = os.listdir(Image_folder)
    img_path = sorted(Image_file_list, key=sort_key)

    for filename in img_path:
        print(filename)
        if filename.endswith(".png"):
            file_path = os.path.join(Image_folder, filename)
            # sample_token = os.path.splitext(filename)[0]
            sample_token = filename.split('.')[0]
            results = model(file_path, verbose = False)
            
            for i in range(len(results[0].boxes.xyxy)): # box coordinates in (left_top_x, left_top_y, width, height) format
                # print((results[0].boxes))
                
                x_min, y_min, x_max, y_max = results[0].boxes.xyxy[i].cpu()
                x_min, y_min, x_max, y_max = float(x_min), float(y_min), float(x_max), float(y_max)
                score = float(results[0].boxes.conf[i].cpu())
                coor = [[x_min, y_max],
                        [x_min, y_min],
                        [x_max, y_min],
                        [x_max, y_max]]
                cls = int((results[0].boxes.cls[i].cpu()))
                # print(cls)
                predicts_object = {'sample_token': f'{sample_token}.png', 'points': coor, 'name': CATEGORY_ID_TO_NAME.get(cls, "unknown"), 'scores': score}
                predictions.append(predicts_object)
    with open(Output_file_path, "w") as outfile:
        json.dump(predictions, outfile, indent=2)

if __name__ == "__main__":
    '''
    # Here, the images' name are timestamp. 
    Because I use the '/data/Radiate_Test/images' to run "drawJSON.py". 
    All of the images' name are timestamp.
    '''
    # Image_folder = '/data/v8/test/images' # Path to Image folder
    # Image_folder = '/data/v8OBB/test/images' # Path to Image folder
    Image_folder = '/data/v8_crop/test/images'

    Output_file_path = '/home/ee904/Repo/yolov8/runs/detect/yolov8s_100e_crop2/yolov8s_100e_crop2.json' # Path to json file
    weight_path =  '/home/ee904/Repo/yolov8/runs/detect/yolov8s_100e_crop2/weights/best.pt' # Yolo weight path
    generateJSON(Image_folder, Output_file_path, weight_path)