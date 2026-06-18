# Overview
The MG400 is the robot used to handled liquids. It has a Sartorius liquid dispensing module attached to the end of its arm: the two operate independently, managed by ROS2. The unit has a designated [webpage](https://www.dobot-robots.com/products/desktop-four-axis/mg400.html) with their overview of the system and, importantly, a FAQ section that contains the user manual and the control software (DobotStudio Pro v2.8.3.0). At the time of this writing, the most up-to-date version of DobotStudio is NOT compatible with the MG400. 

Please consult the user manual for detailed information about the system. Most immediately useful is perhaps Table 3.1 which provides the key for the system's indicator light's meanings.

Additionally, make note of the location of the Emergency Stop button. Pressing this button will immediately stop the system's motion. Afterwards, a full reboot is necessary to continue.

## Manual "teaching" mode
For ease in programming new positions and for removing the robot from errored positions, the MG400 comes with a manual arm movement mode. There is a white button on the forearm of the robot labeled with "Unlock". To activate manual mode, 

1. Grab the underside of the arm to support it once the motors disengage
2. Press and hold the "Unlock" button for ~5 seconds, then release it. The arm should disengage, allow you to move it freely. 
3. Once the robot is in the desired position, click the "Unlock" button to re-engage the motors.

## Connecting to MG400 through the control software
Typicaly, the MG400 is controlled through a python command interface. This is hidden from the user through the system's menus and existing programming. In the event of a collision, however, troubleshooting is beyond the scope of these menus. There is a *very* elementary python script in the home directory of BatteryLab (```clear400error.py```) that may be used to attempt intial diagnostics. 

Dobot's control software for the system (provided on the FAQ section of the webpage linked above) must be used for more granular information and control of the system. Unfortunately, the software is only available as an executable, so it cannot be used on Ubuntu machines (e.g., BatteryLab's Raspberry Pis). Any windows machine should work fine, though it must be connected to the same network as BatteryLab to find the system. 

Once the software has been installed, connect to the MG400 using its assigned IP address. This should be stored in any script that connects to the robot. After connecting, the program should prompt you to move out of TCP/IP mode and into online mode. This switch is necessary to control the robot through this software. If this option is not provided, navigate in the menu to Settings > Remote Control and use the dropdown there to select "Remote" mode.

NOTE: Before disconnecting, be sure to set the robot back to TCP/IP mode, or BatteryLab's scripts will not be able to control the system. 

## Troubleshooting after a collision
The system is equipped with collision detection, though it's unclear exactly under what load this mechanism is triggered. Further, when activated, the system's set response is currently to pause all operation. Considering these points and the potential for human injury or equipment damage, collisions should be avoided through carefully planned operation.

With the connection established, the alarm log should be accessible. Check the alarms for information regarding the cause of the error. These logs may have specific instructions for clearing the error. Otherwise, there will be a 'clear error' button at the bottom of the log list. After clearing the alarms, reduce the jog speed ("Global speed") using the slider in the top right of the interface. Then, use the virtual joysticks to attempt small moves to confirm the robot is working as expected. Slowly move it to its approximate home position.

## Specific Issues
### Noise when robot is activate
When the robot collides or otherwise errors, it sounds a somewhat quiet beeping alarm. Under certain circumstances, the robot will make a much louder 'yelling' noise. In the one instance this was encountered, this was apparently due to a mismatch between the programmed payload and the actual payload: the Sartorius module (~145 g) had been removed from the end of the arm. The system uses a user-provided payload weight to calibrate the internal servo motors, and this mismatch between expected and actual payload weight may have resulted in some kind of oscillations. Once the Sartorius module had been reinstalled, the loud 'whining' noise disappeared and the operation was quiet again. 