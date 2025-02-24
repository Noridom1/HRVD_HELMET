import os
import shutil

# Define paths
frames_folder = 'data_ext/images/train'
labels_folder = 'data_ext/labels/train'
val_images_folder = 'data_ext/images/val'
val_labels_folder = 'data_ext/labels/val'

# Ensure val directories exist
os.makedirs(val_images_folder, exist_ok=True)
os.makedirs(val_labels_folder, exist_ok=True)

# Process each file in the frames folder
for filename in os.listdir(frames_folder):
    if filename.endswith('.jpg'):
        parts = filename.split('_')  # Split based on '_'
        if len(parts) < 2:
            continue  # Skip invalid filenames
        
        video_id = int(parts[0])  # Extract video ID
        
        if video_id >= 101:  # Move only if video ID >= 101
            image_path = os.path.join(frames_folder, filename)
            label_filename = filename.replace('.jpg', '.txt')  # Corresponding label file
            label_path = os.path.join(labels_folder, label_filename)

            # Move image
            shutil.move(image_path, os.path.join(val_images_folder, filename))

            # Move label if it exists
            if os.path.exists(label_path):
                shutil.move(label_path, os.path.join(val_labels_folder, label_filename))
            else:
                print(f"Warning: Label file {label_filename} not found!")

print("Files moved successfully!")
