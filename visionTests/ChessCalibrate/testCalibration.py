import json
import numpy as np
import cv2 as cv

def load_calibration(filepath):
    with open(filepath, 'r') as f:
        calib_data = json.load(f)
    camera_matrix = np.array(calib_data['cameraMatrix'])
    dist_coeffs = np.array(calib_data['distCoeffs'])
    return camera_matrix, dist_coeffs

def undistort_image(img, camera_matrix, dist_coeffs):
    h, w = img.shape[:2]
    new_camera_matrix, roi = cv.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))
    undistorted_img = cv.undistort(img, camera_matrix, dist_coeffs, None, new_camera_matrix)
    x, y, w, h = roi
    undistorted_img = undistorted_img[y:y+h, x:x+w]

    return undistorted_img

if __name__ == '__main__':
    mtx, dist = load_calibration('calibration.json')
    print("Loaded params successfully")

    img = cv.imread("/home/yuanjian/Research/BatteryLab/images/Separator_focus675_light.jpg")
    undistorted_img = undistort_image(img, mtx, dist)
    cv.imshow("Original", img)
    cv.imshow("Undistorted", undistorted_img)
    cv.waitKey(0)
    cv.destroyAllWindows()
