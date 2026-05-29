# Overview
Occasionally, if BatteryLab is left active (but not running anything, i.e., the camera is not actively capturing images), it will time out for some reason. In this state, any requests to the camera for an image capture will error. 

This error was first identified when the system was left active during a substantial code overhaul (unsure exactly how long). 

## Prevention
Until the source of the issue can be resolved (some way to prevent timeout):
1) Do not leave the system active in an idle state for long periods of time
2) If the system was left unattended for a while, either
    a) Restart the system before proceding
    b) Test the camera manually using the Assembly Robot submenu 
