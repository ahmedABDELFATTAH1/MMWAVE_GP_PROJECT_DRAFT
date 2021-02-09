import numpy as np
import serial
import time
from enum import Enum
import json
from radar_configuration import Radar
from threading import Thread

radar = Radar()
radar.setup_radar()
#radar.setup_radar_system_configuration()
#radar.setup_radar_pll_configuration()
#radar.setup_radar_baseband_configuration()
radar.save_readings()
# lines = open('radar_readings.txt', 'r').readlines()
# print (type(lines[2]))


