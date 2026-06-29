The following provides a more detailed guide to starting up BatteryLab. If there is a point of confusion or ambiguity, please revise this guide as-needed to help future users. Thank you! 

# Log in
- Log into the main system (```rasp5-hobbs```). The passphrase for the main user (Yuanjian) is "chibueze". 
- After logging in, briefly review the recent outputs of any command prompts for any unusual errors that need to be addressed.
- Visually inspect the robots for errored states. Do any of the robots appear to have collided with something, or appear mid-motion? Have the emergency stop buttons been pressed? If so, attempt to safely resolve these states before continuing (see other troubleshooting guides).
- Confirm the two Meca500 robots are in [monitor mode](Meca500_arms.md#connecting-to-the-robots-through-the-web-interface) using the web interface

# Hardware activation
Here, you'll activate the subroutines responsible for managing commands to each individual robot. As a note, the ```ssh``` commands below will only work as-given when used on ```rasp5-hobbs```, as the system names are aliases configured on that system.

- Connect to ```rasp4``` using the command ```ssh rasp4``` in a new terminal prompt. On this system, run the command
```bash
ros2 launch battery_lab_bringup rail_rasp.launch.py
```
- Connect to ```rasp5``` using the command ```ssh rasp5``` in a new terminal prompt. On this system, run the command 
```bash
ros2 launch battery_lab_bringup board_rasp.launch.py
```
- In a new terminal prompt, run the command
```bash
ros2 launch battery_lab_bringup out_rasp.launch.py
```
- Finally, to activate the system as a whole, run the command
```bash
ros2 run assembly_robot app
```
# Startup
When starting up, the sartorius liquid dispenser will activate (you'll hear some clicking noises) and the crimper robot will perform a test move. Once each system has been activated and connected, you'll be prompted to accept a component config file:
- The numbers displayed for each component are the position index of where BatteryLab anticipates the next available component to be. As a note, the indexing is not intuitive: each tray of 64 components is divided into 4 subsections (lower-left, lower-right, upper-left, upper-right), and components are exhaustively used from each subsection in that order. They are removed from a subsection columnwise. If you've refilled each component tray, for example, you'd want NOT to accept the previous component config file to reset the counters to ```1```. 

# Assembly
BatteryLab uses an internal representation of electrolytes and battery electrolyte recipes. The main BatteryLab menu has provisions for managing electrolytes, pipette tips, and recipes. 
- Whenever electrolyte vials are filled with a new component, cleaned, or refilled, the electrolyte manager should be used to update the system's knowledge of what compounds are where. Each electrolyte is represented as:
    - ```name```: a user-readable name for the electrolyte
    - ```volume```: the total available volume (in uL)
    - ```v```: a dictionary of component:volume fraction ratios. For example, {"water":0.25, "propylene glycol":0.75} would be a 25 vol% mixture of water in propylene glyol
    - ```s```: a dictionary of salt:molarity values. For example, {"NaCl":0.1, "ZnSO4":0.2} would indicate 0.1 molar NaCl and 0.2 molar ZnSO4. 
    - ```a```: a dictionary of additives:molarity values similar to '```s```'. ```a``` and ```s``` are treated interchangeably in the solver (i.e., specifying 1 molar ZnSO4 in both dictionaries would be equivalent to specifying 2 molar ZnSO4 in either dictionary)
    - ```local_smiles```: a dictionary matching components to manually inputted SMILES strings. If these are not provided, the code will attempt to query PubChem to find SMILES to use as unique component representations
    - ```use_pubchem```: a boolean indicating whether PubChem should be queried if a substance's SMILES isn't provided
- Whenever pipette tips are cleaned or replaced, the pipette tip manager should be used to update the digital representation of the tip rack. If needed, the LiquidRobot interface can be used to 'point' to specific pipette tips to clear up which index corresponds to which position
- Recipes can be created individually using BatteryLab's menu. This is somewhat tedious: a possible alternative is to use an LLM to create recipe files from natural language or a tabular Design-of-Experiment matrix.

Once a recipe or set of recipes has been loaded in using the dedicated menu option, there are options to simulate the recipe using text only (display the steps the liquid robot will take), "mime" the electrolyte dispensing motions (show those steps without actually aspirating/dispensing any electrolyte), or assemble the loaded recipes.