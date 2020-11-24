# Ubuntu装机

## 制作启动盘

镜像源：https://mirrors.tuna.tsinghua.edu.cn/ubuntu-releases/16.04/

ps：最好上官网下载

下载：ubuntu-16.04.6-desktop-amd64.iso /server版需要自己装ubuntu-desktop
使用UltraISO：打开iso文件—启动—写入硬盘映像

## 分区
下载时选择something else, 分区如下（500G+2T）
> 512M efi \
> 460G / \
> 5G /boot \
> 2T /home 

如果没有efi选项，更换进入系统时选择的启动位置
进入空系统后分辨率过低是正常现象，是由于未安装驱动所致。

## 安装ssh和远程桌面
### 安装ssh

```shell
sudo apt install openssh-server
sudo service ssh start
sudo service ssh status
```

### 安装远程桌面
#### 16.04安装：
```shell
sudo apt-get install xrdp  #安装xrdp 
sudo apt-get install xubuntu-desktop -f #安装xubuntu-desktop
sudo vim /etc/xrdp/startwm.sh
# 把最下面的test和exec两行注释掉，添加一行xfce4-session
# 以上操作相当于给每个用户echo xfce4-session >~/.xsession
sudo service xrdp restart
sudo reboot
```
全灰屏，鼠标是个叉，可能是因为xrdp版本低，参考：
https://netdevops.me/2017/installing-xrdp-0.9.1-on-ubuntu-16.04-xenial/

#### 18.04安装：
##### 方法一（推荐）
参考：https://blog.csdn.net/fancyboyhou/article/details/105170696
```shell
wget http://www.c-nergy.be/downloads/xrdp-installer-1.1.zip
unzip xrdp-installer-1.1.zip
chmod +x 777 ./xrdp-installer-1.1.sh 
sudo ./xrdp-installer-1.1.sh 
```

1、如已经安装过XRDP，请先删除后再执行安装脚本。
```shell
sudo ./xrdp-installer-1.1.sh -r # 删除xrdp软件包
```

2、用户在系统上远程登录，将无法在本地登录，反之，在本地登录将不能远程登录。
##### 方法二
```shell
wget http://www.c-nergy.be/downloads/install-xrdp-3.0.zip
unzip install-xrdp-3.0.zip
chmod 777 Install-xrdp-3.0.sh
./Install-xrdp-3.0.sh
```

没有共享剪切板也是因为版本低（官方Ubuntu16.04的源里只有0.6.1-2的版本）
没有菜单栏、tab补全等：https://www.cnblogs.com/defineconst/p/10254613.html

### 配置
#### 全新机器需要设置端口转发，eg: hiwifi.com 互联网-超级端口转发
#### 不是新机器设置静态ip
##### Ubuntu16.04
- 1、查询网络接口的名字
打开命令行，输入`ifconfig`,第一行最左边的名字，就是本机的网络接口，如enp5s0 
- 2、打开修改文件
	`sudo vim /etc/network/interfaces`
	添加：
	> auto enp5s0 # 使用的网络接口，之前查询接口是为了这里  
	> iface enp5s0 inet static // enp5s0这个接口，使用静态ip设置  
	> address 192.168.199.105 // 设置ip地址  
	> netmask 255.255.255.0 // 设置子网掩码  
	> network 192.168.199.255
	> gateway 192.168.199.1 // 设置网关  
	> dns-nameservers 114.114.114.114 // 设置dns服务器地址
- 3、sudo reboot
##### Ubuntu18.04
`sudo vim /etc/netplan/*.yaml`
```
network:
	ethernets:
		enp5s0: #配置的网卡名称,使用ifconfig查看
			addresses: [192.168.199.105/24] #设置IP及掩码
			gateway4: 192.168.199.1 #设置网关
			nameservers:
				addresses: [114.114.114.114, 8.8.8.8] #设置DNS
			version: 2
```
`sudo netplan apply`

#### 固件错误Possible missing firmware解决: 
##### 1、进入如下这个地址，固件文件非常全面，找到适合自己的版本
https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/tree/rtl_nic/
##### 2、切换到刚才报缺少固件的目录，下载对应的文件内容，
```shell
cd /lib/firmware/rtl_nic/
sudo wget https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/tree/rtl_nic/rtl8125a-3.fw
```
## 安装Cuda、Cudnn、英伟达驱动

注意⚠️ 3090只支持455及以上驱动，建议使用pytorch时安装cuda11.0，455驱动。
```shell
pip install torch==1.7.0+cu110 torchvision==0.8.1+cu110 torchaudio===0.7.0 -f https://download.pytorch.org/whl/torch_stable.html
```

### Cuda、驱动推荐安装方式
> 1、在官网下载需要版本的Cuda文件（`*.run`）\
> 2、禁用nouveau第三方驱动，进入命令行界面，禁用图形界面（具体操作见驱动安装部分）\
> 3、运行`.run`文件，选择安装Cuda、驱动等（Sample、Demo、Document不需要安装）\
> 4、重启图形界面（具体操作见驱动安装部分）
> 5、添加环境变量（具体操作见安装Cuda 10.1部分）

### 安装Cudnn10.0
有时候需要改名： solitairetheme8-->tgz
```shell
tar -zxvf xxx.tgz 
sudo cp cuda/include/cudnn.h /usr/local/cuda/include/
sudo cp cuda/lib64/libcudnn* /usr/local/cuda/lib64/ -d
```
查看CUDA版本`cat /usr/local/cuda/version.txt`

查看 CUDNN 版本：
```shell
cat /usr/local/cuda/include/cudnn.h | grep CUDNN_MAJOR -A 2
```
或：
```shell
# 新版本cudnn中cudnn.h不再包含版本信息，版本信息包含在cudnn_version.h文件内
find / -name cudnn_version.h 2>&1 | grep -v "Permission denied" # 查找cudnn_version.h文件
cat /usr/local/cuda/include/cudnn_version.h | grep CUDNN_MAJOR -A 2  # 路径需要替换为上述命令搜索到的文件路径
```

### 其它安装（不推荐，只作参考）
#### 驱动安装
##### 1、禁用nouveau第三方驱动
`sudo gedit /etc/modprobe.d/blacklist.conf`

在最后一行添加：blacklist nouveau
```shell
sudo update-initramfs -u # 对所有内核版本操作 加 -k all
sudo reboot
```
##### 2、重启后按Ctrl+Alt+F1 进入命令行界面
执行命令：lsmod | grep nouveau 查看是否禁用,无反应则已禁用
禁用图形界面：
```shell
sudo service lightdm stop # 关闭桌面 
sudo service lightdm start # 开启桌面
```
或（未装桌面管理器时）：
```shell
sudo systemctl set-default multi-user.target # 关闭桌面
sudo systemctl set-default graphical.target # 开启桌面
```

##### 3、安装驱动
```shell
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt-get update
ubuntu-drivers devices # 查询所有ubuntu推荐的驱动
sudo apt-get install nvidia-430
```
##### 4、重启图形界面，查看安装
```shell
sudo service lightdm start
watch -n 0.1 -d nvidia-smi #查看显卡温度 不跑程序时30-50C均可 刚装好驱动时会热一点 多等一会儿
```
#### 安装cuda10.1 （10.0兼容性不好）
下载`.deb`文件：
```shell
sudo dpkg -i xxx
sudo apt-key add /var/cuda-repo-<version>/7fa2af80.pub #见上条运行结果
sudo apt-get update
sudo apt-get install cuda
sudo gedit ~/.bashrc
```
添加环境变量：
```
export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
export CUDA_HOME=/usr/local/cuda
```
```shell
source ~/.bashrc
```
## 添加用户
### 添加新用户
```shell
sudo adduser xxx
sudo vim /etc/sudoers #添加root权限,添加：xxx ALL=(ALL) ALL
```
### 关联原有用户
```shell
sudo useradd -d /home/xxx -s /bin/bash xxx
sudo chown -R xxx:xxx /home/xxx
sudo usermod -aG sudo xxx #添加sudo权限
sudo passwd xxx
```
## 其他安装（可选）
### 安装anaconda3（导入设置）
#### 配置
```shell
echo 'export PATH="~/anaconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```
### pip换源
```shell
pip install pip -U
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### apt换源
```shell
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo gedit /etc/apt/sources.list
```
按系统版本替换内容：
https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/l,
更新升级

```shell
sudo apt update
sudo apt upgrade
```

### 配置tmux、vim

```shell
sudo apt-get install tmux
sudo apt-get install vim
sudo apt-get install git
sh <(curl https://j.mp/spf13-vim3 -L) # 推荐配置，容易连不上，多试几次
```

### 硬盘挂载

```shell
sudo fdisk -l #查看可挂载的磁盘都有哪些
df -h  #查看已经挂载了哪些磁盘
sudo mkdir /DATA 
sudo mkfs -t ext4 /dev/sda
sudo mount /dev/sda /DATA
vim /etc/fstab 
```
添加到最后一行：UUID=*************  /DATA  ext4  defaults  0  1 
(ls -l /dev/disk/by-uuid | grep sda查看UUID)

### 安装teamviewer

`sudo dpkg -i xxx.deb` 若缺少依赖：sudo apt install -f

### 安装mujoco

- 安装： Follow https://github.com/openai/mujoco-py
- 往~/.bashrc添加环境变量：
```
export LD_LIBRARY_PATH=~/.mujoco/mujoco200/bin${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
```
```shell
cp mjkey.txt ~/.mujoco 
cp mjkey.txt ~/.mujoco/mujoco200/bin
```
```
Export LD_LIBRARY_PATH=~/.mujoco/mujoco200/bin${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
```
```
cd ~/.mujoco/mjpro150/bin 
./simulate ../model/humanoid.xml
```
- Install mujoco-py 参考 https://blog.csdn.net/zhangkzz/article/details/84574772

## 常见问题：
### 重装系统完成后，黑屏左上角光标闪烁：
[https://blog.csdn.net/chengyq116/article/details/102575221](https://blog.csdn.net/chengyq116/article/details/102575221)

#### 1、Advanced options for Ubuntu(开机时按Esc)选择其他内核版本
#### 2、禁用nouveau驱动
```shell
sudo gedit /etc/modprobe.d/blacklist.conf #确认最后一行添加：blacklist nouveau
sudo update-initramfs -u -k all
sudo reboot
```
#### 3、重装显卡驱动
