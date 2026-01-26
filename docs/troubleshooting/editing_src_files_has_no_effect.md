Issue: editing a file somewhere inside the src directory has no effect on system operation. 
First observed: when trying to adjust the height of a component above the lookup camera to be better in-focus.
 
Conclusion: the src directory isn't accessed during runtime. This whole system is compiled from src: when first pulled from GitHub, the package only has ros2_ws/src. In ros2_ws, one then runs "$colcon build" to build and install the packages, of which assembly_robot is one. One could edit the equivalent files inside build a/o install, but these changes would not persist when uploading the directory to GitHub, thus not affecting any future versions of the system.

Solution:
- Most robust: implement changes in src, push changes to GitHub, recompile.
- Most practical: recompile the relevant individual package only and enable symlinks during this reinstall. Symlinks connect  equivalent files in the build/install directories to their sources in the src directory. This way, files inside src (for that package, at least) may be modified, and the effects will transfer directly to the build/install directories that the robots actually access. A how-to document has been created.
