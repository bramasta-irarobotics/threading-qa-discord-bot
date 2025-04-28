from enum import Enum

#Tag Classification
class Tag_Class(Enum):
	device = ["PLC", "HMI", "Robot", "Camera", "Servo", "Simulator", "LiDAR", "Other"]
	software = ["Sysmac (Omron) (PLC)", "Adept ACE (Omron) (PLC)", "CX One (Omron) (PLC)", "TIA Portal (Siemens) (PLC)", "Machine Expert (Schneider) (PLC)", "TwinCAT (Beckhoff) (PLC)", "GX Work (Mitsubishi) (PLC)", "Sysmac NA (Omron) (HMI)", "NB Designer (Omron) (HMI)", "TIA Portal (Siemens) (HMI)", "Operator Terminal Expert (Schneider) (HMI)", "TwinCAT (Beckhoff) (HMI)", "EasyBuilder (Weintek) (HMI)", "Robot Studio (ABB) (Robot)", "EPSON RC+ (EPSON)  (Robot)", "In-Sight Explorer (Cognex) (Camera)", "ASDA Soft (Delta) (Servo)", "SoMove (Schneider) (Servo)", "FlexSim (Simulator)", "SOPAS Engineering Tool (SICK) (LiDAR)", "Other (Other)"]
	topic = ["General Programming Standard", "Case Packer Standard", "Palletizer", "SPM", "Other"]