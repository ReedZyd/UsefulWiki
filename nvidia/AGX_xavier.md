# AGX_xavier

## 刷机

1、准备一台Ubuntu Linux x64 Version 18.04 or 16.04电脑（Linux Host computer），需与Xavier在同一局域网下，并下载安装[NVIDIA SDK Manager](https://developer.nvidia.com/embedded/downloads#?search=NVIDIA%20SDK%20Manager)。

2、Xavier断电状态下使用原装type-c数据线连接Linux Host computer。

3、在Linux Host computer上运行NVIDIA SDK Manager，取消勾选 Host Machine（这个是为主机下载安装文件的，如果想在主机上安装Nvida软件，可以勾选这个，实际上没必要），选择continue进行下一步。

4、选择下载和安装路径，默认即可；勾选 I accept 选项，不要勾选 Download now, install later 选项（可以但没必要）。

5、下载OS镜像，下载完成后配置Xavier账户名称并烧录镜像：
  * 选择 Manaul setup
  * 将 xavier 接通电源，但是保持关机状态
  * 用原装的 type-C 转 USB 线，将 xavier 正面的 type-C 接口与主机的 USB 3.0 接口相连
  * 先按住位于 xavier 侧面的正中间的强制恢复按钮不放，再按住开机按钮不放，等待 2 s 后同时松开。此时，可以看到 xavier 正面的白色电源指示灯亮起。
  * 打开主机的终端，输入 lsusb 命令，如果看到 NVidia Corp 则说明 xavier 与主机连接成功
  * 点击flash按钮烧录镜像。
6、保持Xavier和Linux Host computer连接，开启Xavier后换源：
  ```shell
  # 备份sources.list文件
  sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
  # 打开sources.list文件
  sudo gedit /etc/apt/sources.list
  # 删除原内容，添加下列内容
  deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-updates main restricted universe multiverse
  deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-updates main restricted universe multiverse
  deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-security main restricted universe multiverse
  deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-security main restricted universe multiverse
  deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-backports main restricted universe multiverse
  deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-backports main restricted universe multiverse
  deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic main universe restricted
  deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic main universe restricted
  # 更新
  sudo apt update
  sudo apt upgrade
  ```
 7、回到Linux Host Computer，输入账号密码，开始安装Cuda等软件。
 
NOTE!!!
* 注意NVIDIA的板子是ARM架构，安装一些软件时要选择合适的安装包。
 * 没有ARM架构的安装包：西游、搜狗拼音
 * 最新的可以支持ARM：anaconda
 * 有ARM安装包：google
* 默认选择安装cuda，安装完成后只需要在`~\.bashrc`配置环境变量即可，即添加：
 ```bash
 export CUDA_HOME=/usr/local/cuda-10.2
 export LD_LIBRARY_PATH=/usr/local/cuda-10.2/lib64:$LD_LIBRARY_PATH
 export PATH=/usr/local/cuda-10.2/bin:$PATH
 ```
 * Xavier不需要安装驱动，用不了nvidia-smi
 * 最新的anaconda可以使用了，但没必要！刷机后自带python2.7、python3.6，需要自己安装pip3
 * 默认自带opencv4(2021.07.25)

## 安装pip、torch、其他pypi三方库等
Note!!! 建议直接安装pip3和其他三方库，不要用anaconda
### 下载pip3：
```shell
sudo apt-get install libopenblas-base libopenmpi-dev python3-pip
```
### 安装torch
注意torch必须按xavier[官方教程](https://www.elinux.org/Jetson_Zoo)安装:
* 从官方教程网站上下载torch-1.6.0-cp36-cp36m-linux_aarch64.whl
* 安装：
```shell
pip3 install Cython
pip3 install numpy torch-1.6.0-cp36-cp36m-linux_aarch64.whl
```
* 常遇到Pillow编译不了，需要按照[Pillow官网](https://pillow.readthedocs.io/en/stable/installation.html)手动安装：
```shell
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow
```
### 其他pypi三方库
大部分直接用pip3安装即可，常见Pillow报错，解决方法同上

## 安装ros和部分ros包
### ros：
按照[官方教程](https://www.elinux.org/Jetson_Zoo#ROS)安装：
 ```shell
 # install ROS Melodic
 sudo apt-add-repository universe
 sudo apt-add-repository multiverse
 sudo apt-add-repository restricted

 # add ROS repository to apt sources
 sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'$ sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

 # install ROS Base
 sudo apt-get update
 sudo apt-get install ros-melodic-ros-base

 # add ROS paths to environment
 sudo sh -c 'echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc'
 ```
建议ros包用源码安装，不知道为什么apt安装经常出错
### 安装cv2_bridge
Note!!!注意如果要用python3，编译的时候要手动配置，以下以手动编译与**python3**、**opencv4**兼容的cv2_bridge为例
* 准备
```shell
# 安装依赖
sudo apt-get install python-catkin-tools python3-dev python3-catkin-pkg-modules python3-numpy python3-yaml ros-melodic-cv-bridge
# 创建工作空间
mkdir -p ~/catkin_ws/src
# 初始化工作空间
cd ~/catkin_ws && catkin init
```
* 配置python3
```shell
# 设置cmake变量（以python3.6为例），注意最后一项（x86架构：x86_64_linux-gnu文件夹，aarch64架构：aarch64-linux-gnu文件夹）
catkin config -DPYTHON_EXECUTABLE=/usr/bin/python3 -DPYTHON_INCLUDE_DIR=/usr/include/python3.6m -DPYTHON_LIBRARY=/usr/lib/aarch64-linux-gnu/libpython3.6m.so
catkin config --install
```
* 下载源码
```
cd ~/catkin_ws/src
git clone https://github.com/ros-perception/vision_opencv.git
# 查找cv_bridge版本
apt-cache show ros-melodic-cv-bridge | grep Version
# checkout指定版本（以1.13.0为例）
cd vision_opencv/
git checkout 1.13.0
```

* 配置opencv4要求，一般默认3
https://github.com/ros-perception/vision_opencv/issues/272#issuecomment-471311300
1. Add set (CMAKE_CXX_STANDARD 11) to your top level cmake
2. `vision_opencv/cv_bridge/CMakeLists.txt`16行改为`find_package(OpenCV 4 REQUIRED`
3. `vision_opencv/cv_bridge/src/CMakeLists.txt`35行改为`if (OpenCV_VERSION_MAJOR VERSION_EQUAL 4)`
4. `vision_opencv/cv_bridge/src/module_opencv3.cpp`中改两处：
1) `UMatData* allocate(int dims0, const int* sizes, int type, void* data, size_t* step, int flags, UMatUsageFlags usageFlags) const`改为`UMatData* allocate(int dims0, const int* sizes, int type, void* data, size_t* step, AccessFlag flags, UMatUsageFlags usageFlags) const`
2) `bool allocate(UMatData* u, int accessFlags, UMatUsageFlags usageFlags) const`改为`bool allocate(UMatData* u, AccessFlag accessFlags, UMatUsageFlags usageFlags) const`

* 编译
```shell
cd ../..
catkin build
# 将功能包加到扩展环境中，可以选择每次手动source，也可以把source添加到~/.bashrc中
source install/setup.bash --extend
```

#### google-pinyin
sudo apt-get install fcitx fcitx-googlepinyin -y
https://blog.csdn.net/u013554213/article/details/82429113
### realsense camera 
https://github.com/IntelRealSense/realsense-ros
