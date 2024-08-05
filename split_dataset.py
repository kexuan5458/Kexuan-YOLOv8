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
