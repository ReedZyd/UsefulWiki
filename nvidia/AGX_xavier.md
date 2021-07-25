## AGX_xavier

### Install Jetson Software with SDK Manager

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
默认选择安装cuda，安装完成后只需要在`~\.bashrc`配置环境变量即可，即添加：

https://www.elinux.org/Jetson_Zoo#PyTorch_.28Caffe2.29

#### google-pinyin
sudo apt-get install fcitx fcitx-googlepinyin -y
https://blog.csdn.net/u013554213/article/details/82429113
### realsense camera 
https://github.com/IntelRealSense/realsense-ros
