cmake_minimum_required(VERSION 3.13)

include(pico_sdk_import.cmake)

project(button_midi C CXX ASM)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
pico_sdk_init()

add_executable(button_midi
  button_midi.c
  usb_descriptors.c
)

pico_enable_stdio_usb(button_midi 0)
pico_enable_stdio_uart(button_midi 1)

target_include_directories(button_midi PRIVATE ${CMAKE_CURRENT_LIST_DIR})

pico_add_extra_outputs(button_midi)
target_link_libraries(button_midi PRIVATE pico_stdlib tinyusb_device tinyusb_board)
