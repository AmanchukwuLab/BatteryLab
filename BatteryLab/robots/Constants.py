from enum import Enum
from pydantic import BaseModel
from typing import List


class RobotTool(Enum):
    GRIPPER = 1
    SUCTION = 2
    CAMERA = 3


class Meca500RobotConstants(BaseModel):
    GRIP_F: int = 10
    GRIP_VEL: int = 20
    L_VEL: int = 10
    J_VEL: int = 10
    TCP_GP: List[float] = [60.0, 0, 0, 0, 0, 0]
    TCP_SK: List[float] = [0, 0, 0, 0, 0, 0]
    TCP_CA: List[float] = [0, 0, 0, 0, 0, 0]
    HOME_GP_J: List[float] = [0, 0, 0, 0, 0, 0]
    HOME_SK_J: List[float] = [0, 0, 0, 0, 0, 0]
    HOME_CA_J: List[float] = [0, 0, 0, 0, 0, 0]


class Components(Enum):
    CathodeCase = 1
    Cathode = 2
    Spacer = 3
    Anode = 4
    Washer = 5
    Separator = 6
    SpacerExtra = 7
    AnodeCase = 8


class AssemblySteps(Enum):
    Grab = 1
    Drop = 2
    Press = 3
    Retrieve = 4
    Store = 5


class ComponentProperty:
    def __init__(self):
        self.shape: List[int] = [4, 4]  # the grabPo shape
        self.railPo: List[float] = None
        self.dropPo: List[float] = None
        self.grabPo: List[List[float]] = None


class AssemblyRobotCameraConstants:
    def __init__(self):
        self.HOME_J: List[float] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.TRF: List[float] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.RobotPose: List[float] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.AnodeCase: dict = {}
        self.Anode: dict = {}
        self.Separator: dict = {}
        self.Cathode: dict = {}
        self.Spacer: dict = {}
        self.SpacerExtra: dict = {}
        self.Washer: dict = {}
        self.CathodeCase: dict = {}


class CrimperRobotConstants(BaseModel):
    TRF: List[float] = [20, 0, 95, 0, 0, 0]
    Home: List[float] = [-60, 0, 0, 0, 30, 0]
    PostReadyPose: List[float] = [0, 0, 0, 0, 0, 0]
    PostDownPose: List[float] = [0, 0, 0, 0, 0, 0]
    GrabReadyPose: List[float] = [0, 0, 0, 0, 0, 0]
    GrabbedUpPose: List[float] = [0, 0, 0, 0, 0, 0]
    PhotoCheckPreparePose: List[float] = [0, 0, 0, 0, 0, 0]
    PhotoCheckPose: List[float] = [0, 0, 0, 0, 0, 0]
    CrimperReadyToOperatePose: List[float] = [0, 0, 0, 0, 0, 0]
    CrimperDropPose: List[float] = [0, 0, 0, 0, 0, 0]
    CrimperReadyToPickPose: List[float] = [0, 0, 0, 0, 0, 0]
    CrimperPickPressPose: List[float] = [0, 0, 0, 0, 0, 0]
    CrimperPickPose: List[float] = [0, 0, 0, 0, 0, 0]
    CrimperPickedUpPose: List[float] = [0, 0, 0, 0, 0, 0]
    StorageReadyPose: List[float] = [0, 0, 0, 0, 0, 0]
    StorageDropPose: List[float] = [0, 0, 0, 0, 0, 0]


class AssemblyRobotConstants:
    def __init__(self):
        self.HOME_J = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.TRF = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.GripperTRF = [60, 0, 0, 0, 0, 0]
        self.POST_C_SK_PO: List[float] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.POST_C_GRIPPER_PO: List[float] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.POST_RAIL_LOCATION: float = 100.0
        self.LOOKUP_CAM_SK_PO: List[float] = [0, 0, 0, 0, 0, 0]
        self.LOOKUP_CAM_GRIPPER_PO: List[float] = [0, 0, 0, 0, 0, 0]
        self.LOOKUP_CAM_RAIL_LOCATION: float = 100.0
        self.CathodeCase: dict = {}
        self.Cathode: dict = {}
        self.Separator: dict = {}
        self.Anode: dict = {}
        self.Washer: dict = {}
        self.Spacer: dict = {}
        self.SpacerExtra: dict = {}
        self.AnodeCase: dict = {}


class StepCorrectionConfig(BaseModel):
    name: str
    diam: float
    ksize: int
    minDist: int
    param1: int
    param2: int
    minR: int
    maxR: int


class AutoCorrectionConfig:
    def __init__(self):
        self.CAM_PORT_BOTM: int = 1
        self.CAM_PORT_TOP: int = 2
        ######## Last manually tuned by JWP on 3/18/26
        # Anode: pretty touchy due to uneven reflections. Small radius range helps
        self.Anode_Drop = StepCorrectionConfig(
            name="Anode_Drop",
            diam=15,
            ksize=5,
            minDist=150,
            param1=150,
            param2=20,
            minR=50,
            maxR=60,
        )
        self.Anode_Grab = StepCorrectionConfig(
            name="Anode_Grab",
            diam=15,
            ksize=5,
            minDist=150,
            param1=150,
            param2=20,
            minR=50,
            maxR=60,
        )
        # Cathode: somewhat sensitive. A bit better than anode due to more even reflections
        self.Cathode_Drop = StepCorrectionConfig(
            name="Cathode_Drop",
            diam=14,
            ksize=5,
            minDist=150,
            param1=150,
            param2=22,
            minR=40,
            maxR=50,
        )
        self.Cathode_Grab = StepCorrectionConfig(
            name="Cathode_Grab",
            diam=14,
            ksize=5,
            minDist=150,
            param1=150,
            param2=30,
            minR=40,
            maxR=50,
        )
        # Separator is finnicky due to smoother, sensitive reflection gradients. Might take more tuning.
        self.Separator_Drop = StepCorrectionConfig(
            name="Separator_Drop",
            diam=15.5,
            ksize=5,
            minDist=150,
            param1=130,
            param2=40,
            minR=60,
            maxR=80,
        )
        self.Separator_Grab = StepCorrectionConfig(
            name="Separator_Grab",
            diam=15.5,
            ksize=5,
            minDist=150,
            param1=130,
            param2=40,
            minR=60,
            maxR=80,
        )
        # Spacer is very stable (highly rigid, reflective)
        # NOTE: Anode_Spacer and Cathode_Spacer are never called in the code (ex. assemblyrobot app.py calls
        # Spacer and SpacerExtra) Anode_Spacer and Cathode_Spacer would be more specific names -- it might be
        # better to use those names instead in the future.
        self.Anode_Spacer_Drop = StepCorrectionConfig(
            name="Anode_Spacer",
            diam=15.5,
            ksize=5,
            minDist=150,
            param1=330,
            param2=34,
            minR=50,
            maxR=70,
        )
        self.Cathode_Spacer_Drop = StepCorrectionConfig(
            name="Cathode_Spacer",
            diam=15.5,
            ksize=5,
            minDist=150,
            param1=330,
            param2=34,
            minR=50,
            maxR=70,
        )
        # generic Spacer drop config used by Components.Spacer_Drop.
        self.Spacer_Drop = StepCorrectionConfig(
            name="Spacer_Drop",
            diam=15.5,
            ksize=5,
            minDist=150,
            param1=330,
            param2=34,
            minR=50,
            maxR=70,
        )
        # Optional: SpacerExtra (uses same initial tuning as Spacer)
        self.SpacerExtra_Drop = StepCorrectionConfig(
            name="SpacerExtra_Drop",
            diam=15.5,
            ksize=5,
            minDist=150,
            param1=330,
            param2=34,
            minR=50,
            maxR=70,
        )
        # Cathode case detection is very stable.
        self.CathodeCase_Drop = StepCorrectionConfig(
            name="Cathode_Case",
            diam=19.3,
            ksize=5,
            minDist=150,
            param1=280,
            param2=40,
            minR=60,
            maxR=90,
        )
        # Anode case detection is very stable.
        self.AnodeCase_Drop = StepCorrectionConfig(
            name="Anode_Case",
            diam=19.3,
            ksize=5,
            minDist=150,
            param1=50,
            param2=65,
            minR=50,
            maxR=80,
        )
        # Washer has a wide range to allow detection of both outer and inner circles.
        # It might be better to tune it more finely for one or the other. Param1 and Param2
        # are currently tuned for detecting the outer circle.
        self.Washer_Drop = StepCorrectionConfig(
            name="Washer",
            diam=15.5,
            ksize=5,
            minDist=150,
            param1=100,
            param2=40,
            minR=20,
            maxR=80,
        )
        # Global default (legacy "object_config" replacement)
        self.Reference = StepCorrectionConfig(
            name="Default",
            diam=2,
            ksize=5,
            minDist=150,
            param1=300,
            param2=30,
            minR=45,
            maxR=80,
        )
        # Global default for detecting the suction cup (legacy "suction_config")
        self.Suction_Cup = StepCorrectionConfig(
            name="Suction_Cup",
            diam=4,
            ksize=5,
            minDist=500,
            param1=95,
            param2=35,
            minR=30,
            maxR=50,
        )
        # Extra placeholder
        self.Customize = StepCorrectionConfig(
            name="Customize",
            diam=2,
            ksize=5,
            minDist=100,
            param1=100,
            param2=10,
            minR=110,
            maxR=115,
        )
        # Optional: quick sanity check – every component used during Drop should have a config
        required_drop_names = [f"{c.name}_Drop" for c in Components]
        missing = [name for name in required_drop_names if not hasattr(self, name)]
        if missing:
            # keep this non-fatal but visible
            print(
                f"[AutoCorrectionConfig] WARNING: missing Drop configs for: {missing}"
            )
