#!/usr/bin/env python
# license removed for brevity
import os
import sys
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)

import time
import numpy as np
from monitor import MONITOR
from parser import PARSER

parser = PARSER()

ap_list, client_list = parser.airdump_reader(os.path.join(current_folder, "aaaa-01.csv"))

pos_ap, pos_client = parser.airdump_parser(ap_list, client_list, refresh_time=0.1)
while True:
    ap_list, client_list = parser.airdump_reader(os.path.join(current_folder, "aaaa-01.csv"))
    a = time.time()
    pos_ap, pos_client = parser.airdump_parser(ap_list, client_list, refresh_time=0.1, save_file_name="aaaa", is_show=True)
    b = time.time()
    print("deley : {} secs".format(b-a))

