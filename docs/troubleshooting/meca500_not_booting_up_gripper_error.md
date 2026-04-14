# Overview
During the normal bootup sequence, the gripper test can time out. This has happened for the following reasons:

1. The robot itself isn't powered on

2. The gripper isn't activate (isn't talking with the robot for some reason) 

In the first case, power cycling the robot can fix the issue (press the power button on the robot's base). 

In the second case, the indicator light on the Mecademic Schunk gripper module will be flashing green: it should be solid if everything is working expectedly. If flashing, try power cycling the robot itself as described above. If this doesn't work, try pressing the button just underneath the Schunk indicator light. 
