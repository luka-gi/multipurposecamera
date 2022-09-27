#! /bin/bash

# user-set variables to change the stream options
# i don't know how gstreamer works so be careful changing these
# I know that two display options work: 1024x512 and 512x256
CAPTURE_WIDTH=1024
CAPTURE_HEIGHT=512
FRAMERATE=30
DISPLAY_WIDTH=1280
DISPLAY_HEIGHT=720

# create loopback device
sudo modprobe v4l2loopback

# make sure loopback device was created (should show up as Dummy device)
v4l2-ctl --list-devices

# grab the device id of virtual input
V4L2LOOPBACK_ID=`v4l2-ctl --list-devices | awk '/Dummy/{getline; print}' | grep -o '[0-9]\+'`

# ensure device is running
v4l2-ctl --all -d /dev/video$V4L2LOOPBACK_ID

# run gstreamer pipeline - take raw video and convert, then display to loopback device
gnome-terminal -- gst-launch-1.0 -v nvarguscamerasrc ! "video/x-raw(memory:NVMM), format=NV12, width=$CAPTURE_HEIGHT, height=$CAPTURE_WIDTH, framerate=$FRAMERATE/1" ! nvvidconv ! "video/x-raw, width=1280, height=720, format=I420, framerate=30/1" ! videoconvert ! identity drop-allocation=1 ! "video/x-raw, width=$DISPLAY_WIDTH, height=$DISPLAY_HEIGHT, format=RGB, framerate=30/1" ! v4l2sink device=/dev/video$V4L2LOOPBACK_ID
