cmake_minimum_required(VERSION 3.10)

project(lsb_fast)

add_library(
    lsb_fast
    SHARED
    lsb_fast.cpp
)

set_target_properties(
    lsb_fast
    PROPERTIES
    PREFIX ""
    OUTPUT_NAME "lsb_fast"
)