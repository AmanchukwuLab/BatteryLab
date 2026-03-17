import numpy as np
import cv2
import time
import os
import threading
import json
from datetime import datetime

from ..helper.Logger import Logger
from .Constants import Components, AssemblySteps, AutoCorrectionConfig, StepCorrectionConfig

from pathlib import Path

class AutoCorrection():
    # Module for correcting component placement based on lookup camera images
    def __init__(self, logger: Logger):
        self.logger = logger
        
        # Load in configuration constants (parameters for HoughCircles)
        self.correction_config = AutoCorrectionConfig()
        self.cam_port_bottom = self.correction_config.CAM_PORT_BOTM
        self.cam_port_top = self.correction_config.CAM_PORT_TOP
        self.dir_name = Path(os.path.dirname(__file__)) / "Calibration"
        if not self.dir_name.exists():
            os.makedirs(self.dir_name)
        self.vision_params_path = self.dir_name / "vision_params.json"
        self.vision_params = self.get_vision_params()
        pass

    def detect_object_center(self, img, object_config:dict):
        # Image preprocessing
        img_color = np.copy(img)
        img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
        img_gray = cv2.medianBlur(img_gray, 5)
        
        # Run detection algorithm
        circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, object_config['minDist'], param1=object_config['param1'], param2=object_config['param2'], minRadius=object_config['minR'], maxRadius=object_config['maxR'])
        h, w = img.shape[:2]
        found_circles = []
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for c in circles[0, :]:
                x, y, r = int(c[0]), int(c[1]), int(c[2])
                if x-r <=0 or y-r <= 0 or x+r >= w or y+r >=h:
                    self.logger.info("Detected circle out of scope! Result discarded")
                else:
                    found_circles.append([[x, y], r])
            found_circles = sorted(found_circles, key=lambda x: x[1])
            self.logger.debug(f"sorted circles: {found_circles}")
            found_circles = found_circles[-1] if len(found_circles) > 0 else []
        return found_circles

    def get_vision_params(self):
        # Load previously stored calibration parameters
        try:
            print(f"Checking in {self.vision_params_path} for vision_params.json...")
            with open(self.vision_params_path, mode='r') as f:
                result = json.load(f)
                print("Previously computed vision_params found and loaded successfully.")
                return result
        except Exception as e:
            print(f"Unable to find previously computed vision_params due to exception: {e}")
            return {}

    def write_vision_params(self):
        with open(self.vision_params_path, mode='w') as f:
            json.dump(self.vision_params, f)
        print("vision_params.json modified")
        return None
   
    def compute_conversion(self, img_centered, img_adjusted, dx, dy):
        img_width = min(img_centered.shape[:2])
        # NOTE: these parameters can be tuned using the interactive script in BatteryLab/tests/HoughCircles
        object_config = {
                'minDist': img_width//3,  # We only want one circle, so set this large
                'param1' : 300,           # Too high will miss edges, too low -> noisy edges
                'param2' : 30,            # Higher is stricter (fewer circles, radius tends to be slightly inscribed the actual)
                'minR'   : 45,
                'maxR'   : 80,
                }
        suction_config = object_config.copy()
        suction_config['param1'] = 95
        suction_config['param2'] = 35
        suction_config['minR'] = 30
        suction_config['maxR'] = 50

        # Find circles in both images
        found_circles_center = self.detect_object_center(img_centered, suction_config)

        # Handle multiple circles found
        if len(found_circles_center) == 0:
            # If no circles found, save the image for later reference
            cv2.imwrite(self.dir_name/"Suction_NoCircleDetected_center.png", img_centered)
            print(f"Saving img_centered to {self.dir_name}...")
            time.sleep(2)
            raise ValueError("No circles found during calibration!")
        elif type(found_circles_center[1]) != int:
            msg = "Multiple circles found during machine vision calibration in image of centered suction cup!"
            self.logger.info(msg)
            print(f"found_circles_center: {found_circles_center}")
            
            # Save image for later reference
            cv2.imwrite(self.dir_name/"Suction_MultDetected_center.png", img_centered)

            # Only keep the circle with the smaller radius
            radii = [row[1] for row in found_circles_center]
            found_circles_center = found_circles_center[np.argmin(radii)]
        
        found_circles_adjust = self.detect_object_center(img_adjusted, suction_config)
        if len(found_circles_adjust) == 0:
            # If no circles found, save the image for later reference
            cv2.imwrite(self.dir_name/"Suction_NoCircleDetected_adjust.png", img_adjusted)
            raise ValueError("No circles found during calibration!")
        elif type(found_circles_adjust[1]) != int:
            msg = "Multiple circles found during machine vision calibration in image of adjusted suction cup!"
            self.logger.info(msg)
            print(f"found_circles_adjust: {found_circles_adjust}")
            
            # Save image for later reference
            cv2.imwrite(self.dir_name/"Suction_MultDetected_adjust.png", img_adjusted)
            
            # Only keep the circle with the smaller radius
            radii = [row[1] for row in found_circles_adjust]
            found_circles_adjust = found_circles_adjust[np.argmin(radii)]

        # Save calibration images for future reference
        center_drawn = self.draw_detection(img_centered, found_circles_center, text=str(found_circles_center))
        adjust_drawn = self.draw_detection(img_adjusted, found_circles_adjust, text=str(found_circles_adjust))
        print(f"Saving calibration images in {self.dir_name}")
        cv2.imwrite(self.dir_name / "centered_calibration_image.png", center_drawn)
        cv2.imwrite(self.dir_name / "adjusted_calibration_image.png", adjust_drawn)
        cv2.imwrite(self.dir_name / "BLANK_centered_calibration.png", img_centered)

        # Compute robot-pixel conversion factor
        dx_image = found_circles_adjust[0][0] - found_circles_center[0][0]
        dy_image = found_circles_adjust[0][1] - found_circles_center[0][1]
        x_convert = dx/dy_image # robot space per pixel space (x and y are flipped between the camera and the robot arm! This just depends on how the system was set up.)
        y_convert = dy/dx_image # robot space per pixel space

        # Write conversion factors to machine vision params, then return to user
        self.vision_params['x_convert'] = x_convert
        self.vision_params['y_convert'] = y_convert
        self.vision_params['suction_center'] = found_circles_center[0]
        self.vision_params['date_calibrated'] = datetime.now().strftime("%b_%d_%Y")
        self.vision_params['object_config'] = object_config
        self.vision_params['suction_config'] = suction_config
        self.write_vision_params()
        return self.vision_params
        
    def get_offset_simple(self, img):
        found_circles = self.detect_object_center(img, self.vision_params['object_config'])
        
        # DEBUGGING: save picture with and without circles drawn on
        print("found_circles = ", found_circles) # DEBUGGING
        try:
            print(f"Saving image to {self.dir_name}...")
            cv2.imwrite(self.dir_name / "get_offset_func_image_clean.png", img)
            img_drawn = self.draw_detection(img, found_circles, text=str(found_circles))
            cv2.imwrite(self.dir_name / "get_offset_func_image.png", img_drawn)
        except:
            print("Something went wrong. Proceeding (other error catching should catch the issue)...")

        # Handle cases of none or multiple circles found
        current = datetime.now().strftime("%b_%d_%Y_%I:%M")
        
        if len(found_circles) == 0:
            # If no circles found, save the image for later reference
            cv2.imwrite(self.dir_name / f"NoCircleDetected_offset_{current}.png", img)
            raise ValueError("No circles found for computing offset!")

        elif type(found_circles[1]) != int:
            msg = "Multiple circles found while computing offset! Keeping the circle with smaller radius."
            self.logger.info(msg)
            print(f"found_circles: {found_circles}")
            
            # Save image for later reference
            cv2.imwrite(self.dir_name / "MultDetected_offset_{current}.png", img)
            
            # Only keep the circle with the smaller radius
            radii = [row[1] for row in found_circles]
            found_circles = found_circles[np.argmin(radii)]

        # Compute pixel difference between known center from calibration and the detected center for this component
        dx_pixel = self.vision_params['suction_center'][0] - found_circles[0][0]
        dy_pixel = self.vision_params['suction_center'][1] - found_circles[0][1]

        # Convert to robot arm units
        dy = dx_pixel*self.vision_params['y_convert']
        dx = dy_pixel*self.vision_params['x_convert']
        return dx, dy

    def project_to_3d(self, image_coordinates, H_mtx): 
        """
        This method takes the Homography matrix and the 2d image cartesian coordinates. It returns the (x, y) cartesian coordinates in 3d cartesian world coordinates on floor plane(at z=0). Notice that z coordinate is omitted here and added inside the tracking funtion. 
        
        Parameters
        ----------
        image_coordinates: 2d pixel coordinates (x,y)
        h: 3x3 Homography matrix np.array[3x3]
        Returns
        ----------
        floor_coordinates: List of x, y coordinates in 3d world of same pixel on floor plane i.e. (x,y,z) Considering z=0 and 
        ommitted here.
        """
        # if H_mtx == None:
        #     os.chdir(os.path.join(PATH, 'camera_data'))
        #     H_mtx = np.load('H_mtx.npy')
        #adding 1 for homogenous coordinate system
        x, y, w = H_mtx @ np.array([[*image_coordinates, 1]]).T
        X, Y = np.around(x/w, decimals=3), np.around(y/w, decimals=3) # Transform homogenous coordinates into cart coordinates
        return np.array([X, Y, 0, 0, 0, 0], dtype=np.float32)
    
    def draw_detection(self, img, found_circle, text:str=None):
        img_output = np.copy(img)
        h, w = img_output.shape[:2]
        img_center = (w//2, h//2)
        cv2.drawMarker(img_output, img_center, (0,255,0), cv2.MARKER_CROSS, 10, 1)
        self.logger.debug(f"found_circles:{found_circle}")
        center = found_circle[0]
        cv2.drawMarker(img_output, center, (0,0,255), cv2.MARKER_CROSS, 10, 1)
        cv2.circle(img_output, center, found_circle[1], (255, 0, 255), 1)
        if text:
            cv2.putText(img_output, text, (20, h-20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        return img_output

    def get_offset(self, img, component:Components, state: AssemblySteps):
        """Returns the image, a 6-element matrix with the corrections, and a boolean indicating whether or not the component was successfully picked up.
            Note: ( failure mode) if a component is not detected, the algorithm attempts to detect the suction cup in the image to determine if perhaps the component was not picked up at all. If the suction cup is not detected, however, this function will return "True", assuming that the component detection algorithm was incorrect."""

        # Get calibration data (homography matrix)
        calibration_file = Path(os.path.dirname(__file__)) / "data" / "calibration.json"
        with open(calibration_file, "r") as json_file:
            # Note: H_mtx is a homography matrix, which encodes the distortion/translation of a plane in an image. In this case, it encodes the circle's distortion to get a more accurate measure of 'center'.
            H_mtx = np.array(json.load(json_file)[f"H_mtx_{state}"], dtype=np.float32)

        # Attempt to find the component in the image
        detectedObj = self.detect_object_center(img, getattr(self.correction_config, f"{component.name}_{state}"))
        
        # Handle possible outcomes of attempted detection
        if len(detectedObj) > 0:
            # something was detected
            xy = self.project_to_3d(detectedObj[0], H_mtx)
            img_output = self.draw_detection(img, detectedObj, f"Offset: {xy[:2]}")
            if component == Components.Separator and state == AssemblySteps.Grab:
                correction = np.array([0,0,0,0,0,0], dtype=np.float32)
            else:
                correction = xy*np.array([-1,-1,0,0,0,0], dtype=np.float32)
            self.logger.info(f"{state.name} Offset detected: {xy}")
            return img_output, correction, True
        else:
            # no circles found, try detecting suction cup
            detectedObj = self.detect_object_center(img, self.correction_config.Suction_Cup)
            if len(detectedObj) > 0:
                # suction cup found
                self.logger.info(f"Object {component.name} failed being grabbed!")
                return img, np.array([0,0,0,0,0,0], dtype=np.float32), False
            else:
                # nothing found
                self.logger.info(f"Object {component.name} failed being deteced!")
                # This returns true because it failed to detect the suction cup. 
                # The assumption is that the suction cup detection algorithm is 
                # unlikely to fail, so a failure here indicates that the component was 
                # indeed picked up, just not detected.
                return img, np.array([0,0,0,0,0,0], dtype=np.float32), True

    def take_img(self, state: AssemblySteps, component: Components, nr:int=None):
        # Prepare directories to store metadata from detection
        self.time_stamp = time.strftime("%Y_%m_%d_%Hh_%Mm_%Ss", time.localtime())
        self.dir_name = Path(os.path.dirname(__file__)) / "Alignments" / self.time_stamp[:10] / f"Cell{nr}"
        org_dir = Path(os.path.dirname(__file__)) / "Alignments" / self.time_stamp[:10] / "Origin" / f"{component.name}_{state}"
        org_filename = org_dir /  f"[No{nr}]_{component.name}_{state}_{self.time_stamp[:10]}.jpg"

        if state == AssemblySteps.Grab:
            alpha = 1.0
            beta = 5
            cam = cv2.VideoCapture(self.cam_port_bottom, cv2.CAP_DSHOW)
            ret, img = cam.read()
            cam.release()
        elif state == AssemblySteps.Drop:
            alpha = 2.0
            beta = 50
            cam = cv2.VideoCapture(self.cam_port_top, cv2.CAP_DSHOW)
            ret, img = cam.read()
            cam.release()
        if ret == True:
            img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
            img_output = np.copy(img)
            img_output = cv2.normalize(img_output, None, 0, 255, cv2.NORM_MINMAX)
        else:
            self.logger.error(f"Camera {state} has lost its connection", exc_info=True)
            return

        # Make storage directories if they don't exist yet
        if not self.dir_name.exists():
            os.makedirs(self.dir_name)
        if not org_dir.exists():
            os.makedirs(org_dir)

        # Write the img output
        cv2.imwrite(org_filename, img_output)
        return img
    
    def show_img(self, img, component: Components, nr: int):
        cv2.imshow(f"{component.name} No.[{nr}]", img)
        cv2.waitKey(2000)
        cv2.destroyAllWindows()

    def run_autocorrection(self, state: AssemblySteps, component: Components, nr:int=None, show_img:bool=False, save_img:bool=False):
        img = self.take_img(state, component, nr)
        img_output, correction, grabbed = self.get_offset(img, component, state)
        if save_img and grabbed:
            res_filename = Path(self.dir_name) / f"[No{nr}]_{component.name}_{state}_{self.time_stamp}.jpg"
            cv2.imwrite(res_filename, img_output)
        
        if show_img:
            threading.Thread(name="show_image", target=self.show_img, args=[img_output, component, nr], daemon=True).start()

        return correction, grabbed
