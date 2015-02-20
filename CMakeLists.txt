cmake_minimum_required(VERSION 2.8.4)
project(VisionPorComputadora)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(OpenCV_DIR "/usr/local/Cellar/opencv/2.4.10.1/")
find_package(OpenCV REQUIRED core imgproc highgui video)
include_directories(${OpenCV_INCLUDE_DIRS})

set(SOURCE_FILES pr0.cpp)
set(SOURCE_FILES pr1.cpp)
add_executable(VisionPorComputadora ${SOURCE_FILES})
target_link_libraries(VisionPorComputadora ${OpenCV_LIBS})