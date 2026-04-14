from .AssemblyRobot import AssemblyRobot, assembly_robot_command_loop
from .CrimperRobot import CrimperRobot, crimper_robot_command_loop
from .LiquidRobot import LiquidRobot, liquid_robot_command_loop
from BatteryLab.robots.Constants import Components
from BatteryLab.electrolyte_planner import (
    DEFAULT_STATE_PATH,
    clear_vial,
    load_inventory_state,
    print_vial_statuses,
    save_inventory_state,
    set_vial_contents,
)

import csv
import re
import statistics
import rclpy
from rclpy.node import Node
from pathlib import Path
from datetime import datetime
from typing import Optional
import cv2


def _component_slug(component_name: str) -> str:
    component_name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", component_name)
    component_name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", component_name)
    return component_name.lower()


class BatterySessionTracker:
    LARGE_ADJUSTMENT_STATIC_THRESHOLD = 1.0
    LARGE_ADJUSTMENT_MIN_SAMPLES = 5
    LARGE_ADJUSTMENT_MAD_MULTIPLIER = 3.0

    def __init__(self, session_root: Path):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir = session_root / f"session_{self.session_id}"
        self.lookup_image_dir = self.session_dir / "lookup_images"
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.lookup_image_dir.mkdir(parents=True, exist_ok=True)

        self.records_path = self.session_dir / "battery_records.csv"
        self._battery_records = []
        self._battery_index = 0
        self._component_adjust_history = {}
        self.component_order = [
            Components.CathodeCase,
            Components.Washer,
            Components.Spacer,
            Components.Cathode,
            Components.Separator,
            Components.Anode,
            Components.SpacerExtra,
            Components.AnodeCase,
        ]
        self.fieldnames = [
            "battery_id",
            "session_id",
            "battery_start_time",
            "battery_end_time",
            "battery_status",
        ]
        for component in self.component_order:
            slug = _component_slug(component.name)
            self.fieldnames.extend(
                [
                    f"{slug}_dx",
                    f"{slug}_dy",
                    f"{slug}_detected",
                    f"{slug}_lookup_image",
                    f"{slug}_lookup_reason",
                ]
            )
            self._component_adjust_history[slug] = {"dx": [], "dy": []}
        self._flush()

    def start_battery(self):
        self._battery_index += 1
        record = {
            "battery_id": self._battery_index,
            "session_id": self.session_id,
            "battery_start_time": datetime.now().isoformat(timespec="seconds"),
            "battery_end_time": "",
            "battery_status": "running",
        }
        for component in self.component_order:
            slug = _component_slug(component.name)
            record[f"{slug}_dx"] = ""
            record[f"{slug}_dy"] = ""
            record[f"{slug}_detected"] = ""
            record[f"{slug}_lookup_image"] = ""
            record[f"{slug}_lookup_reason"] = ""
        self._battery_records.append(record)
        self._flush()
        return record

    def _is_large_adjustment_outlier(self, slug: str, dx: float, dy: float) -> bool:
        axis_values = {
            "dx": abs(dx),
            "dy": abs(dy),
        }
        for axis, value in axis_values.items():
            history = self._component_adjust_history[slug][axis]
            if len(history) < self.LARGE_ADJUSTMENT_MIN_SAMPLES:
                continue
            median = statistics.median(history)
            deviations = [abs(v - median) for v in history]
            mad = statistics.median(deviations)
            if mad <= 1e-9:
                continue
            if abs(value - median) > self.LARGE_ADJUSTMENT_MAD_MULTIPLIER * mad:
                return True
        return False

    def _append_adjustment_history(self, slug: str, dx: float, dy: float):
        self._component_adjust_history[slug]["dx"].append(abs(dx))
        self._component_adjust_history[slug]["dy"].append(abs(dy))

    def record_component_result(
        self,
        battery_record: dict,
        component: Components,
        result: dict,
        order: int,
    ):
        slug = _component_slug(component.name)
        dx = float(result.get("dx", 0.0))
        dy = float(result.get("dy", 0.0))
        component_detected = bool(result.get("component_detected", False))

        battery_record[f"{slug}_dx"] = f"{dx:.6f}"
        battery_record[f"{slug}_dy"] = f"{dy:.6f}"
        battery_record[f"{slug}_detected"] = component_detected

        capture_reasons = []
        if not component_detected:
            capture_reasons.append("detection_failed")

        large_static = (
            abs(dx) > self.LARGE_ADJUSTMENT_STATIC_THRESHOLD
            or abs(dy) > self.LARGE_ADJUSTMENT_STATIC_THRESHOLD
        )
        if large_static:
            capture_reasons.append("large_adjustment_static")

        large_outlier = self._is_large_adjustment_outlier(slug, dx, dy)
        if large_outlier:
            capture_reasons.append("large_adjustment_outlier")

        should_capture = len(capture_reasons) > 0

        if should_capture:
            lookup_image = result.get("lookup_image")
            if lookup_image is not None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                filename = (
                    self.lookup_image_dir
                    / f"battery_{battery_record['battery_id']:03d}_step_{order:02d}_{slug}_{timestamp}.png"
                )
                cv2.imwrite(str(filename), lookup_image)
                battery_record[f"{slug}_lookup_image"] = str(filename)
                battery_record[f"{slug}_lookup_reason"] = ";".join(capture_reasons)
            else:
                battery_record[f"{slug}_lookup_reason"] = (
                    ";".join(capture_reasons) + ";image_unavailable"
                )

        self._append_adjustment_history(slug, dx, dy)
        self._flush()

    def finish_battery(self, battery_record: dict, status: str):
        battery_record["battery_end_time"] = datetime.now().isoformat(timespec="seconds")
        battery_record["battery_status"] = status
        self._flush()

    def _flush(self):
        with open(self.records_path, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            writer.writeheader()
            for record in self._battery_records:
                writer.writerow(record)


class AutoBatteryLab(Node):
    def __init__(self):
        super().__init__("auto_battery_lab")
        logger = self.get_logger()
        session_root = Path(__file__).resolve().parents[4] / "images" / "battery_sessions"
        self.session_tracker = BatterySessionTracker(session_root)
        logger.info(f"Battery session records will be stored in {self.session_tracker.session_dir}")
        # Initialize the Assembly Robot
        self.assembly_robot = AssemblyRobot(
            logger=logger, robot_address="192.168.0.100"
        )
        self.assembly_robot.initialize_and_home_robots()
        self.assembly_robot.calibrate_machine_vision(force=False)
        logger.info("Assembly robot vision calibration complete (or reused).")
        self.assembly_robot.move_home_and_out_of_way()

        # Initialize the Liquid Robot
        self.liquid_robot = LiquidRobot(ip="192.168.0.107", logger=logger)
        ok = self.liquid_robot.initialize_robot()
        if not ok:
            print("Failed to initialize the Liquid Robot, program aborted!")
            exit()
        # Initialize the Crimper Robot
        self.crimper_robot = CrimperRobot(logger=logger, robot_address="192.168.0.101")
        self.crimper_robot.initialize_and_home_robots()
        logger.info("Finished intializing the Auto Battery Lab")

    def put_a_component_on_assembly_post(
        self,
        component: Components,
        order: int,
        battery_record: Optional[dict] = None,
    ):
        component_name = component.name
        global_index, subtray_shape, well_grab_pos, rail_pos, subtray_name = (
            self.assembly_robot.get_next_well_of_component(component_name)
        )
        # If separator, crimper needs to close to grab it before assembly robot moves out of the way
        premove_callback = None
        if component == Components.Separator:
            # TESTING: use crimper robot to hold down separator
            if self.assembly_robot.get_rail_pos() > 100.0:
                # Assembly robot too close for crimper operation
                self.assembly_robot.move_zaber_rail(100.0)
            # Move crimper robot into position
            self.crimper_robot.move_to_hold_separator()
            premove_callback = (
                self.crimper_robot.close_gripper_to_hold_separator
            )  # don't call yet!

        self.assembly_robot.grab_component(
            rail_position=rail_pos,
            grab_position=well_grab_pos,
            is_grab=True,
            component_name=component_name,
        )

        result = self.assembly_robot.drop_current_component_to_assembly_post(
            order=order, component=component, premove_callback=premove_callback
        )
        if battery_record is not None:
            self.session_tracker.record_component_result(
                battery_record=battery_record,
                component=component,
                result=result,
                order=order,
            )

        if premove_callback is not None:
            self.crimper_robot.release_separator()  # open gripper and move back home

    def assemble_a_battery(self):
        battery_record = self.session_tracker.start_battery()
        # Prepare all the robots and home them
        try:
            rail_pos = self.assembly_robot.get_rail_pos()
            if rail_pos == -1:
                raise RuntimeError(
                    "The current linear rail pos cannot be determined! Check the status!"
                )
            if rail_pos > 15:
                self.assembly_robot.move_home_and_out_of_way()
            self.liquid_robot.move_home()
            self.crimper_robot.move_home()
            order = 0
            # 1. Put a Cathode Case on the assembly post
            self.put_a_component_on_assembly_post(
                Components.CathodeCase, order, battery_record=battery_record
            )
            order += 1
            # 2. Put the Washer
            self.put_a_component_on_assembly_post(
                Components.Washer, order, battery_record=battery_record
            )
            order += 1
            # 3. Put the Spacer
            self.put_a_component_on_assembly_post(
                Components.Spacer, order, battery_record=battery_record
            )
            order += 1
            # 4. Put the Cathode
            self.put_a_component_on_assembly_post(
                Components.Cathode, order, battery_record=battery_record
            )
            order += 1
            # 5. Put the Separator
            self.put_a_component_on_assembly_post(
                Components.Separator, order, battery_record=battery_record
            )
            order += 1
            # 6. Add the electrolyte - (1) Move assembly robot out of the way
            self.assembly_robot.move_home_and_out_of_way(home=8.0)
            rail_pos = self.assembly_robot.get_rail_pos()
            if rail_pos == -1 or rail_pos > 10:
                raise RuntimeError(
                    "The current linear rail pos cannot be cleared! Check the status!"
                )
            # 6.(2) Add electrolyte
            self.liquid_robot.MG400.move_home()
            # TODO: change tip for different electrolytes
            tip_x, tip_y = 0, 0
            liquid_x, liquid_y = 0, 0
            volume_to_get, volume_for_a_battery = 50, 50
            self.liquid_robot.MG400.get_tip(tip_x, tip_y)
            # TODO: change liquid bottle location for different electrolytes
            self.liquid_robot.MG400.get_liquid(liquid_x, liquid_y, volume_to_get)
            self.liquid_robot.MG400.add_liquid_to_post(volume_for_a_battery)
            self.liquid_robot.MG400.return_liquid(liquid_x, liquid_y)
            self.liquid_robot.MG400.drop_tip(tip_x, tip_y)
            self.liquid_robot.MG400.move_home()
            # 7. Put the Anode
            self.put_a_component_on_assembly_post(
                Components.Anode, order, battery_record=battery_record
            )
            order += 1
            # 8. Put the SpacerExtra
            self.put_a_component_on_assembly_post(
                Components.SpacerExtra, order, battery_record=battery_record
            )
            order += 1
            # 9. Put the AnodeCase
            self.put_a_component_on_assembly_post(
                Components.AnodeCase, order, battery_record=battery_record
            )
            order += 1
            self.assembly_robot.move_home_and_out_of_way()
            rail_pos = self.assembly_robot.get_rail_pos()
            if rail_pos == -1 or rail_pos > 35:
                raise RuntimeError(
                    "The current linear rail pos cannot be cleared! Check the status!"
                )
            # 10. Crimper Robot
            self.crimper_robot.crimp_a_battery(False)
            self.crimper_robot.put_to_storage()
            self.crimper_robot.move_home()
            self.assembly_robot.save_counter_config()
            self.session_tracker.finish_battery(battery_record, status="completed")
        except Exception:
            self.session_tracker.finish_battery(
                battery_record, status="failed"
            )
            raise

    def test_separator_placement(self):
        # Test new crimper-assisted separator placement method
        self.put_a_component_on_assembly_post(Components.Separator, order=4)


def _read_positive_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            print("Please enter a numeric value.")
            continue
        if value <= 0:
            print("Please enter a value greater than zero.")
            continue
        return value


def _is_cancel(value: str) -> bool:
    return value.strip().lower() in {"q", "x", "cancel"}


def _read_positive_float_or_cancel(prompt: str):
    while True:
        raw = input(prompt).strip()
        if _is_cancel(raw):
            return None
        try:
            value = float(raw)
        except ValueError:
            print("Please enter a numeric value, or type 'q' to cancel.")
            continue
        if value <= 0:
            print("Please enter a value greater than zero.")
            continue
        return value


def _read_non_negative_int_or_cancel(prompt: str):
    while True:
        raw = input(prompt).strip()
        if _is_cancel(raw):
            return None
        try:
            value = int(raw)
        except ValueError:
            print("Please enter an integer value, or type 'q' to cancel.")
            continue
        if value < 0:
            print("Please enter a value greater than or equal to zero.")
            continue
        return value


def electrolyte_planner_menu(batterylab: AutoBatteryLab):
    logger = batterylab.get_logger()
    inventory = load_inventory_state()
    logger.info(f"Loaded electrolyte inventory from {DEFAULT_STATE_PATH}")

    prompt = """------------------------
Electrolyte Planner Menu
[V]iew vial status
[A]dd/update vial contents (after physical refill)
[C]leaned vial (mark as empty)
[R]eload inventory from disk
[S]ave inventory to disk
[Enter] Back to main menu
:> """

    while True:
        user_input = input(prompt).strip().lower()
        if len(user_input) > 1:
            user_input = user_input[0]

        if user_input == "":
            break
        if user_input == "v":
            print_vial_statuses(inventory)
            continue
        if user_input == "a":
            print("Type 'q' at any prompt to cancel this operation.")
            x_ind = _read_non_negative_int_or_cancel("Liquid bottle index x: ")
            if x_ind is None:
                print("Canceled add/update operation.")
                continue

            y_ind = _read_non_negative_int_or_cancel("Liquid bottle index y: ")
            if y_ind is None:
                print("Canceled add/update operation.")
                continue

            solution_name = input("Solution name: ").strip()
            if _is_cancel(solution_name):
                print("Canceled add/update operation.")
                continue

            density_g_per_ml = _read_positive_float_or_cancel("Density (g/mL): ")
            if density_g_per_ml is None:
                print("Canceled add/update operation.")
                continue

            volume_ul = _read_positive_float_or_cancel("Current volume in vial (uL): ")
            if volume_ul is None:
                print("Canceled add/update operation.")
                continue

            try:
                inventory = set_vial_contents(
                    inventory,
                    x_ind=x_ind,
                    y_ind=y_ind,
                    solution_name=solution_name,
                    volume_ul=volume_ul,
                    density_g_per_ml=density_g_per_ml,
                )
                save_inventory_state(inventory)
                print(
                    f"Updated vial at (x={x_ind}, y={y_ind}) and saved inventory."
                )
            except Exception as e:
                print(f"Failed to update vial: {e}")
            continue
        if user_input == "c":
            print("Type 'q' to cancel this operation.")
            x_ind = _read_non_negative_int_or_cancel(
                "Liquid bottle index x to mark cleaned/empty: "
            )
            if x_ind is None:
                print("Canceled clean operation.")
                continue

            y_ind = _read_non_negative_int_or_cancel(
                "Liquid bottle index y to mark cleaned/empty: "
            )
            if y_ind is None:
                print("Canceled clean operation.")
                continue

            confirm = input(
                f"Confirm cleaning vial at (x={x_ind}, y={y_ind})? This sets its volume to 0.0 uL (y/n or q to cancel): "
            ).strip().lower()
            if _is_cancel(confirm):
                print("Canceled clean operation.")
                continue
            if confirm != "y":
                print("Canceled.")
                continue
            try:
                inventory = clear_vial(inventory, x_ind=x_ind, y_ind=y_ind)
                save_inventory_state(inventory)
                print(
                    f"Marked vial at (x={x_ind}, y={y_ind}) as cleaned and saved inventory."
                )
            except Exception as e:
                print(f"Failed to clear vial: {e}")
            continue
        if user_input == "r":
            inventory = load_inventory_state()
            print("Reloaded inventory from disk.")
            continue
        if user_input == "s":
            save_inventory_state(inventory)
            print("Saved inventory to disk.")
            continue

        print("The choice is not valid. Please try again.")


def command_loop(batterylab: AutoBatteryLab):
    prompt = """Press [Enter] to quit, [A]ssembly to go to assembly_robot's command list,
[L]iquid to go to liquid_robot's command list, [C]rimper to go to crimper_robot's command list.
[B]attery to finish assemble a battery from scratch to storage.
[E]lectrolyte planner to manage vial contents and cleaning status.
:> """
    batterylab.assembly_robot.load_counter_config()
    while True:
        user_input = input(prompt).strip().lower()
        if len(user_input) > 1:
            user_input = user_input[0]
        if user_input == "":
            break
        elif user_input == "a":
            assembly_robot_command_loop(batterylab.assembly_robot)
        elif user_input == "l":
            liquid_robot_command_loop(batterylab.liquid_robot)
        elif user_input == "c":
            crimper_robot_command_loop(batterylab.crimper_robot)
        elif user_input == "b":
            try:
                batterylab.assemble_a_battery()
            except Exception as e:
                batterylab.get_logger().error(f"Battery assembly failed: {e}")
        elif user_input == "e":
            electrolyte_planner_menu(batterylab)
        elif user_input == "s":
            if input("Run separator placement test? (y/n, default n): ").strip().lower() == "y":
                batterylab.test_separator_placement()
        else:
            print("The choice is not valid. Please try again.")


def main():
    rclpy.init()
    batterylab = AutoBatteryLab()

    command_loop(batterylab)
    batterylab.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
