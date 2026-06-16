import sys
if sys.prefix == '/home/yuanjian/Research/BatteryLab/lab_venv':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/yuanjian/Research/BatteryLab/install/BatteryLab'
