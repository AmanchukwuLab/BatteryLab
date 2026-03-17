#!/home/yuanjian/Research/BatteryLab/lab_venv/bin/python3
from BatteryLab.robots.RailMeca500 import RailMeca500

from BatteryLab.robots.AutoCorrection import AutoCorrection
from BatteryLab.robots.Constants import (
    AssemblyRobotConstants,
    AssemblyRobotCameraConstants,
    Components,
    RobotTool,
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
from datetime import datetime

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

    def move_home_and_out_of_way(self):
        self.rail_meca500.move_home(tool=RobotTool.SUCTION)
        self.move_zaber_rail(40.0)

    def move_zaber_rail(self, rail_pos: float):
        self.logger.info(f"Assembly Robot Moving to {rail_pos}")
        future = self.zaber_rail.send_move_request(rail_pos)
        while rclpy.ok():
            rclpy.spin_once(self.zaber_rail)
            self.get_logger().info("waiting for the moving request to complete...")
            time.sleep(1)
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

    def drop_current_component_to_assembly_post(self, order: int = 1):
        # First, take a photo and use to compute needed adjustment
        img = self.take_a_look_up_photo()
        dx, dy = self.auto_correction.get_offset_simple(img)

        # Proceed placing component
        self.rail_meca500.move_home()
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
        self.move_zaber_rail(rail_pos)
        self.rail_meca500.robot.MoveJoints(*mid_point_joints)
        self.rail_meca500.robot.WaitIdle(30)
        
        # Adjst robot_pos (pedestal drop coords) based on vision info
        print(f"Adjusting robot_pos ({robot_pos}) by dx = {dx} and dy = {dy}") # DEBUGGING
        robot_pos[0] += dx
        robot_pos[1] += dy
        self.rail_meca500.pick_place(robot_pos, is_grab=False)


    def calibrate_machine_vision(self, force = False):
        """Used to:
                1) take a picture and find the center of the suction cup (in pixels)
                2) calibrate pixels-to-robot units by taking a picture at (defaultx+dx, defaulty+dy), using HoughCircles to find the center of the suction cup (in pixels), then computing x_convert = (dx/(x_pixel_original-x_pixel_new)) and similarly for y_convert.
                3) store these variables in a calibration file for later reference.
        The calibration parameters may already exist. Setting the optional parameter 'force' to True will force the system to recalibrate.
        """
        print("Starting machine vision calibration routine...")
        # Check if calibration data already exists
        if not force:
            vision_params = self.auto_correction.get_vision_params()
            available_params = list(vision_params.keys())
            needed = ['x_convert', 'y_convert', 'suction_center']
            
            ready = True
            for needed_param in needed:
                if needed_param not in available_params:
                    print(f"{needed_param} not found in calibration file. Must recalibrate.")
                    ready = False

            # TODO: automatically check vision_params['date_calibrated']. If it's been a long time, force the system to re-calibrate.

            if ready == True:
                print("All calibration parameters found, moving on...")
                self.vision_params = vision_params
                return None
        else:
            print("Calibration route forced via 'force' parameter. Recalibrating...")

        # Specify suction tool
        self.rail_meca500.change_tool(RobotTool.SUCTION)
        
        # Take a picture of the empty suction cup
        img_suction_center = self.take_a_look_up_photo(rehome=False)

        # Take a picture with a slight adjustment
        dx, dy = -15, -15 # Note: these are restricted to a max of 20 (trimmed in take_a_look_up_photo). 

        img_suction_adjust = self.take_a_look_up_photo(dx=dx, dy=dy, rehome=False, midpoint=False)

        # Circle finding algorithm finds suction easier with inverted images
        img_suction_center = cv2.bitwise_not(img_suction_center)
        img_suction_adjust = cv2.bitwise_not(img_suction_adjust)
        
        # Compute conversion factors
        self.vision_params = self.auto_correction.compute_conversion(img_suction_center, img_suction_adjust, dx, dy)
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
        d_limit = 20
        if dx != 0:
            dx = max(-d_limit, min(d_limit, dx))
        if dy != 0:
            dy = max(-d_limit, min(d_limit, dy))

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
            time.sleep(1)
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
        self, rail_position, grab_position, is_grab=True, component_name="suction"
    ):
        """Grab a component for battery or return it to the tray.
        This requires a cooperation between the rail and the Meca500 robotic arm on top of it.
        """
        # Move home based on the tooling
        if component_name == "Washer":
            self.rail_meca500.change_tool(tool_name=RobotTool.GRIPPER)
            self.rail_meca500.move_home()
        else:
            self.rail_meca500.change_tool(tool_name=RobotTool.SUCTION)
            self.rail_meca500.move_home()

        # Move the Zaber Rail
        self.move_zaber_rail(rail_position)
        self.logger.debug(f"Assembly Robot will start picking soon.")
        # Let Meca500 pick up the component and move it home
        self.rail_meca500.pick_place(grab_position, is_grab=is_grab)

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

    def load_position_files(self):
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

    def drop_component(
        self,
        drop_po,
        component: Components,
        nr: int,
        auto_calib: bool = True,
        grab_check: bool = True,
        save_img: bool = True,
        show_image: bool = False,
    ):
        """Drop the component to the assembly post with autocorrection"""
        # TODO: add autocorrection on top of grab_component
        pass


def get_component_location_from_user(robot, component_prompt):
    success = False
    while not success:
        component_name = input(component_prompt)
        try:
            component = getattr(robot.assemblyRobotConstants, component_name)
            success = True
        except:
            if component_name.lower() == 'exit' or component_name.lower() == 'e':
                print("Cancelling operation...")
                return None
            print(f"Component '{component_name}' not recognized. Try again!")
    available_locations = list(component.keys())
    if len(available_locations) == 0:
        print(
            f"The selected component <{component_name}> has not been manually positioned yet!"
        )
        exit()
    sub_location = input(
        f"Which corner do you want to test (all, {available_locations}): "
    )
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

def get_user_confirmation(confirm=''):
    '''Checks if user input matches the parameter 'confirm' (default: 'Y'), case sensitive. If user presses return (input=None), the function will not error.'''
    response = '8.53973422267' # Nonsense to avoid false positives

    while response != confirm:
        if confirm == "":
            response = input("Hit <Enter> to confirm and move on.")
        else:
            response = input(f"Type {confirm} to confirm and move on.")
    return None

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
[Z] to move to a component well for manual adjustment.
[0] to move the assembly robot out of the way
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
            test_all = input(
                f"Do you want to test the four corners or test all? (all/corners) default is corners:"
            )
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
                for i in test_range:
                    print(f"reaching the position of well {i}: {grabpos[i]}")
                    robot.grab_component(
                        railpos, grabpos[i], is_grab=True, component_name=component_name
                    )
                    robot.grab_component(
                        railpos,
                        grabpos[i],
                        is_grab=False,
                        component_name=component_name,
                    )
        elif input_str == "C":
            # Take a photo of the selected tray
            component_name = input(component_prompt)
            image = robot.take_a_tray_photo(component_name)
            cur_time = datetime.now().strftime("%Y-%m-%d-%H-%M:%S")
            image_file = str(
                Path(image_path) / f"ArmCam-{component_name}-{cur_time}.jpg"
            )
            cv2.imwrite(image_file, image)
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
                robot.drop_current_component_to_assembly_post()
            else:
                print("The index you give is not valid for the robot to grab!")
                continue
        elif input_str == "G":
            # Grab a compoent or put it back
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
            # Manual adjustment for well positions.
            results = get_component_location_from_user(robot, component_prompt)
            if results == None:
                continue
            if len(results) != 1:
                print("You can only adjust one component at a time. Operation aborted!")
                continue
            shape, grabpos, railpos, sub_location, component_name = results[0]
            index = get_location_index_from_user(shape, sub_location)
            if not (index >= 0 and index < len(grabpos)):
                print("The index you give is not valid to do manual adjustment!")
                continue
            level = float(
                input(
                    "Please provide the level you want the manual adjustment to be (1 is highest, and 0 is closest to the tray):"
                )
            )
            robot.manual_adjustment(railpos, grabpos[index], level)
            finished = input(
                "Have you finished adjusting? Press Enter to move up and home the robot:"
            )
            robot.manual_adjustment(railpos, grabpos[index], 1)
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
            cur_time = datetime.now().strftime("$Y-%m-%d-%H-%M:%S")
            image_file = str(
                Path(image_path) / f"Lookup-{component_name}-{cur_time}.jpg"
            )
            print(f"writing image to {image_file}")
            cv2.imwrite(image_file, image)
            robot.rail_meca500.move_home(tool=RobotTool.SUCTION)
            robot.grab_component(
                railpos, grabpos[index], is_grab=False, component_name=component_name
            )
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
    robot.calibrate_machine_vision(force=False) # force requires calibration to be rerun

    # Main loop
    assembly_robot_command_loop(robot, image_path=str(image_path))
    
    # End program
    robot.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
