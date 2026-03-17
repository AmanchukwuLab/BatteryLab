import cv2
import numpy as np
from time import sleep
import sys
import argparse
import subprocess
import re

# Auxiliary function for get/set focus_absolute
def get_focus(device='/dev/video0'):
    cmd = f'v4l2-ctl -d {device} --get-ctrl=focus_absolute'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    match = re.search(r"focus_absolute: (\d+)", result.stdout)
    if match: 
        return int(match.group(1))
    return None

def set_focus(focus, device='/dev/video0'):
    subprocess.run(f"v4l2-ctl -d {device} --set-ctrl=focus_auto=0", shell = True)
    subprocess.run(f"v4l2-ctl -d {device} --set-ctrl=focus_absolute={focus}", shell=True)
    print(f"Focus set to {focus}")
    return None

initial_focus = get_focus()

# Set up argparser
parser = argparse.ArgumentParser()
parser.add_argument('focus_absolute', type=int, help='Value for absolute focus')
parser.add_argument('--show', choices=['True', 'False'], default='True', help='Whether to show the captured image.')
parser.add_argument('--save', choices=['True', 'False'], default='False', help='Whether to save the captured image.')
parser.add_argument('--savename', default='boringname', help='Name for saved image')
args = parser.parse_args()

# Set the focus
set_focus(args.focus_absolute)

# Open the camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Could not open the camera")

# Capture image
ret, frame = cap.read()
if not ret:
    raise RuntimeError("Cound not read a frame from the device")

# Display image
if args.show == 'True':
    cv2.imshow("image", frame)
    while True:
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q') or k == 27: # q or ESC
            break
        if cv2.getWindowProperty("image", cv2.WND_PROP_VISIBLE) < 1:
            break

# Write the image
if args.save == 'True':
    cv2.imwrite(f"{args.savename}_focus_{focus}.jpg", frame)

# Reset focus to original value
set_focus(initial_focus)

cap.release()
cv2.destroyAllWindows() # Redundant. Shuts all cv2 windows.
