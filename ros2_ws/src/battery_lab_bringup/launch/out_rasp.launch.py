import os
from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable, DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import PythonExpression
from pathlib import Path
from launch.actions import ExecuteProcess

def generate_launch_description():

    set_ros_domain_id = SetEnvironmentVariable("ROS_DOMAIN_ID", "42")
    
    # This isn't the most elegant, but it should work to force manual focus.  
    set_camera_hardware = ExecuteProcess(
        cmd=[[
            'v4l2-ctl -d /dev/video0 ',
            '--set-ctrl=white_balance_automatic=1 ',
            '--set-ctrl=focus_automatic_continuous=0 ',
            '--set-ctrl=focus_absolute=100'        
        ]],
        shell=True
    )
    return LaunchDescription(
        [
            set_ros_domain_id,
            # SetEnvironmentVariable('PATH', os.path.join(venv_path, 'bin') + ':' + os.environ['PATH']),
            # # Set the PYTHONPATH to include the virtual environment's site-packages
            # SetEnvironmentVariable('PYTHONPATH', os.path.join(venv_path, 'lib', 'python3.12', 'site-packages')),
            # Node(
            #     package='camera_service',
            #     executable='camera_server',
            #     name='tower_camera_server',
            #     output='screen',
            #     parameters=[
            #         {'service_name': '/batterylab/tower_camera'}
            #     ]
            # ),
            Node(
                package="usb_cam",
                executable="usb_cam_node_exe",
                name="tower_usb_cam",
                output="screen",
                parameters=[
                    {
                        "video_device": "/dev/video0",
                        "camera_name": "my_tower_cam",
                        "image_width": 640,
                        "image_height": 480,
                        "framerate": 30.0,
                        "pixel_format": "yuyv",
                        
                        "extra_control_names": [
                            "white_balance_automatic", 
                            "focus_automatic_continuous"
                        ],
                        # (0 = False/Manual, 1 = True/Auto)
                        "extra_control_values": [
                            1, # white_balance_automatic: Auto
                            0  # focus_automatic_continuous: Manual (Unlocks focus_absolute)
                        ],
                        "focus_absolute": 200,
                    }
                ],
                remappings=[("/image_raw", "/camera/tower_camera")],
            ),
            set_camera_hardware,
        ]
    )
