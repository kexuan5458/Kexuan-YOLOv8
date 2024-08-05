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
