import numpy as np
from BatteryLab.helper.Logger import Logger
from BatteryLab.robots.AutoCorrection import AutoCorrection
from BatteryLab.robots.Constants import AutoCorrectionConfig
import cv2

# Set up component configs
configs = AutoCorrectionConfig()

# Set up logger and AutoCorrection module
log_path = "/home/yuanjian/Research/BatteryLab/logs/"
logger = Logger("circle_detect_test", log_path, "circle_detect_test.log")
correcter = AutoCorrection(logger)

# Define image path
img_folder_path = "/home/yuanjian/Research/BatteryLab/images/"
# img_name = "circle_detect_test.jpg"
img_name = "Spacer_focus675_light.jpg"
image_path = img_folder_path + img_name

# Load the image
img = cv2.imread(image_path)
img_width = min(img.shape[:2])
 
# Identify circles, display image
object_config = {
        'minDist': img_width//10, # We only want one circle, so set this large
        'param1' : 250,           # Too high will miss edges, too low -> noisy edges
        'param2' : 30,            # Higher is stricter (fewer circles)
        'minR'   : img_width//10,
        'maxR'   : img_width//5,
        }
if 'suction' in img_name:
    img = cv2.bitwise_not(img)    # invert image to more easily detect suction cup
    object_config['param1'] = 250
    object_config['param2'] = 30
    object_config['minR'] = img_width//20
    object_config['maxR'] = img_width//8

found_circles = correcter.detect_object_center(img, object_config)
print(f"found_circles: {found_circles}")
newimage = correcter.draw_detection(img, found_circles)
cv2.imshow("Identified Circles", newimage)

# Handle exit gracefully
while True:
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q') or k == 27: # q or ESC
        break
    if cv2.getWindowProperty("Identified Circles", cv2.WND_PROP_VISIBLE) < 1:
        break

cv2.destroyAllWindows() # Redundant. Shuts all cv2 windows.
print("Test complete")
