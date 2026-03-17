import cv2
import numpy as np
from time import sleep
import sys
import subprocess
import re
import argparse
import math

argparser = argparse.ArgumentParser()
argparser.add_argument("--resolution", type=float, help='Fraction of available focus values to capture an image for (ex. for focus_absolute:(0,255), setting "--resolution 1.0" would capture 256 images, "resolution 0.5" would capture 128 images, etc...)', default=0.25)
args = argparser.parse_args()
# Error checking
if args.resolution < 0. or args.resolution > 1.:
    raise ValueError(f"Resolution must be between 0 and 1 (set to {args.resolution}.")

# Auxiliary function for get/set focus_absolute
def get_focus(device='/dev/video0'):
    cmd = f'v4l2-ctl -d {device} --list-ctrls'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    focus_match = re.search(r"focus_absolute.*value=(\d+)", result.stdout)
    minmax_match = re.search(f"focus_absolute.*min=(\d+).*max=(\d+)", result.stdout)

    # Parse matches 
    if focus_match: 
        focus = int(focus_match.group(1))
    else:
        focus = None

    if minmax_match:
        minval = int(minmax_match.group(1))
        maxval = int(minmax_match.group(2))
    else:
        minval, maxval = None, None
   
    return focus, minval, maxval

def set_focus(focus, device='/dev/video0'):
    subprocess.run(f"v4l2-ctl -d {device} --set-ctrl=focus_automatic_continuous=0", shell = True)
    subprocess.run(f"v4l2-ctl -d {device} --set-ctrl=focus_absolute={focus}", shell=True)
    print(f"Focus set to {focus}")
    return None

initial_focus, minfocus, maxfocus = get_focus()


# Open the camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Could not open the camera")

# Set up movie capturing
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
ret, frame=cap.read()
if not ret:
    raise RuntimeError("Could not read initial frame")
print(frame.shape, type(frame.shape))
height, width = frame.shape[:2]
out = cv2.VideoWriter('focus_movie.avi', fourcc, 20.0, (width, height))

if not out.isOpened():
    raise RuntimeError("VideoWriter failed to open.")

# Capture images at incremental focus values
focus_range = maxfocus-minfocus
n_frames = math.ceil((focus_range)*args.resolution)
for i in range(n_frames+1):
    focus = min(maxfocus, int(focus_range*i/n_frames+minfocus))
    # Set the focus
    set_focus(focus)
    sleep(0.15)

    # Capture image
    ret, frame = cap.read()
    if not ret:
        raise RuntimeError("Cound not read a frame from the device")
    # Add focus value to frame
    cv2.putText(frame, f"focus={focus}", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0))

    # Add frame to movie
    out.write(frame)
    cv2.imshow('frame', frame)
    cv2.waitKey(1)

# Reset focus to original value
set_focus(initial_focus)

cap.release()
out.release()
cv2.destroyAllWindows() # Redundant. Shuts all cv2 windows.
