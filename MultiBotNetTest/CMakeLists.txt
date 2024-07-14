cmake_minimum_required(VERSION 3.8)
project(packets_msgs)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(packets_msgs REQUIRED) 
find_package(builtin_interfaces REQUIRED)

# # Include Cpp "include" directory
# include_directories(include)

# # Add executables
# add_executable(listener src/JitterPlotter_1stRef.py)


# # Install executables
# install(TARGETS
#     listener
#     DESTINATION lib/${PROJECT_NAME}
# )

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Packet.msg"
  DEPENDENCIES builtin_interfaces
)

# Install Python modules
# ament_python_install_package(${PROJECT_NAME})


# Install Python modules
install(
    PROGRAMS
    src/JitterPlotter_1stRef.py
    src/CollectThenCompute.py
    src/talker_qos.py
    src/IncrementalErrorProof.py
    DESTINATION lib/${PROJECT_NAME}
)

# if(BUILD_TESTING)
#   find_package(ament_lint_auto REQUIRED)
#   # the following line skips the linter which checks for copyrights
#   # comment the line when a copyright and license is added to all source files
#   set(ament_cmake_copyright_FOUND TRUE)
#   # the following line skips cpplint (only works in a git repo)
#   # comment the line when this package is in a git repo and when
#   # a copyright and license is added to all source files
#   set(ament_cmake_cpplint_FOUND TRUE)
#   ament_lint_auto_find_test_dependencies()
# endif()



ament_package()
