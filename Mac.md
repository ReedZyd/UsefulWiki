## git
### generate ssh-key
ssh-keygen -t rsa -b 4096 -C "zyd1998424@163.com"
### copy content of pub-key
pbcopy < ~/.ssh/id_rsa.pub # ubuntu: xsel 见https://blog.csdn.net/yuanlongquan753/article/details/51050822


## homebrew
### install

* 常规安装脚本（推荐）
```shell
/bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"
```
* 极速安装脚本（精简版）
/bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)" speed

### uninstall
/bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/HomebrewUninstall.sh)"

### Some Errors
https://gitee.com/cunkai/HomebrewCN/blob/master/error.md

