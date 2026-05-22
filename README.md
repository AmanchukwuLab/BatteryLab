# BatteryLab

This system is a semi-autonomous laboratory workstation for manufacturing CR2032 coin-cell batteries, aimed at accelerating the process of discovering/testing new electrolytes. It uses 2 robotic arms, a liquid dispensing module, a linear rail, a number of 3D printed parts, and several cameras to achieve this end.

<figure>
  <img
  src="figures/LabOverview.png"
  alt="The BatteryLab Design">
  <figcaption>Figure 1. The physical design of the autonomous BatteryLab</figcaption>
</figure>

## Getting Started

> We assume that the hardware has been set up properly as illustrated in Figure 1. We will address the hardware requirement in the next section for users that want to build the system from scratch.

The code base can be separated to two parts:

1. The `BatteryLab` directory, which contains code that directly controls the robot, suction system, linear rail, and all the utility functions that rely purely on Python. Users should create a virtual environment with `python -m venv lab_venv` to install the Python dependencies. Do not use conda environment because they work poorly with ROS 2.

2. The `ros2_ws` directory, which contains several ROS2 packages. ROS (Robot Operating System) is a set of software libraries, needed because we physically connect the cameras, linear rails, suction systems to different Raspberry Pis. They communicate with each other using ROS 2 services/topics. For instance, the assembly robot needs to use several cameras, the linear rail, and the suction system to pick & place battery components. The suction system and arm camera are moving with the robotic arm while the fixed camera and linear rail controller do not move with the robot. They are connected to different Raspberry Pis to avoid cable and pipe length problems.

### Installing and testing code dependencies

You can install the Python dependencies with the following commands.

```bash
python -m venv lab_venv
source lab_venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Then you can use `app.py` in the root folder to test each of the robot to ensure they work properly individually.

Ensure [ROS 2 Jazzy](https://docs.ros.org/en/jazzy/Installation.html) is properly installed in your system. To make things easier, we recommend installing Ubuntu 24.04 to all the Raspberry Pis. You should be able to build the packages using the following commands. Since we use the `cv_bridge` package to transfer image data among ROS 2 nodes, you may encounter a numpy compatibility issue as discussed in [known issues](./docs/known_issues/cv_bridge_incompatible_with_Numpy2.0.md)

```bash
source /opt/ros/jazzy/
cd ros2_ws
colcon build
```

You can ssh into each Raspberry Pi to launch each ROS 2 node or use the launch file we prepared for you.

> The launch file and the ROS 2 packages are still under development.

### Launching the system
Start all the necessary ROS 2 services by running the following commands on specified machines. Note that each of them should be run on different Raspberry Pis.

```bash
# on the Raspberry Pi mounted on the linear rail (rasp4):
ros2 launch battery_lab_bringup rail_rasp.launch.py
# on the Raspberry Pi mounted on the breadboard by the liquid dispenser (rasp5):
ros2 launch battery_lab_bringup board_rasp.launch.py
# on the Raspberry Pi mounted outside the main breadboard (rasp5-hobbs):
ros2 launch battery_lab_bringup out_rasp.launch.py
```

Then you can start controlling the whole battery lab on any machines that supports ROS 2 and in the same network.

```bash
# to control the assembly robot
ros2 run assembly_robot assembly_robot
# to control the liquid handling robot
ros2 run assembly_robot liquid_robot
# to control the crimper robot
ros2 run assembly_robot crimper_robot
```

Alternatively, you can run the general command-line app to run the whole assembly process with just one command.

```bash
ros2 run assembly_robot app
```

Within the app, you can:
- Press **[B]atch** to load a JSON recipes file and assemble a series of cells in sequence. The app will prompt for the file path.
- Press **[O]ne** to assemble a single battery.

Each assembled battery's record includes the recipe name and payload (stored as JSON) so the cell is linked to its formulation.

Example recipe file (for the [B]atch option):

```json
[
  {
    "recipe_name": "baseline_cell_01",
    "electrolyte_volume_ul": 50,
    "ingredients": [
      {"solution_name": "ZnSO4_1M_water", "volume_ul": 20},
      {"solution_name": "ZnCl2_1M_water", "volume_ul": 30}
    ]
  },
  {
    "recipe_name": "variant_cell_02",
    "electrolyte_volume_ul": 50,
    "ingredients": [
      {"solution_name": "ZnSO4_1M_water", "volume_ul": 25},
      {"solution_name": "ZnCl2_1M_water", "volume_ul": 25}
    ]
  }
]
```

We may eventually develop a web-based UI for easier control with a graphical interface.

## Hardware Requirements

We use the following hardware items. You do not need to use the identical items to achieve the same functionalities, but it would be easy to set up and apply our code if you use the same hardware.

- 2 Mecademic [Meca500](https://www.mecademic.com/meca500-industrial-robot/) robotic arms and 2 [MEGP-25E](https://www.mecademic.com/product/megp-25e-electric-parallel-gripper/) grippers.
- 1 [Dobot MG400](https://www.dobot-robots.com/products/desktop-four-axis/mg400.html) robotic arm.
- 1 1500mm Zaber linear rail [X-LRT1500BL-E08C](https://www.zaber.com/products/linear-stages/X-LRT-EC/specs?part=X-LRT1500BL-E08C).
- 1 [Sartorius 1-ch 200 $\mu l$](https://shop.sartorius.com/us/p/rline-1-ch-200-l-dispensing-module/710993) rLine dispensing module.
- 2 Newport optical breadboards [M-PG-23-2-ML](https://www.newport.com/p/M-PG-23-2-ML).
- 1 DIY [suction system](https://www.aliexpress.us/item/3256802124499190.html?spm=a2g0o.order_list.order_list_main.5.77f21802SE7IHi&gatewayAdapt=glo2usa).
- 2 Raspberry Pi 5s and 1 Raspberry Pi 4.
- 1 [TOB-DF-160](https://www.tobmachine.com/coin-cell-crimping-machine_c134?gad_source=1&gclid=Cj0KCQjwrKu2BhDkARIsAD7GBov9F47aTY1ZMRAuWiKtbsL2JQtdZlmeonXlnT11z4B-JgYZ6LxH1a0aAs9AEALw_wcB) Battery Crimper.
- Several 3D printable parts.

### The Assembly Robot

The assembly robot is a Meca500 on the linear rail. We used a 3D-printed adaptor to mount a Raspberry Pi on the Zaber AP257-ENG4299 adaptor plate. The suction system can be mounted on top of the Raspberry Pi. There is a 8MP Arducam mounted to the MEGP-25 gripper. The customized gripper has two ending effects: (1) a two-pronged gripper to pick up the spring; (2) a suction cup to pick up the other battery components.

<figure>
  <img
  src="figures/assembly_robot.png"
  alt="The Assembly Robot">
  <figcaption>Figure 2. The design of the assembly robot.</figcaption>
</figure>

### The Liquid Handling Robot

The liquid handling robot is a Dobot MG400. We mount the Sartorius liquid dispening module to the flange with a customized adaptor. The robot needs adaptors to be mounted to the optical breadboard: the base has holes with M5 threads, and we designed 4 M5-M6 holders to mount it safely to the breadboard.

<figure>
  <img
  src="figures/liquid_robot.png"
  alt="The Liquid Handling Robot">
  <figcaption>Figure 3. The design of the liquid handling robot.</figcaption>
</figure>

### The Crimping & Storage Robot

We use a second Meca500 to move the assembled battery to a crimper and then back to the storage post. The gripper arm is 3D printed. We also need a electronic crimper to the right of the robotic arm, which is not illustrated in the 3D design.

<figure>
  <img
  src="figures/crimper_robot.png"
  alt="The Crimping & Storage Robot">
  <figcaption>Figure 4. The design of the crimping & storage robot.</figcaption>
</figure>

## Documentation
Further documentation (including troubleshooting, known issues, and future aims) can be found in the `docs` subfolder.
