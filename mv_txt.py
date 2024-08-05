# Select all of the labels to a big folder
# Below is a bash file 'mv_txt.sh'
'''
for folder in 'junction_1_13' 'motorway_1_0' 'junction_1_2' 'junction_1_0' 'city_2_0' 'city_4_0' 'junction_1_7' 'junction_1_6' 'junction_2_3' 'city_1_1' 'junction_2_1' 'city_3_2' 'junction_3_0' 'motorway_2_1' 'city_3_1' 'junction_3_1' 'city_3_0' 'city_1_0' 'rural_1_1' 'city_3_3' 'junction_2_2' 'city_5_0' 'motorway_2_0' 'junction_1_3' 'rural_1_3' 'junction_1_4' 'junction_1_1' 'junction_1_14' 'junction_1_5' 'junction_1_15' 'junction_2_0' 'junction_2_5' 'junction_1_9' 'junction_3_3' 'fog_8_2' 'rain_2_0' 'city_6_0' 'fog_8_0' 'city_1_3' 'junction_1_8' 'night_1_1' 'night_1_3' 'rain_4_1' 'night_1_0' 'junction_1_10' 'city_7_0' 'junction_2_6' 'fog_6_0' 'rain_3_0' 'rain_4_0' 'night_1_5' 'night_1_4' 'motorway_2_2' 'junction_1_11' 'night_1_2' 'snow_1_0' 'city_3_7' 'junction_3_2' 'fog_8_1' 'junction_1_12'
do
    mv /data/RADIATE/"${folder}"/labels_crop/* .
    
done
'''
# According to the images which splitted to ['train', 'val', 'test'] before, 
# move the corresponding label file(.txt) to the specific distination
import shutil
import os

source_folder = "/data/R_all_image/labels/"
destination_folder = "/data/radiate_origin_classification/test/images/"
txt_number = 0
image_number = len(os.listdir(destination_folder))

for file in os.listdir(destination_folder):
    filename = file.split('.')[0]
    txtname = filename + '.txt'
    source_path = os.path.join(source_folder, txtname)
    if os.path.exists(source_path):     # txt exist
        destination_path = "/data/radiate_origin_classification/test/labels/" + filename + '.txt'
        txt_number += 1
        shutil.move(source_path, destination_path)  # both are full path
    else:                               # txt does not exist
        deleted = destination_folder + filename + '.png'
        os.remove(deleted)
        image_number -= 1
        print(filename)
print("len of images:", image_number)
print("len of txt: ", txt_number)
    