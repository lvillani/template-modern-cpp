configure_file(project_version.cpp.in project_version.cpp @ONLY)

add_library(project_version STATIC ${CMAKE_CURRENT_BINARY_DIR}/project_version.cpp)

target_include_directories(project_version PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_include_directories(project_version PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/..)
