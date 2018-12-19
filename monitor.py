#!/usr/bin/env python
# license removed for brevity
import os
import sys
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)

import random
import math
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import time
from utils.wifi_hd_detector import WIFI_HD_DETECTOR
from utils.sys_utils import SYS_UTILS
from utils.data_reader import DATA_READER
from utils.console_formatter import Console_Formatter

class MONITOR:
    version_ = "1.0"
    console = Console_Formatter(__name__)
    sys_util = SYS_UTILS()
    data_reader = DATA_READER()
    wifi_detector = None
    wifi_graph = nx.DiGraph()
    
    flag_wifi_is_init = False
    packet_old = {}
    
    def __init__(self):
        pass
        
    def __del__(self):
        if self.flag_wifi_is_init:
            self.wifi_detector.run(is_silent=True)
            for i in range(len(self.wifi_detector.interface)):
                if len(self.wifi_detector.interface[i]) > 3:
                    if self.wifi_detector.interface[i][0:3] == "mon" or self.wifi_detector.interface[i][-3:] == "mon":
                        self.monitor_mode_stop(self.wifi_detector.interface[i])
                    
    def init(self, interface=None):
        print(self.console.INFO("Initializing ..."))
        self.wifi_detector = WIFI_HD_DETECTOR()
        self.flag_wifi_is_init = self.wifi_detector.is_init()
        if interface == None:
            if self.flag_wifi_is_init:
		if len(self.wifi_detector.interface) == 0:
		    print(self.console.FATAL("Please activating by [sudo] / [su] !"))
		    self.flag_wifi_is_init = False
		else:
                    self.monitor_mode_start(self.wifi_detector.interface[0])
                    self.wifi_detector.run(is_silent=True)
        else:
            self.monitor_mode_start(interface)
        return self.flag_wifi_is_init

    def airdump(self, interface=None, save_file_name=None, berlin=None, channel=None, bssid=None, essid=None, output_format="csv", is_beacons=False, is_manufacturer=False, is_uptime=False, is_associate=False):
        '''
        save_file_name <prefix>: Dump file prefix
        berlin <secs>: Time before removing the AP/client from the screen when no more packets are received
        is_beacons : Record all beacons in dump file
        is_manufacturer : Display manufacturer from IEEE OUI list
        is_uptime : Display AP Uptime from Beacon Timestamp
        '''
        print(self.console.INFO("Air dumping ..."))
        args = []
        cmd = ["airodump-ng"]
        if save_file_name != None:
            args = np.append(args, "-w")
            args = np.append(args, save_file_name)
        if channel != None:
            args = np.append(args, "-c")
            args = np.append(args, channel)
        if bssid != None:
            args = np.append(args, "--bssid")
            args = np.append(args, bssid)
        if essid != None:
            args = np.append(args, "--essid")
            args = np.append(args, essid)
        if is_beacons:
            args = np.append(args, "--beacons")
        if is_manufacturer:
            args = np.append(args, "--manufacturer")
        if is_uptime:
            args = np.append(args, "--uptime")
        if is_associate:
            args = np.append(args, "-a")
        if berlin != None:
            args = np.append(args, "--berlin")
            args = np.append(args, berlin)
        if output_format != None:
            args = np.append(args, "--output-format")
            args = np.append(args, output_format)
            
        if interface == None:
            if self.flag_wifi_is_init:
                for i in range(len(self.wifi_detector.interface)):
                    if len(self.wifi_detector.interface[i]) > 3:
                        if self.wifi_detector.interface[i][0:3] == "mon" or self.wifi_detector.interface[i][-3:] == "mon":
                            print(self.console.INFO("Air dumping interface : {}".format(self.wifi_detector.interface[i])))
                            cmd = np.append(cmd, args)
                            cmd = np.append(cmd, self.wifi_detector.interface[i])
                            stdout = self.sys_util.sys_check_output(cmd)
                            #stdout, stderr = self.sys_util(cmd)
                            line_new = self.sys_util.msg_line_split(stdout)
                            return line_new
            else:
                return None
        else:
            print(self.console.INFO("Air dumping interface : {}".format(interface)))
            cmd = np.append(cmd, args)
            cmd = np.append(cmd, interface)
            stdout, stderr = self.sys_util(cmd)
            line_new = self.sys_util.msg_line_split(stdout)
            return line_new
            
    def monitor_mode_start(self, interface, channel=None, frequency=None):
        print(self.console.WARN("Starting interface : {}".format(interface)))
        stdout, stderr = self.sys_util(['airmon-ng', 'start', interface])
        line_new = self.sys_util.msg_line_split(stdout)
        return line_new
        
    def monitor_mode_stop(self, interface, channel=None, frequency=None):
        print(self.console.WARN("Stoping interface : {}".format(interface)))
        stdout, stderr = self.sys_util(['airmon-ng', 'stop', interface])
        line_new = self.sys_util.msg_line_split(stdout)
        return line_new
        
    def monitor_mode_check(self):
        stdout, stderr = self.sys_util(['airmon-ng', 'check'])
        line_new = self.sys_util.msg_line_split(stdout)
        return line_new
        
        
def main(**kwargs):
    monitor = MONITOR()

    monitor.init()
    msg = monitor.airdump(**kwargs)

if __name__ == "__main__":
    args = sys.argv[1:]
    kwargs = {}
    for i in range(0, len(args),2):
        kwargs[args[i]] = args[i+1]
    main(**kwargs)

