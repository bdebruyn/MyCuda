cmake_minimum_required(VERSION 3.15 FATAL_ERROR)
include(/opt/modules/Azul3D.cmake)

cmake_policy(SET CMP0012 NEW)
get_filename_component(target ${CMAKE_CURRENT_SOURCE_DIR} NAME)

message(STATUS "=================================================================================")
message(STATUS "BUIDING REPO ${target}")
message(STATUS "=================================================================================")

project(${target} C CXX)

#   #
#   # -- cannot run a simple executable using hpc++. Disable compiler check
#   #
#   set(CMAKE_CUDA_COMPILER_WORKS 1)
#   #
#   # -- No clue if this actually does anything
#   #
#   include(/opt/nvidia/hpc_sdk/Linux_x86_64/22.5/cmake/NVHPCConfig.cmake)
#   #
#   # -- appears library paths must be manually set for hpc 22.5
#   #
#   project(${target} C CXX CUDA)
#   #
#   # -- appears library paths must be manually set for hpc 22.5
#   #
#   set(HPC_LIB_PATH
#      /opt/nvidia/hpc_sdk/Linux_x86_64/22.5/comm_libs/hpcx/hpcx-2.11/ompi/lib
#      /opt/nvidia/hpc_sdk/Linux_x86_64/22.5/comm_libs/hpcx/hpcx-2.11/nccl_rdma_sharp_plugin/lib
#      /opt/nvidia/hpc_sdk/Linux_x86_64/22.5/comm_libs/hpcx/hpcx-2.11/sharp/lib
#      /opt/nvidia/hpc_sdk/Linux_x86_64/22.5/comm_libs/hpcx/hpcx-2.11/hcoll/lib
#      /opt/nvidia/hpc_sdk/Linux_x86_64/22.5/comm_libs/hpcx/hpcx-2.11/ucc/lib/ucc
#      /opt/nvidia/hpc_sdk/Linux_x86_64/22.5/comm_libs/hpcx/hpcx-2.11/ucc/lib
#      /opt/nvidia/hpc_sdk/Linux_x86_64/22.5/comm_libs/hpcx/hpcx-2.11/ucx/mt/lib/ucx
#      /opt/nvidia/hpc_sdk/Linux_x86_64/22.5/comm_libs/hpcx/hpcx-2.11/ucx/mt/lib
#      /opt/nvidia/hpc_sdk/Linux_x86_64/22.5/comm_libs/nvshmem/lib
#      /opt/nvidia/hpc_sdk/Linux_x86_64/22.5/comm_libs/nccl/lib
#      /opt/nvidia/hpc_sdk/Linux_x86_64/22.5/math_libs/lib64
#      /opt/nvidia/hpc_sdk/Linux_x86_64/22.5/compilers/lib
#      /opt/nvidia/hpc_sdk/Linux_x86_64/22.5/compilers/extras/qd/lib
#      /opt/nvidia/hpc_sdk/Linux_x86_64/22.5/cuda/extras/CUPTI/lib64
#      /opt/nvidia/hpc_sdk/Linux_x86_64/22.5/cuda/lib64
#      /opt/nvidia/hpc_sdk/Linux_x86_64/22.5/comm_libs/hpcx/latest/hcoll/lib
#      /opt/nvidia/hpc_sdk/Linux_x86_64/22.5/comm_libs/hpcx/latest/ompi/lib
#      /opt/nvidia/hpc_sdk/Linux_x86_64/22.5/comm_libs/hpcx/latest/nccl_rdma_sharp_plugin/lib
#      /opt/nvidia/hpc_sdk/Linux_x86_64/22.5/comm_libs/hpcx/latest/sharp/lib
#      /opt/nvidia/hpc_sdk/Linux_x86_64/22.5/comm_libs/hpcx/latest/ucx/mt/lib
#      /opt/nvidia/hpc_sdk/Linux_x86_64/22.5/comm_libs/hpcx/latest/ucx/mt/lib/ucx
#   )

# set(CMAKE_VERBOSE_MAKEFILE ON)

if (CMAKE_CROSSCOMPILING)
   set(THREADS_PTHREAD_ARG "2" CACHE STRING "Forcibly set by CMakeLists.txt." FORCE)
endif()

message(STATUS "CMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER}")

if (SDK)
   list(APPEND libraries "boost_chrono")
   # only need CMAKE_TOOLCHAIN_FILE and all the options are set
   set(CMAKE_TOOLCHAIN_FILE "OEToolchainConfig.cmake")
   message(STATUS "Using SDK")
endif ()

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Conan setup
include(${PROJECT_SOURCE_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

# required for "YouCompleteMe". Only works for "Unix Makefiles" and "Ninja"
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# place binaries and libraries according to GNU standards
include(GNUInstallDirs)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_LIBDIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_LIBDIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_BINDIR})

set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -O0 -Wfatal-errors -fno-omit-frame-pointer")
set(CMAKE_COLOR_MAKEFILE ON)
enable_testing()

# Added for External Projects
include(ExternalProject)

set(CMAKE_DEBUG_POSTFIX "")
message(STATUS CMAKE_DEBUG_POSTFIX IS ${CMAKE_DEBUG_POSTFIX})
message(STATUS CMAKE_PREFIX_PATH IS ${CMAKE_PREFIX_PATH})
message(STATUS CMAKE_FIND_ROOT_PATH is ${CMAKE_FIND_ROOT_PATH})

message(STATUS "ALL_LIBS_SHARED=${ALL_LIBS_SHARED}")

if (ALL_LIBS_SHARED)
   set(LIB_TYPE "SHARED")
else()
   set(LIB_TYPE "STATIC")
endif()

set(CMAKE_CXX_FLAGS "-Wall -Wno-deprecated")
set(CMAKE_C_FLAGS "-Wall -Wno-deprecated")

# For now, install in local self-contained directory, not on system
# TODO: System install paths if ${CMAKE_INSTALL_PREFIX} = /usr or /usr/local
    set(INSTALL_ROOT      ".")                      # ./
    set(INSTALL_CMAKE     "cmake")                  # ./cmake
    set(INSTALL_EXAMPLES  ".")                      # ./
    set(INSTALL_DATA      ".")                      # ./
    set(INSTALL_BIN       ".")                      # ./
    set(INSTALL_SHARED    "lib")                    # ./lib
    set(INSTALL_LIB       "lib")                    # ./lib
    set(INSTALL_INCLUDE   "include")                # ./include
    set(INSTALL_DOC       "doc")                    # ./doc
    set(INSTALL_SHORTCUTS "misc")                   # ./misc
    set(INSTALL_ICONS     "misc")                   # ./misc
    set(INSTALL_INIT      "misc")                   # ./misc

# Set runtime path
set(CMAKE_SKIP_BUILD_RPATH            FALSE) # Add absolute path to all dependencies for BUILD
set(CMAKE_BUILD_WITH_INSTALL_RPATH    FALSE) # Use CMAKE_INSTALL_RPATH for INSTALL, NOT BUILD
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH FALSE) # Do NOT add path to dependencies for INSTALL

# Find libraries relative to binary if we're not building for the appareo GW300.
if (NOT CMAKE_CROSSCOMPILING)
   set(CMAKE_INSTALL_RPATH "$ORIGIN/${INSTALL_LIB}")
endif()

#-----------------------------------------------------------------------------
# Boost settings
#-----------------------------------------------------------------------------

SET(Boost_USE_STATIC_LIBS ON)

#-----------------------------------------------------------------------------
# Debug and warnings
#-----------------------------------------------------------------------------

if (DEBUG)
   set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DDEBUG -g")
   set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -DDEBUG -g")
endif()

if (WARNINGS_AS_ERRORS)
   set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Werror")
   set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Werror")
endif()

if (MINGW)
   set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -static-libstdc++ -static -Wl,-allow-multiple-definition")
   set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -static-libgcc")
endif()

#-----------------------------------------------------------------------------
#  Common External Libraries 
#-----------------------------------------------------------------------------

if (UNIX)
   list(APPEND EXTERNAL_LIBS "pthread" "rt")
endif()

#-----------------------------------------------------------------------------
# set the path to the output directory 
#-----------------------------------------------------------------------------

if(${XTRA_MSGS})
   message(STATUS "EXTERNAL_INCLUDE_PATH = ${EXTERNAL_INCLUDE_PATH}")
   message(STATUS "EXTERNAL_LIBS =         ${EXTERNAL_LIBS}")
   message(STATUS "EXTERNAL_LIB_PATH =     ${EXTERNAL_LIB_PATH}")
endif()

get_filename_component(repo_name ${CMAKE_CURRENT_SOURCE_DIR} NAME)

if (EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/src")
   add_subdirectory(src)
else()
   message(STATUS "NOT FOUND: ${CMAKE_CURRENT_SOURCE_DIR}/src")
endif()

if (EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/tests")
   add_subdirectory(tests)
else()
   message(STATUS "NOT FOUND: ${CMAKE_CURRENT_SOURCE_DIR}/tests")
endif()

if (EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/apps")
   add_subdirectory(apps)
else()
   message(STATUS "NOT FOUND: ${CMAKE_CURRENT_SOURCE_DIR}/apps")
endif()

if (EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/deploySchema")
   add_subdirectory(deploySchema)
else()
   message(STATUS "NOT FOUND: ${CMAKE_CURRENT_SOURCE_DIR}/deploySchema")
endif()

