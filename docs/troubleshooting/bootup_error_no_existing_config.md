# Overview
When booting up the system, the following error is provided: *"You don't have an existing config, will start from scratch"*.

**First observed:** recompiling the assembly_robot package to add symlinks for modification matching between src, build, and install directories.

Code traceback:
    1. src/assembly_robot/assembly_robot/Assembly_robot.py prints the error message if not self.counter_file.exists()
    2. counter_file is grabbed from assembly_robot/yaml/assembly_counter.yaml
        a. Before recompiling assembly_robot, I made a copy of the whole BatteryLab directory. Checking there for a backup.

Conclusion: original config file is preserved in BatteryLabCopy under ros2_ws/install/assembly_robot/share/assembly_robot/yaml

Solution: copied the file to the equivalent directory in the main BatteryLab repo.

