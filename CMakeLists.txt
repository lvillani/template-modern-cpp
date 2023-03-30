cmake_minimum_required(VERSION 3.22)

project(
  template-modern-cpp
  VERSION 0.0.0
  LANGUAGES CXX)

set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(spdlog REQUIRED)

add_subdirectory(src)
