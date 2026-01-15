cmake_minimum_required(VERSION 3.14)
project(my_benchmark)

# Add an option to select the function version, default to 1
option(FUNC_VERSION "Select function version to benchmark" 1)
message(STATUS "Benchmarking FUNC_VERSION=${FUNC_VERSION}")


include(FetchContent)
FetchContent_Declare(
  googlebenchmark
  GIT_REPOSITORY https://github.com/google/benchmark.git
  GIT_TAG v1.8.3
)
set(BENCHMARK_ENABLE_TESTING OFF CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googlebenchmark)

add_executable(bench main.cc bench.cc)

# Add the preprocessor definition to the target
target_compile_definitions(bench PRIVATE FUNC=${FUNC_VERSION})

target_link_libraries(bench benchmark::benchmark)

# with -O3 we could get faster execution but the disassembed code is longer and hard to read
target_compile_options(bench PRIVATE "-O1")
target_link_options(bench PRIVATE "-O1")
