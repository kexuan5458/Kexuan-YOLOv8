# Author: ChiJun Chang

import cv2
import json

input_file_path = '/home/ee904/Repo/yolov8/output.json'

results = []

with open(input_file_path, 'r') as json_file:
    results = json.load(json_file)

def draw_rectangle(image_path, x1, y1, x2, y2, color=(0, 0, 255), thickness=2):
    # Load the image
    image = cv2.imread(image_path)

    # Draw a rectangle on the image
    cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)

    # Display the image with the rectangle
    cv2.imshow('Image with Rectangle', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

for result in results:
    draw_rectangle(result['file_path'], int(result['x1']), int(result['y1']), int(result['x2']), int(result['y2']))