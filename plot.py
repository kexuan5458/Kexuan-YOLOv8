import matplotlib.pyplot as plt
import csv

# Read data from CSV file
file_path = '/home/ee904/Repo/yolov8/runs/detect/train/results.csv'  # Replace with the actual path to your CSV file

epochs = []
box_losses = []
cls_losses = []
dfl_losses = []

with open(file_path, 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        epochs.append(int(row['epoch']))
        box_losses.append(float(row['train/box_loss']))
        cls_losses.append(float(row['train/cls_loss']))
        dfl_losses.append(float(row['train/dfl_loss']))

# Plot the losses
plt.figure(figsize=(10, 6))
plt.plot(epochs, box_losses, label='Box Loss')
plt.plot(epochs, cls_losses, label='Class Loss')
plt.plot(epochs, dfl_losses, label='Objectness Loss')

# Customize the plot
plt.title('YOLO Training Losses Over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
