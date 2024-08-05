# FIND different name's files between 2 folders.
import os
import shutil

folder_1 = "/data/v8_crop/test/images/"
folder_2 = "/data/v8_crop/test/labels/" # MORE files
list_1 = os.listdir(folder_1)
list_2 = os.listdir(folder_2)           # MORE files

test_list = []
for file in list_1:
    name = (file.split('.'))[0]
    test_list.append(name)

for find in list_2: 
    findName = (find.split('.'))[0]
    if findName not in test_list:
        print(findName)                # Redundant files

