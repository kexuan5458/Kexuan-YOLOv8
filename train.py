from ultralytics import YOLO

model = YOLO('/home/ee904/Repo/yolov8/runs/detect/train3/weights/last.pt')

results = model.train(save_period=1, data='cfg/default.yaml', imgsz=1152, epochs=100, resume=True)

success = model.export()