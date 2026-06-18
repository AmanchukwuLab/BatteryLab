# Overview
Two of the three main robots used in BatteryLab are Mecademic Meca500 robot arms. These are small, 6-axis robots that can be operated both through a web-based interface as well as a python API. 

## Connecting to the robots through the web interface
Each Meca500 robot has been configured with a static IP address on the local network. The RailRobot is ```192.168.0.100```, and the CrimperRobot is ```192.168.0.101```. To connect to each robot, enter its respective IP address into the address bar of a web browser that is connected through the same network. This will launch Mecademic's proprietary robot interface. 

The robots first need to be powered on. Once the robot has been physically activated (power button on the base of the robot), they must be digitally activated. In the top-right of the web interface, activate the robot using the power button shown there. 

Once activated, the robot can be in either "Monitoring" or "Control" mode. If the robot is set to the latter, the web interface may be used to control the robot's joints manually. 

> CAUTION: especially at higher jogging speeds, the robot can move unpredictably based on user commands. Ensure sufficient distance between the robot and users, and be cautious of potential equipment damage from these sudden movements.

For BatteryLab to be capable of controlling the robots, they must be set to ```Monitoring``` mode. If both robots are not in this setting, BatteryLab's control program will not launch properly and will provide an error asking if both machines are in Monitor mode. 


## Other troubleshooting

### Gripper not booting up properly
During the normal bootup sequence, the connection to each gripper attachment on each robot is tested. This test can time out, which may be caused by one of the following reasons:

1. The robot itself isn't powered on

2. The gripper isn't activated (isn't talking with the robot for some reason) 

In the first case, power cycling the robot can fix the issue (press the power button on the robot's base). 

In the second case, the indicator light on the Mecademic Schunk gripper module will be flashing green: it should be solid if everything is working expectedly. If flashing, try power cycling the robot itself as described above. If this doesn't work, try pressing the button just underneath the Schunk indicator light. 
