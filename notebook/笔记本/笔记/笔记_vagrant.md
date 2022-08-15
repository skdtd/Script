# 命令
```bash
# 添加box
vagrant box add e:\Downloads\CentOS-7.box --name centos-7
# 查看box列表
vagrant box list
# 创建虚拟机
vagrant init centos-7
# 启动虚拟机
vagrant up
# 查看虚拟机状态
vagrant status
# 连接虚拟机
vagrant ssh
# 停止虚拟机
vagrant halt
# 暂停虚拟机
vagrant suspend
# 恢复虚拟机
vagrant resume
# 重载虚拟机(重新加载 Vagrantfile 中的配置信息)
vagrant reload
# 删除虚拟机
vagrant destroy
# 查看ssh配置
vagrant ssh-config
# 打包当前环境为box
vagrant package
```


# Vagrantfile
```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure("2") do |config|
  # 官方文档                https://docs.vagrantup.com
  # boxes                  https://vagrantcloud.com/search
  # virtualbox客户机增强包  https://download.virtualbox.org/virtualbox
  
  # 虚机的镜像(必须项)
  config.vm.box = "CentOS7"

  # 端口转发,每行都是新增项,所以禁用默认22->2222转发时需要如下设置
  # config.vm.network "forwarded_port", guest: 22, host: 2222, id: "ssh", disabled: "true"
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # 私有网络配置(网段不存在时会在启动时自动创建)
  # config.vm.network "private_network", ip: "192.168.33.10"

  # DHCP的私有网络
  # config.vm.network "private_network", type: "dhcp"

  # 公共网络配置
  # config.vm.network "public_network"

  # 同步目录配置(只有在虚拟机启动时进行一次从宿主到虚拟机的同步)
  # config.vm.synced_folder "../data", "/vagrant_data", type: "rsync" # 使用同步模式,不加此选项在虚拟机未安装客户机增强包的时候会报错
  # 不添加 type: "rsync" 时为目录挂载,双向同步,但是需要安装客户机增增强包
  # config.vm.synced_folder "../data", "/vagrant_data"

  # 修改虚拟机规格
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   # 开启图形界面
  #   vb.gui = true
  #   # 设置使用CPU核数
  #   vb.cpu = 2
  #   # Customize the amount of memory on the VM:
  #   # 设置内存(MB)
  #   vb.memory = 1024
  # end

  # 特殊场景下启动会调用下列命令
  # 1. 虚拟机第一次使用vagrant up
  # 2. vagrant provision
  # 3. 重启的时候 vagrant reload --provision,带上 --provision 选项
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL
end
```

# 客户机增强包安装
```bash
# 1. VirtualBox -> 设置 -> 存储 -> 添加虚拟光驱 -> 控制器 -> IDE -> VBoxGuestAdditions_x.x.x.ios

# 2. vagrant/vagrant 登录虚拟机 sudo -i 切换到 root , lsblk 查看是否已经挂载映像

# 3. 将映像挂载到文件系统
mount /dev/sr0 /mnt

# 4. 运行安装程序
./VBoxLinuxAdditions.run 

# 第4部报错时需要更新内核kernel-devel 和 Release 版本号一致
uname -r &&  yum info kernel-devel # 查看版本号和内核版本号
yum update -y && yum install -y gcc kernel-devel # 更新内核版本为最新版本

# 5. 检查模块是否已经加载
lsmod | grep vbox
```
