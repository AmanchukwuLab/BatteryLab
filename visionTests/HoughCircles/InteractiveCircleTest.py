import numpy as np
from BatteryLab.helper.Logger import Logger
from BatteryLab.robots.AutoCorrection import AutoCorrection
from BatteryLab.robots.Constants import AutoCorrectionConfig
import cv2
import sys

# Set up component configs
configs = AutoCorrectionConfig()

# Set up logger and AutoCorrection module
log_path = "/home/yuanjian/Research/BatteryLab/logs/"
logger = Logger("circle_detect_test", log_path, "circle_detect_test.log")
correcter = AutoCorrection(logger)

# Define image path
# img_folder_path = "/home/yuanjian/Research/BatteryLab/images/"
img_folder_path = './'

if len(sys.argv)>1:
    img_name = sys.argv[1]
else:
    img_name = 'suction_new.jpg'

image_path = img_folder_path + img_name

# Load the image
img = cv2.imread(image_path, cv2.IMREAD_COLOR)
img_width = min(img.shape[:2])
print(f"img_width={img_width}")

# Identify circles, display image
object_config = {
        'minDist': img_width//3, # We only want one circle, so set this large
        'param1' : 250,           # Too high will miss edges, too low -> noisy edges
        'param2' : 30,            # Higher is stricter (fewer circles)
        'minR'   : 60,
        'maxR'   : 95,
        }
if 'suction' in img_name:
    img = cv2.bitwise_not(img)    # invert image to more easily detect suction cup
    object_config['param2'] = 40
    object_config['minR'] = 40
    object_config['maxR'] = 80

# Make a working copy so we don't destroy original defaults
interactive_config = object_config.copy()

def update(_=None):
    """Run detection and redraw using current interactive parameters."""
    found_circles = correcter.detect_object_center(img, interactive_config)
    print(f"found_circles: {found_circles}")

    # draw_detection crashes if found_circles is empty, so guard it
    if found_circles:
        newimage = correcter.draw_detection(img.copy(), found_circles)
    else:
        newimage = img.copy()

    cv2.imshow("Identified Circles", newimage)

def set_minDist(v):
    interactive_config['minDist'] = max(1, v)  # minDist must be >= 1
    update()

def set_param1(v):
    interactive_config['param1'] = max(1, v)   # param1 must be >= 1
    update()

def set_param2(v):
    interactive_config['param2'] = max(1, v)   # param2 must be >= 1
    update()

def set_minR(v):
    interactive_config['minR'] = max(1, v)     # min radius must be >= 1
    # Ensure maxR >= minR to avoid invalid range
    if interactive_config['maxR'] < interactive_config['minR']:
        interactive_config['maxR'] = interactive_config['minR']
        cv2.setTrackbarPos("maxR", "Identified Circles", interactive_config['maxR'])
    update()

def set_maxR(v):
    interactive_config['maxR'] = max(interactive_config['minR'], v)  # maxR >= minR
    update()

# Create window and trackbars
cv2.namedWindow("Identified Circles", cv2.WINDOW_NORMAL)

cv2.createTrackbar("minDist", "Identified Circles",
                   interactive_config['minDist'], img_width, set_minDist)
cv2.createTrackbar("param1", "Identified Circles",
                   interactive_config['param1'], 500, set_param1)
cv2.createTrackbar("param2", "Identified Circles",
                   interactive_config['param2'], 200, set_param2)
cv2.createTrackbar("minR", "Identified Circles",
                   interactive_config['minR'], img_width, set_minR)
cv2.createTrackbar("maxR", "Identified Circles",
                   interactive_config['maxR'], img_width, set_maxR)

# Run once at startup using original defaults
update()

# Handle exit gracefully
while True:
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q') or k == 27: # q or ESC
        break
    if k == ord('p'):
        print("\nCurrent object_config:")
        print("{")
        for k2, v2 in interactive_config.items():
            print(f"    '{k2}': {v2},")
        print("}")
    if cv2.getWindowProperty("Identified Circles", cv2.WND_PROP_VISIBLE) < 1:
        break

cv2.destroyAllWindows() # Redundant. Shuts all cv2 windows.
print("Test complete")
