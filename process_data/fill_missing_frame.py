import os
import random
from process_data.process_data import video_mapping

# Define paths
output_images_path = "../data_ext/images/train"  # Folder where images are stored
output_labels_path = "../data_ext/labels/train"  # Folder where annotation files should be

# Get all frame images from the output images folder
frame_files = [f for f in os.listdir(output_images_path) if f.endswith(".jpg")]
label_files = [f for f in os.listdir(output_labels_path) if f.endswith(".txt")]
for label in label_files[:10]:
    print(label)
print(len(label_files))
# Extract expected label filenames and video numbers
expected_labels = {}
for frame in frame_files:
    video_num, frame_id = frame.replace(".jpg", "").split("_")  # Extract video number and frame ID
    expected_labels[f"{video_num}_{frame_id}.txt"] = video_mapping.get(int(video_num), "Unknown_Video")

# Get existing label files
existing_labels = set(os.listdir(output_labels_path))

# Find missing annotation files
missing_annotations = {fname: vname for fname, vname in expected_labels.items() if fname not in existing_labels}

# Print up to 5 missing annotation files with their original video name
print("Missing annotation files (showing up to 5 examples):")
for missing_file, video_name in random.sample(list(missing_annotations.items()), min(5, len(missing_annotations))):
    print(f"Missing: {missing_file}, Video: {video_name}")

print(f"Total missing annotation files: {len(missing_annotations)}")
for missing_file in missing_annotations.keys():
    filepath = os.path.join(output_labels_path, missing_file)
    open(filepath, 'w').close()  # Correct way to create an empty file

