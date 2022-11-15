#! /bin/bash

if [ $# -eq 0 ]; then
./setup_v4l2.sh
source /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openposevenv/bin/activate; python ./main.py
elif [ $1 == "-h" ]; then
source /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openposevenv/bin/activate; python ./main.py $1
else
./setup_v4l2.sh
source /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openposevenv/bin/activate; python ./main.py $@
fi


