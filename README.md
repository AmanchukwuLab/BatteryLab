# BatteryLab

This system is a semi-autonomous laboratory workstation for manufacturing CR2032 coin-cell batteries, aimed at accelerating the process of discovering/testing new electrolytes. It uses 2 robotic arms, a liquid dispensing module, a linear rail, a number of 3D printed parts, and several cameras to achieve this end.

<figure>
  <img
  src="figures/LabOverview.png"
  alt="The BatteryLab Design">
  <figcaption>Figure 1. The physical design of BatteryLab</figcaption>
</figure>

The code included in this directory includes capabilities for interfacing with each robot individually (e.g., test or adjust individual functions) and the whole system in concert, including the assembly of a series of coin cells with unique electrolyte recipes. Additionally, an electrolyte planner module is included. This now uses solvency-style `Electrolyte` definitions for recipes and stock identities, evaluates a batch of recipes' feasibility, and manages tip usage to avoid contamination. Further details about this module can be found in its [dedicated README](BatteryLab_files\BatteryLab\BatteryLab\electrolyte_planner\README.md).

## Hardware Requirements

The following hardware has been employed. While identical items are not necessarily essential to achieve the same overall functionality, the system will be easiest to set up and replicate with the same hardware.

- 2 Mecademic [Meca500](https://www.mecademic.com/meca500-industrial-robot/) robotic arms and 2 [MEGP-25E](https://www.mecademic.com/product/megp-25e-electric-parallel-gripper/) grippers
- 1 1500mm Zaber linear rail [X-LRT1500BL-E08C](https://www.zaber.com/products/linear-stages/X-LRT-EC/specs?part=X-LRT1500BL-E08C)
- 1 [Dobot MG400](https://www.dobot-robots.com/products/desktop-four-axis/mg400.html) robotic arm
- 1 [Sartorius 1-ch 200 $\mu l$](https://shop.sartorius.com/us/p/rline-1-ch-200-l-dispensing-module/710993) rLine dispensing module
- 2 Newport optical breadboards [M-PG-23-2-ML](https://www.newport.com/p/M-PG-23-2-ML)
- 1 DIY Raspberry Pi-compatible [suction cup system](https://www.aliexpress.us/item/3256802124499190.html?spm=a2g0o.order_list.order_list_main.5.77f21802SE7IHi&gatewayAdapt=glo2usa)
- 2 Raspberry Pi 5s and 1 Raspberry Pi 4
- 1 [TOB-DF-160](https://www.tobmachine.com/coin-cell-crimping-machine_c134?gad_source=1&gclid=Cj0KCQjwrKu2BhDkARIsAD7GBov9F47aTY1ZMRAuWiKtbsL2JQtdZlmeonXlnT11z4B-JgYZ6LxH1a0aAs9AEALw_wcB) Battery Crimper
- Several 3D printable parts (files included or linked)

### The Assembly Robot

The assembly robot is a Meca500 installed on the linear rail. We used a 3D-printed adaptor to mount a Raspberry Pi on the Zaber AP257-ENG4299 adaptor plate. The customized gripper has two endings: (1) a two-pronged gripper to pick up the spring, and (2) a suction cup to pick up the other battery components. The suction system can be mounted on top of the Raspberry Pi. There is a 8MP Arducam mounted to the MEGP-25 gripper, which will eventually be used to automatically detect the locations of available components in their trays.

<figure>
  <img
  src="figures/assembly_robot.png"
  alt="The Assembly Robot">
  <figcaption>Figure 2. The design of the assembly robot.</figcaption>
</figure>

### The Liquid Handling Robot

The liquid handling robot is a Dobot MG400. We mounted the Sartorius liquid dispening module to the optical breadboard flanges with a customized adaptor. The robot needs these adaptors because the base has holes with M5 rather than M6 threads.

<figure>
  <img
  src="figures/liquid_robot.png"
  alt="The Liquid Handling Robot">
  <figcaption>Figure 3. The design of the liquid handling robot.</figcaption>
</figure>

### The Crimping & Storage Robot

We use a second Meca500 to move the assembled battery from the assembly pedestal to a crimper and then back to a storage post. The gripper arm is 3D printed. We also need a electronic crimper to the right of the robotic arm, which is not illustrated in the 3D design.

<figure>
  <img
  src="figures/crimper_robot.png"
  alt="The Crimping & Storage Robot">
  <figcaption>Figure 4. The design of the crimping & storage robot.</figcaption>
</figure>

## Software Requirements

If you have not worked with GitHub or a Unix-type shell before, see the [guide posted in the ```docs``` folder](docs\Shell_and_GitHub_tutorial.md).

The codebase can be separated into two main parts:

1. The internal `BatteryLab` directory, which contains code that directly controls the robots, suction system, linear rail, and all the utility functions.

2. The `ros2_ws` directory, which contains several ROS2 packages. ROS (Robot Operating System) is a set of software libraries needed to coordinate robotic systems that are physically connected to different Raspberry Pis (the cameras, linear rails, suction systems, etc.). They communicate with each other using ROS2 services/topics. For instance, the assembly robot needs to use several cameras, the linear rail, and the suction system to pick & place battery components. The suction system and arm camera are moving with the robotic arm while the fixed camera and linear rail controller do not move with the robot. They are connected to different Raspberry Pis to avoid cable and pipe length problems. Details concerning the installation of ROS2 are provided below.

### Installing and testing code dependencies

To ensure compatibility with the existing code, we recommend installing Ubuntu 24.04 on each of the Raspberry Pis. Python should come pre-installed with Ubuntu; as of June 2026, our systems are running Python 3.12.3.

First, clone this (BatteryLab) repository into the local storage of each Raspberry Pi on the system. Users should then create a virtual environment manually to install the Python dependencies. A conda environment is not advised because they work poorly with ROS2. The virtual environment and necessary Python dependencies are installed using the following commands:

```bash
python -m venv lab_venv
source lab_venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Note that these commands must be run from inside the main BatteryLab directory so that ```requirements.txt``` can be found.

### Installing ROS2

Ensure [ROS2 Jazzy](https://docs.ros.org/en/jazzy/Installation.html) is properly installed in your system. You should be able to build the packages using the following commands:

```bash
source /opt/ros/jazzy/
cd ros2_ws
colcon build
```

Since we use the `cv_bridge` package to transfer image data among ROS2 nodes, you may encounter a numpy compatibility issue as discussed in [known issues](./docs/known_issues/cv_bridge_incompatible_with_Numpy2.0.md).

## Launching the system
<!--You can ssh into each Raspberry Pi to launch each ROS2 node or use the launch file we prepared for you.

> NOTE: The launch file and the ROS2 packages have not been fully developed-->

Start all the necessary ROS2 services by running the following commands on the specified Raspberry Pis. As a reminder, the systems can only talk with each other if they are connected through the same network. If you can't ```ssh``` between them, ROS2 likely can't pass information either.

```bash
# on the Raspberry Pi mounted on the linear rail ("rasp4" on our system):
ros2 launch battery_lab_bringup rail_rasp.launch.py

# on the Raspberry Pi mounted on the breadboard by the liquid dispenser ("rasp5" on our system):
ros2 launch battery_lab_bringup board_rasp.launch.py

# on the Raspberry Pi mounted outside the main breadboard ("rasp5-hobbs" on our system):
ros2 launch battery_lab_bringup out_rasp.launch.py
```

At this point, the following general command-line app manages the whole system with just one command and acts as a wrapper for individual robot command menus and the battery building process as a whole:

```bash
ros2 run assembly_robot app
```

### Preparing to assemble cells
Currently, materials for each of the 64 possible coin cells must be stocked manually. The default configuration includes a cathode case, spring/washer, spacer, cathode, separator, anode, spacer, and anode case.

Additionally, electrolytes must be stocked in the 16 available vials, and pipette tips must be loaded into the storage rack. As electrolytes are being stocked, their identities should be entered as solvency-style JSON objects with `name`, `volume`, `v`, `s`, and `a`. The interface for completing this process is available in `app.py`.


### Assembling cells
Once the materials have been stocked, the main ```app.py``` program allows you to:
- Press **[O]ne** to assemble a single demo battery. This will use a default "recipe" of 0uL of the substance in the vial at coordinate ```(x = 0, y = 0)```
- Press **[B]atch** to load a JSON recipes file and assemble a series of cells in sequence. The app will prompt for either a file path or the use of a GUI to select a file.

An example recipe file (for the [B]atch option) looks like this:

```json
[
  {
    "recipe_name": "baseline_cell_01",
    "target_electrolyte": {
      "name": "baseline_target",
      "volume": 0.05,
      "v": {"water": 0.5, "propylene glycol": 0.5}
    },
  }
]
```

Each assembled battery's record includes the recipe name and payload (stored as JSON) so the cell is linked to its formulation.

We may eventually develop a web-based UI for easier control with a graphical interface.

## Further Documentation
Further documentation (including troubleshooting, known issues, and how-to's) can be found in the [`docs`](docs/) subfolder. This includes an [ongoing work](docs/OngoingWork.md) file documenting proposed additions to the system.

## Acknowledgements
This system was based on the initial version of the ["AutoBASS" system](https://github.com/Helge-Stein-Group/AutoBASS) developed by Dr. Helge Stein's group at the Technical University of Munich. Some initial published works featuring the system include [Digital Discovery, 2024,3, 1342-1349](https://doi.org/10.1039/D4DD00002A) and [Digital Discovery, 2022,1, 755-762](https://doi.org/10.1039/D2DD00046F).

The construction of the [Amanchukwu Lab](https://amanchukwu.uchicago.edu/)'s version of that system was initially led by [Yuanjian Liu](https://github.com/legendperceptor/), including hardware development and initial codebase modifications. Later work by [Jared Porter](https://github.com/jwp91) focused on refining machine vision correction, electrolyte recipe management, as well as UI and hardware interface improvements.

<!--
Originally authored by Yuanjian Liu (~2024?)
Revised by Jared Porter (June 2026)
-->