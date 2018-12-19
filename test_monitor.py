#!/usr/bin/env python
# license removed for brevity
import os
import sys
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)

import numpy as np
from monitor import MONITOR

monitor = MONITOR()

monitor.init()
msg = monitor.airdump(save_file_name="aaaa", is_beacons=True, is_associate=True, is_manufacturer=True, is_uptime=True)
print(msg)

