import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Could not open the camera")

ret, frame = cap.read()
print("Frame shape:", frame.shape)

cap.release()
