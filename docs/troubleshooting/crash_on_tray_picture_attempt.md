# Overview
The main BatteryLab app crashes when requested to take a photo of one of the component trays, displaying an error like "unrecognized image encoder = []"

- This error occurred after adjusting some cables when replacing a 3D printed bracket. 

# Fix
All BatteryLab subprocesses need to be restarted.
1. Exit the main BatteryLab application if it hasn't already crashed closed 
2. End the three subprocesses (e.g., out_rasp.launch.py) using Ctrl-C on each ssh'd RPi terminal
3. Restart BatteryLab as normal 
