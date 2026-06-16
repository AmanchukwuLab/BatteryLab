#!/home/yuanjian/Research/BatteryLab/lab_venv/bin/python3
import rclpy
from rclpy.node import Node
from BatteryLab.robots.MG400 import MG400, main_loop
from sartorius.sartorius_client import SartoriusClient

MAX_PIPETTE_VOLUME = 200 # in microliters, per equipment specs

class LiquidRobot(Node):
    def __init__(self, ip="192.168.0.107", logger=None):
        super().__init__("liquid_robot")
        self.logger = self.get_logger() if logger is None else logger
        self.sartorius = SartoriusClient()
        self.MG400 = MG400(logger=self.logger, ip=ip, sartorius_rline=self.sartorius)

    def initialize_robot(self):
        ok = self.MG400.intialize_robot()
        if not ok:
            print("Failed to initialize MG400, program aborted!")
            return False
        return True

    def __del__(self):
        self.disconnect()

    def move_home(self):
        self.MG400.move_home()

    def disconnect(self):
        self.MG400.disconnect()
        self.logger.info("The MG400 robot has successfully disconnected!")


def manual_position_loop(liquid_robot: LiquidRobot):
    cartesian = liquid_robot.MG400.dashboard.GetPose()
    joints = liquid_robot.MG400.dashboard.GetAngle()
    print(f"The current cartesian coordinates are [{cartesian}]")
    print(f"The current joint angles are [{joints}]")
    mode = input(
        "do you want to drive in joints (J) or cartesian (C)? Type in J or C: "
    )
    if mode == "J":
        parameters_str = input("Please type in the 4 joints [J1, J2, J3, J4]:")
    elif mode == "C":
        parameters_str = input(
            "Please type in the 4 cartesian coordinates: [X, Y, Z, R]:"
        )
    else:
        print("The mode you select does not exist! Please select J or C!")
        return

    parameters_str = parameters_str.strip("[]")
    parameters = [float(x) for x in parameters_str.split(",")]
    if mode == "J":
        print(f"The robot is moving with JointMovJ to {parameters}")
        liquid_robot.MG400.movectl.JointMovJ(*parameters)
    elif mode == "C":
        print(f"The robot is moving with MovJ to cartesian coordinates {parameters}")
        liquid_robot.MG400.movectl.MovJ(*parameters)

def get_tip_coords():
    while True:
        print("Enter 'q' to quit.")
        x_input = input("Please input tip index x: ").strip().replace('.', '')
        y_input = input("Please input tip index y: ").strip().replace('.', '')
        if x_input == 'q' or y_input == 'q':
            return None, None
        try:
            x = int(x_input)
            y = int(y_input)
            if x < 0 or y < 0:
                print("Invalid input. Please enter non-negative values.")
                continue
            else:
                if x >= 8: # TODO: check these!
                    print("Invalid input. Tip index x must be less than 8.")
                    continue
                if y >= 12:
                    print("Invalid input. Tip index y must be less than 12.")
                    continue
            return x, y
        except ValueError:
            print("Invalid input. Please enter numeric values.")

def get_liquid_coords():
    while True:
        print("Enter 'q' to quit.")
        x_input = input("Please input liquid bottle index x: ").strip().replace('.', '')
        y_input = input("Please input liquid bottle index y: ").strip().replace('.', '')
        if x_input == 'q' or y_input == 'q':
            return None, None
        try:
            x = int(x_input)
            y = int(y_input)
            if x < 0 or y < 0:
                print("Invalid input. Please enter non-negative values.")
                continue
            else:
                if x >= 4:
                    print("Invalid input. Liquid bottle index x must be less than 4.")
                    continue
                if y >= 4:
                    print("Invalid input. Liquid bottle index y must be less than 4.")
                    continue
            return x, y
        except ValueError:
            print("Invalid input. Please enter numeric values.")

def get_volume():
    """Ensure that the user inputs a valid positive integer for volume."""
    while True:
        print("Enter 'q' to quit.")
        volume_input = input("Please input volume (positive integer): ").strip()
        if volume_input == 'q':
            return None
        try:
            volume = int(volume_input)
            if volume > 0 and volume <= MAX_PIPETTE_VOLUME:
                return volume
            else:
                print(f"Invalid input. Volume must be a positive integer between 1 and {MAX_PIPETTE_VOLUME}.")
        except ValueError:
            print("Invalid input. Please enter a positive integer for volume.")

def liquid_robot_command_loop(liquidRobot: LiquidRobot):
    prompt = """Press [Enter] to quit,
[0] to home the robot,
[M] to drive to tip case/liquid case,
[G] to get tip at tipcase (x,y),
[A] to get liquid at liquid case (x,y) with volume,
[D] to return tip to tipcase (x,y),
[R] to return liquid to liquidcase(x,y),
[J] to dispense liquid with volume to the post.
[S] to move to the assembly post.
[Z] to enter manual positioning mode.
[T] to manually adjust tip-case corner XY positions (applies to up and down corners).
[P] to reload MG400 positions from the config file.
:> 
"""
    try:
        while True:
            input_str = input(prompt).strip().upper()
            if input_str == "":
                break
            elif input_str == "Z":
                manual_position_loop(liquidRobot)
            elif input_str == "T":
                liquidRobot.MG400.manual_adjust_tip_up_positions()
            elif input_str == "0":
                liquidRobot.MG400.move_home()
            elif input_str == "M":
                choice = input("Please select which case to go (tip/liquid):")
                if choice == "tip":
                    x, y = get_tip_coords()
                    if x is not None and y is not None:
                        liquidRobot.MG400.move_to_tip_case(x, y)
                elif choice == "liquid":
                    x, y = get_liquid_coords()
                    if x is not None and y is not None:
                        liquidRobot.MG400.move_to_liquid(x, y)
                else:
                    print("Invalid choice!")
            elif input_str == "G":
                x, y = get_tip_coords()
                if x is not None and y is not None:
                    liquidRobot.MG400.get_tip(x, y)
            elif input_str == "D":
                x, y = get_tip_coords()
                if x is not None and y is not None:
                    liquidRobot.MG400.drop_tip(x, y)
            elif input_str == "R":
                x, y = get_liquid_coords()
                if x is not None and y is not None:
                    liquidRobot.MG400.return_liquid(x, y)
            elif input_str == "J":
                volume = get_volume()
                if volume is not None:
                    liquidRobot.MG400.add_liquid_to_post(volume)
            elif input_str == "S":
                liquidRobot.MG400.move_to_assemble_post()
            elif input_str == "A":
<<<<<<< HEAD
                x, y = get_liquid_coords()
                if x is not None and y is not None:
                    volume = get_volume()
                    if volume is not None:
                        liquidRobot.MG400.get_liquid(x, y, volume)
=======
                x = int(input("Please input liquid bottle index x:").strip())
                y = int(input("Please input liquid bottle index y:").strip())
                volume = float(input("Please input volume:").strip())
                liquidRobot.MG400.get_liquid(x, y, volume)
>>>>>>> 057afcf6ddaded7378307362c59cc0f9964c62b4
            elif input_str == "P":
                liquidRobot.MG400.parse_position_file()
                print("Reloaded MG400 positions from the configuration file.")
            else:
                print("Invalid input. Please enter a valid option.")
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    finally:
        #liquidRobot.disconnect()
        #print("MG400 disconnected safely.")
        pass # the above lines were causing errors when the liquid robot menu was used 
             # before assembly: there isn't a provision to re-connect to the liquid robot.


def liquid_robot_example():
    liquid_robot = LiquidRobot(ip="192.168.0.107")
    ok = liquid_robot.initialize_robot()
    if not ok:
        print("Failed to initialize the Liquid Robot, program aborted!")
        exit()
    liquid_robot_command_loop(liquid_robot)
    liquid_robot.disconnect()
    print("MG400 disconnected safely.")


def main():
    rclpy.init()
    liquid_robot_example()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
