from ultralytics import YOLO

# Load the pre-trained YOLOv9 model
model = YOLO('yolov8n.pt')

# Train the model on CPU
model.train(
    data='D:/OD+Tracking/yolov9/data_ext/data.yaml',  # ✅ Absolute path
    epochs=10, 
    batch=16, 
    imgsz=640, 
    device='cpu'
)
