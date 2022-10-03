#! /bin/bash

# user-set variables to change the stream options
# i don't know how gstreamer works so be careful changing these
# I know that two capture options work: 1024x512 and 512x256
SENSOR_IMXL=0
SENSOR_IMXR=1
SENSOR_IMXL_LOOPBACK=3
SENSOR_IMXR_LOOPBACK=4
CAPTURE_WIDTH=1024
CAPTURE_HEIGHT=512
FRAMERATE=30
DISPLAY_WIDTH=1280
DISPLAY_HEIGHT=720

# create loopback device
sudo modprobe v4l2loopback video_nr=$SENSOR_IMXL_LOOPBACK,$SENSOR_IMXR_LOOPBACK card_label="Dummy video device 1","Dummy video device 2"

# make sure loopback device was created (should show up as Dummy device)
v4l2-ctl --list-devices

# ensure device is running
v4l2-ctl --all -d /dev/video$SENSOR_IMXL
v4l2-ctl --all -d /dev/video$SENSOR_IMXR
v4l2-ctl --all -d /dev/video$SENSOR_IMXL_LOOPBACK
v4l2-ctl --all -d /dev/video$SENSOR_IMXR_LOOPBACK

# run gstreamer pipeline - take raw video and convert, then display to loopback device
gnome-terminal -- gst-launch-1.0 -v nvarguscamerasrc sensor_id=$SENSOR_IMXL ! "video/x-raw(memory:NVMM), format=NV12, width=$CAPTURE_HEIGHT, height=$CAPTURE_WIDTH, framerate=$FRAMERATE/1" ! nvvidconv ! "video/x-raw, width=1280, height=720, format=I420, framerate=30/1" ! videoconvert ! identity drop-allocation=1 ! "video/x-raw, width=$DISPLAY_WIDTH, height=$DISPLAY_HEIGHT, format=RGB, framerate=30/1" ! v4l2sink device=/dev/video$SENSOR_IMXL_LOOPBACK

gnome-terminal -- gst-launch-1.0 -v nvarguscamerasrc sensor_id=$SENSOR_IMXR ! "video/x-raw(memory:NVMM), format=NV12, width=$CAPTURE_HEIGHT, height=$CAPTURE_WIDTH, framerate=$FRAMERATE/1" ! nvvidconv ! "video/x-raw, width=1280, height=720, format=I420, framerate=30/1" ! videoconvert ! identity drop-allocation=1 ! "video/x-raw, width=$DISPLAY_WIDTH, height=$DISPLAY_HEIGHT, format=RGB, framerate=30/1" ! v4l2sink device=/dev/video$SENSOR_IMXR_LOOPBACK
