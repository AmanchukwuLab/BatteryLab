# Overview
Both of the robot arms' positions are preprogrammed. These preprogrammed locations may be slightly adjusted using some machine vision component, but only by a small amount. If the positions need to be adjusted (e.g., redesigning the system's layout), the following notes apply. 


# Preliminary Note
Adjusting the robot arms' positions without caution can lead to collisions, potentially damaging equipment. To avoid this, some initial work is recommended:

- The robot arms' internal software handles the movement from position to position. This software is accessed through python functions that accept destination positions as arguments. Take a look at the documentation for this package, found [here](https://github.com/Mecademic/mecademicpy), for some examples.
- It is worthwhile to experiment with the robots' movement within the Mecademic software online before using the Python interface. See the relevant how_to page in this directory. 

# Procedure
This procedure uses the Assembly robot's lookup camera position as an example. The procedure for the crimper robot shold be very similar. 

1. Identify the driving python file. 
    - For the assembly robot, the main operation file is at ```ros2_ws/src/assembly_robot/assembly_robot/AssemblyRobot.py```. 
2. Locate the function that moves to the location we'd like to change.
    - For the lookup camera position, this is the take_a_lookup_photo() function
3. Inside this function, find where the location is specified. 
    - Inside the take_a_lookup_photo() function, the robot is given the command MovePos(robot_pos) 
4. Trace the position argument to where it is first imported. Note the path to the position file.
    - Towards the beginning of the file, the assemblyRobotConstants dictionary is created from position_file, which is at ```assembly_robot/yaml/well_positions.yaml```
5. Navigate to the positions file and modify the position with caution.
    - The safest way to do this is to identify the exact position you'd like to modify to by using the web interface. 
6. After modifying the position file, the system will need to be restarted for the change to take effect.
