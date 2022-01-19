# docker 二进制安装

## 获取docker二进制文件版本最新版
```bash
DOCKER_VERSION=$(curl -sS https://download.docker.com/linux/static/stable/x86_64/ | grep -Po "docker-(\d+\.){2}(\d+)" | uniq | grep -Ev "ce|rootless" | sed -n '$p') && echo ${DOCKER_VERSION}
```
## 下载解压并复制到启动目录
```bash
curl -OC -  https://download.docker.com/linux/static/stable/x86_64/${DOCKER_VERSION}.tgz  # -C - 自动断点续传
tar -zvxf docker-19.03.6.tgz
cp docker/* /usr/bin/
```
## 启动dcoker
```bash
/usr/bin/dockerd
```

### 设置为服务
```bash
vim /etc/systemd/system/docker.service
chmod +x /etc/systemd/system/docker.service
```
```ini
[Unit]
Description=Docker Application Container Engine
Documentation=https://docs.docker.com
After=network-online.target firewalld.service
Wants=network-online.target

[Service]
Type=notify
ExecStart=/usr/bin/dockerd
ExecReload=/bin/kill -s HUP $MAINPID
LimitNOFILE=infinity
LimitNPROC=infinity
TimeoutStartSec=0
Delegate=yes
KillMode=process
Restart=on-failure
StartLimitBurst=3
StartLimitInterval=60s

[Install]
WantedBy=multi-user.target
```
```bash
systemctl daemon-reload             #重载配置文件
systemctl start docker              #启动Docker
systemctl stop docker               #关闭docker
systemctl restart  docker           #重启docker
systemctl enable docker.service     #设置开机自启
systemctl status docker             #查看Docker状态
```



#
#


# k8s安装
## kubectl
```shell
# 下载最新版kubectl
curl -LO "https://dl.k8s.io/release/$(curl -sSL https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# 非root用户安装
mkdir -p ~/.local/bin/kubectl
mv ./kubectl ~/.local/bin/kubectl
echo 'export PATH=$PATH:~/.local/bin/kubectl' >> ~/.bashrc

# root用户安装
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

```

## cfssl
```shell
CFSSL_VERSION=$(curl -sS https://github.com/cloudflare/cfssl/releases/latest | grep -Po '\d+(\.\d+){2}')
curl -L --remote-name-all https://github.com/cloudflare/cfssl/releases/download/v${CFSSL_VERSION}/{cfssljson_${CFSSL_VERSION}_linux_amd64,cfssl_${CFSSL_VERSION}_linux_amd64,cfssl-certinfo_${CFSSL_VERSION}_linux_amd64}

chmod +x cfssl*

for name in `ls cfssl*`; do mv $name ${name%_${CFSSL_VERSION}_linux_amd64}; done

mv cfssl* /usr/bin

tee /opt/ssl/k8sca/ca-config.json << EOF
{
    "signing": {
        "default": {
            "expiry": "87600h"
        },
        "profiles": {
            "kubernetes": {
                "usages": [
                    "signing",
                    "key encipherment",
                    "server auth",
                    "client auth"
                ],
                "expiry": "87600h"
            }
        }
    }
}
EOF

tee /opt/ssl/k8sca/ca-csr.json << EOF
{
    "CN": "kubernetes",
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "C": "CN",
            "L": "Shanghai",
            "O": "kubernetes",
            "ST": "Shanghai",
            "OU": "kubernetes"
        }
    ]
}
EOF
```

# etcd
```shell
ETCD_VERSION=$(curl -sS https://github.com/etcd-io/etcd/releases/latest | grep -Po '\d+(\.\d+){2}')
curl -LO https://github.com/etcd-io/etcd/releases/download/v${ETCD_VERSION}/etcd-v${ETCD_VERSION}-linux-amd64.tar.gz
tar -zxf etcd-v${ETCD_VERSION}-linux-amd64.tar.gz --strip-components=1 -C /usr/local/bin etcd-v${ETCD_VERSION}-linux-amd64/etcd{,ctl}
```


# kubenetes
```shell
K8S_VERSION=$(curl -L -s https://dl.k8s.io/release/stable.txt)
curl -LO https://dl.k8s.io/${K8S_VERSION}/kubernetes-server-linux-amd64.tar.gz


# 所有master节点解压kubelet，kubectl等到 /usr/local/bin
# master需要全部组件，node节点只需要 /usr/local/bin kubelet、kube-proxy
tar -xf kubernetes-server-linux-amd64.tar.gz --strip-components=3 -C /usr/local/bin kubernetes/server/bin/kube{let,ctl,-apiserver,-controller-manager,-scheduler,-proxy}

# 单独下载
K8S_VERSION=$(curl -L -s https://dl.k8s.io/release/stable.txt)
curl -LO "https://dl.k8s.io/release/${K8S_VERSION}/bin/linux/amd64/kube-apiserver"
curl -LO "https://dl.k8s.io/release/${K8S_VERSION}/bin/linux/amd64/kube-controller-manager"
curl -LO "https://dl.k8s.io/release/${K8S_VERSION}/bin/linux/amd64/kubectl"
curl -LO "https://dl.k8s.io/release/${K8S_VERSION}/bin/linux/amd64/kubelet"
curl -LO "https://dl.k8s.io/release/${K8S_VERSION}/bin/linux/amd64/kube-proxy"
curl -LO "https://dl.k8s.io/release/${K8S_VERSION}/bin/linux/amd64/kube-scheduler"
```

# master需要的组件: Controller manager, etcd, scheduler, api server, kubectl
# node需要的组件: kubelet, kube-proxy




## curl并发访问
https://www.jianshu.com/p/025e4f3cf668

< urls.txt xargs -r -L 3 -P 10 curl -LOsS
## getopts和getopt的使用
https://cloud.tencent.com/developer/article/1043821
## Shell 黑科技之匿名函数实现任务并行化
https://cloud.tencent.com/developer/article/1043998
## 玩转 SHELL 脚本之：Shell 命令 Buffer 知多少？
https://cloud.tencent.com/developer/article/1043855
## 玩转 Linux 之：磁盘分区、挂载知多少？
https://cloud.tencent.com/developer/article/1043832
## 玩转 SHELL 脚本之：linux date 知多少？
https://cloud.tencent.com/developer/article/1043762
## shell解析yaml
https://github.com/jasperes/bash-yaml/blob/master/script/yaml.sh
# 代码片段
https://gist.github.com/pkuczynski










# 无网络升级内核
```shell
升级方法：

在能上网的机器下载内核rpm包，传到不能上网的机器安装

准备两台机器：

192.168.1.1（能上网）和192.168.1.2（不能上网）

两台机器的系统版本：

[root@localhost ~]# uname -r
3.10.0-1062.el7.x86_64
[root@localhost ~]# cat /etc/redhat-release
CentOS Linux release 7.7.1908 (Core)

192.168.1.1操作如下：
https://elrepo.org/linux/kernel/el7/x86_64/RPMS/     下载地址
修改yum配置文件，让yum安装的内核rpm包能够保存在本地：vi /etc/yum.conf   把keepcache=0改为1
导入ELRepo仓库的公共密钥rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
安装ELRepo仓库的yum源rpm -Uvh http://www.elrepo.org/elrepo-release-7.0-3.el7.elrepo.noarch.rpm
查看可用的内核安装包yum --disablerepo="*" --enablerepo="elrepo-kernel" list available
安装内核包yum --enablerepo=elrepo-kernel install kernel-lt --downloadonly  --downloaddir=.（kernel-lt根据第4步列出来的选择）
[root@localhost packages]# pwd
/var/cache/yum/x86_64/7/elrepo-kernel/packages
[root@localhost packages]# ll
total 106772
-rw-r--r-- 1 root root 52542012 Jul 22 09:34 kernel-lt-5.4.134-1.el7.elrepo.x86_64.rpm
传安装包：scp /var/cache/yum/x86_64/7/elrepo-kernel/packages/kernel-lt-5.4.134-1.el7.elrepo.x86_64.rpm 192.168.1.2:/opt
192.168.1.2操作如下：

安装内核：rpm -ivh /opt/kernel-lt-5.4.134-1.el7.elrepo.x86_64.rpm
检查是否安装成功，看到5.4.134已经存在：sudo awk -F\' '$1=="menuentry " {print i++ " : " $2}' /etc/grub2.cfg
编辑 /etc/default/grub 文件设置 GRUB_DEFAULT=0，sed -i 's/saved/0/g' /etc/default/grub通过上面查询显示的编号为 0 的内核作为默认内核
生成 grub 配置文件并重启grub2-mkconfig -o /boot/grub2/grub.cfg && reboot
查看内核：
[root@localhost ~]# uname -a
Linux localhost.localdomain 5.4.134-1.el7.elrepo.x86_64 #1 SMP Thu Jul 22 08:58:15 EDT 2021 x86_64 x86_64 x86_64 GNU/Linux
[root@localhost ~]# cat /etc/redhat-release
CentOS Linux release 7.7.1908 (Core)
```


