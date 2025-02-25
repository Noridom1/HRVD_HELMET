import os
import shutil
import argparse

def split(frames_folder, labels_folder, val_images_folder, val_labels_folder):
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

def main():
    parser = argparse.ArgumentParser(description="Process video and annotation paths.")
    parser.add_argument("--frames_folder", type=str, required=True, help="Path to the frames directory")
    parser.add_argument("--labels_folder", type=str, required=True, help="Path to the labels directory")
    parser.add_argument("--val_images_folder", type=str, required=True, help="Path to save val frames")
    parser.add_argument("--val_labels_folder", type=str, required=True, help="Path to save val labels")
    
    args = parser.parse_args()
    
    frames_folder = args.frames_folder
    labels_folder = args.labels_folder
    val_images_folder = args.val_images_folder
    val_labels_folder = args.val_labels_folder
    
    # Print paths to verify
    print(f"Frames Path: {frames_folder}")
    print(f"Labels Path: {labels_folder}")
    print(f"Val Images Path: {val_images_folder}")
    print(f"Val Labels Path: {val_labels_folder}")
    
    # Ensure val directories exist
    os.makedirs(val_images_folder, exist_ok=True)
    os.makedirs(val_labels_folder, exist_ok=True)

    split(frames_folder, labels_folder, val_images_folder, val_labels_folder)

    print("Splited train_val successfully")

if __name__ == "__main__":
    main()
