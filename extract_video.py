import cv2
from pathlib import Path
import os
import sys


img_path = Path("./colmap_data/images")
img_path.mkdir(parents=True, exist_ok=True)

# Get the video file path
video_file = "./vdo/test2.MOV"

if not os.path.exists(video_file):
    print(f"Video file not found: {video_file}")
    exit()

# Open video file
cap = cv2.VideoCapture(video_file)

frame_no = 0
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#total_frames = 2400

frame_start=100
frame_freq=10

while cap.isOpened():
    ret, frame = cap.read()

    if not ret or frame is None:
        print(f"\nFrame {frame_no} is unreadable or video ended.")
        break  # Stop if video ends or frame is unreadable

    # Skip the first framestart frames
    if frame_no < frame_start:
        frame_no += 1
        continue

    if frame_no % frame_freq == 0:  # Save every nth frame
        target = str(img_path / f'{frame_no}.jpg')
        cv2.imwrite(target, frame)

    # Display progress bar every 100 frames
    if frame_no % 100 == 0:
        progress = int((frame_no / total_frames) * 50)
        sys.stdout.write(f"\rProgress: [{'#' * progress}{'.' * (50 - progress)}] {frame_no}/{total_frames} frames")
        sys.stdout.flush()

    frame_no += 1

    if frame_no > total_frames:
        break

cap.release()
print("\nProcessing complete!")
