#!/home/yuanjian/Research/BatteryLab/lab_venv/bin/python3
from BatteryLab.robots.RailMeca500 import RailMeca500

from BatteryLab.robots.AutoCorrection import AutoCorrection
from BatteryLab.robots.Constants import (
    AssemblyRobotConstants,
    AssemblyRobotCameraConstants,
    Components,
    RobotTool,
    AssemblySteps,  # add this import
)

from BatteryLab.helper.utils import (
    create_assembly_robot_constants_from_manual_positions,
    create_assembly_robot_camera_constants_from_manual_positions,
)
from linear_rail_control.linear_rail_client import LinearRailClient
import numpy as np
import ast

import yaml
from pathlib import Path
from rclpy.node import Node
import rclpy
import time
import cv2
import sys
import termios
import tty
from datetime import datetime
from typing import Callable, Optional

from ament_index_python.packages import get_package_share_path
from camera_service.camera_client import ImageClient
from suction_pump.suction_client import SuctionPumpClient


class ComponentRunOutError(Exception):
    """The error indicates the component has run out and requires a refill"""
    pass


class AssemblyRobot(Node):
    def __init__(self, logger=None, robot_address="192.168.0.100"):
        super().__init__("assembly_robot")
        self.suction_pump_client = SuctionPumpClient()
        self.logger = self.get_logger() if logger is None else logger
        self.auto_correction = AutoCorrection(logger=self.logger)
        self.D_LIMIT = 10.1  # Limit for dx and dy adjustments during vision calibration or machine vision-based correction.
        self.rail_meca500 = RailMeca500(
            logger=self.logger,
            robot_address=robot_address,
            suction_pump=self.suction_pump_client,
        )
        # self.status = dict(Progress=dict(Initiate=0, LastStep=None), Meca500Ready=False, ZaberRailReady=False)

        self.zaber_rail = LinearRailClient()
        self.assemblyRobotConstants = AssemblyRobotConstants()
        self.assemblyRobotCameraConstants = AssemblyRobotCameraConstants()
        self.look_up_camera_client = ImageClient(
            node_name="assembly_robot_lookup_camera_client",
            serv_name="/batterylab/lookup_camera",
        )
        self.arm_camera_client = ImageClient(
            node_name="assembly_robot_arm_camera_client",
            serv_name="/batterylab/rail_meca500_camera",
        )
        # The following dictionary is used for in-order usage of the components
        # #TODO: If using computer vision model to detect the next available location, we do not need to rely on the counters.
        self.component_current_counter_dict = {
            Components.CathodeCase.name: 0,
            Components.Cathode.name: 0,
            Components.Spacer.name: 0,
            Components.SpacerExtra.name: 0,
            Components.Anode.name: 0,
            Components.Washer.name: 0,
            Components.Separator.name: 0,
            Components.AnodeCase.name: 0,
        }

        self.counter_file = (
            Path(get_package_share_path("assembly_robot"))
            / "yaml"
            / "assembly_counter.yml"
        )
        # directory for lookup images used for Hough tuning
        self.lookup_tuning_dir = Path(
            "/home/yuanjian/Research/BatteryLab/images/lookup_tuning"
        )
        self.lookup_tuning_dir.mkdir(parents=True, exist_ok=True)


    def save_counter_config(self):
        with open(self.counter_file, "w") as f:
            yaml.dump(self.component_current_counter_dict, f)


    def load_counter_config(self):
        if self.counter_file.exists():
            with open(self.counter_file, "r") as f:
                counter_dict_on_file = yaml.safe_load(f)
            print("The current counter config on file: ", counter_dict_on_file)
            user_input = input(
                "Do you want to use the existing config? (Yes/No) Default is Yes:"
            ).lower()
            if user_input == "" or user_input == "yes":
                self.component_current_counter_dict = counter_dict_on_file
            else:
                self.save_counter_config()
        else:
            print("You don't have an existing config, will start from scratch")


    def load_position_files(self):
        # First, create position constants based on manually taught positions from YAML files
        position_file = (
            Path(get_package_share_path("assembly_robot"))
            / "yaml"
            / "well_positions.yaml"
        )
        with open(position_file, "r") as f:
            try:
                constant_positions = yaml.safe_load(f)
                print("Loaded constant_positions for assembly robot!")
            except yaml.YAMLError as e:
                print("Cannot load the well positions YAML file with error: ", e)

        self.assemblyRobotConstants = (
            create_assembly_robot_constants_from_manual_positions(constant_positions)
        )

        # Then, create the camera position constants with a similar method
        camera_position_file = (
            Path(get_package_share_path("assembly_robot"))
            / "yaml"
            / "arm_camera_positions.yaml"
        )
        with open(camera_position_file, "r") as f:
            try:
                camera_constant_positions = yaml.safe_load(f)
            except yaml.YAMLError as e:
                print("Cannot load the camera positions YAML file with error: ", e)
        self.assemblyRobotCameraConstants = (
            create_assembly_robot_camera_constants_from_manual_positions(
                camera_manual_positions=camera_constant_positions
            )
        )


    def initialize_and_home_robots(self):
        self.load_position_files()

        robot_pos = self.assemblyRobotConstants.LOOKUP_CAM_SK_PO
        self.logger.info(f"CHECK: LOOKUP_CAM_SK_PO = {robot_pos}")
        ok = self.rail_meca500.initializeRobot()
        if not ok:
            print("The Meca500 cannot be connected")
            exit()
        self.logger.info("Start testing the gripper!")
        self.rail_meca500.robot.SetGripperForce(5)
        self.rail_meca500.robot.GripperOpen()
        self.rail_meca500.robot.WaitGripperMoveCompletion(5)
        self.rail_meca500.robot.GripperClose()
        self.rail_meca500.robot.WaitGripperMoveCompletion(5)
        self.rail_meca500.robot.GripperOpen()
        self.rail_meca500.robot.WaitGripperMoveCompletion(5)
        self.logger.info("The gripper is functioning properly!")


    def get_rail_pos(self) -> float:
        future = self.zaber_rail.send_get_pos_request()
        while rclpy.ok():
            rclpy.spin_once(self.zaber_rail)
            if future.done():
                try:
                    response = future.result()
                except Exception as e:
                    self.zaber_rail.get_logger().info(f"Service call failed {e}")
                    return -1
                else:
                    return response.current_pos
        return -1


    def get_next_well_of_component(
        self, component_name, given_available_index: int = None
    ):
        component = getattr(self.assemblyRobotConstants, component_name)
        available_locations = sorted(list(component.keys()))
        locations = [component[sub_location] for sub_location in available_locations]
        total_num_of_components = np.sum(
            [np.prod(location.shape) for location in locations]
        )
        current_index = (
            given_available_index
            if given_available_index is not None
            else self.component_current_counter_dict[component_name]
        )
        global_index = current_index
        if current_index >= total_num_of_components:
            message = f"The component <{component_name}> has run out! Please refill!"
            self.logger.error(message)
            raise ComponentRunOutError(message)
        current_sublocation_index = -1
        for i, location in enumerate(locations):
            next_current_index = current_index - np.prod(location.shape)
            if next_current_index < 0:
                current_sublocation_index = i
                break
            else:
                current_index -= next_current_index
        current_subtray = locations[current_sublocation_index]
        if given_available_index is None:
            self.component_current_counter_dict[component_name] += 1
        return (
            global_index,
            current_subtray.shape,
            current_subtray.grabPo[current_index],
            current_subtray.railPo,
            available_locations[current_sublocation_index],
        )


    def move_home_and_out_of_way(self, home: float = 30.0):
        self.rail_meca500.move_home(tool=RobotTool.SUCTION)
        self.move_zaber_rail(home)


    def move_zaber_rail(self, rail_pos: float):
        self.logger.info(f"Assembly Robot Moving to {rail_pos}")
        future = self.zaber_rail.send_move_request(rail_pos)
        while rclpy.ok():
            rclpy.spin_once(self.zaber_rail)
            self.get_logger().info("waiting for the moving request to complete...")
            time.sleep(0.1) # originally 1.0
            if future.done():
                try:
                    response = future.result()
                except Exception as e:
                    self.get_logger().error(
                        "Service call failed and Zaber rail cannot move"
                    )
                else:
                    self.get_logger().info(
                        f"Moving request success: {response.success}"
                    )
                break
        # make sure the move is finished
        self.get_logger().debug(f"Assembly Robot move request finished")


    def drop_current_component_to_assembly_post(
        self,
        order: int = 1,
        component: Components = Components.Spacer,
        premove_callback: Optional[Callable[[], None]] = None,
        separator_dx_dy_max = 5.0
    ):
        """
        Drop the currently held component onto the assembly post, using vision-based correction.

        component: which component type is on the suction head; its Hough parameters
                   (from AutoCorrectionConfig) will be used when calling get_offset.
        premove_callback: an optional function to call before the assembly robot moves away from
            placing the component. Used to close the crimper robot's gripper on the separator.
        separator_dx_dy_max: a more strict limit for the separator component to avoid collision with the crimper robot
        """
        # First, take a photo at lookup camera and compute needed adjustment.
        img = self.take_a_look_up_photo()
        dx = dy = 0.0
        component_detected = False
        lookup_image = img
        
        # Check if image was successfully captured
        if img is None:
            self.get_logger().error(
                f"Failed to capture image for {component.name} correction; "
                "continuing with zero correction."
            )
            component_detected = False
            lookup_image = None
        else:
            try:
                img_out, correction, component_detected = self.auto_correction.get_offset(
                    img, component=component, state=AssemblySteps.Drop
                )
                lookup_image = img_out
                if not component_detected:
                    self.get_logger().warning(
                        f"Vision did not identify {component.name}; "
                        "proceeding without positional correction."
                    )
                else:
                    if correction is None or len(correction) < 2:
                        raise ValueError(
                            f"Invalid correction vector from get_offset: {correction}"
                        )
                    dx, dy = float(correction[0]), float(correction[1])
            except Exception as e:
                # Homography or detection failed; optional scalar fallback
                self.get_logger().warning(
                    f"get_offset (homography-based) failed for {component.name} "
                    f"at Drop step ({e}); falling back to get_offset_simple."
                )
                try:
                    dx, dy = self.auto_correction.get_offset_simple(img)
                except Exception as e2:
                    self.get_logger().error(
                        f"get_offset_simple also failed ({e2}); "
                        "continuing with zero correction."
                    )
                    dx = dy = 0.0
                component_detected = False
                lookup_image = img

        # Apply stricter limits for the separator to avoid collision with the crimper robot
        if component == Components.Separator:
            if abs(dx) > separator_dx_dy_max or abs(dy) > separator_dx_dy_max:
                self.get_logger().warning(
                    f"Vision correction for Separator hit stricter limit ({separator_dx_dy_max}). Correcting to this maximum." 
                )
                dx = max(-separator_dx_dy_max, min(separator_dx_dy_max, dx))
                dy = max(-separator_dx_dy_max, min(separator_dx_dy_max, dy))

        # Get helper information for placing component
        current_tool = self.rail_meca500.get_current_tool()
        rail_pos = self.assemblyRobotConstants.POST_RAIL_LOCATION
        if current_tool == RobotTool.SUCTION:
            robot_pos = self.assemblyRobotConstants.POST_C_SK_PO.copy()
            robot_pos[2] += order * 0.05
            mid_point_joints = [-90, 0, 0, 0, 45, 0]
        elif current_tool == RobotTool.GRIPPER:
            robot_pos = self.assemblyRobotConstants.POST_C_GRIPPER_PO.copy()
            mid_point_joints = [-90, 0, 0, 0, 0, 0]
        else:
            self.get_logger().error("The current tool is invalid for a snapshot")
            return

        # Adjust robot_pos (pedestal drop coords) based on vision info
        dx = max(-self.D_LIMIT, min(self.D_LIMIT, dx))
        dy = max(-self.D_LIMIT, min(self.D_LIMIT, dy))
        if abs(dx) == self.D_LIMIT:
            self.get_logger().warning(
                f"dx correction for {component.name} hit limit of {self.D_LIMIT}; "
                "check vision system and calibration."
            )
        if abs(dy) == self.D_LIMIT:
            self.get_logger().warning(
                f"dy correction for {component.name} hit limit of {self.D_LIMIT}; "
                "check vision system and calibration."
            )
        self.get_logger().info(
            f"Applying vision correction for {component.name} drop: dx={dx:.4f}, dy={dy:.4f}"
        )
        robot_pos[0] += dx
        robot_pos[1] += dy

        # Move arm to pedestal drop position (rail not moved yet)
        self.rail_meca500.pick_place_part1(
            robot_pos, is_grab=False, premove_callback=premove_callback
        )
        # Move to correct rail position
        self.move_zaber_rail(rail_pos)
        # Finish placing component on pedestal
        self.rail_meca500.pick_place_part2(
            robot_pos, is_grab=False, premove_callback=premove_callback
        )
        
        return {
            "dx": dx,
            "dy": dy,
            "component_detected": component_detected,
            "lookup_image": lookup_image,
        }


    def calibrate_machine_vision(self, force=False):
        """Used to:
        1) take a picture and find the center of the suction cup (in pixels)
        2) calibrate pixels-to-robot units by taking a picture at (defaultx+dx, defaulty+dy), using HoughCircles to find the center of the suction cup (in pixels), then computing x_convert and y_convert.
        3) (extended) compute a pixel→robot homography from multiple offsets, so the more rigorous AutoCorrection code can be used.
        """
        print("Starting machine vision calibration routine...")
        # Check if calibration data already exists
        if not force:
            vision_params = self.auto_correction.get_vision_params()
            # Only scalar factors & suction_center are needed now
            needed = ["x_convert", "y_convert", "suction_center"]

            ready = True
            for needed_param in needed:
                if needed_param not in vision_params:
                    print(
                        f"{needed_param} not found in calibration file. Must recalibrate."
                    )
                    ready = False
                    break

            # Also require homography for Drop state
            homography_ready = self.auto_correction.has_homography(AssemblySteps.Drop)

            if ready and homography_ready:
                print(
                    "All calibration parameters (scalar + homography) found, moving on..."
                )
                self.vision_params = vision_params
                return None
        else:
            print("Calibration route forced via 'force' parameter. Recalibrating...")

        # Specify suction tool
        self.rail_meca500.change_tool(RobotTool.SUCTION)

        # Base pose: lookup camera position
        base_pose = np.array(self.assemblyRobotConstants.LOOKUP_CAM_SK_PO, dtype=float)
        base_x, base_y = base_pose[0], base_pose[1]

        # Take a picture of the empty suction cup at base pose
        img_suction_center = self.take_a_look_up_photo(rehome=False)

        # Single offset used for legacy scalar conversion
        dx_single, dy_single = -10, -10  # Note: trimmed in take_a_look_up_photo
        img_suction_adjust = self.take_a_look_up_photo(
            dx=dx_single, dy=dy_single, rehome=False, midpoint=False
        )

        # Invert images for easier circle detection
        img_suction_center_inv = cv2.bitwise_not(img_suction_center)
        img_suction_adjust_inv = cv2.bitwise_not(img_suction_adjust)

        # Compute scalar conversion factors + suction_center + configs
        self.vision_params = self.auto_correction.compute_conversion(
            img_suction_center_inv, img_suction_adjust_inv, dx_single, dy_single
        )

        # ---- NEW: multi-offset homography calibration ----
        print("Computing homography from multiple dx,dy offsets around lookup pose...")

        # Define offsets: four corners around (0,0) in robot X/Y
        d = np.abs(dx_single)
        offsets = [
            (d, d),
            (d, -d),
            (-d, d),
            (-d, -d),
        ]

        image_points = [self.vision_params["suction_center"]]
        world_points = [(0, 0)]

        # Build Hough config for detecting the suction cup during homography sampling
        suction_cfg = self.auto_correction.correction_config.Suction_Cup
        suction_hough = {
            "minDist": suction_cfg.minDist,
            "param1": suction_cfg.param1,
            "param2": suction_cfg.param2,
            "minR": suction_cfg.minR,
            "maxR": suction_cfg.maxR,
        }

        # We are already at the correct rail position; just re-use rehome=False
        for dx_i, dy_i in offsets:
            img_i = self.take_a_look_up_photo(
                dx=dx_i, dy=dy_i, rehome=False, midpoint=False
            )
            img_i_inv = cv2.bitwise_not(img_i)

            found = self.auto_correction.detect_object_center(img_i_inv, suction_hough)
            if not found:
                self.get_logger().warn(
                    f"Homography sample at (dx,dy)=({dx_i},{dy_i}) had no suction circle; skipping this sample."
                )
                continue

            (u, v), _ = found  # found structure: [[u,v], r]
            image_points.append((float(u), float(v)))

            # We want the homography matrix to yield a robot coordinate offset, so the world points are simply the dx, dy offsets in robot units
            world_points.append((dx_i, dy_i))

        if len(image_points) >= 4:
            # Allows for one of the four images to fail detection while still computing a homography
            try:
                self.auto_correction.compute_and_store_homography(
                    image_points=image_points,
                    world_points=world_points,
                    state=AssemblySteps.Drop,  # use Drop state for lookup camera drop correction
                )
            except Exception as e:
                self.get_logger().error(f"Failed to compute/store homography: {e}")
        else:
            self.get_logger().warn(
                f"Not enough valid homography samples collected ({len(image_points)}). "
                "AutoCorrection.get_offset will still fall back to existing behavior."
            )

        # Move the robot out of the way
        self.move_home_and_out_of_way()
        return None


    def take_a_look_up_photo(self, dx=0, dy=0, rehome=True, midpoint=True):
        """Homes the rail_meca500's arm position, moves to the lookup camera, then takes and returns a photo.

        Optional inputs:
            dx: amount (in meca500 units) to adjust x position of lookup location
                default = 0, limit = +-20
            dy: amount (in meca500 units) to adjust y position of lookup location
                default = 0, limit = +-20
            rehome: if set to False, robot arm will not return to arm position home before running this routine. This is used in the machine vision calibration step, in which a photo is taken, then a small xy adjustment is made and another photo taken. Returning to the arm's home position would be unnecessary.
            midpoint: if set to False, the robot arm will not move to the midpoint of its movement to the camera position. This is only used for the SECOND PHOTO of the calibrate_machine_vision routine, as moving back to the midpoint is unnecessary.
                default = True
        """
        # Enforce limits for dx and dy
        if dx != 0:
            dx = max(-self.D_LIMIT, min(self.D_LIMIT, dx))
        if dy != 0:
            dy = max(-self.D_LIMIT, min(self.D_LIMIT, dy))
        if abs(dx) == self.D_LIMIT:
            self.get_logger().warning(
                f"dx adjustment of {dx} hit limit of {self.D_LIMIT}; check vision system and calibration."
            )
        if abs(dy) == self.D_LIMIT:
            self.get_logger().warning(
                f"dy adjustment of {dy} hit limit of {self.D_LIMIT}; check vision system and calibration."
            )

        # Home robot arm's position
        if rehome:
            self.rail_meca500.move_home()

        # Get robot constants
        current_tool = self.rail_meca500.get_current_tool()
        rail_pos = self.assemblyRobotConstants.LOOKUP_CAM_RAIL_LOCATION
        if current_tool == RobotTool.SUCTION:
            # Need to make a copy due to possible modification (dx, dy)
            robot_pos = self.assemblyRobotConstants.LOOKUP_CAM_SK_PO.copy()
            mid_point_joints = [-90, 0, 0, 0, 45, 0]
        elif current_tool == RobotTool.GRIPPER:
            robot_pos = self.assemblyRobotConstants.LOOKUP_CAM_GRIPPER_PO.copy()
            mid_point_joints = [-90, 0, 0, 0, 0, 0]
        else:
            self.get_logger().error("The current tool is invalid for a snapshot")
            return

        # Adjust robot_pos for calibration routine
        if dx != 0:
            robot_pos[0] += dx
        if dy != 0:
            robot_pos[1] += dy

        # Move robot into position
        if midpoint:
            self.move_zaber_rail(rail_pos)
            self.rail_meca500.robot.MoveJoints(*mid_point_joints)
        self.rail_meca500.robot.WaitIdle(30)
        print(f"Moving to camera position: {robot_pos}")
        self.rail_meca500.robot.MovePose(*robot_pos)
        self.rail_meca500.robot.WaitIdle(10)
        self.rail_meca500.robot.Delay(0.2)

        # Take and return picture
        # TODO: use get_image for storing the image or analysis
        for i in range(2):
            self.look_up_camera_client.send_request()
            rclpy.spin_until_future_complete(
                self.look_up_camera_client, self.look_up_camera_client.future
            )
            time.sleep(0.5)
        # self.look_up_camera_client.display_image()
        image = self.look_up_camera_client.get_image()
        return image


    def take_a_tray_photo(self, component_name: str):
        component_dict = getattr(self.assemblyRobotCameraConstants, component_name)
        rail_pos = component_dict["rail_pos"]
        self.rail_meca500.change_tool(RobotTool.CAMERA)
        robot_pos = (
            self.assemblyRobotCameraConstants.RobotPose
            if "cartesian" not in component_dict
            else component_dict["cartesian"]
        )
        self.rail_meca500.robot.MovePose(*robot_pos)
        self.rail_meca500.robot.WaitIdle(30)
        self.rail_meca500.robot.Delay(0.2)
        self.move_zaber_rail(rail_pos)
        print(f"To take a photo, moving to Robot Pos {robot_pos}")
        # TODO: use get_image for storing the image or analysis
        self.arm_camera_client.send_request()
        rclpy.spin_until_future_complete(
            self.arm_camera_client, self.arm_camera_client.future
        )
        # self.arm_camera_client.display_image()
        return self.arm_camera_client.get_image()


    def grab_component(
        self,
        rail_position,
        grab_position,
        is_grab=True,
        component_name="suction",
        home_before: bool = True,
        home_after: bool = True,
        move_rail: bool = True,
    ):
        """Grab a component for battery or return it to the tray.
        This requires a cooperation between the rail and the Meca500 robotic arm on top of it.
        """
        # Move home based on the tooling
        if component_name == "Washer":
            self.rail_meca500.change_tool(tool_name=RobotTool.GRIPPER)
        else:
            self.rail_meca500.change_tool(tool_name=RobotTool.SUCTION)

        if home_before:
            self.rail_meca500.move_home()

        # Move the Zaber Rail
        if move_rail:
            self.move_zaber_rail(rail_position)
        self.logger.debug(f"Assembly Robot will start picking soon.")
        # Let Meca500 pick up the component and move it home
        self.rail_meca500.pick_place(
            grab_position,
            is_grab=is_grab,
            home_after=home_after,
        )


    def manual_adjustment(
        self, rail_position, grab_position, level: float = 1, component_name="suction"
    ):
        """Move the robot arm close to the tray for manual adjustment."""
        # Move home based on the tooling
        if component_name == "Washer":
            self.rail_meca500.change_tool(tool_name=RobotTool.GRIPPER)
            self.rail_meca500.move_home()
        else:
            self.rail_meca500.change_tool(tool_name=RobotTool.SUCTION)
            self.rail_meca500.move_home()

        # Move the Zaber Rail
        self.move_zaber_rail(rail_position)
        self.logger.debug(f"Assembly Robot will move for manual adjustment soon.")
        self.rail_meca500.move_to_pick_position(grab_position, level=level)


    def _manual_mode_offset_limits(self, use_pick_position: bool):
        """Return conservative per-axis jog limits for manual positioning."""
        if use_pick_position:
            return np.array([20.0, 20.0, 8.0, 0.0, 0.0, 0.0], dtype=float)
        return np.array([20.0, 20.0, 20.0, 0.0, 0.0, 0.0], dtype=float)


    def _clamp_pose_to_limits(
        self,
        pose,
        base_pose,
        offset_limits,
        z_lower_limit: Optional[float] = None,
    ):
        """Clamp a pose to a small envelope around the selected manual base pose."""
        candidate = np.array(pose, dtype=float)
        base = np.array(base_pose, dtype=float)
        lower = base - offset_limits
        upper = base + offset_limits
        if z_lower_limit is not None:
            lower[2] = max(lower[2], float(z_lower_limit))
        clamped = np.minimum(np.maximum(candidate, lower), upper)
        if not np.allclose(clamped, candidate):
            self.logger.warning(
                "Manual jog target exceeded soft limits and was clamped to a safer pose."
            )
        return clamped.tolist()


    def _move_to_manual_base_pose(
        self,
        rail_position,
        base_position,
        component_name: str,
        use_pick_position: bool,
        level: float,
        tool_name: Optional[RobotTool] = None,
        initial_z_offset: float = 0.0,
        skip_prep: bool = False,
    ):
        """Move into the manual base pose using the safer approach pattern already used elsewhere."""
        if use_pick_position:
            if skip_prep:
                # In batch reteach mode we are already on the correct rail/tool; avoid
                # homing to keep iteration fast and collision-safe.
                # Use a safe above-tray approach, then lower to the working pose.
                approach_pose = list(base_position)
                approach_pose[2] = base_position[2] + 30
                self.rail_meca500.robot.MovePose(*approach_pose)
                self.rail_meca500.robot.WaitIdle(10)
                base_pose = list(base_position)
                if level > 0:
                    base_pose[2] = base_position[2] + 30 * level
                self.rail_meca500.robot.MoveLin(*base_pose)
                self.rail_meca500.robot.WaitIdle(10)
                return base_pose
            # Always approach tray wells from an elevated pose first, then descend.
            self.manual_adjustment(
                rail_position, base_position, level=1.0, component_name=component_name
            )
            base_pose = list(base_position)
            base_pose[2] = base_position[2] + 30 * level
            self.rail_meca500.robot.MoveLin(*base_pose)
            self.rail_meca500.robot.WaitIdle(10)
            return base_pose

        # If moving to the lookup camera or pedestal, use the midpoint move
        if tool_name == RobotTool.GRIPPER:
            self.rail_meca500.change_tool(tool_name=RobotTool.GRIPPER)
            self.rail_meca500.move_home()
            midpoint_joints = [-90, 0, 0, 0, 0, 0]
        else:
            self.rail_meca500.change_tool(tool_name=RobotTool.SUCTION)
            self.rail_meca500.move_home()
            midpoint_joints = [-90, 0, 0, 0, 45, 0]

        self.move_zaber_rail(rail_position)
        self.rail_meca500.robot.MoveJoints(*midpoint_joints)
        self.rail_meca500.robot.WaitIdle(10)
        approach_pose = list(base_position)
        if initial_z_offset != 0.0:
            approach_pose[2] += initial_z_offset
        self.rail_meca500.robot.MovePose(*approach_pose)
        self.rail_meca500.robot.WaitIdle(10)
        return approach_pose


    def manual_arm_control_mode(
        self,
        rail_position,
        base_position,
        level: float = 0.0,
        component_name: str = "suction",
        step_size: float = 1.0,
        use_pick_position: bool = True,
        z_lower_limit: Optional[float] = None,
        tool_name: Optional[RobotTool] = None,
        initial_z_offset: float = 0.0,
        skip_prep: bool = False,
    ):
        """Enter keyboard-based manual arm control for fine-tuning a single pose."""
        current_pose = self._move_to_manual_base_pose(
            rail_position=rail_position,
            base_position=base_position,
            component_name=component_name,
            use_pick_position=use_pick_position,
            level=level,
            tool_name=tool_name,
            initial_z_offset=initial_z_offset,
            skip_prep=skip_prep,
        )
        base_pose = list(current_pose)
        offset_limits = self._manual_mode_offset_limits(use_pick_position)

        # Set step size limits
        min_step = 0.01
        max_step = 5.0
        step_size = max(min_step, min(max_step, step_size))
        helper_text = (
            """
            
=====================================================
Manual arm control mode initiated. Controls: 
-----------------------------------------------------
Up(-x), Down(+x), Right(+y), Left(-y), u(+z), d(-z), 
p(print), o(return to base), h(help), space(pause), 
r(resume), +(bigger step), -(smaller step), 
i(input set step), v(toggle suction), q(quit).
=====================================================

"""
        )
        self.logger.info(
            helper_text
        )

        # Allow manual operation of the robot around a set area of the base pose
        motion_paused = False
        suction_on = False
        while True:
            key = read_keypress()
            if key in ("q", "Q"):
                if motion_paused:
                    decision = (
                        input(
                            "Motion is paused. Type 'keep' to keep paused and quit, or 'resume' to resume then quit (default keep): "
                        )
                        .strip()
                        .lower()
                    )
                    if decision == "resume":
                        try:
                            self.rail_meca500.robot.ResumeMotion()
                            self.rail_meca500.robot.WaitMotionResumed(5)
                            motion_paused = False
                            print("Motion resumed; exiting manual mode.")
                        except Exception as e:
                            self.logger.error(
                                f"Unable to resume robot motion safely before quit: {e}"
                            )
                            print("Keeping paused state and exiting manual mode.")
                    else:
                        print("Keeping paused state and exiting manual mode.")
                self.logger.info("Exiting manual arm control mode.")
                break
            elif key == " ":
                try:
                    self.rail_meca500.robot.PauseMotion()
                    self.rail_meca500.robot.WaitMotionPaused(5)
                    motion_paused = True
                    print("Motion paused. Press r to resume or q to quit.")
                except Exception as e:
                    self.logger.error(f"Unable to pause robot motion safely: {e}")
                continue
            elif key in ("r", "R"):
                if motion_paused:
                    try:
                        self.rail_meca500.robot.ResumeMotion()
                        self.rail_meca500.robot.WaitMotionResumed(5)
                        motion_paused = False
                        print("Motion resumed.")
                    except Exception as e:
                        self.logger.error(f"Unable to resume robot motion safely: {e}")
                else:
                    print("Motion is not paused.")
                continue
            elif motion_paused:
                print("Motion is paused. Press r to resume or q to quit.")
                continue
            elif key == "UP":
                current_pose[0] -= step_size
            elif key == "DOWN":
                current_pose[0] += step_size
            elif key == "RIGHT":
                current_pose[1] += step_size
            elif key == "LEFT":
                current_pose[1] -= step_size
            elif key in ("u", "U"):
                current_pose[2] += step_size
            elif key in ("d", "D"):
                current_pose[2] -= step_size
            elif key in ("p", "P"):
                print(
                    f"Current arm coordinates: x={current_pose[0]:.4f}, y={current_pose[1]:.4f}, z={current_pose[2]:.4f}, "
                    f"alpha={current_pose[3]:.4f}, beta={current_pose[4]:.4f}, gamma={current_pose[5]:.4f}, step={step_size:.4f}"
                )
                continue
            elif key in ("o", "O"):
                current_pose = list(base_pose)
                print("Returning to original/base manual position.")
            elif key in ("h", "H"):
                self.logger.info(
                    helper_text
                )
                continue
            elif key in ("+", "="):
                step_size = min(max_step, step_size * 2.0)
                print(f"Step size increased to {step_size:.4f}")
                continue
            elif key in ("-", "_"):
                step_size = max(min_step, step_size / 2.0)
                print(f"Step size decreased to {step_size:.4f}")
                continue
            elif key in ("i", "I"):
                new_step = input(
                    f"Enter new step size in [{min_step}, {max_step}] (current {step_size:.4f}): "
                ).strip()
                try:
                    value = float(new_step)
                    if value < min_step or value > max_step:
                        print(
                            f"Invalid step size {value}. Keep current step {step_size:.4f}."
                        )
                    else:
                        step_size = value
                        print(f"Step size set to {step_size:.4f}")
                except ValueError:
                    print(
                        f"Cannot parse '{new_step}'. Keep current step {step_size:.4f}."
                    )
                continue
            elif key in ("v", "V"):
                if self.rail_meca500.get_current_tool() != RobotTool.SUCTION:
                    print("Suction toggle is only available while using the suction tool.")
                    continue
                try:
                    if suction_on:
                        self.rail_meca500.suction_pump.drop()
                        suction_on = False
                        print("Suction OFF")
                    else:
                        self.rail_meca500.suction_pump.continues_pick()
                        suction_on = True
                        print("Suction ON")
                except Exception as e:
                    self.logger.error(f"Failed to toggle suction: {e}")
                continue
            else:
                continue

            current_pose = self._clamp_pose_to_limits(
                current_pose,
                base_pose,
                offset_limits,
                z_lower_limit=z_lower_limit,
            )
            self.rail_meca500.robot.MoveLin(*current_pose)
            self.rail_meca500.robot.WaitIdle(10)

        if suction_on:
            try:
                self.rail_meca500.suction_pump.drop()
            except Exception as e:
                self.logger.error(f"Failed to turn suction off while exiting manual mode: {e}")
        return current_pose


    def _get_corner_name_for_well_index(self, shape, well_index: int):
        """Map a row-major well index to one of the four YAML corner keys."""
        if len(shape) != 2:
            return None
        m, n = int(shape[0]), int(shape[1])
        corner_map = {
            0: "top_left",
            n - 1: "bottom_left",
            (m - 1) * n: "top_right",
            m * n - 1: "bottom_right",
        }
        return corner_map.get(int(well_index))


    def _apply_single_well_pose_in_memory(
        self,
        component_name: str,
        sub_location: str,
        well_index: int,
        adjusted_pose,
    ):
        component = getattr(self.assemblyRobotConstants, component_name)
        if sub_location not in component:
            raise KeyError(
                f"Sublocation '{sub_location}' not found under component '{component_name}'."
            )
        subtray = component[sub_location]
        if not (0 <= well_index < len(subtray.grabPo)):
            raise IndexError(
                f"Well index {well_index} out of range for {component_name}/{sub_location}."
            )
        subtray.grabPo[well_index] = list(adjusted_pose)


    def _persist_single_corner_pose_to_yaml(
        self,
        component_name: str,
        sub_location: str,
        shape,
        well_index: int,
        adjusted_pose,
    ):
        """Persist a single corner pose by directly replacing the matching YAML corner."""
        corner_name = self._get_corner_name_for_well_index(shape, well_index)
        if corner_name is None:
            raise ValueError(
                "Only corner wells can be persisted directly to YAML corners. "
                "Use corner test mode or pick one of the four corner indices."
            )
        position_file = (
            Path(get_package_share_path("assembly_robot"))
            / "yaml"
            / "well_positions.yaml"
        )
        with open(position_file, "r") as f:
            manual_positions = yaml.safe_load(f)

        if component_name not in manual_positions:
            raise KeyError(f"Component '{component_name}' not found in {position_file}")
        if sub_location not in manual_positions[component_name]:
            raise KeyError(
                f"Sublocation '{sub_location}' not found for component '{component_name}' in {position_file}"
            )

        subtray = manual_positions[component_name][sub_location]
        if corner_name not in subtray:
            raise KeyError(
                f"Corner '{corner_name}' not found for {component_name}/{sub_location} in {position_file}"
            )

        subtray[corner_name]["cartesian"] = [float(v) for v in adjusted_pose]

        with open(position_file, "w") as f:
            yaml.safe_dump(manual_positions, f, sort_keys=False)


    def auto_grab_a_component_to_assembly_post(self, component_name: str):
        component = getattr(self.assemblyRobotConstants, component_name)
        available_locations = list(component.keys())
        # take a picutre of the component
        tray_photo = self.take_a_tray_photo(component_name)
        # TODO: deal with the photo to find available components
        sublocation = available_locations[0]  # the sublocation is default to 0 for now
        location = component[sublocation]
        auto_well_grab_pos = location.grabPo[
            0
        ]  # the grab well index is default to 0 for now
        rail_position = location.railPo
        # grab the decided component
        self.grab_component(
            rail_position=rail_position,
            grab_position=auto_well_grab_pos,
            is_grab=True,
            component_name=component_name,
        )
        # move the component to the assembly post
        self.grab_component(
            self.assemblyRobotConstants.POST_RAIL_LOCATION,
            self.assemblyRobotConstants.POST_C_SK_PO,
            is_grab=False,
            component_name=component_name,
        )


    def capture_lookup_images_for_all_components(self):
        """
        Automatically grab one example of each component type, move to the lookup
        camera, take a photo at the standard lookup position, and save it to a
        common directory for HoughCircles tuning.
        The component is then returned to its original well.
        """
        self.logger.info("Starting automatic lookup image capture for all components.")

        # fixed order covering the seven unique components
        component_sequence = [
            Components.CathodeCase,
            Components.Washer,
            Components.Spacer,
            Components.Cathode,
            Components.Separator,
            Components.Anode,
            Components.AnodeCase,
        ]

        for comp in component_sequence:
            name = comp.name
            try:
                # 1) get next available well for this component
                (
                    global_index,
                    subtray_shape,
                    well_grab_pos,
                    rail_pos,
                    subtray_name,
                ) = self.get_next_well_of_component(name)
            except Exception as e:
                self.logger.error(f"Failed to get next well for {name}: {e}")
                continue

            self.logger.info(
                f"[LookupCapture] Component={name}, global_index={global_index}, "
                f"subtray={subtray_name}, rail_pos={rail_pos}"
            )

            # 2) grab the component from its tray
            try:
                self.grab_component(
                    rail_position=rail_pos,
                    grab_position=well_grab_pos,
                    is_grab=True,
                    component_name=name,
                )
            except Exception as e:
                self.logger.error(f"Failed to grab {name}: {e}")
                continue

            # 3) move to lookup camera and take a photo at standard location
            try:
                img = self.take_a_look_up_photo()
            except Exception as e:
                self.logger.error(f"Failed to take lookup photo for {name}: {e}")
                # try to put component back before continuing
                try:
                    self.grab_component(
                        rail_position=rail_pos,
                        grab_position=well_grab_pos,
                        is_grab=False,
                        component_name=name,
                    )
                except Exception as e2:
                    self.logger.error(
                        f"Failed to return component {name} after camera error: {e2}"
                    )
                continue

            # 4) save the image
            timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            filename = (
                self.lookup_tuning_dir
                / f"Lookup-{name}-idx{global_index}-{timestamp}.jpg"
            )
            try:
                cv2.imwrite(str(filename), img)
                self.logger.info(f"Saved lookup image for {name} to {filename}")
            except Exception as e:
                self.logger.error(f"Failed to save lookup image for {name}: {e}")

            # 5) return component to the same well
            try:
                self.rail_meca500.move_home(tool=RobotTool.SUCTION)
                self.grab_component(
                    rail_position=rail_pos,
                    grab_position=well_grab_pos,
                    is_grab=False,
                    component_name=name,
                )
            except Exception as e:
                self.logger.error(
                    f"Failed to return component {name} to tray after capture: {e}"
                )

        # move system out of the way when done
        self.move_home_and_out_of_way()
        self.logger.info("Finished automatic lookup image capture for all components.")


def get_component_location_from_user(
    robot,
    component_prompt,
    selected_component_name: Optional[str] = None,
    allow_all: bool = True,
):
    if selected_component_name is None:
        success = False
        while not success:
            component_name = input(component_prompt)
            try:
                component = getattr(robot.assemblyRobotConstants, component_name)
                success = True
            except:
                if component_name.lower() == "exit" or component_name.lower() == "e":
                    print("Cancelling operation...")
                    return None
                print(f"Component '{component_name}' not recognized. Try again!")
    else:
        component_name = selected_component_name
        component = getattr(robot.assemblyRobotConstants, component_name, None)
        if component is None:
            print(f"Component '{component_name}' not recognized. Operation aborted.")
            return None

    available_locations = list(component.keys())
    if len(available_locations) == 0:
        print(
            f"The selected component <{component_name}> has not been manually positioned yet!"
        )
        return None

    all_hint = "all, " if allow_all else ""
    sub_location = input(
        f"Which corner do you want to test ({all_hint}{available_locations}): "
    ).lower()

    if (not allow_all) and sub_location == "all":
        print("Selecting 'all' is not allowed for this operation.")
        return None

    result = []
    if sub_location == "all":
        for sub_location in available_locations:
            location = component[sub_location]
            result.append(
                (
                    location.shape,
                    location.grabPo,
                    location.railPo,
                    sub_location,
                    component_name,
                )
            )
    elif sub_location not in available_locations:
        print("The sublocation you picked is not valid! Operation aborted.")
        return None
    else:
        location = component[sub_location]
        result.append(
            (
                location.shape,
                location.grabPo,
                location.railPo,
                sub_location,
                component_name,
            )
        )
    return result


def get_location_index_from_user(shape, sub_location):
    assert len(shape) == 2
    index = input(
        f"The shape of the sub_location is {shape}.\nwhich index do you want the robot to reach for {sub_location}, range [0, {shape[0] * shape[1]}), you can also provide a location [x, y]:"
    )
    try:
        index = int(index)
    except ValueError as e:
        try:
            coordinates = ast.literal_eval(index)  # convert the input to a list
            index = shape[1] * coordinates[0] + coordinates[1]
        except:
            print(f"Error encountered parsing location '{index}'. Please try again.")
            return -1
    return index


def get_user_confirmation(confirm=""):
    """Checks if user input matches the parameter 'confirm' (default: 'Y'), case sensitive. If user presses return (input=None), the function will not error."""
    response = "8.53973422267"  # Nonsense to avoid false positives

    while response != confirm:
        if confirm == "":
            response = input("Hit <Enter> to confirm and move on.")
        else:
            response = input(f"Type {confirm} to confirm and move on.")
    return None


def get_tool_name_from_user(location_name: str) -> Optional[RobotTool]:
    """Prompt user to choose suction or gripper for a manual core location."""
    print(f"Which tool do you want to use for {location_name}?")
    print("[1] suction")
    print("[2] gripper")
    print("[E] Exit")
    selection = input(":> ").strip().lower()
    if selection in ("e", "exit"):
        print("Cancelling manual adjustment...")
        return None
    if selection in ("1", "s", "suction"):
        return RobotTool.SUCTION
    if selection in ("2", "g", "gripper"):
        return RobotTool.GRIPPER
    print(f"Invalid tool selection '{selection}'.")
    return None


def get_manual_core_location_from_user(robot):
    """Prompt user to select one core location for manual adjustment."""
    tray_components = [
        Components.CathodeCase.name,
        Components.Cathode.name,
        Components.Spacer.name,
        Components.SpacerExtra.name,
        Components.Anode.name,
        Components.Washer.name,
        Components.Separator.name,
        Components.AnodeCase.name,
    ]

    print("Select a core location to adjust:")
    for i, name in enumerate(tray_components, 1):
        print(f"[{i}] {name} tray anchor")
    print("[9] Lookup camera")
    print("[10] Placement pedestal")
    print("[E] Exit")

    selection = input(":> ").strip().lower()
    if selection in ("e", "exit"):
        print("Cancelling manual adjustment...")
        return None

    try:
        index = int(selection)
    except ValueError:
        print(f"Invalid selection '{selection}'.")
        return None

    if 1 <= index <= len(tray_components):
        component_name = tray_components[index - 1]
        tray_results = get_component_location_from_user(
            robot,
            component_prompt="",
            selected_component_name=component_name,
            allow_all=False,
        )
        if tray_results is None or len(tray_results) != 1:
            return None

        shape, grabpos, railpos, sub_location, component_name = tray_results[0]

        well_index = get_location_index_from_user(shape, sub_location)
        if not (0 <= well_index < len(grabpos)):
            print(
                f"Invalid well index '{well_index}' for sub-location '{sub_location}'."
            )
            return None

        return {
            "name": f"{component_name} tray ({sub_location}, well {well_index})",
            "rail_position": railpos,
            "base_position": grabpos[well_index],
            "component_name": component_name,
            "use_pick_position": True,
        }

    if index == 9:
        tool_name = get_tool_name_from_user("Lookup camera")
        if tool_name is None:
            return None
        return {
            "name": "Lookup camera",
            "rail_position": robot.assemblyRobotConstants.LOOKUP_CAM_RAIL_LOCATION,
            "base_position": (
                robot.assemblyRobotConstants.LOOKUP_CAM_SK_PO
                if tool_name == RobotTool.SUCTION
                else robot.assemblyRobotConstants.LOOKUP_CAM_GRIPPER_PO
            ),
            "component_name": "suction",
            "use_pick_position": False,
            "tool_name": tool_name,
        }

    if index == 10:
        tool_name = get_tool_name_from_user("Placement pedestal")
        if tool_name is None:
            return None
        return {
            "name": "Placement pedestal",
            "rail_position": robot.assemblyRobotConstants.POST_RAIL_LOCATION,
            "base_position": (
                robot.assemblyRobotConstants.POST_C_SK_PO
                if tool_name == RobotTool.SUCTION
                else robot.assemblyRobotConstants.POST_C_GRIPPER_PO
            ),
            "component_name": "suction",
            "use_pick_position": False,
            "z_lower_limit": (
                robot.assemblyRobotConstants.POST_C_SK_PO[2]
                if tool_name == RobotTool.SUCTION
                else robot.assemblyRobotConstants.POST_C_GRIPPER_PO[2]
            ),
            "tool_name": tool_name,
            "initial_z_offset": 4.0,
        }

    print(f"Selection '{selection}' is out of range.")
    return None

def read_keypress() -> str:
    """Read one keypress, including terminal arrow escape sequences."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
        if key == "\x1b":
            next_char = sys.stdin.read(1)
            if next_char == "[":
                arrow = sys.stdin.read(1)
                if arrow == "A":
                    return "UP"
                if arrow == "B":
                    return "DOWN"
                if arrow == "C":
                    return "RIGHT"
                if arrow == "D":
                    return "LEFT"
            return "ESC"
        return key
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def assembly_robot_command_loop(
    robot: AssemblyRobot,
    image_path="/home/yuanjian/Research/BatteryLab/images",
):
    prompt = """Press [Enter] to quit.
[S] to test component pick up (universal for suction/gripper).
[G] to pick up/put back a component from a user defined well.
[M] to move a component to the assembly post.
[C] to take a photo of the desired tray.
[L] to grab a component and move to the lookup camera for a picture.
[Z] to manually adjust the robot arm at set positions
[0] to move the assembly robot out of the way
[H] to auto-grab one of each component and save lookup photos for Hough tuning.
[R] to reload the robotic placement and re-check for machine vision constants from the YAML files
[MV] to force recalibration of machine vision parameters
:> """

    component_prompt = """Which type of component do you want to test? Choose from the following
["CathodeCase", "Cathode", "Spacer", "SpacerExtra", "Anode", "Washer", "Separator", "AnodeCase"] ("e" or "exit" to cancel)
:> """

    while True:
        input_str = input(prompt).strip().upper()
        if input_str == "":
            break
        elif input_str == "0":
            # Move the assembly robot out of the way to rail_pos 0.0
            robot.move_home_and_out_of_way()
        elif input_str == "S":
            # Test the components pick-up and put them back
            results = get_component_location_from_user(robot, component_prompt)
            if results == None:
                continue
            reteach_mode = (
                input("Enter re-teaching mode? (y/n, default n): ").strip().lower()
                == "y"
            )
            test_all = input(
                f"Do you want to test the four corners or test all? (all/corners) default is corners:"
            )
            if reteach_mode and test_all == "all":
                print(
                    "Re-teaching mode only supports corner wells. Switching to corners mode."
                )
                test_all = "corners"
            for shape, grabpos, railpos, sub_location, component_name in results:
                test_range = [
                    0,
                    shape[1] - 1,
                    (shape[0] - 1) * shape[1],
                    len(grabpos) - 1,
                ]
                print(f"The test range: {test_range}")

                if test_all == "all":
                    test_range = range(0, len(grabpos))

                if component_name == "Washer":
                    robot.rail_meca500.change_tool(tool_name=RobotTool.GRIPPER)
                else:
                    robot.rail_meca500.change_tool(tool_name=RobotTool.SUCTION)
                robot.rail_meca500.move_home()
                robot.move_zaber_rail(railpos)
                robot.rail_meca500.move_to_pick_position(grabpos[test_range[0]], level=1.0)

                for i in test_range:
                    print(f"reaching the position of well {i}: {grabpos[i]}")
                    if reteach_mode:
                        adjusted_pose = robot.manual_arm_control_mode(
                            rail_position=railpos,
                            base_position=grabpos[i],
                            level=0.0,
                            component_name=component_name,
                            step_size=0.5,
                            use_pick_position=True,
                            skip_prep=True,
                        )
                        save_adjusted = input(
                            "Save adjusted pose for this well (persist + current session)? (y/n, default y): "
                        ).strip().lower()
                        if save_adjusted in ("", "y", "yes"):
                            try:
                                robot._apply_single_well_pose_in_memory(
                                    component_name=component_name,
                                    sub_location=sub_location,
                                    well_index=i,
                                    adjusted_pose=adjusted_pose,
                                )
                                robot._persist_single_corner_pose_to_yaml(
                                    component_name=component_name,
                                    sub_location=sub_location,
                                    shape=shape,
                                    well_index=i,
                                    adjusted_pose=adjusted_pose,
                                )
                                print(
                                    f"Replaced YAML corner pose for {component_name}/{sub_location}/index {i}."
                                )
                            except Exception as e:
                                print(
                                    f"Failed to persist adjusted pose for {component_name}/{sub_location}/index {i}: {e}"
                                )
                            grabpos[i] = adjusted_pose
                            print(f"Updated well {i} pose to: {grabpos[i]}")

                    robot.grab_component(
                        railpos,
                        grabpos[i],
                        is_grab=True,
                        component_name=component_name,
                        home_before=False,
                        home_after=False,
                        move_rail=False,
                    )
                    robot.grab_component(
                        railpos,
                        grabpos[i],
                        is_grab=False,
                        component_name=component_name,
                        home_before=False,
                        home_after=False,
                        move_rail=False,
                    )
                robot.rail_meca500.move_home()
        elif input_str == "C":
            # Take a photo of the selected tray
            component_name = input(component_prompt)
            image = robot.take_a_tray_photo(component_name)
            if image is not None:
                cur_time = datetime.now().strftime("%Y-%m-%d-%H-%M:%S")
                image_file = str(
                    Path(image_path) / f"ArmCam-{component_name}-{cur_time}.jpg"
                )
                cv2.imwrite(image_file, image)
            else:
                print("ERROR: Failed to capture tray photo. Continuing without saving.")
        elif input_str == "M":
            # Move the component to the assembly post
            results = get_component_location_from_user(robot, component_prompt)
            if results == None:
                continue
            if len(results) != 1:
                print(
                    "You can only move one component to the assembly post at a time. Operation aborted!"
                )
                continue
            shape, grabpos, railpos, sub_location, component_name = results[0]
            index = get_location_index_from_user(shape, sub_location)
            if index >= 0 and index < len(grabpos):
                robot.grab_component(
                    railpos, grabpos[index], is_grab=True, component_name=component_name
                )
                robot.drop_current_component_to_assembly_post(
                    component=Components[component_name]
                )
            else:
                print("The index you give is not valid for the robot to grab!")
                continue
        elif input_str == "G":
            # Grab a component or put it back
            results = get_component_location_from_user(robot, component_prompt)
            if results == None:
                continue
            if len(results) != 1:
                print("You can only grab one component at a time. Operation aborted!")
                continue
            shape, grabpos, railpos, sub_location, component_name = results[0]
            index = get_location_index_from_user(shape, sub_location)
            if not (index >= 0 and index < len(grabpos)):
                print("The index you give is not valid for the robot to grab!")
                continue
            is_grab_input = input("Do you want to grab it or put it back? (grab/put):")
            if is_grab_input == "grab":
                is_grab = True
            else:
                is_grab = False
            robot.grab_component(
                railpos, grabpos[index], is_grab=is_grab, component_name=component_name
            )

        elif input_str == "Z":
            # Manual adjustment for core positions (8 trays + lookup + pedestal).
            location = get_manual_core_location_from_user(robot)
            if location is None:
                continue

            level = 0.0
            if location["use_pick_position"]:
                try:
                    level = float(
                        input(
                            "Please provide the level for tray adjustment (1 is highest, 0 is closest to tray):"
                        )
                    )
                    level = max(0.0, min(1.0, level))
                except ValueError:
                    print("Invalid level. Using default level 1.0")
                    level = 1.0

            initial_step = 1.0
            step_input = input(
                "Initial manual step size (recommended 0.5~1.5, press Enter for 1.0): "
            ).strip()
            if step_input != "":
                try:
                    initial_step = float(step_input)
                except ValueError:
                    print(f"Cannot parse '{step_input}'. Using default 1.0")

            print(
                f"Manual control at {location['name']}. Keys: up(-x), down(+x), right(+y), left(-y), u(+z), d(-z), p(print), o(return to base), space(pause), r(resume), +, -, i, q"
            )
            robot.manual_arm_control_mode(
                location["rail_position"],
                location["base_position"],
                level=level,
                component_name=location["component_name"],
                step_size=initial_step,
                use_pick_position=location["use_pick_position"],
                z_lower_limit=location.get("z_lower_limit"),
                tool_name=location.get("tool_name"),
                initial_z_offset=location.get("initial_z_offset", 0.0),
            )
            robot.rail_meca500.move_home()
            
        elif input_str == "L":
            # Move a component to the lookup camera for a picture
            results = get_component_location_from_user(robot, component_prompt)
            if results == None:
                continue
            shape, grabpos, railpos, sub_location, component_name = results[0]
            if len(results) != 1:
                print("You can only move one component at a time. Operation aborted!")
                continue
            index = get_location_index_from_user(shape, sub_location)
            if not (index >= 0 and index < len(grabpos)):
                print("The index you give is not valid for the robot to grab!")
                continue
            robot.grab_component(
                railpos, grabpos[index], is_grab=True, component_name=component_name
            )
            image = robot.take_a_look_up_photo()
            if image is not None:
                cur_time = datetime.now().strftime("%Y-%m-%d-%H-%M:%S")
                image_file = str(
                    Path(image_path) / f"Lookup-{component_name}-{cur_time}.jpg"
                )
                print(f"writing image to {image_file}")
                cv2.imwrite(image_file, image)
            else:
                print("ERROR: Failed to capture lookup image. Continuing without saving.")
            robot.rail_meca500.move_home(tool=RobotTool.SUCTION)
            robot.grab_component(
                railpos, grabpos[index], is_grab=False, component_name=component_name
            )
        elif input_str == "H":
            # Automatically grab one of each component and capture lookup images
            robot.capture_lookup_images_for_all_components()
        elif input_str == "R":
            robot.load_position_files()
            robot.calibrate_machine_vision(force=False)
        elif input_str == "MV":
            robot.calibrate_machine_vision(force=True)
        else:
            print(f"Input {input_str} not recognized! Try again.")


def main():
    # Initialize
    rclpy.init()
    # log_path = "/home/yuanjian/Research/BatteryLab/logs"
    # logger = Logger("assembly_robot_test", log_path, "assembly_robot_test.log")
    robot = AssemblyRobot(logger=None, robot_address="192.168.0.100")
    robot.initialize_and_home_robots()
    image_path = Path("/home/yuanjian/Research/BatteryLab/images/")
    image_path.mkdir(exist_ok=True)

    # Calibrate robot-to-pixel distances if needed
    robot.calibrate_machine_vision(
        force=False
    )  # force requires calibration to be rerun

    # Main loop
    assembly_robot_command_loop(robot, image_path=str(image_path))

    # End program
    robot.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()