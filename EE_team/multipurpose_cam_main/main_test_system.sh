#! /bin/bash
./setup_v4l2.sh

source /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openposevenv/bin/activate; python ./main.py $@
