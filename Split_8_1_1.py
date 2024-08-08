# Mix Radiate_Good, Radiate_Good_and_Bad and Test.
# Split them to train(8) ,val(1) and test(1).
import os
import shutil
import random
from math import ceil

# 路徑設定
image_dir = '/data/R_all_image/image'
labels_dir = '/data/R_all_image/labels'
labels_obb_dir = '/data/R_all_image/labels_obb'

train_dir = '/data/train'
valid_dir = '/data/valid'
test_dir = '/data/test'

# 創建目標資料夾
for folder in [train_dir, valid_dir, test_dir]:
    for subfolder in ['image', 'labels', 'labels_obb']:
        os.makedirs(os.path.join(folder, subfolder), exist_ok=True)

# 讀取labels資料夾中的所有檔案名稱
label_files = os.listdir(labels_dir)
label_files = [f for f in label_files if f.endswith('.txt')]

# 打亂檔案順序
random.shuffle(label_files)

# 按照8:1:1比例分配
total_files = len(label_files)  # array length of label_files
train_split = ceil(total_files * 0.8)
valid_split = ceil(total_files * 0.1)

train_files = label_files[:train_split] # from 0 to 80%
valid_files = label_files[train_split:train_split + valid_split]  # from 80% to 90%
test_files = label_files[train_split + valid_split:]  # from 90% to end

# 複製檔案函數
def copy_files(file_list, target_folder):
    for file_name in file_list:
        base_name = os.path.splitext(file_name)[0]
        # 複製圖像檔案
        shutil.copy(os.path.join(image_dir, base_name + '.png'), os.path.join(target_folder, 'image', base_name + '.png'))
        # 複製label檔案
        shutil.copy(os.path.join(labels_dir, file_name), os.path.join(target_folder, 'labels', file_name))
        # 複製label_obb檔案
        shutil.copy(os.path.join(labels_obb_dir, file_name), os.path.join(target_folder, 'labels_obb', file_name))

# 複製檔案到train, valid, test資料夾
copy_files(train_files, train_dir)
print('Train_files Split Finish')
copy_files(valid_files, valid_dir)
print('Valid_files Split Finish')
copy_files(test_files, test_dir)
print('Test_files Split Finish')



'''

# Spilt dataset by 3:1 ratio.
# Mix Radiate_Good and Radiate_Good_and_Bad.
# Split them to train(3) and val(1).

import os
import random
import shutil

# Define the paths to the folders containing images and text files
folder1_path = "/data/Radiate_Good"
folder2_path = "/data/Radiate_Good_and_Bad"
mixed_images_path = "/data/Radiate_Train/images"
mixed_texts_path = "/data/Radiate_Train/labels"

# Function to match images with their corresponding text files
def match_images_with_texts(folder_path):
    image_text_pairs = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".png"):  # Adjust file extensions as needed
                image_path = os.path.join(root, file)
                text_file = os.path.splitext(file)[0] + ".txt"
                text_path = os.path.join(root, text_file)

                if os.path.exists(text_path):
                    image_text_pairs.append((image_path, text_path))
                    # print('Matched:', image_path, text_path)
                else:
                    print('No matching text file found for:', image_path)

    return image_text_pairs

# Get image and text file pairs for each folder
folder1_pairs = match_images_with_texts(folder1_path)
folder2_pairs = match_images_with_texts(folder2_path)

# Combine the pairs from both folders
all_pairs = folder1_pairs + folder2_pairs

# Shuffle the list of pairs
random.shuffle(all_pairs)

# Calculate the split ratio
split_ratio = 0.75  # 3:1 ratio

# Split the pairs into train and test sets
train_size = int(len(all_pairs) * split_ratio)
train_pairs = all_pairs[:train_size]
val_pairs = all_pairs[train_size:]

# Function to move image-text pairs to the mixed folders
def move_pairs_to_folder(pairs, image_folder, text_folder):
    for image_path, text_path in pairs:
        shutil.copy(image_path, image_folder)
        shutil.copy(text_path, text_folder)

# Move train pairs to mixed folders
move_pairs_to_folder(train_pairs, "/data/Radiate_Train/images", "/data/Radiate_Train/labels")

# Move test pairs to mixed folders
move_pairs_to_folder(val_pairs, "/data/Radiate_Valid/images", "/data/Radiate_Valid/labels")
'''