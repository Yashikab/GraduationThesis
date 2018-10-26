project(coresets)
cmake_minimum_required(VERSION 3.0)

set(BOOST_ROOT /opt/boost_1_67_0)


### C++11
add_compile_options(-std=c++11)

### pkgconfig (for pkg_check_modules)
find_package(PkgConfig REQUIRED)

### Python includes
pkg_check_modules(PYTHON3 python3 REQUIRED)
include_directories(${PYTHON3_INCLUDE_DIRS})

### Boost includes
include_directories(${BOOST_ROOT}/include)
link_directories(${BOOST_ROOT}/lib)

### Build
add_library(coresets SHARED coresets.cpp)
set_target_properties(coresets PROPERTIES SUFFIX ".so")

target_link_libraries(coresets boost_numpy35 boost_python35)