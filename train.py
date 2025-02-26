from ultralytics import YOLO

# Load the pre-trained YOLOv9 model
model = YOLO('yolov8n.pt')

# Train the model on CPU
model.train(
    data='/content/HRVD_HELMET/data/data.yaml',  # ✅ Absolute path
    epochs=30, 
    batch=32, 
    imgsz=640, 
    device='cuda:0',
    save_period=10
)
