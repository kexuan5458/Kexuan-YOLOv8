'''
用YOLO_gt_Preprocess.sh 跑過所有/data/RADIATE的資料夾
'''
import json
import os
import argparse
import math

# init params
parser = argparse.ArgumentParser()
parser.add_argument("--folder", help="folder with radiate dataset",
                    default='city_1_0',
                    type=str)
args = parser.parse_args()
root_dir = '/data/RADIATE'
folder = args.folder
annotation_name = folder + '_coco_annotations.json'
annotation_path = os.path.join(root_dir, folder, annotation_name)

# 讀取COCO格式的JSON文件
with open(annotation_path, 'r') as f:
    coco_data = json.load(f)

# 創建labels資料夾
if not os.path.exists('labels'):
    # os.makedirs(os.path.join(root_dir, folder,'labels'))
    os.makedirs(os.path.join(root_dir, folder,'labels_crop'))

# 解析COCO JSON文件
images = {image['id']: image for image in coco_data['images']}
categories = {category['id']: category['name'] for category in coco_data['categories']}

for annotation in coco_data['annotations']:
    # 角度轉換為弧度
    angle = annotation['angle']
    angle_rad = math.radians(-angle)    ## VERY IMPORTANT: -angle
    
    # 定義旋轉矩陣
    cos_angle = math.cos(angle_rad)
    sin_angle = math.sin(angle_rad)
    
    # 取得對應的圖片信息
    image_id = annotation['image_id']
    image_info = images[image_id]
    image_width = image_info['width']
    image_height = image_info['height']
    new_image_width = 800
    new_image_height = 800
    vector_x = (image_width - new_image_width) / 2
    vector_y = (image_height - new_image_height) / 2
    
    bbox = annotation['bbox']
    # 計算YOLO格式所需的座標
    # center_x = (bbox[0] + bbox[2] / 2) / image_width
    # center_y = (bbox[1] + bbox[3] / 2) / image_height
    # width = bbox[2] / image_width
    # height = bbox[3] / image_height
    # crop後，YOLO格式所需的座標
    cx = ((bbox[0] - vector_x) + bbox[2] / 2)
    cy = ((bbox[1] - vector_y) + bbox[3] / 2)
    center_x = cx / new_image_width
    center_y = cy / new_image_height
    width = bbox[2] / new_image_width
    height = bbox[3] / new_image_height

    # 定義四個頂點
    points = [
        (-bbox[2] / 2, -bbox[3] / 2),
        (bbox[2] / 2, -bbox[3] / 2),
        (bbox[2] / 2, bbox[3] / 2),
        (-bbox[2] / 2, bbox[3] / 2)
    ]

    # 旋轉並平移頂點
    rotated_points = []
    for point in points:
        x_new = cos_angle * point[0] - sin_angle * point[1] + cx
        y_new = sin_angle * point[0] + cos_angle * point[1] + cy
        # 判斷bbox在image中
        if(x_new >= 0 and x_new <= new_image_width and
           y_new >= 0 and y_new <= new_image_height):
            rotated_points.append((x_new / image_width, y_new / image_height))

    if(len(rotated_points) == 4):
        category_id = annotation['category_id']
        # 取得對應的class
        class_id = category_id  # 如果需要使用class名稱，可以改為categories[category_id]
        
        # Create YOLO格式的標註
        yolo_annotation = f"{class_id} {center_x} {center_y} {width} {height}"
        
        # 取得對應的圖片文件名，並構建標註文件名
        image_filename = image_info['file_name']
        annotation_filename = os.path.splitext(image_filename)[0] + '.txt'
        
        # 將標註寫入對應的txt文件中
        with open(os.path.join(root_dir, folder,'labels_crop', annotation_filename), 'a') as f:
            f.write(yolo_annotation + '\n')

