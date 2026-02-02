import cv2
import numpy as np

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
count = np.loadtxt('counter.txt')
count += 1
cv2.imwrite(f"camera-pic-of-chessboard-{count}.jpg", frame)
np.savetxt('counter.txt', np.array([count]))

cap.release()
cv2.destroyAllWindows() # Redundant. Shuts all cv2 windows.
