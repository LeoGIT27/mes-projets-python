cmake_minimum_required(VERSION 3.20)
project(NotSoffiz LANGUAGES CXX)

add_executable(NotSoffiz WIN32 main.cpp)
target_compile_features(NotSoffiz PRIVATE cxx_std_17)
target_link_libraries(NotSoffiz PRIVATE gdiplus shell32)

add_custom_command(TARGET NotSoffiz POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_directory
            "${CMAKE_SOURCE_DIR}/assets"
            "$<TARGET_FILE_DIR:NotSoffiz>/assets")