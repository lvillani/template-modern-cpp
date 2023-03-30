add_executable(app main.cpp)

target_link_libraries(app spdlog::spdlog project_version)
