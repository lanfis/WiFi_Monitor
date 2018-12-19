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
from utils.sys_utils import SYS_UTILS
from utils.data_reader import DATA_READER
from utils.console_formatter import Console_Formatter


class PARSER:
    version_ = "1.0"
    console = Console_Formatter(__name__)
    sys_util = SYS_UTILS()
    data_reader = DATA_READER()
    wifi_graph = nx.DiGraph()
    
    flag_wifi_is_init = False
    packet_old = {}
    
    ap_list = {}
    client_list = {}
    connect_list = {}
    
    pos_ap = {}
    pos_client = {}
    pos_connect = {}
    
    
    def __init__(self):
        pass
        
    def __del__(self):
        pass
                    
    def init(self):
        print(self.console.INFO("Initializing ..."))

        
    def airdump_reader(self, load_dump_file_name):
        load_dump_file_name = os.path.join(current_folder, load_dump_file_name)
        print(self.console.INFO("Loading airdumping file : {} ...".format(load_dump_file_name)))
        dump_data = self.data_reader.load_file(load_dump_file_name)
        print(self.console.INFO("Reading airdumping file ..."))
        
        ap_info_list = []
        client_info_list = []
        
        is_ap = False
        for i in range(len(dump_data)):
            if(len(dump_data[i].strip()) > 0):
                if is_ap:
                    ap_info_list = np.append(ap_info_list, dump_data[i].strip())
                else:
                    client_info_list = np.append(client_info_list, dump_data[i].strip())
            else:
                is_ap = not is_ap
        return ap_info_list, client_info_list
        
    def airdump_parser(self, ap_info_list, client_info_list, refresh_time=0.1, elast_time=30.0, save_file_name=None, is_show=True):
        print(self.console.INFO("Parsing data ..."))
        
        for i in range(1, len(ap_info_list)):
            data = ap_info_list[i].split(',')
            if len(data) < 14:
                continue
            bssid = data[0].strip()
            channel = data[3].strip()
            power = data[8].strip()
            essid = data[13].strip()
            #self.ap_list = self.ap_list + [bssid]
            last_time_seen = data[2].strip()
            last_time = float(self.get_time_stamp(last_time_seen))
            current_time = float(time.time())
            if int(power) > -10:
                ap_color = 0.0
                ap_size = 20.0
            else:
                ap_color = 100+float(power)
                ap_size = 100+int(power) if 100+int(power) < 60 else 60
            if current_time - last_time < elast_time:
                self.pos_ap = self.airdump_parser_graph_pos(self.pos_ap, bssid, (100-ap_color))
                if not bssid in self.wifi_graph.nodes():
                    self.wifi_graph.add_node(bssid)
                self.pos_ap = self.airdump_parser_graph_pos_min_seperate(self.pos_ap, bssid, self.pos_ap, min_width=10)
                try:
                    label_string = str(bssid + "\n" + essid + "\n" + power + " dBm" + "\n" + "CH: " + channel).encode('utf-8')
                except Exception:
                    label_string = str(bssid + "\n\n" + power + " dBm" + "\n" + "CH: " + channel).encode('utf-8')
                self.ap_list[bssid] = [ap_color/100.0, ap_size*20, label_string]
            else:
                if bssid in self.ap_list:
                    del self.ap_list[bssid]
                    if bssid in self.wifi_graph.nodes():
                        self.wifi_graph.remove_node(bssid)
                if bssid in self.pos_ap:
                    del self.pos_ap[bssid]
                    
        
        for i in range(1, len(client_info_list)):
            data = client_info_list[i].split(',')
            if len(data) < 6:
                continue
            client_bssid = data[0].strip()
            ap_bssid = data[5].strip()
            power = data[3].strip()
            packets = data[4].strip()
            last_time_seen = data[2].strip()
            last_time = float(self.get_time_stamp(last_time_seen))
            current_time = float(time.time())
            if int(power) > -10:
                client_color = 0.0
                client_size = 20.0
            else:
                client_color = 100+float(power)
                client_size = 100+int(power) if 100+int(power) < 60 else 60
            
            if current_time - last_time < elast_time:
                self.pos_client = self.airdump_parser_graph_pos(self.pos_client, client_bssid, (100-client_color))
                if not client_bssid in self.wifi_graph.nodes():
                    self.wifi_graph.add_node(client_bssid)
                self.pos_client = self.airdump_parser_graph_pos_min_seperate(self.pos_client, client_bssid, self.pos_ap, min_width=10)
                self.pos_client = self.airdump_parser_graph_pos_min_seperate(self.pos_client, client_bssid, self.pos_client, min_width=10)
                label_string = (client_bssid + "\n\n").encode('utf-8')
                self.client_list[client_bssid] = [client_color/100.0, client_size*20, label_string]
            else:
                if client_bssid in self.client_list:
                    del self.client_list[client_bssid]
                    if client_bssid in self.wifi_graph.nodes() and (not client_bssid in self.ap_list):
                        self.wifi_graph.remove_node(client_bssid)
                if client_bssid in self.pos_client:
                    del self.pos_client[client_bssid]

                        
            if client_bssid in self.pos_ap:
                self.pos_client[client_bssid] = self.pos_ap[client_bssid]
            elif client_bssid in self.pos_client and ap_bssid in self.pos_ap:#Repositioning the client and ap because of unreasonably too long connection
                self.pos_client[client_bssid][0] = abs(self.pos_client[client_bssid][0]) if self.pos_ap[ap_bssid][0] > 0 else -abs(self.pos_client[client_bssid][0])
                self.pos_client[client_bssid][1] = abs(self.pos_client[client_bssid][1]) if self.pos_ap[ap_bssid][1] > 0 else -abs(self.pos_client[client_bssid][1])
                for count in range(4):
                    if self.length(np.array([self.pos_client[client_bssid][0]-self.pos_ap[ap_bssid][0], self.pos_client[client_bssid][1]-self.pos_ap[ap_bssid][1]])) < 75:
                        break
                    self.pos_client = self.airdump_parser_graph_pos(self.pos_client, client_bssid, (100-client_color), add_array=self.pos_ap[ap_bssid], is_get_new=True)
                    self.pos_client = self.airdump_parser_graph_pos_min_seperate(self.pos_client, client_bssid, self.pos_ap, min_width=10)
                    self.pos_client = self.airdump_parser_graph_pos_min_seperate(self.pos_client, client_bssid, self.pos_client, min_width=10)
                 
                    
            edge_pair = (client_bssid, ap_bssid)
            if current_time - last_time < elast_time and client_bssid in self.client_list and ap_bssid in self.ap_list:
                if not (client_bssid, ap_bssid) in self.packet_old:
                    self.packet_old[(client_bssid, ap_bssid)] = 0
                packets_speed = float(int(packets)-self.packet_old[(client_bssid, ap_bssid)])/10.0
                packets_speed = packets_speed if packets_speed > 1 else 1
                packets_speed = packets_speed if packets_speed < 10 else 10
                connect_width = packets_speed
                packets_sum = float(packets)/10000.0 if float(packets)/10000.0 < 1.0 else 1.0
                #packets_sum = packets_sum if packets_sum > 1 else 1
                connect_color = packets_sum#float(packets_speed))
                self.packet_old[(client_bssid, ap_bssid)] = int(packets)
                connect_label = str(packets).encode('utf-8')
                self.connect_list[edge_pair] = [connect_color, connect_width, connect_label, last_time]
                self.pos_connect[ap_bssid] = self.pos_ap[ap_bssid]
                self.pos_connect[client_bssid] = self.pos_client[client_bssid]
            elif (not current_time - last_time < elast_time) and client_bssid in self.client_list and ap_bssid in self.ap_list:
                if edge_pair in self.connect_list:
                    del self.connect_list[edge_pair]
                    '''
                    if ap_bssid in self.pos_connect:
                        del self.pos_connect[ap_bssid]
                    if client_bssid in self.pos_connect:
                        del self.pos_connect[client_bssid]
                    '''
            if not client_bssid in self.client_list:
                for i in self.connect_list.keys():
                    if i[0] == client_bssid:
                        del self.connect_list[i]
                        if i[0] in self.pos_connect and not i[1] in self.pos_connect:
                            del self.pos_connect[i[0]]
            if not ap_bssid in self.ap_list:
                for i in self.connect_list.keys():
                    if i[1] == ap_bssid:
                        del self.connect_list[i]
                        if i[1] in self.pos_connect and not i[0] in self.pos_connect:
                            del self.pos_connect[i[1]]
            
        current_time = float(time.time())
        for i in self.connect_list.keys():
            if current_time - self.connect_list[i][3] > elast_time:
                del self.connect_list[i]
                
        ap_color_list = []
        ap_size_list = []
        ap_label_list = {}
        for i in self.ap_list.keys():
            ap_color_list = np.append(ap_color_list, self.ap_list[i][0])
            ap_size_list = np.append(ap_size_list, self.ap_list[i][1])
            ap_label_list[i] = self.ap_list[i][2]
        
        nx.draw_networkx_nodes(self.wifi_graph, self.pos_ap, nodelist=self.ap_list.keys(), node_shape='^', node_size=ap_size_list, node_color=ap_color_list, cmap=plt.cm.jet, vmax=0.8, vmin=0.0, alpha=0.5)
        nx.draw_networkx_labels(self.wifi_graph, self.pos_ap, labels=ap_label_list, font_size=6)
        
        client_color_list = []
        client_size_list = []
        client_label_list = {}
        for i in self.client_list.keys():
            client_color_list = np.append(client_color_list, self.client_list[i][0])
            client_size_list = np.append(client_size_list, self.client_list[i][1])
            client_label_list[i] = self.client_list[i][2]
            
        nx.draw_networkx_nodes(self.wifi_graph, self.pos_client, nodelist=self.client_list, node_shape='o', node_size=client_size_list, node_color=client_color_list, cmap=plt.cm.jet, vmax=0.8, vmin=0.0, alpha=0.5)
        nx.draw_networkx_labels(self.wifi_graph, self.pos_client, labels=client_label_list, font_size=6)
        
        connect_color = []
        connect_width = []
        connect_label_label_list = {}
        for i in self.connect_list.keys():
            connect_color = np.append(connect_color, self.connect_list[i][0])
            connect_width = np.append(connect_width, self.connect_list[i][1])
            connect_label_label_list[i] = self.connect_list[i][2]
        
        if len(self.pos_connect) > 0:
            nx.draw_networkx_edges(self.wifi_graph, self.pos_connect, edgelist=self.connect_list.keys(), arrowstyle='->', arrowsize=16, edge_color=connect_color, cmap=plt.cm.jet, edge_vmax=1.0, edge_vmin=0.0, width=connect_width, alpha=0.5)
            nx.draw_networkx_edge_labels(self.wifi_graph, self.pos_connect, edge_labels=connect_label_label_list, alpha=0.5, label_pos=0.5, font_size=6)
        
        plt.axis([-120, 120, -120, 120])
        plt.grid()
        #fig = plt.figure()
        #plt.show()
        
        if save_file_name != None:
            plt.savefig(save_file_name+".png", format='png')
        if is_show:
            plt.ion()
            plt.pause(refresh_time)
        plt.cla()
        
        return self.pos_ap, self.pos_client
        
    def airdump_parser_graph_pos(self, pos, bssid, power, add_array=[], is_get_new=False):
        if not bssid in pos or is_get_new:
            pos = self.airdump_parser_graph_pos_(pos, bssid, power, add_array)
        pos[bssid] = self.airdump_parser_graph_power_adjust(pos[bssid], power)
        return pos
        
    def airdump_parser_graph_pos_(self, pos, bssid, power, add_array=[]):
        pos[bssid] = np.array([random.uniform(-10.0, 10.0), random.uniform(-10.0, 10.0)])
        if len(add_array) > 0:
            pos[bssid] = np.array([pos[bssid][0]+add_array[0], pos[bssid][1]+add_array[1]])
        pos[bssid] = self.airdump_parser_graph_power_adjust(pos[bssid], power)
        return pos
        
    def airdump_parser_graph_pos_min_seperate(self, pos_ori, bssid, pos_ex, min_width=20):
        for i in pos_ex.keys():
            if i != bssid:
                for count in range(4):
                    if self.length(np.array([pos_ex[i][0]-pos_ori[bssid][0], pos_ex[i][1]-pos_ori[bssid][1]])) > min_width:
                        break
                    angle = random.uniform(-math.pi, math.pi)
                    x = pos_ori[bssid][0]
                    y = pos_ori[bssid][1]
                    pos_ori[bssid][0] = math.cos(angle) * x - math.sin(angle) * y
                    pos_ori[bssid][1] = math.sin(angle) * x + math.cos(angle) * y
        return pos_ori
        
    
    def airdump_parser_graph_power_adjust(self, array, power):
        length = self.length(array)
        array[0] = array[0] / length * abs(power)
        array[1] = array[1] / length * abs(power)
        return array
        
    def length(self, array):
        return math.sqrt(math.pow(array[0], 2.0) + math.pow(array[1], 2.0))
        
    def get_time_stamp(self, tt):
        try:
            return time.mktime(time.strptime(tt, "%Y-%m-%d %H:%M:%S"))
        except Exception:
            return time.time()


        
def main(**kwargs):
    parser = PARSER()

    ap_list, client_list = parser.airdump_reader(load_dump_file_name)
    pos_ap, pos_client = parser.airdump_parser(ap_list, client_list, **kwargs)
    while True:
        ap_list, client_list = parser.airdump_reader(load_dump_file_name)
        a = time.time()
        pos_ap, pos_client = parser.airdump_parser(ap_list, client_list, **kwargs)
        b = time.time()
        print("deley : {} secs".format(b-a))

if __name__ == "__main__":
    args = sys.argv[1:]
    kwargs = {}
    for i in range(0, len(args),2):
        kwargs[args[i]] = args[i+1]
    load_dump_file_name = raw_input("Input dump file name : ").strip()
    main(**kwargs)
