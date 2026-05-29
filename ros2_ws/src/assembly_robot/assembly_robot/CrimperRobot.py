#!/home/yuanjian/Research/BatteryLab/lab_venv/bin/python3
from BatteryLab.robots.BreadboardMeca500 import BreadBoardMeca500
from BatteryLab.helper.Logger import Logger
from BatteryLab.robots.MG400 import read_keypress
from BatteryLab.robots.Constants import RobotTool
import rclpy
from rclpy.node import Node
from camera_service.camera_client import ImageClient
import cv2


class CrimperRobot(Node):

    EDITABLE_POSES = [
        "PostReadyPose",
        "PostDownPose",
        "GrabReadyPose",
        "GrabbedUpPose",
        "PhotoCheckPreparePose",
        "PhotoCheckPose",
        "CrimperReadyToOperatePose",
        "CrimperDropPose",
        "CrimperReadyToPickPose",
        "CrimperPickPressPose",
        "CrimperPickPose",
        "CrimperPickedUpPose",
        "StorageReadyPose",
        "StorageDropPose",
    ]

    SAFE_POSE_SEQUENCES = {
        "post": [
            ("PostReadyPose", "pose"),
            ("PostDownPose", "lin"),
            ("GrabReadyPose", "lin"),
            ("GrabbedUpPose", "lin"),
        ],
        "crimper_pickup": [
            ("CrimperReadyToOperatePose", "pose"),
            ("CrimperDropPose", "lin"),
            ("CrimperReadyToPickPose", "lin"),
            ("CrimperPickPressPose", "lin"),
            ("CrimperPickPose", "lin"),
            ("CrimperPickedUpPose", "lin"),
        ],
        "storage": [
            ("StorageReadyPose", "pose"),
            ("StorageDropPose", "lin"),
            ("StorageReadyPose", "lin"),
        ],
    }

    POSE_TO_SEQUENCE = {
        "PostReadyPose": ("post", 0),
        "PostDownPose": ("post", 1),
        "GrabReadyPose": ("post", 2),
        "GrabbedUpPose": ("post", 3),
        "CrimperReadyToOperatePose": ("crimper_pickup", 0),
        "CrimperDropPose": ("crimper_pickup", 1),
        "CrimperReadyToPickPose": ("crimper_pickup", 2),
        "CrimperPickPressPose": ("crimper_pickup", 3),
        "CrimperPickPose": ("crimper_pickup", 4),
        "CrimperPickedUpPose": ("crimper_pickup", 5),
        "StorageReadyPose": ("storage", 0),
        "StorageDropPose": ("storage", 1),
    }

    def __init__(self, logger=None, robot_address="192.168.0.101"):
        super().__init__("crimper_robot")
        self.logger = self.get_logger() if logger is None else logger
        self.crimper_robot = BreadBoardMeca500(
            logger=self.logger, robot_address=robot_address
        )
        self.tower_camera_client = ImageClient(
            node_name="crimper_tower_camera", serv_name="/batterylab/lookup_camera"
        )

    def _pose_value(self, pose_name: str) -> list[float]:
        if not hasattr(self.crimper_robot.crimperRobotConstants, pose_name):
            raise ValueError(f"Unknown crimper pose '{pose_name}'")
        pose = getattr(self.crimper_robot.crimperRobotConstants, pose_name)
        return [float(value) for value in pose]

    def _set_pose_value(self, pose_name: str, pose: list[float]) -> None:
        setattr(
            self.crimper_robot.crimperRobotConstants,
            pose_name,
            [float(value) for value in pose],
        )

    def _print_pose_help(self):
        print(
            "Controls: arrows move x/y, u/d move z, p prints current pose, o returns to original pose, "
            "h prints help, + or = increases step, - or _ decreases step, s saves this pose, k keeps original, q quits."
        )

    def _format_pose_row(self, index: int, pose_name: str) -> str:
        pose = self._pose_value(pose_name)
        return (
            f"{index:>2}. {pose_name:<25} "
            f"x={pose[0]:>8.3f}  y={pose[1]:>8.3f}  z={pose[2]:>8.3f}  "
            f"a={pose[3]:>8.3f}  b={pose[4]:>8.3f}  c={pose[5]:>8.3f}"
        )

    def _move_to_pose(self, pose: list[float], move_kind: str) -> None:
        if move_kind == "pose":
            self.crimper_robot.robot.MovePose(*pose)
        else:
            self.crimper_robot.robot.MoveLin(*pose)
        self.crimper_robot.robot.WaitIdle(30)

    def _sequence_for_pose(self, pose_name: str) -> tuple[list[tuple[str, str]], int]:
        sequence_key, stop_index = self.POSE_TO_SEQUENCE.get(pose_name, (None, 0))
        if sequence_key is None:
            return [(pose_name, "pose")], 0
        return self.SAFE_POSE_SEQUENCES[sequence_key], stop_index

    def _move_sequence_segment(
        self, sequence: list[tuple[str, str]], start_index: int, end_index: int
    ) -> None:
        for route_pose_name, move_kind in sequence[start_index : end_index + 1]:
            pose = self._pose_value(route_pose_name)
            self._move_to_pose(pose, move_kind)

    def _adjust_single_pose(self, pose_name: str, updated_poses: dict[str, list[float]]):
        original_pose = self._pose_value(pose_name)
        current_pose = original_pose.copy()
        sequence, selected_index = self._sequence_for_pose(pose_name)
        route_started = False

        self.crimper_robot.robot.SetTrf(*self.crimper_robot.crimperRobotConstants.TRF)
        self._move_sequence_segment(sequence, 0, selected_index)
        route_started = True

        min_step = 0.01
        max_step = 5.0
        step_size = 1.0
        helper_text = (
            f"\nCrimper pose adjustment mode for '{pose_name}' started.\n"
            "=====================================================\n"
        )
        self.logger.info(helper_text)
        self._print_pose_help()

        while True:
            key = read_keypress()
            if key in ("q", "Q"):
                decision = input(
                    "Quit pose adjustment. Save accepted pose updates so far? (y/n, default y): "
                ).strip().lower()
                if decision in ("", "y", "yes"):
                    updated_poses[pose_name] = current_pose.copy()
                else:
                    print("Discarded changes from this session.")
                break
            if key in ("s", "S"):
                updated_poses[pose_name] = current_pose.copy()
                print(
                    f"Saved updated pose '{pose_name}': x={current_pose[0]:.3f}, y={current_pose[1]:.3f}, z={current_pose[2]:.3f}"
                )
                break
            if key in ("k", "K"):
                updated_poses[pose_name] = original_pose.copy()
                current_pose = original_pose.copy()
                print(f"Kept original pose for '{pose_name}'.")
                break
            if key in ("h", "H"):
                self._print_pose_help()
                continue
            if key in ("+", "="):
                step_size = min(max_step, step_size * 2.0)
                print(f"Step size increased to {step_size:.3f}")
                continue
            if key in ("-", "_"):
                step_size = max(min_step, step_size / 2.0)
                print(f"Step size decreased to {step_size:.3f}")
                continue
            if key in ("p", "P"):
                print(
                    f"Current pose ({pose_name}): x={current_pose[0]:.3f}, y={current_pose[1]:.3f}, z={current_pose[2]:.3f}, "
                    f"a={current_pose[3]:.3f}, b={current_pose[4]:.3f}, c={current_pose[5]:.3f}, step={step_size:.3f}"
                )
                continue
            if key in ("o", "O"):
                current_pose = original_pose.copy()
                print("Returning to original pose.")
                self._move_sequence_segment(sequence, 0, selected_index)
                continue

            moved = False
            if key == "UP":
                current_pose[0] -= step_size
                moved = True
            elif key == "DOWN":
                current_pose[0] += step_size
                moved = True
            elif key == "RIGHT":
                current_pose[1] += step_size
                moved = True
            elif key == "LEFT":
                current_pose[1] -= step_size
                moved = True
            elif key in ("u", "U"):
                current_pose[2] += step_size
                moved = True
            elif key in ("d", "D"):
                current_pose[2] -= step_size
                moved = True

            if moved:
                self.crimper_robot.robot.MoveLin(*current_pose)
                self.crimper_robot.robot.WaitIdle(30)

        if route_started and selected_index + 1 < len(sequence):
            self._move_sequence_segment(sequence, selected_index + 1, len(sequence) - 1)

        self.move_home()
        return True

    def _save_updated_crimper_poses(self, updated_poses: dict[str, list[float]]) -> None:
        for pose_name, pose in updated_poses.items():
            self._set_pose_value(pose_name, pose)
        self.crimper_robot.save_crimper_position_config()
        self.crimper_robot.reload_crimper_position_config()
        print(f"Saved updated crimper poses to {self.crimper_robot.crimper_robot_constants_config_file}")

    def manual_adjust_crimper_positions(self):
        updated_poses: dict[str, list[float]] = {}
        pose_names = self.EDITABLE_POSES
        print("Crimper pose adjustment mode started.")
        print("Select a pose to adjust, then use the keyboard to move it.")

        while True:
            print("\nAvailable poses:")
            for index, pose_name in enumerate(pose_names, start=1):
                print(self._format_pose_row(index, pose_name))
            selection = input(
                "Choose pose number to adjust, or press Enter to finish: "
            ).strip()
            if selection == "":
                break
            try:
                pose_index = int(selection) - 1
            except ValueError:
                print("Invalid selection.")
                continue
            if pose_index < 0 or pose_index >= len(pose_names):
                print("Invalid selection.")
                continue

            pose_name = pose_names[pose_index]
            should_continue = self._adjust_single_pose(pose_name, updated_poses)
            if not should_continue:
                break

        if updated_poses:
            final_choice = input(
                "Write updated crimper poses to storage file? (y/n, default y): "
            ).strip().lower()
            if final_choice in ("", "y", "yes"):
                self._save_updated_crimper_poses(updated_poses)
            else:
                print("Discarded changes from this session.")
        self.move_home()

    def initialize_and_home_robots(self):
        ok = self.crimper_robot.initializeRobot()
        if not ok:
            print("The Crimper Meca500 cannot be connected")
            exit()
        self.crimper_robot.move_home(tool=RobotTool.GRIPPER)

    def move_home(self):
        self.crimper_robot.move_home(tool=RobotTool.GRIPPER)

    def exitRobot(self):
        self.crimper_robot.exitRobot()

    def move_to_hold_separator(self):
        self.crimper_robot.move_to_pick_up_ready_pose()

    def close_gripper_to_hold_separator(self):
        self.crimper_robot.close_gripper()

    def release_separator(self):
        self.crimper_robot.open_gripper()
        self.crimper_robot.return_from_pick_up()

    def crimp_a_battery(self, use_camera_check: bool = False):
        self.crimper_robot.pick_up_from_assembly_post()
        if use_camera_check:
            ok = self.check_battery_is_picked()
            if not ok:
                print("The battery is not picked up!")
                self.logger.error("The battery is not picked up properly")
                return
        self.crimper_robot.drop_to_crimper()
        # TODO: Call the crimper to do the crimping work
        self.crimper_robot.pick_up_from_crimper()
        if use_camera_check:
            ok = self.check_battery_is_picked()
            if not ok:
                print("The battery is not picked up!")
                self.logger.error("The battery is not picked up properly")
                return
        self.logger.info("Finished crimping a battery!")

    def put_to_storage(self):
        self.crimper_robot.put_to_storage()

    def drop_back_to_assembly_post(self):
        self.crimper_robot.drop_back_to_assembly_post()

    def check_battery_is_picked(self) -> bool:
        self.crimper_robot.move_for_photo_check()
        image = self.tower_camera_client.get_image()
        # TODO: Analyze the image to determine if the battery is in there
        self.tower_camera_client.display_image()
        human_decision = input("Is the battery there (yes/no), default is yes:")
        self.crimper_robot.move_away_from_photo_check()
        if human_decision == "yes" or human_decision == "":
            return True
        else:
            return False


def crimper_robot_command_loop(robot: CrimperRobot):
    prompt = """Press [Enter] to quit.
[M] to manually adjust crimper poses.
[P] to pick up from the post.
[C] to drop the battery to the crimper.
[D] to pick the battery up from the crimper
[S] to store the battery in the storage post.
[B] to put the battery back to the assembly post.
[G] to grab from the post, do the crimping and put back to the post.
[A] to run the whole process and store the battery in storage post.
[T] to move to the camera tower and see the picture.
:> """

    while True:
        input_str = input(prompt).strip().upper()
        if input_str == "":
            break
        elif input_str == "M":
            robot.manual_adjust_crimper_positions()
        elif input_str == "P":
            robot.crimper_robot.move_home(RobotTool.SUCTION)
            robot.crimper_robot.pick_up_from_assembly_post()
        elif input_str == "C":
            robot.crimper_robot.move_home(RobotTool.SUCTION)
            robot.crimper_robot.drop_to_crimper()
        elif input_str == "D":
            robot.crimper_robot.move_home(RobotTool.SUCTION)
            robot.crimper_robot.pick_up_from_crimper()
        elif input_str == "S":
            robot.crimper_robot.move_home(RobotTool.SUCTION)
            robot.crimper_robot.put_to_storage()
        elif input_str == "B":
            robot.crimper_robot.move_home(RobotTool.SUCTION)
            robot.drop_back_to_assembly_post()
            robot.move_home()
        elif input_str == "G":
            robot.crimper_robot.move_home(RobotTool.SUCTION)
            robot.crimp_a_battery(False)
            robot.drop_back_to_assembly_post()
            robot.move_home()
        elif input_str == "A":
            use_camera = input(
                "Do you want to use camera_check? (yes/no), default is yes:"
            )
            if use_camera == "" or use_camera == "yes":
                robot.crimp_a_battery(use_camera_check=True)
            else:
                robot.crimp_a_battery(use_camera_check=False)

            robot.put_to_storage()
            robot.move_home()
        elif input_str == "T":
            is_picked = robot.check_battery_is_picked()
            print(f"The battery is picked: {is_picked}")
        else:
            print("The command you gave is not recognized!")
    robot.crimper_robot.move_home(tool=RobotTool.GRIPPER)


def main():
    rclpy.init()
    log_path = "/home/yuanjian/Research/BatteryLab/logs"
    logger = Logger("assembly_robot_test", log_path, "assembly_robot_test.log")
    robot = CrimperRobot(logger, robot_address="192.168.0.101")
    robot.initialize_and_home_robots()
    crimper_robot_command_loop(robot=robot)
    robot.exitRobot()
    robot.destroy_node()
    rclpy.shutdown()
