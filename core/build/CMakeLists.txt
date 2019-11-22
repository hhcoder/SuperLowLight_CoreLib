cmake_minimum_required(VERSION 2.8.11)
project(AI_SUPER_NIGHT_SHOT)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS "-O3 -g -Wall -fno-rtti")

# set(HALIDE_ROOT_DIR "../../external/Halide/")
# set(HALIDE_GEN_DIR "../../build/")

# if(" ${HALIDE_ROOT_DIR}" STREQUAL " ")
#     message( FATAL_ERROR "Specify HALIDE_ROOT_DIR variable in the cmake file." )
# endif()

set(src_files
    process.cpp
    )

# include_directories(${HALIDE_ROOT_DIR}/include ${HALIDE_GEN_DIR})
# link_directories(${HALIDE_ROOT_DIR}/bin)
# link_directories(${HALIDE_GEN_DIR})
#
# add_executable(nr ${src_files})

target_link_libraries(nr Halide libabnr_gen.a)

