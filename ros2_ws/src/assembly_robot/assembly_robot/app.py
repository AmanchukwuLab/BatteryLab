from .AssemblyRobot import AssemblyRobot, assembly_robot_command_loop
from .CrimperRobot import CrimperRobot, crimper_robot_command_loop
from .LiquidRobot import LiquidRobot, liquid_robot_command_loop
from BatteryLab.robots.Constants import Components

import rclpy
from rclpy.node import Node


class AutoBatteryLab(Node):
    def __init__(self):
        super().__init__("auto_battery_lab")
        logger = self.get_logger()
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

    def put_a_component_on_assembly_post(self, component: Components, order: int):
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

        self.assembly_robot.drop_current_component_to_assembly_post(
            order=order, component=component, premove_callback=premove_callback
        )

        if premove_callback is not None:
            self.crimper_robot.release_separator()  # open gripper and move back home

    def assemble_a_battery(self):
        # Prepare all the robots and home them
        rail_pos = self.assembly_robot.get_rail_pos()
        if rail_pos == -1:
            self.get_logger().error(
                "The current linear rail pos cannot be determined! Check the status!"
            )
            return
        if rail_pos > 15:
            self.assembly_robot.move_home_and_out_of_way()
        self.liquid_robot.move_home()
        self.crimper_robot.move_home()
        order = 0
        # 1. Put a Cathode Case on the assembly post
        self.put_a_component_on_assembly_post(Components.CathodeCase, order)
        order += 1
        # 2. Put the Washer
        self.put_a_component_on_assembly_post(Components.Washer, order)
        order += 1
        # 3. Put the Spacer
        self.put_a_component_on_assembly_post(Components.Spacer, order)
        order += 1
        # 4. Put the Cathode
        self.put_a_component_on_assembly_post(Components.Cathode, order)
        order += 1
        # 5. Put the Separator
        self.put_a_component_on_assembly_post(Components.Separator, order)
        order += 1
        # 6. Add the electrolyte - (1) Move assembly robot out of the way
        self.assembly_robot.move_home_and_out_of_way(home=5.0)
        rail_pos = self.assembly_robot.get_rail_pos()
        if rail_pos == -1 or rail_pos > 10:
            self.get_logger().error(
                "The current linear rail pos cannot be cleared! Check the status!"
            )
            return
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
        self.put_a_component_on_assembly_post(Components.Anode, order)
        order += 1
        # 8. Put the SpacerExtra
        self.put_a_component_on_assembly_post(Components.SpacerExtra, order)
        order += 1
        # 9. Put the AnodeCase
        self.put_a_component_on_assembly_post(Components.AnodeCase, order)
        order += 1
        self.assembly_robot.move_home_and_out_of_way()
        rail_pos = self.assembly_robot.get_rail_pos()
        if rail_pos == -1 or rail_pos > 35:
            self.get_logger().error(
                "The current linear rail pos cannot be cleared! Check the status!"
            )
            return
        # 10. Crimper Robot
        self.crimper_robot.crimp_a_battery(False)
        self.crimper_robot.put_to_storage()
        self.crimper_robot.move_home()
        self.assembly_robot.save_counter_config()

    def test_separator_placement(self):
        # Test new crimper-assisted separator placement method
        self.put_a_component_on_assembly_post(Components.Separator, order=4)


def command_loop(batterylab: AutoBatteryLab):
    prompt = """Press [Enter] to quit, [A]ssembly to go to assembly_robot's command list,
[L]iquid to go to liquid_robot's command list, [C]rimper to go to crimper_robot's command list.
[B]attery to finish assemble a battery from scratch to storage.
:> """
    batterylab.assembly_robot.load_counter_config()
    while True:
        user_input = input(prompt).strip().lower()
        if user_input == "":
            break
        elif user_input == "a":
            assembly_robot_command_loop(batterylab.assembly_robot)
        elif user_input == "l":
            liquid_robot_command_loop(batterylab.liquid_robot)
        elif user_input == "c":
            crimper_robot_command_loop(batterylab.crimper_robot)
        elif user_input == "b":
            batterylab.assemble_a_battery()
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
