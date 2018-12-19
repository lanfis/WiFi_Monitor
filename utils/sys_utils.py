#!/usr/bin/env python
# license removed for brevity
import os
import sys
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)

import numpy as np
import subprocess
from subprocess import Popen, PIPE

class SYS_UTILS:
    #PUBLIC
    #PRIVATE
    
    def __init__(self):
        pass
        
    def __call__(self, cmd):
        return self.sys_call(cmd)
        
    def sys_call(self, cmd):
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        stdout = p.stdout.read()
        stderr = p.stderr.read()
        #output = p.stdin.write()
        return stdout, stderr
        
    def sys_check_output(self, cmd):
        try:
            return subprocess.check_output(cmd)
        except subprocess.CalledProcessError as excp:
            print("command error : {}".format(cmd))
            return excp.output
        
    def msg_line_split(self, msg):
        lines = msg.split(os.linesep)
        line_new = []
        for i in range(len(lines)):
            if len(lines[i]) > 0:
                line_new = np.append(line_new, lines[i])
        '''
        for i in range(len(lines)):
            line = lines[i]
            vals = line.split(":")
            if len(vals) > 1:
                for j in range(len(vals)):
                    vals[j] = vals[j].strip()
        '''
        return line_new
        
    def msg_split(self, msg, sign = ' '):
        vals = msg.split(sign)
        val_new = []
        for i in range(len(vals)):
            val_new = np.append(val_new, vals[i].strip())
        return val_new
        
    '''
    def get_cpu_info(self):
        output = self.sys_call(["lscpu"])
        lines = output.split(os.linesep)
        for i in range(len(lines)):
            line = lines[i]
            vals = line.split(":")
            if len(vals) > 1:
                for j in range(len(vals)):
                    vals[j] = vals[j].strip()
                self.CPU_INFO[vals[0]] = vals[1]
        self.SOCKETS = int(self.CPU_INFO['Socket(s)'])
        self.CORES =  int(int(self.CPU_INFO['Core(s) per socket']) * self.SOCKETS)
        self.THREADS = int(int(self.CPU_INFO['Thread(s) per core']) * self.CORES)
        return self.CPU_INFO
    '''
'''
sys = SYS_UTILS()    
#cmd = ["airodump-ng", "mon0"]
cmd = ["ifconfig"]
#a = sys(["ifconfig"])
#a = sys(cmd)
a, b = sys.sys_call(cmd)
#a = sys.sys_check_output(cmd)
a = sys.msg_line_split(a)
print(a)
#print(b)
'''
