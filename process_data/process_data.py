import os
import shutil
import pandas as pd

# Define paths
videos_path = "D:\\HELMET dataset\\part_1"
annotation_path = "D:\\HELMET dataset\\annotation"
output_images_path = "data_ext/images/train"
output_labels_path = "data_ext/labels/train"

# 🔹 Define class mapping (modify as needed)
class_mapping = {
    "DNoHelmetP1NoHelmet": 0,
    "DHelmetP1Helmet": 1,
    "DHelmet": 2,
    "DNoHelmet": 3,
    "DHelmetP1NoHelmet": 4,
    "DHelmetP0NoHelmetP1NoHelmet": 5,
    "DHelmetP1NoHelmetP2NoHelmet": 6,
    "DNoHelmetP1NoHelmetP2NoHelmet": 7,
    "DHelmetP1NoHelmetP2Helmet": 8,
    "DNoHelmetP1Helmet": 9,
    "DHelmetP0NoHelmetP1NoHelmetP2Helmet": 10,
    "DNoHelmetP0NoHelmetP1NoHelmet": 11,
    "DNoHelmetP0NoHelmet": 12,
    "DHelmetP0NoHelmet": 13,
    "DNoHelmetP1HelmetP2Helmet": 14,
    "DHelmetP1HelmetP2Helmet": 15,
    "DNoHelmetP0NoHelmetP1NoHelmetP2NoHelmet": 16,
    "DHelmetP0NoHelmetP1NoHelmetP2NoHelmet": 17,
    "DHelmetP0NoHelmetP1Helmet": 18,
    "DHelmetP1HelmetP2NoHelmet": 19,
    "DNoHelmetP1NoHelmetP2NoHelmetP3NoHelmet": 20,
    "DHelmetP0Helmet": 21,
    "DNoHelmetP1NoHelmetP2Helmet": 22,
    "DHelmetP0NoHelmetP1HelmetP2Helmet": 23,
    "DHelmetP1NoHelmetP2NoHelmetP3Helmet": 24,
    "DHelmetP0HelmetP1Helmet": 25,
    "DNoHelmetP0NoHelmetP1Helmet": 26,
    "DHelmetP1NoHelmetP2NoHelmetP3NoHelmet": 27,
    "DNoHelmetP0NoHelmetP1NoHelmetP2NoHelmetP3NoHelmet": 28,
    "DHelmetP0HelmetP1NoHelmetP2Helmet": 29,
    "DHelmetP0HelmetP1NoHelmetP2NoHelmet": 30,
    "DNoHelmetP0HelmetP1NoHelmet": 31,
    "DHelmetP0HelmetP1HelmetP2Helmet": 32,
    "DHelmetP0NoHelmetP1NoHelmetP2NoHelmetP3Helmet": 33,
    "DNoHelmetP0NoHelmetP1NoHelmetP2Helmet": 34,
    "DHelmetP0NoHelmetP1NoHelmetP2NoHelmetP3NoHelmet": 35
}

# Create output directories
os.makedirs(output_images_path, exist_ok=True)
os.makedirs(output_labels_path, exist_ok=True)

# Get a sorted list of available videos in part_1
video_folders = sorted(os.listdir(videos_path))

# Create a mapping of video names to numbers
video_mapping = {video: idx + 1 for idx, video in enumerate(video_folders)}

# Process each video folder
for video_name, video_number in video_mapping.items():
    video_frames_path = os.path.join(videos_path, video_name)
    
    if not os.path.isdir(video_frames_path):
        continue  # Skip non-folder items
    
    for frame_file in os.listdir(video_frames_path):
        if frame_file.endswith(".jpg"):
            original_frame_path = os.path.join(video_frames_path, frame_file)
            new_frame_name = f"{video_number}_{frame_file}"
            new_frame_path = os.path.join(output_images_path, new_frame_name)
            shutil.copy(original_frame_path, new_frame_path)

# Process annotation files
for video_name, video_number in video_mapping.items():
    annotation_file = os.path.join(annotation_path, f"{video_name}.csv")
    
    # Check if annotation file exists
    if not os.path.exists(annotation_file):
        print(f"Skipping {video_name}, no annotation found.")
        continue

    # Read the annotation CSV
    df = pd.read_csv(annotation_file, delimiter=',')  # Ensure correct delimiter

    # Process each row in the annotation file
    for _, row in df.iterrows():
        frame_id = row["frame_id"]
        x, y, w, h = row["x"], row["y"], row["w"], row["h"]
        label = row["label"]

        # Construct new frame and label filenames
        #new_frame_name = f"{video_number}_{frame_id}.jpg"
        new_label_name = f"{video_number}_{str(frame_id).zfill(2)}.txt"

        # Path to the label file
        label_path = os.path.join(output_labels_path, new_label_name)

        # Convert bounding box to YOLO format
        img_width, img_height = 1920, 1080  # Adjust according to actual frame size
        x_center = (x + w / 2) / img_width
        y_center = (y + h / 2) / img_height
        width = w / img_width
        height = h / img_height

        # Get class ID
        class_id = class_mapping[label]  

        # Append bounding box information to the label file
        with open(label_path, "a") as label_file:
            label_file.write(f"{class_id} {x_center} {y_center} {width} {height}\n")

print("Data preparation complete!")