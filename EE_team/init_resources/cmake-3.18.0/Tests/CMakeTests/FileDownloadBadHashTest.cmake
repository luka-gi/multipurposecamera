if(NOT "/home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/cmake-3.18.0/Tests/CMakeTests" MATCHES "^/")
  set(slash /)
endif()
set(url "file://${slash}/home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/cmake-3.18.0/Tests/CMakeTests/FileDownloadInput.png")
set(dir "/home/smartcam/Desktop/EE_code/multipurposecamera/EE_team/init_resources/cmake-3.18.0/Tests/CMakeTests/downloads")

file(DOWNLOAD
  ${url}
  ${dir}/file3.png
  TIMEOUT 2
  STATUS status
  EXPECTED_HASH SHA1=5555555555555555555555555555555555555555
  )
