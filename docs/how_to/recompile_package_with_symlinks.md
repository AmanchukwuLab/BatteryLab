# Overview
Symlinks connect equivalent files in the build/install directories to their sources in the src directory. This way, files inside src (for that package, at least) may be modified, and the effects will transfer directly to the build/install directories that the robots actually access.

# Procedure
This uses the assembly_robot package as an example. In principle, this same could be done for any of the subpackages of the system. 
    1. Navigate to ros2_ws
    2. $rm -rf build/assembly_robot install/assembly_robot
    3. $colcon build --packages-select assembly_robot --symlink-install
        a. Installing with symlinks messess up some of the package metadata that importlib uses. We can resolve this by manually installing the metadata:
    4. Navigate to ros2_ws/src/assembly_robot
    5. $pip install -e .
        a. Note: this workaround was identified using ChatGPT5.1. Copied the master directory beforehand in case it broke anything; it has been working as expected.
