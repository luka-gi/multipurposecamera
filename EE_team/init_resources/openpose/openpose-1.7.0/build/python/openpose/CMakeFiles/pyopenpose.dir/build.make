# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.18

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Disable VCS-based implicit rules.
% : %,v


# Disable VCS-based implicit rules.
% : RCS/%


# Disable VCS-based implicit rules.
% : RCS/%,v


# Disable VCS-based implicit rules.
% : SCCS/s.%


# Disable VCS-based implicit rules.
% : s.%


.SUFFIXES: .hpux_make_needs_suffix_list


# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/bin/cmake

# The command to remove a file.
RM = /usr/local/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build

# Include any dependencies generated for this target.
include python/openpose/CMakeFiles/pyopenpose.dir/depend.make

# Include the progress variables for this target.
include python/openpose/CMakeFiles/pyopenpose.dir/progress.make

# Include the compile flags for this target's objects.
include python/openpose/CMakeFiles/pyopenpose.dir/flags.make

python/openpose/CMakeFiles/pyopenpose.dir/openpose_python.cpp.o: python/openpose/CMakeFiles/pyopenpose.dir/flags.make
python/openpose/CMakeFiles/pyopenpose.dir/openpose_python.cpp.o: ../python/openpose/openpose_python.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object python/openpose/CMakeFiles/pyopenpose.dir/openpose_python.cpp.o"
	cd /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build/python/openpose && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/pyopenpose.dir/openpose_python.cpp.o -c /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/python/openpose/openpose_python.cpp

python/openpose/CMakeFiles/pyopenpose.dir/openpose_python.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/pyopenpose.dir/openpose_python.cpp.i"
	cd /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build/python/openpose && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/python/openpose/openpose_python.cpp > CMakeFiles/pyopenpose.dir/openpose_python.cpp.i

python/openpose/CMakeFiles/pyopenpose.dir/openpose_python.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/pyopenpose.dir/openpose_python.cpp.s"
	cd /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build/python/openpose && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/python/openpose/openpose_python.cpp -o CMakeFiles/pyopenpose.dir/openpose_python.cpp.s

# Object files for target pyopenpose
pyopenpose_OBJECTS = \
"CMakeFiles/pyopenpose.dir/openpose_python.cpp.o"

# External object files for target pyopenpose
pyopenpose_EXTERNAL_OBJECTS =

python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: python/openpose/CMakeFiles/pyopenpose.dir/openpose_python.cpp.o
python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: python/openpose/CMakeFiles/pyopenpose.dir/build.make
python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: src/openpose/libopenpose.so.1.7.0
python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: /usr/lib/aarch64-linux-gnu/libopencv_dnn.so.4.1.1
python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: /usr/lib/aarch64-linux-gnu/libopencv_gapi.so.4.1.1
python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: /usr/lib/aarch64-linux-gnu/libopencv_highgui.so.4.1.1
python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: /usr/lib/aarch64-linux-gnu/libopencv_ml.so.4.1.1
python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: /usr/lib/aarch64-linux-gnu/libopencv_objdetect.so.4.1.1
python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: /usr/lib/aarch64-linux-gnu/libopencv_photo.so.4.1.1
python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: /usr/lib/aarch64-linux-gnu/libopencv_stitching.so.4.1.1
python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: /usr/lib/aarch64-linux-gnu/libopencv_video.so.4.1.1
python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: /usr/lib/aarch64-linux-gnu/libopencv_videoio.so.4.1.1
python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: /usr/lib/aarch64-linux-gnu/libglog.so
python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: caffe/lib/libcaffe.so
python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: /usr/lib/aarch64-linux-gnu/libopencv_calib3d.so.4.1.1
python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: /usr/lib/aarch64-linux-gnu/libopencv_features2d.so.4.1.1
python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: /usr/lib/aarch64-linux-gnu/libopencv_flann.so.4.1.1
python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: /usr/lib/aarch64-linux-gnu/libopencv_imgcodecs.so.4.1.1
python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: /usr/lib/aarch64-linux-gnu/libopencv_imgproc.so.4.1.1
python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: /usr/lib/aarch64-linux-gnu/libopencv_core.so.4.1.1
python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: /usr/local/cuda/lib64/libcudart_static.a
python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: /usr/lib/aarch64-linux-gnu/librt.so
python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: /usr/lib/aarch64-linux-gnu/libglog.so
python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: caffe/lib/libcaffe.so
python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: caffe/lib/libcaffe.so
python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so: python/openpose/CMakeFiles/pyopenpose.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX shared module pyopenpose.cpython-36m-aarch64-linux-gnu.so"
	cd /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build/python/openpose && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/pyopenpose.dir/link.txt --verbose=$(VERBOSE)
	cd /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build/python/openpose && /usr/bin/strip /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build/python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so

# Rule to build all files generated by this target.
python/openpose/CMakeFiles/pyopenpose.dir/build: python/openpose/pyopenpose.cpython-36m-aarch64-linux-gnu.so

.PHONY : python/openpose/CMakeFiles/pyopenpose.dir/build

python/openpose/CMakeFiles/pyopenpose.dir/clean:
	cd /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build/python/openpose && $(CMAKE_COMMAND) -P CMakeFiles/pyopenpose.dir/cmake_clean.cmake
.PHONY : python/openpose/CMakeFiles/pyopenpose.dir/clean

python/openpose/CMakeFiles/pyopenpose.dir/depend:
	cd /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0 /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/python/openpose /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build/python/openpose /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build/python/openpose/CMakeFiles/pyopenpose.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : python/openpose/CMakeFiles/pyopenpose.dir/depend

