#!/bin/bash

port=50051

python3 rc_server.py -p $port -s /dev/ttyUSB0 -b 115200 &
ip=`ifconfig wlan0 | awk '/inet / {print $2}'`
echo Listening for client on $ip:$port
