import numpy as np
import cv2
import time
import os
import threading
import json
from datetime import datetime

from ..helper.Logger import Logger
from .Constants import (
    Components,
    AssemblySteps,
    AutoCorrectionConfig,
    StepCorrectionConfig,
)

from pathlib import Path


class AutoCorrection:
    # Module for correcting component placement based on lookup camera images
    def __init__(self, logger: Logger, silent: bool = False):
        self.logger = logger

        # Load in configuration constants (parameters for HoughCircles)
        self.correction_config = AutoCorrectionConfig()
        self.cam_port_bottom = self.correction_config.CAM_PORT_BOTM
        self.cam_port_top = self.correction_config.CAM_PORT_TOP
        self.dir_name = Path(os.path.dirname(__file__)) / "Calibration"
        if not self.dir_name.exists():
            os.makedirs(self.dir_name)
        self.vision_params_path = self.dir_name / "vision_params.json"
        self.vision_params = self.get_vision_params(silent=silent)
        pass

    def detect_object_center(self, img, object_config: dict):
        # Image preprocessing
        img_color = np.copy(img)
        img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
        img_gray = cv2.medianBlur(img_gray, 5)

        # Run detection algorithm
        circles = cv2.HoughCircles(
            img_gray,
            cv2.HOUGH_GRADIENT,
            1,
            object_config["minDist"],
            param1=object_config["param1"],
            param2=object_config["param2"],
            minRadius=object_config["minR"],
            maxRadius=object_config["maxR"],
        )
        h, w = img.shape[:2]
        valid = []
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for c in circles[0, :]:
                x, y, r = int(c[0]), int(c[1]), int(c[2])
                if x - r <= 0 or y - r <= 0 or x + r >= w or y + r >= h:
                    self.logger.info("Detected circle out of scope! Result discarded")
                else:
                    valid.append([[x, y], r])
            # sort ascending by radius and keep largest (component), consistent return type
            valid = sorted(valid, key=lambda x: x[1])
            if len(valid) > 0:
                self.logger.debug(f"sorted circles: {valid}")
                return valid[-1]  # single [[x,y], r]
        # no valid circles
        return []

    def get_vision_params(self, silent=False):
        # Load previously stored calibration parameters
        try:
            if not silent:
                print(
                    f"Checking in {self.vision_params_path} for vision_params.json..."
                )
            with open(self.vision_params_path, mode="r") as f:
                result = json.load(f)
                if not silent:
                    print(
                        "Previously computed vision_params found and loaded successfully."
                    )
                return result
        except FileNotFoundError:
            print(
                f"vision_params.json not found at {self.vision_params_path}. A new one will be created after calibration."
            )
            return {}
        except Exception as e:
            print(f"Unable to load vision_params due to exception: {e}")
            return {}

    def write_vision_params(self):
        with open(self.vision_params_path, mode="w") as f:
            json.dump(self.vision_params, f)
        print("vision_params.json modified")
        return None

    def compute_conversion(self, img_centered, img_adjusted, dx, dy):
        img_width = min(img_centered.shape[:2])

        # Use the "Default" section from AutoCorrectionConfig instead of object_config/suction_config
        default_cfg: StepCorrectionConfig = self.correction_config.Reference
        suction_cfg: StepCorrectionConfig = self.correction_config.Suction_Cup

        object_config = {
            "minDist": default_cfg.minDist,
            "param1": default_cfg.param1,
            "param2": default_cfg.param2,
            "minR": default_cfg.minR,
            "maxR": default_cfg.maxR,
        }
        suction_config = {
            "minDist": suction_cfg.minDist,
            "param1": suction_cfg.param1,
            "param2": suction_cfg.param2,
            "minR": suction_cfg.minR,
            "maxR": suction_cfg.maxR,
        }

        # Find circles in both images
        found_circles_center = self.detect_object_center(img_centered, suction_config)

        if not found_circles_center:
            # If no circles found, save the image for later reference
            cv2.imwrite(
                self.dir_name / "Suction_NoCircleDetected_center.png", img_centered
            )
            print(f"Saving img_centered to {self.dir_name}...")
            time.sleep(2)
            raise ValueError("No circles found during calibration!")

        found_circles_adjust = self.detect_object_center(img_adjusted, suction_config)
        if not found_circles_adjust:
            cv2.imwrite(
                self.dir_name / "Suction_NoCircleDetected_adjust.png", img_adjusted
            )
            raise ValueError("No circles found during calibration!")

        # Save calibration images for future reference
        center_drawn = self.draw_detection(
            img_centered, found_circles_center, text=str(found_circles_center)
        )
        adjust_drawn = self.draw_detection(
            img_adjusted, found_circles_adjust, text=str(found_circles_adjust)
        )
        print(f"Saving calibration images in {self.dir_name}")
        cv2.imwrite(self.dir_name / "centered_calibration_image.png", center_drawn)
        cv2.imwrite(self.dir_name / "adjusted_calibration_image.png", adjust_drawn)
        cv2.imwrite(self.dir_name / "BLANK_centered_calibration.png", img_centered)

        # Compute robot-pixel conversion factor
        dx_image = found_circles_adjust[0][0] - found_circles_center[0][0]
        dy_image = found_circles_adjust[0][1] - found_circles_center[0][1]
        if dx_image == 0 or dy_image == 0:
            raise ValueError(
                f"Degenerate calibration: dx_image={dx_image}, dy_image={dy_image}"
            )
        x_convert = dx / dy_image
        y_convert = dy / dx_image

        # Only keep scalar factors and suction_center; object_config/suction_config are deprecated
        self.vision_params["x_convert"] = x_convert
        self.vision_params["y_convert"] = y_convert
        self.vision_params["suction_center"] = found_circles_center[0]
        self.vision_params["date_calibrated"] = datetime.now().strftime("%b_%d_%Y")
        self.write_vision_params()
        return self.vision_params

    # helper to convert a StepCorrectionConfig into a HoughCircles config dict
    def _step_config_to_hough_dict(self, cfg: StepCorrectionConfig) -> dict:
        return {
            "minDist": cfg.minDist,
            "param1": cfg.param1,
            "param2": cfg.param2,
            "minR": cfg.minR,
            "maxR": cfg.maxR,
        }

    # helper to detect suction cup using AutoCorrectionConfig.Suction_Cup (no vision_params)
    def _detect_suction_with_calib_config(self, img):
        suction_cfg: StepCorrectionConfig = self.correction_config.Suction_Cup
        hough = self._step_config_to_hough_dict(suction_cfg)
        return self.detect_object_center(img, hough)

    def get_offset_simple(self, img):
        # object_config is deprecated; use Reference config for generic detection
        if "suction_center" not in self.vision_params:
            raise ValueError(
                "vision_params missing 'suction_center'; run calibrate_machine_vision first."
            )
        if (
            "x_convert" not in self.vision_params
            or "y_convert" not in self.vision_params
        ):
            raise ValueError(
                "vision_params missing conversion factors; run calibrate_machine_vision first."
            )

        default_cfg: StepCorrectionConfig = self.correction_config.Reference
        object_config = self._step_config_to_hough_dict(default_cfg)

        found_circle = self.detect_object_center(img, object_config)

        # DEBUGGING: save picture with and without circles drawn on
        print("found_circles = ", found_circle)
        try:
            print(f"Saving image to {self.dir_name}...")
            cv2.imwrite(self.dir_name / "get_offset_func_image_clean.png", img)
            if found_circle:
                img_drawn = self.draw_detection(
                    img, found_circle, text=str(found_circle)
                )
            else:
                img_drawn = img
            cv2.imwrite(self.dir_name / "get_offset_func_image.png", img_drawn)
        except Exception as e:
            print(f"Saving debug images failed with error {e}, continuing...")

        current = datetime.now().strftime("%b_%d_%Y_%I:%M")

        if not found_circle:
            cv2.imwrite(self.dir_name / f"NoCircleDetected_offset_{current}.png", img)
            raise ValueError("No circles found for computing offset!")

        # Compute pixel difference between known center from calibration and detected center
        dx_pixel = self.vision_params["suction_center"][0] - found_circle[0][0]
        dy_pixel = self.vision_params["suction_center"][1] - found_circle[0][1]

        # Convert to robot arm units
        dy = dx_pixel * self.vision_params["y_convert"]
        dx = dy_pixel * self.vision_params["x_convert"]
        return dx, dy

    def get_offset(self, img, component: Components, state: AssemblySteps):
        """Returns the image, a correction matrix, and a success flag.
        Uses component/step-specific Hough parameters and a homography matrix."""
        # Build HoughCircles config from StepCorrectionConfig
        cfg = getattr(self.correction_config, f"{component.name}_{state.name}", None)
        if cfg is None:
            raise ValueError(
                f"No AutoCorrectionConfig entry for {component.name}_{state.name}"
            )

        hough_cfg = self._step_config_to_hough_dict(cfg)

        # Attempt to find the component in the image
        detected_obj = self.detect_object_center(img, hough_cfg)

        if detected_obj:
            # For a positive detection, we require a homography for this step
            if not self.has_homography(state):
                raise RuntimeError(
                    f"Homography for state {state.name} is missing. "
                    "Run calibrate_machine_vision() before assembly."
                )
            H_mtx = self.get_homography_matrix(state)
            # detected_obj is [[x,y], r] -> pass center only
            xy = self.project_to_3d(detected_obj[0], H_mtx)
            img_output = self.draw_detection(img, detected_obj, f"Offset: {xy[:2]}")
            correction = xy * np.array([-1, -1, 0, 0, 0, 0], dtype=np.float32)
            self.logger.info(
                f"{state.name} Offset detected (xy): {xy} for {component.name}"
            )
            return img_output, correction, True
        else:
            # no circles found, try detecting suction cup with calibrated config
            try:
                detected_suction = self._detect_suction_with_calib_config(img)
            except ValueError as e:
                self.logger.warning(
                    f"Suction detection skipped due to calibration error: {e}"
                )
                detected_suction = []

            if detected_suction:
                self.logger.info(f"Object {component.name} failed being grabbed!")
                return img, np.zeros(6, dtype=np.float32), False
            else:
                self.logger.info(
                    f"Object {component.name} failed being detected."
                )
                return img, np.zeros(6, dtype=np.float32), False

    def project_to_3d(self, image_coordinates, H_mtx):
        """
        Map 2D image coordinates (x, y) via homography into robot X,Y.
        Returns a 6D vector [X, Y, 0, 0, 0, 0] with scalar floats.
        """
        # image_coordinates is [x, y]
        x, y, w = H_mtx @ np.array([[image_coordinates[0], image_coordinates[1], 1]]).T
        # unwrap to Python floats / 0-d numpy scalars
        X = float(np.around(x / w, decimals=3))
        Y = float(np.around(y / w, decimals=3))
        return np.array([X, Y, 0.0, 0.0, 0.0, 0.0], dtype=np.float32)

    def draw_detection(self, img, found_circle, text: str = None):
        img_output = np.copy(img)
        h, w = img_output.shape[:2]
        img_center = (w // 2, h // 2)
        cv2.drawMarker(img_output, img_center, (0, 255, 0), cv2.MARKER_CROSS, 10, 1)
        self.logger.debug(f"found_circles:{found_circle}")
        if found_circle:
            center = tuple(found_circle[0])
            cv2.drawMarker(img_output, center, (0, 0, 255), cv2.MARKER_CROSS, 10, 1)
            cv2.circle(img_output, center, found_circle[1], (255, 0, 255), 1)
        if text:
            cv2.putText(
                img_output,
                text,
                (20, h - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                2,
            )
        return img_output

    def get_homography_matrix(self, state: AssemblySteps):
        """Fetch the homography matrix for the given state."""
        calibration_file = Path(os.path.dirname(__file__)) / "data" / "calibration.json"
        with open(calibration_file, "r") as json_file:
            data = json.load(json_file)
        key = f"H_mtx_{state.name}"
        if key not in data:
            raise KeyError(f"{key} not found in {calibration_file}")
        return np.array(data[key], dtype=np.float32)

    def has_homography(self, state: AssemblySteps) -> bool:
        calibration_file = Path(os.path.dirname(__file__)) / "data" / "calibration.json"
        if not calibration_file.exists():
            return False
        try:
            with open(calibration_file, "r") as json_file:
                data = json.load(json_file)
            return f"H_mtx_{state.name}" in data
        except Exception as e:
            self.logger.warning(
                f"Failed to read homography file {calibration_file}: {e}"
            )
            return False

    def compute_and_store_homography(
        self, image_points, world_points, state: AssemblySteps
    ):
        """
        Compute homography H from image pixel coords to robot XY and store it
        in data/calibration.json under key f"H_mtx_{state.name}".
        image_points: list of (u, v) pixel coordinates
        world_points: list of (X, Y) robot coordinates (same order as image_points)
        """
        img_pts = np.array(image_points, dtype=np.float32)
        wrd_pts = np.array(world_points, dtype=np.float32)

        if img_pts.shape[0] < 4:
            raise ValueError(
                "Need at least 4 point correspondences to compute homography"
            )

        H, mask = cv2.findHomography(img_pts, wrd_pts, method=0)
        if H is None:
            raise ValueError("cv2.findHomography failed to compute a matrix")

        # Load or create calibration.json
        calib_path = Path(os.path.dirname(__file__)) / "data" / "calibration.json"
        calib_path.parent.mkdir(parents=True, exist_ok=True)
        if calib_path.exists():
            with open(calib_path, "r") as f:
                calib_data = json.load(f)
        else:
            calib_data = {}

        calib_data[f"H_mtx_{state.name}"] = H.tolist()

        with open(calib_path, "w") as f:
            json.dump(calib_data, f, indent=2)

        self.logger.info(f"Stored homography for state {state.name}: H={H}")
        return H

    def take_img(self, state: AssemblySteps, component: Components, nr: int = None):
        # Prepare directories to store metadata from detection
        self.time_stamp = time.strftime("%Y_%m_%d_%Hh_%Mm_%Ss", time.localtime())
        self.dir_name = (
            Path(os.path.dirname(__file__))
            / "Alignments"
            / self.time_stamp[:10]
            / f"Cell{nr}"
        )
        org_dir = (
            Path(os.path.dirname(__file__))
            / "Alignments"
            / self.time_stamp[:10]
            / "Origin"
            / f"{component.name}_{state}"
        )
        org_filename = (
            org_dir / f"[No{nr}]_{component.name}_{state}_{self.time_stamp[:10]}.jpg"
        )

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

    def run_autocorrection(
        self,
        state: AssemblySteps,
        component: Components,
        nr: int = None,
        show_img: bool = False,
        save_img: bool = False,
    ):
        img = self.take_img(state, component, nr)
        img_output, correction, grabbed = self.get_offset(img, component, state)
        if save_img and grabbed:
            res_filename = (
                Path(self.dir_name)
                / f"[No{nr}]_{component.name}_{state}_{self.time_stamp}.jpg"
            )
            cv2.imwrite(res_filename, img_output)

        if show_img:
            threading.Thread(
                name="show_image",
                target=self.show_img,
                args=[img_output, component, nr],
                daemon=True,
            ).start()

        return correction, grabbed
