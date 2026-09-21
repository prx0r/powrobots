"""Core enums for POWRobots."""

from enum import Enum


class RobotType(Enum):
    INDUSTRIAL_ARM = "industrial_arm"
    COBOT = "cobot"
    SCARA = "scara"
    DELTA = "delta"
    CARTESIAN = "cartesian"
    AMR = "amr"
    AGV = "agv"
    HUMANOID = "humanoid"
    MOBILE_MANIPULATOR = "mobile_manipulator"
    WAREHOUSE_ROBOT = "warehouse_robot"
    AGRICULTURAL_ROBOT = "agricultural_robot"
    CONSTRUCTION_ROBOT = "construction_robot"
    MEDICAL_ROBOT = "medical_robot"
    INSPECTION_ROBOT = "inspection_robot"
    DRONE_AIR = "drone_air"
    DRONE_GROUND = "drone_ground"
    DRONE_MARINE = "drone_marine"
    AUTONOMOUS_PLANT = "autonomous_plant"


class Application(Enum):
    WELDING = "welding"
    PALLETISING = "palletising"
    PICK_PLACE = "pick_place"
    MACHINE_TENDING = "machine_tending"
    ASSEMBLY = "assembly"
    PACKING = "packing"
    SORTING = "sorting"
    INSPECTION = "inspection"
    PAINTING = "painting"
    DISPENSING = "dispensing"
    MATERIAL_HANDLING = "material_handling"
    WAREHOUSE_TRANSPORT = "warehouse_transport"
    AGRICULTURE = "agriculture"
    CONSTRUCTION = "construction"
    HEALTHCARE = "healthcare"
    LABORATORY = "laboratory"
    NUCLEAR = "nuclear"
    DEFENCE = "defence"
    FOOD_PROCESSING = "food_processing"


class ComponentCategory(Enum):
    SERVO_MOTOR = "servo_motor"
    STEPPER_MOTOR = "stepper_motor"
    MOTOR_DRIVE = "motor_drive"
    SERVO_DRIVE = "servo_drive"
    ENCODER_ABSOLUTE = "encoder_absolute"
    ENCODER_INCREMENTAL = "encoder_incremental"
    RESOLVER = "resolver"
    GEARBOX_HARMONIC = "gearbox_harmonic"
    GEARBOX_CYCLOIDAL = "gearbox_cycloidal"
    PLANETARY_GEARBOX = "planetary_gearbox"
    BEARING = "bearing"
    LINEAR_RAIL = "linear_rail"
    BALLSCREW = "ballscrew"
    CONTROLLER = "controller"
    PLC = "plc"
    INDUSTRIAL_PC = "industrial_pc"
    CPU = "cpu"
    GPU = "gpu"
    MCU = "mcu"
    FPGA = "fpga"
    DRAM = "dram"
    NAND = "nand"
    SSD = "ssd"
    NETWORK_INTERFACE = "network_interface"
    ETHERCAT = "ethercat"
    PROFINET = "profinet"
    CAN = "can"
    CAMERA = "camera"
    DEPTH_CAMERA = "depth_camera"
    LIDAR = "lidar"
    RADAR = "radar"
    FORCE_TORQUE_SENSOR = "force_torque_sensor"
    PROXIMITY_SENSOR = "proximity_sensor"
    SAFETY_SCANNER = "safety_scanner"
    LIGHT_CURTAIN = "light_curtain"
    EMERGENCY_STOP = "emergency_stop"
    RELAY = "relay"
    CONTACTOR = "contactor"
    POWER_SUPPLY = "power_supply"
    INVERTER = "inverter"
    BATTERY = "battery"
    BMS = "bms"
    CONNECTOR = "connector"
    CABLE = "cable"
    CABLE_CHAIN = "cable_chain"
    GRIPPER = "gripper"
    VACUUM_GENERATOR = "vacuum_generator"
    PNEUMATIC_VALVE = "pneumatic_valve"
    END_EFFECTOR = "end_effector"
    WELDING_EQUIPMENT = "welding_equipment"
    TEACH_PENDANT = "teach_pendant"
    FAN = "fan"
    FILTER = "filter"
    LUBRICANT = "lubricant"


class ReliabilityTier(Enum):
    A = "A"  # official government/OEM/API
    B = "B"  # established industry association/distributor
    C = "C"  # marketplace/integrator/company publication
    D = "D"  # third-party directory/news
    E = "E"  # inference


class EvidenceType(Enum):
    CONTRACT_AWARD = "contract_award"
    CASE_STUDY = "case_study"
    PLANNING_DOCUMENT = "planning_document"
    COMPANY_ANNOUNCEMENT = "company_announcement"
    JOB_POSTING = "job_posting"
    INTEGRATOR_CASE_STUDY = "integrator_case_study"
    MANUFACTURER_CASE_STUDY = "manufacturer_case_study"
    GRANT_PROJECT = "grant_project"
    TENDER = "tender"
    ANNUAL_REPORT = "annual_report"
    USED_EQUIPMENT_DISPOSAL = "used_equipment_disposal"
    TRADE_DATA = "trade_data"
    DIRECTORY_LISTING = "directory_listing"
    SAFETY_RECALL = "safety_recall"


class BOMConfidence(Enum):
    EXACT = "exact"          # Tier A: specific known component
    FAMILY = "family"        # Tier B: known technology family
    INFERRED = "inferred"    # Tier C: typical architecture


class AccessStatus(Enum):
    OPEN = "open"
    APPROVED = "approved"
    TERMS_REVIEW = "terms_review"
    PERMISSION_REQUIRED = "permission_required"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"
