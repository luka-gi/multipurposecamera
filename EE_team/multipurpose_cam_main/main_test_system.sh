#! /bin/bash

if [ $1 != "-h" ]; then
./setup_v4l2.sh
fi

source /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openposevenv/bin/activate; python ./main.py $@
