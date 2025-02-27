import cv2
import torch
import numpy as np
from deep_sort_realtime.deepsort_tracker import DeepSort
from ultralytics import YOLO

# Config Value
video_path = 'data/test.mp4'
conf_threshold = 0.4
tracking_class = 0
TARGET_WIDTH = 640
TARGET_HEIGHT = 640
OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 720

# Initialize DeepSORT
tracker = DeepSort(max_age=30)

# Initialize YOLOv9
weight_path = 'results/epoch_30/epoch30.pt'
device = 'cpu'
model = YOLO(weight_path)

# Load class names
with open('data/classes.names', 'r') as f:
    class_names = f.read().strip().split('\n')

colors = np.random.randint(0, 255, size=(len(class_names), 3), dtype=np.uint8)

cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # Stop when video ends

    frame_resized = cv2.resize(frame, (TARGET_WIDTH, TARGET_HEIGHT))

    # Run YOLO inference
    results = model(frame)  

    detect = []
    for result in results:
        for box in result.boxes.data:  # Extract detected boxes
            x1, y1, x2, y2, confidence, class_id = box.tolist()
            class_id = int(class_id)

            # Filter detections by confidence and class
            if class_id != tracking_class or confidence < conf_threshold:
                continue

            detect.append([
                [int(x1), int(y1), int(x2 - x1), int(y2 - y1)],  # Convert to (x, y, w, h)
                confidence,
                class_id
            ])

    # Update tracker with detections
    tracks = tracker.update_tracks(detect, frame=frame)

    for track in tracks:
        if track.is_confirmed():
            track_id = track.track_id
            bbox = track.to_tlbr()  # Get bounding box in (x1, y1, x2, y2) format
            x1, y1, x2, y2 = map(int, bbox)
            class_id = track.det_class
            color = colors[class_id]

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            label = f"ID {track_id}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    frame_resized_output = cv2.resize(frame, (OUTPUT_WIDTH, OUTPUT_HEIGHT))
    cv2.imshow('Tracking', frame_resized_output)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
