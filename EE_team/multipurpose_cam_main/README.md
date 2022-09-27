# multipurposecamera main codebase
 
# TLDR - run shell scripts v4l2_setup.sh and subsystem0.1.sh. use arguments -v for verbose and -d for display

# BEFORE YOU BEGIN:

## OpenPose

We found that [these instructions](https://spyjetson.blogspot.com/2021/02/jetpack-45-install-latest-version-of_13.html) worked best for our setup even though we are on Jetpack 4.4. We included a version (OpenPose-1.7.0) that definitely currently works on NVIDIA Jetson Xavier NX with Jetpack SDK version 4.4.1 (install jtop to check this information as well as resource useage). 

### Note that a specific version of CMAKE is required. This is in the blog instructions.
### Note the 3rd party repos that need to be installed. This is also in the blog instructions.

## Virtual Environment

Installing some python modules may cause integral jetson modules to stop working, therefore a virtual environment (we used 3.6) needs to be set up. As shown in the shell scripts, the venv we use is currently in [openposevenv](/EE_team/init_resources/openpose) but should eventually be moved.

## V4L2loopback

### This applies to the IMX219 stereo with CSI ports that we are using

We need the camera code to be able to run sequentially. A photo must finish writing before we analyze it. We don't need a buffer since we must stay live, so we don't need to write until OpenPose has finished and output. Our camera captures in 10-bit Bayer RGRG/GBGB format, which we must convert to RGB. We originally used a gstream pipeline to do the conversion, but had trouble capturing this information in the python virtual environment. Our workaround was to create a virtual device using V4L2loopback and make the gstream pipeline convert to RGB video and display to this device. This way we could treat it as a separate device, and access it from the python cv module directly. 

### Follow the instructions on their repo and run setup_v4l2.sh.

## As of now one subsystem works. Run the shell file to run in the correct python environment.
## use arguments -v for verbose and -d for display


