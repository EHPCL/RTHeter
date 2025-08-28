cmake_minimum_required(VERSION 3.10)
project(HeterSchedulerSim)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
# uncomment the following two lines if you want to simulate the execution variation
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g")
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DVARI_PROC")
file(GLOB SOURCE_FILES ./src/cpp/*.cpp)
include_directories(${CMAKE_SOURCE_DIR}/src/cpp)

add_executable(main ${SOURCE_FILES} test/main.cpp)
target_link_libraries(  main )

target_compile_definitions(main PRIVATE)

# Execute the following command to generate the build directory
# cmake -S . -B build
