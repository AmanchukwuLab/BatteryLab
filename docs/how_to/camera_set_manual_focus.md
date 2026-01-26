# Overview
The lookup camera we use employs auto-focus by default. This is great for videocalling, but not for taking focused images of small components in a larger image field. Because the location of each component is fixed, we can manually set the focus ourselves. This is done using the ```v4l2``` package (video 4 linux 2.0). 

# Commands
1. Show all devices on the current system
    - $ v4l2-ctl --list-devices
2. Show available controls on a given device (/dev/video0 in this case). Note: if "focus_absolute" isn't present, the camera likely isn't capable of manual focus. 
    - Note what the auto focus parameter is called (e.g., 'focus_auto', or 'focus_automatic_continuous', or something else). 
    - Note the acceptable range of 'focus_absolute'. 
    - $ v4l2-ctl -d /dev/video0 --all
3. Deactivate the auto focus setting (using the name noted in step 2)
    - $ v4l2-ctl -d /dev/video0 --set-ctrl=focus_automatic_continuous=0
4. Set focus to some value within the acceptable range
    - $ v4l2-ctl -d /dev/video0 --set-ctrl=focus_absolute=50

# Notes on our system
For the Arducam (lookup camera):
- The auto-focus parameter is called "focus_automatic_continous"
- The focus_absolute parameter has a range of [1, 1023]. 
