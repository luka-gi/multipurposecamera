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
include examples/tutorial_api_cpp/CMakeFiles/08_heatmaps_from_image.bin.dir/depend.make

# Include the progress variables for this target.
include examples/tutorial_api_cpp/CMakeFiles/08_heatmaps_from_image.bin.dir/progress.make

# Include the compile flags for this target's objects.
include examples/tutorial_api_cpp/CMakeFiles/08_heatmaps_from_image.bin.dir/flags.make

examples/tutorial_api_cpp/CMakeFiles/08_heatmaps_from_image.bin.dir/08_heatmaps_from_image.cpp.o: examples/tutorial_api_cpp/CMakeFiles/08_heatmaps_from_image.bin.dir/flags.make
examples/tutorial_api_cpp/CMakeFiles/08_heatmaps_from_image.bin.dir/08_heatmaps_from_image.cpp.o: ../examples/tutorial_api_cpp/08_heatmaps_from_image.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object examples/tutorial_api_cpp/CMakeFiles/08_heatmaps_from_image.bin.dir/08_heatmaps_from_image.cpp.o"
	cd /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build/examples/tutorial_api_cpp && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/08_heatmaps_from_image.bin.dir/08_heatmaps_from_image.cpp.o -c /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/examples/tutorial_api_cpp/08_heatmaps_from_image.cpp

examples/tutorial_api_cpp/CMakeFiles/08_heatmaps_from_image.bin.dir/08_heatmaps_from_image.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/08_heatmaps_from_image.bin.dir/08_heatmaps_from_image.cpp.i"
	cd /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build/examples/tutorial_api_cpp && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/examples/tutorial_api_cpp/08_heatmaps_from_image.cpp > CMakeFiles/08_heatmaps_from_image.bin.dir/08_heatmaps_from_image.cpp.i

examples/tutorial_api_cpp/CMakeFiles/08_heatmaps_from_image.bin.dir/08_heatmaps_from_image.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/08_heatmaps_from_image.bin.dir/08_heatmaps_from_image.cpp.s"
	cd /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build/examples/tutorial_api_cpp && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/examples/tutorial_api_cpp/08_heatmaps_from_image.cpp -o CMakeFiles/08_heatmaps_from_image.bin.dir/08_heatmaps_from_image.cpp.s

# Object files for target 08_heatmaps_from_image.bin
08_heatmaps_from_image_bin_OBJECTS = \
"CMakeFiles/08_heatmaps_from_image.bin.dir/08_heatmaps_from_image.cpp.o"

# External object files for target 08_heatmaps_from_image.bin
08_heatmaps_from_image_bin_EXTERNAL_OBJECTS =

examples/tutorial_api_cpp/08_heatmaps_from_image.bin: examples/tutorial_api_cpp/CMakeFiles/08_heatmaps_from_image.bin.dir/08_heatmaps_from_image.cpp.o
examples/tutorial_api_cpp/08_heatmaps_from_image.bin: examples/tutorial_api_cpp/CMakeFiles/08_heatmaps_from_image.bin.dir/build.make
examples/tutorial_api_cpp/08_heatmaps_from_image.bin: src/openpose/libopenpose.so.1.7.0
examples/tutorial_api_cpp/08_heatmaps_from_image.bin: /usr/lib/aarch64-linux-gnu/libopencv_dnn.so.4.1.1
examples/tutorial_api_cpp/08_heatmaps_from_image.bin: /usr/lib/aarch64-linux-gnu/libopencv_gapi.so.4.1.1
examples/tutorial_api_cpp/08_heatmaps_from_image.bin: /usr/lib/aarch64-linux-gnu/libopencv_highgui.so.4.1.1
examples/tutorial_api_cpp/08_heatmaps_from_image.bin: /usr/lib/aarch64-linux-gnu/libopencv_ml.so.4.1.1
examples/tutorial_api_cpp/08_heatmaps_from_image.bin: /usr/lib/aarch64-linux-gnu/libopencv_objdetect.so.4.1.1
examples/tutorial_api_cpp/08_heatmaps_from_image.bin: /usr/lib/aarch64-linux-gnu/libopencv_photo.so.4.1.1
examples/tutorial_api_cpp/08_heatmaps_from_image.bin: /usr/lib/aarch64-linux-gnu/libopencv_stitching.so.4.1.1
examples/tutorial_api_cpp/08_heatmaps_from_image.bin: /usr/lib/aarch64-linux-gnu/libopencv_video.so.4.1.1
examples/tutorial_api_cpp/08_heatmaps_from_image.bin: /usr/lib/aarch64-linux-gnu/libopencv_videoio.so.4.1.1
examples/tutorial_api_cpp/08_heatmaps_from_image.bin: /usr/lib/aarch64-linux-gnu/libglog.so
examples/tutorial_api_cpp/08_heatmaps_from_image.bin: /usr/lib/aarch64-linux-gnu/libgflags.so
examples/tutorial_api_cpp/08_heatmaps_from_image.bin: /usr/lib/aarch64-linux-gnu/libopencv_calib3d.so.4.1.1
examples/tutorial_api_cpp/08_heatmaps_from_image.bin: /usr/lib/aarch64-linux-gnu/libopencv_features2d.so.4.1.1
examples/tutorial_api_cpp/08_heatmaps_from_image.bin: /usr/lib/aarch64-linux-gnu/libopencv_flann.so.4.1.1
examples/tutorial_api_cpp/08_heatmaps_from_image.bin: /usr/lib/aarch64-linux-gnu/libopencv_imgcodecs.so.4.1.1
examples/tutorial_api_cpp/08_heatmaps_from_image.bin: /usr/lib/aarch64-linux-gnu/libopencv_imgproc.so.4.1.1
examples/tutorial_api_cpp/08_heatmaps_from_image.bin: /usr/lib/aarch64-linux-gnu/libopencv_core.so.4.1.1
examples/tutorial_api_cpp/08_heatmaps_from_image.bin: /usr/local/cuda/lib64/libcudart_static.a
examples/tutorial_api_cpp/08_heatmaps_from_image.bin: /usr/lib/aarch64-linux-gnu/librt.so
examples/tutorial_api_cpp/08_heatmaps_from_image.bin: /usr/lib/aarch64-linux-gnu/libglog.so
examples/tutorial_api_cpp/08_heatmaps_from_image.bin: caffe/lib/libcaffe.so
examples/tutorial_api_cpp/08_heatmaps_from_image.bin: caffe/lib/libcaffe.so
examples/tutorial_api_cpp/08_heatmaps_from_image.bin: examples/tutorial_api_cpp/CMakeFiles/08_heatmaps_from_image.bin.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable 08_heatmaps_from_image.bin"
	cd /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build/examples/tutorial_api_cpp && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/08_heatmaps_from_image.bin.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
examples/tutorial_api_cpp/CMakeFiles/08_heatmaps_from_image.bin.dir/build: examples/tutorial_api_cpp/08_heatmaps_from_image.bin

.PHONY : examples/tutorial_api_cpp/CMakeFiles/08_heatmaps_from_image.bin.dir/build

examples/tutorial_api_cpp/CMakeFiles/08_heatmaps_from_image.bin.dir/clean:
	cd /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build/examples/tutorial_api_cpp && $(CMAKE_COMMAND) -P CMakeFiles/08_heatmaps_from_image.bin.dir/cmake_clean.cmake
.PHONY : examples/tutorial_api_cpp/CMakeFiles/08_heatmaps_from_image.bin.dir/clean

examples/tutorial_api_cpp/CMakeFiles/08_heatmaps_from_image.bin.dir/depend:
	cd /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0 /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/examples/tutorial_api_cpp /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build/examples/tutorial_api_cpp /home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/openpose/openpose-1.7.0/build/examples/tutorial_api_cpp/CMakeFiles/08_heatmaps_from_image.bin.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : examples/tutorial_api_cpp/CMakeFiles/08_heatmaps_from_image.bin.dir/depend

