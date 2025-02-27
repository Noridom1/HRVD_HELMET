from ultralytics import YOLO
import sys
import os
import argparse
from OC_SORT.trackers.ocsort_tracker.ocsort import OCSort

weight_path = 'results/epoch_30/epoch30.pt'
model = YOLO(weight_path)

INPUT_HEIGHT = 1088
INPUT_WIDTH = 1088
OUTPUT_HEIGHT = 640
OUTPUT_WIDTH = 640

class ODTracker():
    def __init__(self, detector, tracker):
        self.detector = detector
        self.tracker = tracker

    def predict(self, video_path, extracted=False):
        
        
def main():
    parser = argparse.ArgumentParser(description="Process video and annotation paths.")
    parser.add_argument("--video_path", type=str, required=True, help="Path to the video directory")
    parser.add_argument("--extracted", type=bool, help="Whether the video has been extracted into frames", default=False)
    parser.add_argument("--output_dir", type=str, required=False, help="Path to save extracted images", default='inference_results')
    
    args = parser.parse_args()


if __name__ == "__main__":
    main()


