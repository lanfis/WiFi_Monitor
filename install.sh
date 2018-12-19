#!/bin/sh
sudo apt-get -y update;
sudo apt-get install -y python-tk;
#sudo apt-get -y full-upgrade;
sudo apt-get install -y python-pip;
sudo -H pip2 install --upgrade pip;
sudo -H pip2 install networkx
sudo -H pip2 install numpy;
sudo -H pip2 install matplotlib;

sudo apt-get install -y python3-pip;
sudo -H pip3 install --upgrade pip;
sudo -H pip3 install networkx
sudo -H pip3 install numpy;
sudo -H pip3 install matplotlib;

sudo apt-get install -y build-essential autoconf automake libtool pkg-config libnl-3-dev libnl-genl-3-dev libssl-dev libsqlite3-dev libpcre3-dev ethtool shtool rfkill zlib1g-dev libpcap-dev;
sudo apt-get install -y aircrack-ng;
