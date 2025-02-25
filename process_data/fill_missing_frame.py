import os
import random
from process_data.process_data import video_mapping
import argparse

def fill(output_images_path, output_labels_path):
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
        open(filepath, 'w').close()


def main():
    parser = argparse.ArgumentParser(description="Process video and annotation paths.")

    parser.add_argument("--output_images_path", type=str, required=True, help="Path to save extracted images")
    parser.add_argument("--output_labels_path", type=str, required=True, help="Path to save extracted labels")
    
    args = parser.parse_args()

    output_images_path = args.output_images_path
    output_labels_path = args.output_labels_path
    
    # Print paths to verify
    print(f"Output Images Path: {output_images_path}")
    print(f"Output Labels Path: {output_labels_path}")

    fill(output_images_path, output_labels_path)

if __name__ == "__main__":
    main()
