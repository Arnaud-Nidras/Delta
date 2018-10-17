#!/bin/bash
pkill -f gst
gst-launch-1.0 -v v4l2src device=/dev/video0 ! video/x-raw,framerate=30/1,width=1280,height=720 ! videoconvert ! x264enc tune=zerolatency speed-preset=ultrafast qp-min=18 pass=5 quantizer=21 bitrate=90000 aud=false ! h264parse ! rtph264pay config-interval=1 pt=96 ! udpsink host=192.168.136 port=8004