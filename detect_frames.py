import cv2
import os
from ultralytics import YOLO

# Load the YOLO model
model = YOLO("results/epoch_30/epoch30.pt")

# Define folders
input_folder = "data/Mandalay_1_131"
output_folder = "inference_results/Mandalay_1_131"
os.makedirs(output_folder, exist_ok=True)

# Define sizes
YOLO_WIDTH, YOLO_HEIGHT = 640, 640  # YOLO input size
OUTPUT_WIDTH, OUTPUT_HEIGHT = 1080, 720  # Desired output size

# Get list of image files
image_files = sorted([f for f in os.listdir(input_folder) if f.endswith((".jpg", ".png", ".jpeg"))])

# Process each image
for image_file in image_files:
    image_path = os.path.join(input_folder, image_file)
    
    # Read the image
    frame = cv2.imread(image_path)
    if frame is None:
        continue  # Skip if the image cannot be loaded

    # Resize the frame for YOLO detection
    frame_resized = cv2.resize(frame, (YOLO_WIDTH, YOLO_HEIGHT))

    # Run YOLO detection
    results = model(frame_resized)

    # Visualize detection results
    annotated_frame = results[0].plot()

    # Resize the output to 1080x720
    final_output = cv2.resize(annotated_frame, (OUTPUT_WIDTH, OUTPUT_HEIGHT))

    # Save the processed image
    output_path = os.path.join(output_folder, image_file)
    cv2.imwrite(output_path, final_output)

    # Display the output
    cv2.imshow("YOLO Tracking", final_output)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cv2.destroyAllWindows()
