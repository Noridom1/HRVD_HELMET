from ultralytics import YOLO

model = YOLO('results/epoch_30/epoch30.pt')

results = model.track()