import cv2
from ultralytics import YOLO

# Load the YOLO model
model = YOLO("results/epoch_30/epoch30.pt")

# Open the video file
video_path = "data/test.mp4"
cap = cv2.VideoCapture(video_path)

# Define the desired resolution (e.g., 640x480)
TARGET_WIDTH = 640
TARGET_HEIGHT = 640
OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 720

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Resize the frame to the desired resolution
        frame_resized = cv2.resize(frame, (TARGET_WIDTH, TARGET_HEIGHT))

        # Run YOLO tracking on the resized frame
        results = model(frame_resized)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        annotated_frame = cv2.resize(annotated_frame, (OUTPUT_WIDTH, OUTPUT_HEIGHT))
        cv2.imshow("YOLO11 Tracking", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
