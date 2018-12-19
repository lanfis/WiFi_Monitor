#!/usr/bin/env python
# license removed for brevity
import os
import sys
current_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_folder)

import numpy as np
import time
import csv
from console_formatter import Console_Formatter

class DATA_READER:
    #PUBLIC
    file_data_path = None


    #PRIVATE
    consoler_ = Console_Formatter(__name__)
    fid_file_ = None
    data_list = []

    def __init__(self):
        pass

    def __del__(self):
        self.close_file()

    def load_file(self, data_path=None):
        self.file_data_path = self.file_data_path if data_path == None else data_path
        if not self.check_path(data_path):
            #print(self.consoler_.WARN("index file : \"{}\" not found !".format(self.data_path)))
            print(self.consoler_.WARN("Loading file : {} not found !".format(self.file_data_path)))
            return None
        #print(self.consoler_.INFO("loading index file ..."))
        print(self.consoler_.INFO("Loading file : {} ...".format(self.file_data_path)))
        self.close_file()
        self.fid_file_ = open(self.file_data_path, 'r+')
        #print(self.consoler_.INFO("Loading file : {} ok !".format(self.file_data_path)))
        self.data_list = self.fid_file_.readlines()
        return self.data_list
        '''
        data_list = []
        with open(data_path, 'r') as fid:
            infile_cursor = csv.reader(fid, delimiter=',')
            
            for row in infile_cursor:
                data_list = np.append(data_list, row)# [row[0], row[1]])
        return data_list
        '''

    def write_file(self, data, recursive_search=False):
        if self.fid_file_ == None:
            print(self.consoler_.WARN("File not load !"))
            return False
        it_ = iter(self.data_list)
        while recursive_search:
            try:
                if next(it_).strip() == data.strip():
                    return False
            except StopIteration:
                break
            
        data = "{}\n".format(data)
        self.data_list = np.append(self.data_list, data)
        print(self.consoler_.INFO("Writing file : {} ...".format(self.file_data_path)))
        self.fid_file_.write(data)
        #print(self.consoler_.INFO("Writing file : {} ok !".format(self.file_data_path)))
        return True

    def close_file(self, fid=None):
        fid = self.fid_file_ if fid == None else fid
        if fid != None:
            fid.close()
        self.fid_file_ = None

    def check_path(self, path):
        return os.path.exists(path)

    def current_time(self):
        return time.strftime("%Y%m%d%H%M%S", time.localtime()) #%Y-%m-%d %H:%M:%S

    def current_time_stamp(self):
        return time.time()



