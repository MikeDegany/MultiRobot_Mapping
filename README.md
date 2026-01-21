# Networking in Collaborative Multi-Robot Systems for Enhanced Mapping and Navigation

## Table of Contents
1. [Introduction](#introduction)
2. [System Overview](#system-overview)
3. [Hardware Setup](#hardware-setup)
4. [Software Architecture](#software-architecture)
5. [Networking](#networking)
6. [Mapping](#mapping)
7. [Navigation](#navigation)
8. [Experimental Setup](#experimental-setup)
9. [Conclusion](#conclusion)

<sub><sup>To jump straight into the implementation setup go to [Experimental Setup](#experimental-setup)</sup></sub>

## Introduction

This project is to implement Mapping and Navigation with multiple robots, meeting the growing need for efficient coordination in real-world tasks. It uses ROS2 and DDS for communication and data sharing between robots.

## System Overview

The system consists of multiple mobile robots interconnected via a Wi-Fi network, with a central PC handling the mapping and navigation tasks. The robots employ a Graph-based SLAM technique, integrating localized laser scans to construct and optimize a pose graph for a collaborative map.

![System Overview](docs/media/multirobotSetup.png "System Overview")

## Hardware Setup

- Multiple TurtleBot4 Standard robots
- Fast and Powerful WiFi Router
- Central computer for data processing
Each robot is equipped with:
- iRobot Create3 mobile base
- Raspberry Pi 4B
- 2D LIDAR sensors
-  Wi-Fi card (iRobot Create3 only supports 2.4 GHz)

## Software Architecture

The software stack includes:
1. ROS2 for robot control and communication
2. DDS (Simple Discovery protocol) for efficient data distribution
3. DDS Domain ID bridge
4. SLAM-Toolbox for mapping
5. ROS2 navigation stack for autonomous navigation


## Mapping

The system uses a Graph-based SLAM approach:
1. Robots equipped with 2D laser sensors
2. Localized laser scans
3. Pose graph creation
4. Map optimization

![Mapping Hierarchy](docs/media/MappingHierarchy.png)

Multiple robots share pose graphs to create a collaborative map.

## Navigation

The ROS NAV2 navigation stack is integrated for autonomous navigation:
- Path planning
- Obstacle avoidance
- Integration with SLAM systems

The navigation stack allows robots to navigate through dynamic environments and adapt to real-time changes.

## Experimental Setup

To set up multiple robots, begin by configuring a single robot. The TurtleBot 4 User Manual provides an excellent guide for this process: [TurtleBot 4 User Manual](https://turtlebot.github.io/turtlebot4-user-manual/).

This tutorial uses ROS2 Humble and includes portions adapted from the original TurtleBot 4 manual.

### Setting Up Multiple Robots

Once you've set up a single robot and mastered mapping and navigation, it's time to configure multiple robots.

By default, each TurtleBot 4 uses the same [topic, action, and service names](../software/turtlebot4_common.md#ros-2-interfaces) for communication. If two default TurtleBot 4 robots are connected to the same network, their topics will interfere with each other, leading to unwanted behaviors.

There are two primary methods for running multiple TurtleBot 4 robots on a single network: **ROS_DOMAIN_ID** and **namespacing**. In this project, we will use both approaches together to make it functional.



## ROS_DOMAIN_ID

The **ROS_DOMAIN_ID** is an environment variable used in ROS 2 to change the ports that ROS 2 processes use for communication. This effectively allows us to separate different ROS 2 processes from communicating with each other on the same network. For a detailed explanation, click [here](https://docs.ros.org/en/galactic/Concepts/About-Domain-ID.html).

We can leverage this by assigning a unique **ROS_DOMAIN_ID** to each of our robots. This will ensure that communication between robots does not occur. The **ROS_DOMAIN_ID** can be set to any value between 0 and 101, inclusively.

### Setting the environment variable

There are four locations in which the **ROS_DOMAIN_ID** environment variable must be set:
 - Create® 3
 - RPi4 Terminal
 - RPi4 Robot Upstart Job
 - User PC


SSH into your TurtleBot 4 and run the turtlebot4 setup tool:

```bash
turtlebot4-setup
```

Navigate to 'Bash Setup' in the 'ROS Setup' menu, then change your `ROS_DOMAIN_ID`. Save the settings, then apply settings in the main menu.

<figure class="aligncenter">
    <img src="https://github.com/turtlebot/turtlebot4-user-manual/blob/gh-pages/tutorials/media/domain_id.gif" alt="ROS_DOMAIN_ID" style="width: 100%"/>
    <figcaption>Setting the ROS_DOMAIN_ID</figcaption>
</figure>

This will apply the new `ROS_DOMAIN_ID` to the Create3®, RPi4 Terminal, and RPi4 Robot Upstart job.

On the user PC, set the `ROS_DOMAIN_ID` in your *setup.bash* file and source it. See [Installing ROS 2](../setup/basic.md#installing-ros-2) for more details.


Once the Create® 3 application has restarted, try calling `ros2 topic list` on both your PC and the RPi4 to ensure that all topics are visible.


## Namespacing

Namespacing is a method of adding a prefix to topic names to group certain topics, or to make them unique. 
By namespacing all topics on a TurtleBot 4, we can have a full set of unique topics for that robot. This allows
us to run multiple robots on the same `ROS_DOMAIN_ID`.

It is common to use the name of the robot as the namespace. For example, 
if we have a robot named `robot1`, the namespaced topics would look like:

```bash
ubuntu@ubuntu:~$ ros2 topic list
/parameter_events
/TB1/battery_state
/TB1/cmd_audio
/TB1/cmd_lightring
/TB1/cmd_vel
/TB1/diagnostics
/TB1/dock_status
/TB1/function_calls
/TB1/hazard_detection
/TB1/imu
/TB1/interface_buttons
/TB1/ip
/TB1/ir_intensity
/TB1/ir_opcode
/TB1/joint_states
/TB1/joy
/TB1/joy/set_feedback
/TB1/kidnap_status
/TB1/mobility_monitor/transition_event
/TB1/mouse
/TB1/odom
/TB1/robot_description
/TB1/robot_state/transition_event
/TB1/scan
/TB1/slip_status
/TB1/static_transform/transition_event
/TB1/stop_status
/TB1/tf
/TB1/tf_static
/TB1/wheel_status
/TB1/wheel_ticks
/TB1/wheel_vels
/rosout
```

Namespacing is not supported in Galactic.


To set the robot namespace, SSH into your TurtleBot 4 and run the turtlebot4 setup tool:

```bash
turtlebot4-setup
```

Navigate to 'Bash Setup' in the 'ROS Setup' menu, then change the `ROBOT_NAMESPACE` setting. 
Save the settings, then apply settings in the main menu.

<figure class="aligncenter">
    <img src="https://github.com/turtlebot/turtlebot4-user-manual/blob/gh-pages/tutorials/media/namespace.gif" alt="namespace" style="width: 100%"/>
    <figcaption>Setting the robot namespace</figcaption>
</figure>

This will apply the new namespace to the Create® 3, RPi4 Terminal, and RPi4 Robot Upstart job.


### Domain Bridge


Assigning separate ROS_DOMAIN_IDs to the devices in the network will have several benefits, but the PC cannot see the robots in the networks, means the PC cannot subscribe to the topics published by robots. Therefore, we need to use a bridge to transform data from a DOMAIN_ID to another. 
This would be done using [domain_bridge](https://github.com/ros2/domain_bridge), a ROS 2 domain bridge. Bridges ROS communication between different ROS domain IDs. Read the document to be familiar with how domain bridge works. 

Run the following commands to install the domain_bridge: 

```bash
mkdir -p domain_bridge_ws/src 

cd domain_bridge_ws 

git clone –b humble https://github.com/ros2/domain_bridge.git src/ 

colcon build 
```

You must provide the path to a YAML configuration file as the last argument to the executable. when running the domain_bridge which has been provided in domain_bridge folder for this project. 

![Mapping Hierarchy](docs/media/DomainBridge.png)


### Multi-robot SLAM

Mutlirobot SLAM is to map the environment collaboratively using multiple robots and generate a collaborative map of the environment. To do so, you should install the following SLAM package which has been gotten from [here](https://github.com/SteveMacenski/slam_toolbox/pull/592)
```bash
mkdir -p multirobot_slam/src 

cd multirobot_slam 

git clone https://github.com/MikeDegany/multislam_toolbox.git src/ 

colcon build 
```

After you install the package you need to change the following parameters: 

In config.xml change ```base_frame``` to ```base_link```
In .launch file change ```/scan``` to ```scan```


 -### Setup Multirobot Mapping and Navigation

Now that you have installed the reqyured packages on the system. You are ready to run the project: 

- #### Robots should be off
All Turtlebot4 robots should be off at the beginning. 
- #### Run domain_bridge on the PC
```bash
cd domain_bridge_we 

source install/setup.bash  

ros2 run domain_bridge domain_bridge [path to the config file] (exampler: src/examples/test_bridge.yaml) 
```
- Turn on the Robots
Plug the Turtlebots into dock station to turn on 
wait until all [TB_NAMESPACE]/odom and -TB_NAMESPACE/scan topics appear. We have chosen TB1, TB2, etc for the robots.

- #### Run SLAM, NAV, and RVIZ for each robot separately
```bash 
Terminal 1, launch multirobot_slam: 

cd multirobot_slam 

source install/setup.bash 

ros2 launch slam_toolbox online_async_multirobot_launch.py namespace:=[NAMESPACE OF TB] 

 

Terminal 2, launch Nav2: 

Ros2 launch turtlebot4_navigation nav2.launch.py namespace:=[NAMESPACE OF TB] 

 

Terminal 3, launch RViz:   

ros2 launch turtlebot4_viz view_robot.launch.py namespace:=[NAMESPACE OF TB] 
```





### Viewing the Robot in RViz

On the user PC, `turtlebot4_desktop` launch files can use a `namespace` argument to view a specific robot:

```bash
ros2 launch turtlebot4_viz view_model.launch.py namespace:=/TB1
```

### Launching Robots in Simulation

The first robot can be launched normally, with the addition of a `namespace`. All other parameters are still available as shown below:

```bash
ros2 launch turtlebot4_ignition_bringup turtlebot4_ignition.launch.py namespace:=/TB1 nav2:=true slam:=false localization:=true rviz:=true
```

Any additional robots must be launched using the `turtlebot4_spawn` launch file, a unique `namespace` and a unique spawn location:

```bash
ros2 launch turtlebot4_ignition_bringup turtlebot4_spawn.launch.py namespace:=/TB2 x:=0.0 y:=1.0 nav2:=true slam:=false localization:=true rviz:=true
```

### Launching Navigation

The SLAM, Localization and Nav2 launch files all support namespacing and can be launched as follows:

```bash
ros2 launch turtlebot4_navigation slam.launch.py namespace:=/TB1
ros2 launch turtlebot4_navigation localization.launch.py map:=office.yaml namespace:=/TB1
ros2 launch turtlebot4_navigation nav2.launch.py namespace:=/TB1
```

Replace `TB1` with the desired robot namespace. 





Experiments were conducted to evaluate the performance and efficiency of the multi-robot mapping and navigation system in an indoor environment.

In order to evaluate the network, the python scripts provided in MultiBotNetTest could be run. You create the package on robots and the PC, then run _publisher.py_ on a robot/robots and _plot.py_ on the PC. You can try different scenarios depending on your evaluation desires. 

## Future Work
 - Implement the networking system using Zenoh

## Conclusion

This project successfully addressed the challenges of mapping and navigation with multiple robots through a comprehensive approach encompassing networking, mapping, and navigation. The system demonstrates the feasibility and potential applications of multi-robot systems in various real-world scenarios.
