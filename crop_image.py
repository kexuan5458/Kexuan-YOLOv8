# the upper left corner of the crop box would be at (w//2 - cw//2, h//2 - ch//2)
# its lower right corner is at (w//2 + cw//2, h//2 + ch//2)
from PIL import Image
import os

root_dir = '/data/v8/test/images/'
new_path = '/data/v8_crop/test/images/'
if not os.path.exists(new_path):
    os.makedirs(new_path)

for file_name in os.listdir(root_dir):
    if file_name.endswith(('.jpg', '.jpeg', '.png')):  # Filter image files
        full_path = os.path.join(root_dir + file_name)
        img = Image.open(full_path)
        w, h = img.size
        cw, ch = 800, 800
        box = w//2 - cw//2, h//2 - ch//2, w//2 + cw//2, h//2 + ch//2
        cropped_img = img.crop(box)

        
        save_path = os.path.join(new_path + file_name)
        print(save_path)
        cropped_img.save(save_path)