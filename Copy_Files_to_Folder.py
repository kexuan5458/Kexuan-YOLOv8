# Select all of the labels to a big folder
# Select all of the labels_obb to a big folder
# Select all of the images to a big folder
import os
import shutil
import argparse

# init params
parser = argparse.ArgumentParser()
parser.add_argument("--folder", help="folder with radiate dataset",
                    default='city_1_0',
                    type=str)
args = parser.parse_args()
root_dir = '/data/RADIATE'
folder = args.folder
# choose image or label folder
src = os.path.join(root_dir, folder, 'labels') # Navtech_Cartesian/ labels/ labels_obb

src_files = os.listdir(src)
for file_name in src_files:
    full_file_name = os.path.join(src, file_name)
    if os.path.isfile(full_file_name):
        shutil.copy(full_file_name, '/data/R_all_image/labels') # Navtech_Cartesian/ labels/ labels_obb