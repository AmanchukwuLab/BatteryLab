import cv2
import numpy as np
from time import sleep
import sys

# Delay to get into position
# delay = 3 #seconds
# for i in range(delay):
#     print(f"Capturing in {delay-i}...")
#     sleep(1)

# Open the camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Could not open the camera")

# Capture and display an image
ret, frame = cap.read()
if not ret:
    raise RuntimeError("Cound not read a frame from the device")

cv2.imshow("image", frame)
while True:
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q') or k == 27: # q or ESC
        break
    if cv2.getWindowProperty("image", cv2.WND_PROP_VISIBLE) < 1:
        break

# Write the image
if len(sys.argv)>1:
    focus = sys.argv[1]
else:
    focus = "NULL"
cv2.imwrite(f"focus_{focus}.jpg", frame)

cap.release()
cv2.destroyAllWindows() # Redundant. Shuts all cv2 windows.
