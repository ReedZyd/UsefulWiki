## AGX_xavier
### Install Jetson Software with SDK Manager
1、准备一台Ubuntu Linux x64 Version 18.04 or 16.04电脑（Linux Host computer），需与Xavier在同一局域网下，并用type-c数据线连接。
2、在Linux Host computer上下载安装[NVIDIA SDK Manager](https://developer.nvidia.com/embedded/downloads#?search=NVIDIA%20SDK%20Manager)。
3、运行NVIDIA SDK Manager，选择需要下载部分（保持默认即可）。

NOTE!!!
会自动安装cuda，安装完成后只需要配置环境变量即可：

https://www.elinux.org/Jetson_Zoo#PyTorch_.28Caffe2.29

#### google-pinyin
sudo apt-get install fcitx fcitx-googlepinyin -y
https://blog.csdn.net/u013554213/article/details/82429113
### realsense camera 
https://github.com/IntelRealSense/realsense-ros
