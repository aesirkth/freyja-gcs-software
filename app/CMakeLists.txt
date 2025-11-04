cmake_minimum_required(VERSION 3.22)

set(BOARD_ROOT ${CMAKE_CURRENT_LIST_DIR})
set(BOARD freyja_gcs)

find_package(Zephyr)

project(freyja_gcs_fw)

target_sources(app PRIVATE 
    src/main.c
    src/usb_com.c
    src/can_com.c
    src/clock.c
)