import os
import shutil

# Define the main directory containing the 60 sub-folders
main_directory = "/data/RADIATE"

# Loop through each sub-folder in the main directory
for subfolder in os.listdir(main_directory):
    subfolder_path = os.path.join(main_directory, subfolder)
    
    if os.path.isdir(subfolder_path):
        # The full path to the "labels" folder
        labels_folder = os.path.join(subfolder_path, "labels")
        
        # Check if the "labels" folder exists and delete it if it does
        if os.path.exists(labels_folder) and os.path.isdir(labels_folder):
            shutil.rmtree(labels_folder)
            print(f"Deleted: {labels_folder}")
        else:
            print(f"No 'labels' folder found in: {subfolder_path}")

print("Deletion process completed.")
