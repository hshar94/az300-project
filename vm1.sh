#!/bin/sh
sudo ufw allow 5000/tcp
sudo apt-get update
sudo apt-get install python3
sudo apt-get install python3-pip
pip3 install azure-storage
pip3 install configparser
pip3 install flask
pip3 install --pre azure-cosmos
