# scout mini

https://github.com/agilexrobotics/scout_mini_ros

## Setup CAN-To-USB adapter 

1. Enable gs_usb kernel module
   
    ```shell
    sudo modprobe gs_usb
    ```

2. Bringup can device
   
   ```shell
   sudo ip link set can0 up type can bitrate 500000
   ```

3. If no error occured during the previous steps, you should be able to see the can device now by using command
   
   ```shell
   ifconfig -a
   ```

4. Install and use can-utils to test the hardware
   
    ```shell
    sudo apt install can-utils
    ```

5. Testing command
   
    ```shell
    # receiving data from can0
    candump can0
    # send data to can0
    cansend can0 001#1122334455667788
    ```

Two scripts inside the "scout_bringup/scripts" folder are provided for easy setup. You can run "./setup_can2usb.bash" for the first-time setup and run "./bringup_can2usb.bash" to bring up the device each time you unplug and re-plug the adapter.

## Basic usage of the ROS package

1. Install dependent ROS packages

    ```shell
    sudo apt install ros-melodic-teleop-twist-keyboard
    sudo apt-get install ros-melodic-joint-state-publisher-gui
    sudo apt install ros-melodic-ros-controllers
    sudo apt install ros-melodic-webots-ros
    ```

    Change ros-melodic-* in the command to ros-kinetic-* if you're using ROS Kinetic.


2. Clone the packages into your catkin workspace and compile

    (the following instructions assume your catkin workspace is at: ~/catkin_ws/src)

    ```shell
    cd ~/catkin_ws/src
    git clone https://github.com/agilexrobotics/scout_mini_ros.git
    cd ..
    catkin_make
    ```

3. Launch ROS nodes

* Start the base node for the real robot

    ```shell
    roslaunch scout_bringup scout_minimal.launch
    ```
