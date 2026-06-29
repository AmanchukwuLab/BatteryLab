This page contains a running list of open problems or projects that would be worthwhile additions to BatteryLab. 

# Urgent
These issues are those hindering BatteryLab's accuracy or precision:

- Sartorius integer limitation
    - The sartorius (liquid pipetter) python module problematically rounds volumes to the nearest integer *silently*. The hardware specifications indicate, however, that the system is physically capable of 0.5 uL increments. There are two major issues to be addressed here:
        1. The module should be revised to allow 0.5 uL increments. This may require consulting user manuals for the system, revising the package's source code, then rebuilding it.
        2. When the volume is necessarily rounded to the nearest 0.5 uL increment, BatteryLab should be informed so the metadata for the assembled coin cell can be modified. In practice, this could look something like a volume-checking function within the sartorius python module that checks for non-0.5uL values, rounds them, then returns a flag with the actual dispensed volume. The BatteryLab metadata manager would then catch this flag and update the recorded recipe for the cell and inform the user that the composition had been adjusted to match hardware specifications. In short, the metadata for the assembled battery should contain both the requested recipe amounts as well as the *actual* recipe dispensed.

- Sartorius lower volume limitation
    - The sartorius (liquid pipetter) module is apparently limited to a minimum dispensing volume of 5uL. Similar to the integer limitation described immediately above, this will fail silently. This is problematic for recipes with trace components, i.e., additives or trace salts: if one recipe requested 2.4 uL of an additive and the next requested 2.6 uL of the same, the batteries would in truth have 0 and 5 uL of the additive, respectively. Worse, the records would falsely indicate 2.4 and 2.6 uL. There are a handful of issues to address:
        1. Verify that the module is factually incapable of reliably dispensing sub-5uL quantities of liquid.
        2. Determine how the sartorius python module currently handles sub-5uL quantities (if it does at all). 
        3. Similarly to the integer limitation above, BatteryLab should be informed during assembly if a volume below 5uL is requested. When this occurs, the metadata stored for that battery should be updated to contain the requested recipe as well as the *actual* recipe. 

- Possible vial volume redundancy
    - Note: this concerns the interaction between the [solvency module](../BatteryLab/solvency/) and the [electrolyte planner module](../BatteryLab/electrolyte_planner/).
    - The ```Electrolyte``` objects have a 'volume' attribute. The individual ```vial``` objects (containing Electrolyte objects as one attribute) also have a 'volume attribute'. The following questions should be clarified to ensure the system is running as expected:
        1. Are these two volumes internally forced to match somehow? If yes, this issue may be considered resolved. 
        2. If not (1), do some functions (e.g., digitially 'cleaning' vials, checking for recipe feasibility) use one volume while other functions use another? 
        3. If yes (2), this must be resolved so the digitally stored volume amounts are consistent. Once one or the other is selected as the "correct" volume, the other should be removed entirely to avoid confusion and redundancy.

# Quality-of-Life

These changes would be nice additions, but do not necessarily hinder BatteryLab's efficacy (roughly in priority order):

- Add an abort/cancel/pause function to gracefully exit battery assembly if needed
    - The exact behavior when canceling a job mid-assembly is untested, specifically the degree of metadata preservation. If a large batch of recipes is submitted and needs to be cancelled, the system should preserve the metadata of each assembled cell and note to the user at exactly which step the assembly process was stopped. 
    - This function could also be used to handle edge cases in which an error occurs during a large batch. If a non-critical error occurs somehow (e.g., camera times out), the system should provide a user prompt with such options as attempting to clear robot errors, re-homing robots in an order given by the user, resume the current cell, restart the current cell, or abort the process.
    - The overall goal here is to ==mitigate the frustration due to process errors as much and as safely as possible==.

- Use existing tray camera to detect battery component and pipette tip availability
    - Currently (June 2026), the system relies on a set of internal counters to know which battery components are available. The same is true for pipette tips. The assembly robot arm has a camera equipped for taking pictures of the component tray. Using a circle-detection algorithm (e.g., HoughCircles), it should be possible to detect which of the available 64 slots are filled for each component. This would require:
        1. Determining how to access the "look down" camera (existing unutilized interface? new interface?)
        2. Tuning HoughCircles (or other algorithm) for detecting up to 64 components at once in a given photo
        3. Testing reliability of component detection (error rate, lighting effects, etc.)
        4. Replacing the current component counter system

- Increasing robot speed
    - The linear rail's speed and each robot's jog speeds have been deliberately limited for safety during development. Once confidence in the system has been established, increasing the robots' speeds would easily reduce the amount of time to assemble a cell. 
    - NOTE: increasing the speed is only worthwhile if the system is not otherwise constrained by another step in the analysis process. Currently, the number of cells that can be analyzed is limited by the number of available testing channels in the lab: it doesn't make much sense to produce cells at a significantly faster rate than they can be tested. 

- Update ```electrolyte_planner``` module README file. This was originally created using gen-AI (GitHub Copilot) for the initial draft, but the code has changed substantially since that time. The information in that document is likely inaccurate or omissive. 

- Removing improper instances of ```print```
    - Certain of BatteryLab's functions ```print``` directly to the console rather than using the session logger. This is preferable for items that should not be stored after a session concludes (e.g., menu options, single-use robot control functions) but is bad practice for events during assembly that should be recorded. There may be scattered instances of the latter, which should be corrected to using the session logger.

- Dedicated recipe manager menu
    - There are currently options to manually create or select a recipe within BatteryLab's CLI. As the number of proposed and existing recipes increases, it may be useful to add a dedicated menu with more options (e.g., delete recipes, merge recipes, edit recipes, etc.)

<!--
Originally written by Jared Porter (June 2026)
-->