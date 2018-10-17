#!/bin/bash

pkill -f CameraSocket.py
pkill -f PipeSocket.py
pkill -f Main.py
clear
echo "---------------------------------------------------------"
echo "|######################DELTA ROBOT######################|"
echo "---------------------------------------------------------"
python ./CameraConnector/CameraSocket.py $PWD &
python Main.py $PWD