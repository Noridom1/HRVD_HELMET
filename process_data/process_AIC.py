import os
import cv2
import pandas as pd
from collections import defaultdict

def parse_gt_file(gt_path):
    """ Parse ground truth file and return dictionary {(video_id, frame): [detections]} """
    detections = defaultdict(list)
    with open(gt_path, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            video_id, frame, x, y, w, h, obj_class = parts
            video_id, frame, x, y, w, h = map(int, [video_id, frame, x, y, w, h])
            detections[(video_id, frame)].append((x, y, w, h, obj_class))
    return detections

def merge_bounding_boxes(detections):
    """ Merge bounding boxes for motorcycles with their associated people """
    merged_data = []
    for (video_id, frame), objects in detections.items():
        motorcycles = [obj for obj in objects if obj[4] == 'motorcycle']
        people = [obj for obj in objects if 'Helmet' in obj[4] or 'NoHelmet' in obj[4]]
        
        for idx, (mx, my, mw, mh, _) in enumerate(motorcycles):
            x_min, y_min = mx, my
            x_max, y_max = mx + mw, my + mh
            labels = ['motorcycle']
            
            for px, py, pw, ph, p_class in people:
                if (px >= x_min and py >= y_min and px + pw <= x_max and py + ph <= y_max):
                    labels.append(p_class)
                    x_min, y_min = min(x_min, px), min(y_min, py)
                    x_max, y_max = max(x_max, px + pw), max(y_max, py + ph)
            
            merged_data.append((video_id, frame, idx, x_min, y_min, x_max - x_min, y_max - y_min, labels))
    return merged_data

def process_videos(video_path, output_path, detections):
    output_frames = os.path.join(output_path, 'frames')
    output_labels = os.path.join(output_path, 'labels')
    """ Extract frames from videos, crop objects, and save """
    os.makedirs(output_frames, exist_ok=True)
    os.makedirs(output_labels, exist_ok=True)

    videos_cnt = 0
    for video_id in set(v[0] for v in detections.keys()):
        video_file = os.path.join(video_path, f"{str(video_id).zfill(3)}.mp4")
        if not os.path.exists(video_file):
            continue
        cap = cv2.VideoCapture(video_file)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        
        while cap.isOpened():
            frame_id = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            if (video_id, frame_id) not in detections:
                cap.grab()
                continue
            
            ret, frame = cap.read()
            if not ret:
                break
            
            for obj_id, (x, y, w, h, labels) in enumerate(merge_bounding_boxes({(video_id, frame_id): detections[(video_id, frame_id)]})):
                cropped_img = frame[y:y+h, x:x+w]
                img_name = f"{video_id}_{frame_id}_{obj_id}.jpg"
                txt_name = f"{video_id}_{frame_id}_{obj_id}.txt"
            
                cv2.imwrite(os.path.join(output_frames, img_name), cropped_img)
                with open(os.path.join(output_labels, txt_name), 'w') as f:
                    f.write(" ".join(labels))
        videos_cnt += 1
        print(f"processed {videos_cnt}/100 videos")
        cap.release()

# Example usage
gt_path = "D:\\aicity2024_track5_train\\gt.txt"
video_path = "D:\\aicity2024_track5_train\\videos"
output_path = "data\\AIC2024"

detections = parse_gt_file(gt_path)
process_videos(video_path, output_path, detections)

