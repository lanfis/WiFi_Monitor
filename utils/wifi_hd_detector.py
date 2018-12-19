#!/usr/bin/env python
# license removed for brevity
import os
import sys
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)

import numpy as np
from sys_utils import SYS_UTILS
from console_formatter import Console_Formatter

class WIFI_HD_DETECTOR:
    sys_util = SYS_UTILS()    
    console = Console_Formatter(__name__)
    
    interface = []
    chipset = []
    driver = []
    
    flag_is_init = False
    
    def __init__(self):
        self.run()
    
    def run(self, is_silent=False):
        if not is_silent:
            print(self.console.INFO("Detecting wifi hardware ..."))
        stdout, stderr = self.sys_util(['airmon-ng'])
        line_new = self.sys_util.msg_line_split(stdout)
    
        idx_interface = 0
        idx_chipset = 2
        idx_driver = 3
        val  = self.sys_util.msg_split(line_new[0], '\t')
        if len(val) > 3:
            for i in range(len(val)):                    
                idx_interface = int(i) if val[i] == "Interface" else idx_interface
                idx_chipset = int(i) if val[i] == "Chipset" else idx_chipset
                idx_driver = int(i) if val[i] == "Driver" else idx_driver
        
        self.interface = []
        self.chipset = []
        self.driver = []
        for i in range(1, len(line_new)):
            val  = self.sys_util.msg_split(line_new[i], '\t')        
            self.interface = np.append(self.interface, val[idx_interface])       
            self.chipset = np.append(self.chipset, val[idx_chipset])       
            self.driver = np.append(self.driver, val[idx_driver])
        
        if not is_silent:
            for i in range(len(self.interface)):
                print(self.console.INFO("Interface : {:<10}, Chipset : {:<10}, Driver : {:<10}".format(self.interface[i], self.chipset[i], self.driver[i])))
        
        self.flag_is_init = True
        return self.flag_is_init
        
    def is_init(self):
        return self.flag_is_init
