#!/usr/bin/env python
# license removed for brevity
import os
import sys
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)

import numpy as np
from parser import PARSER

parser = PARSER()
'''
monitor.init()
msg = monitor.airdump(save_file_name="aaaa", is_beacons=True, is_manufacturer=True, is_uptime=True)
print(msg)
'''

ap_list, client_list = parser.airdump_reader(os.path.join(current_folder, "aaaa-01.csv"))

pos = parser.airdump_parser(ap_list, client_list, refresh_time=100, elast_time=99999999, save_file_name="aaaa", is_show=False)
'''
for i in range(10):
    pos = monitor.airdump_parser(ap_list, client_list, pos)
'''
print(pos)
