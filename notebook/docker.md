# [docker命令][docker命令]
生命周期  |容器操作 |rootfs  |镜像仓库 |本地管理|信息版本
:--------|:--------|:-------|:-------|:-------|:------
[run]    |[ps]     |[commit]|[login] |[images]|[info]
[start]  |[inspect]|[cp]    |[pull]  |[rmi]   |[version]
[stop]   |[top]    |[diff]  |[push]  |[tag]
[restart]|[attach] |        |[search]|[build]
[kill]   |[events] |        |        |[history]
[rm]     |[logs]   |        |        |[save]
[pause]  |[wait]   |        |        |[load]
[unpause]|[export] |        |        |[import]
[create] |[port]   |
[exec]   |

# docker网络类型
```bash
# 查看docker网络
docker network ls
# bridge
#   桥接网络: 与宿主机通信,并使用宿主机的网络连接外网

# overlay network in swarm mode
#   Swarm集群中的覆盖网络: 集群内部节点通信,不会对其他服务器以及宿主机开放

# custom:v
#   自定义网络
```

# 创建网络
```bash
# 基于bridge创建新的网络(不指定--driver bridge时,默认就是此选项)
docker network create --driver bridge {网络名}
# 指定镜像使用指定网络驱动
docker run -itd --name={容器名} --network={网络名} {镜像名}
# 为容器添加新网络
docker network connect {网络名} {容器名}
# 为容器移除网络
docker network disconnect {网络名} {容器名}
# 删除一个网络
docker network rm {网络名}
```

# DockerFile保留字
```DockerFile
# 保留字
FROM            # 基础镜像
MAINTAINER      # 作者信息
RUN             # 容器构建时需要执行的命令
EXPOSE          # 容器对外暴露的端口
WORKDIR         # 登录容器终端时默认目录
ENV             # 设置构建镜像过程中的环境变量
ADD             # 将宿主机目录下的文件拷贝进镜像,并且自动处理URL和解压缩tar包
COPY            # 类似ADD,拷贝文件和目录到镜像中(例: COPY <src> <dist> ; COPY ["<src>", "<dist>"])
VOLUME          # 容器数据卷
CMD             # 指定一个容器启动时要运行的命令,可以有多个CMD命令,但是只有最后一个生效
ENTRYPOINT      # 指定一个容器启动时要运行的命令,多个ENTRYPOINT命令会不断追加
ONBUILD         # 当构建一个被继承的DockerFile时运行的命令,父镜像在被子镜像继承后父镜像的ONBUILD被触发
.dockerignore   # 忽略某些文件
USER            # 指定用户可以运行这个DockerFile文件
```
# 启动命令示例
```bash
# tomcat(pache-tomcat-9.0.8)
docker run -d -p 9000:8080 --name mytomcat \
-v /{HOST_PATH}/{WORK_DIR}:/usr/local/tomcat/webapps/{WORK_DIR} \  # 挂载工程目录
-v /{HOST_PATH}/logs:/usr/local/tomcat/logs \                      # 挂载日志目录
--privileged=true                                                  # 特权登录
tomcat

# mysql(5.6)
docker run -p 9999:3306 --name mysql \
-v /{HOST_PATH}/conf:/etc/mysql/conf.d \    # 挂载配置目录
-v /{HOST_PATH}/logs:/logs \                # 挂载日志目录
-v /{HOST_PATH}/data:/var/lib/mysql \       # 挂载数据目录
-e MYSQL_ROOT_PASSWORD=xxxxxx \
-d mysql:5.6

# redis(3.2)
docker run -p 8888:6379 \
-v /{HOST_PATH}/data:/data \                                    # 挂载数据目录
-v /{HOST_PATH}/conf/redis.conf:/usr/local/etc/redis.conf \     # 挂载配置目录
-d redis:3.2 redis-server /usr/local/etc/redis/redis.conf \
--appendonly yes                                                # 启动备份
```

# [docker swarm集群](https://www.runoob.com/docker/docker-swarm.html)
## 安装
### 1.  环境准备
```markdown
# 1.1 所有节点都需要安装docker engine
# 1.2 docker宿主机的ip地址固定,所有工作节点必须可以访问管理节点
# 1.3 集群管理节点必须使用相应的协议,并且端口可用
#       集群管理通信:   TCP         2377
#       节点通信:       TCP和UDP    7946
#       覆盖型网络:     UDP         4789    (overlay驱动)
```
### 2.  创建docker swarm
```bash
# 在管理节点上初始化集群(--advertise-addr: 指定管理节点IP)
# 执行后会产生一个token,用来添加节点用
docker swarm init --advertise-addr 192.168.100.100

# 查看新增的网络驱动(overlay覆盖型网络)
docker network ls

# 查看集群信息(在管理节点上执行)
docker node ls
```
### 3.  向集群中添加节点
```bash
# 在工作节点上执行
docker swarm join --token {TOKEN} 192.168.100.100:2377
```
### 4.  部署服务
```bash
# 部署一个服务(示例)(--network: 指定服务使用的网络名, --replicas: 服务的副本数)
docker service create --network {网络名} --replicas 1 --name {服务名} alpine ping docker.com
# 查看集群中服务列表
docker service ls
# 查看服务的详细信息
docker service inspect {服务名}
# 查看服务在集群上的分配以及运行情况
docker service ps {服务名}

# 修改服务副本数量
docker service scale {服务名}=5
# 删除一个服务
docker service rm {服务名}
```








<!-- URL LIST -->
[docker命令官方手册]: https://docs.docker.com/engine/reference/commandline/docker/ "docker命令官方手册"
[docker安装]: https://www.runoob.com/docker/centos-docker-install.html "docker安装"
[docker命令]: https://www.runoob.com/docker/docker-command-manual.html "docker命令"
[docker过滤参数]: https://www.runoob.com/docker/docker-ps-command.html#div-comment-43785 "docker命令 ps的过滤参数"
[docker命令手册]: https://www.kancloud.cn/woshigrey/docker/934967 "docker命令手册"
[docker命令手册(events)]: https://www.kancloud.cn/woshigrey/docker/935883 "events命令"
[run]:     https://docs.docker.com/engine/reference/run/                  "创建并启动容器"
[ps]:      https://docs.docker.com/engine/reference/commandline/ps/       "列出当前容器"
[commit]:  https://docs.docker.com/engine/reference/commandline/commit/   "从容器创建镜像"
[login]:   https://docs.docker.com/engine/reference/commandline/login/    "登陆到Docker镜像仓库"
[images]:  https://docs.docker.com/engine/reference/commandline/images/   "列出当前所有镜像"
[info]:    https://docs.docker.com/engine/reference/commandline/info/     "查看docker信息"
[start]:   https://docs.docker.com/engine/reference/commandline/start/    "启动容器"
[inspect]: https://docs.docker.com/engine/reference/commandline/inspect/  "获取容器元数据"
[cp]:      https://docs.docker.com/engine/reference/commandline/cp/       "复制文件"
[pull]:    https://docs.docker.com/engine/reference/commandline/pull/     "从仓库拉取镜像"
[rmi]:     https://docs.docker.com/engine/reference/commandline/rmi/      "删除镜像"
[version]: https://docs.docker.com/engine/reference/commandline/version/  "查看docker版本"
[stop]:    https://docs.docker.com/engine/reference/commandline/stop/     "停止容器(优雅停止)"
[top]:     https://docs.docker.com/engine/reference/commandline/top/      "查看容器内进程"
[diff]:    https://docs.docker.com/engine/reference/commandline/diff/     "检查容器里文件结构的更改"
[push]:    https://docs.docker.com/engine/reference/commandline/push/     "推送镜像到仓库"
[tag]:     https://docs.docker.com/engine/reference/commandline/tag/      "标记本地镜像"
[restart]: https://docs.docker.com/engine/reference/commandline/restart/  "重启容器"
[attach]:  https://docs.docker.com/engine/reference/commandline/attach/   "连接到容器"
[search]:  https://docs.docker.com/engine/reference/commandline/search/   "查找容器"
[build]:   https://docs.docker.com/engine/reference/commandline/build/    "使用Dockerfile创建镜像"
[kill]:    https://docs.docker.com/engine/reference/commandline/kill/     "强制停止容器"
[events]:  https://docs.docker.com/engine/reference/commandline/events/   "查看宿主机上容器发生的事件"
[history]: https://docs.docker.com/engine/reference/commandline/history/  "查看指定镜像的创建历史"
[rm]:      https://docs.docker.com/engine/reference/commandline/rm/       "删除容器"
[logs]:    https://docs.docker.com/engine/reference/commandline/logs/     "查看容器日志"
[save]:    https://docs.docker.com/engine/reference/commandline/save/     "将指定镜像保存成tar归档文件"
[pause]:   https://docs.docker.com/engine/reference/commandline/pause/    "暂停容器"
[wait]:    https://docs.docker.com/engine/reference/commandline/wait/     "阻塞容器直到停止,然后打印退出代码"
[load]:    https://docs.docker.com/engine/reference/commandline/load/     "导入使用save生成的容器归档文件"
[unpause]: https://docs.docker.com/engine/reference/commandline/unpause/  "复苏容器"
[export]:  https://docs.docker.com/engine/reference/commandline/export/   "将文件系统作为一个tar归档文件导出(不压缩)"
[import]:  https://docs.docker.com/engine/reference/commandline/import/   "从归档文件中创建镜像"
[create]:  https://docs.docker.com/engine/reference/commandline/create/   "创建但不运行容器"
[port]:    https://docs.docker.com/engine/reference/commandline/port/     "查看容器映射端口"
[exec]:    https://docs.docker.com/engine/reference/commandline/exec/     "在容器中执行命令"
<!-- URL LIST END -->












# docker 离线安装
1. [下载安装包](https://download.docker.com/linux/static/stable/x86_64/)(此步骤需要在线完成)
2. 解压
```bash
tar xzvf /path/to/<FILE>.tar.gz
```
3. 复制到`/usr/bin`目录
```bash
cp docker/* /usr/bin/
```
4. 注册服务
```bash
tee /etc/systemd/system/docker.service << EOF
[Unit]
Description=Docker Application Container Engine
Documentation=https://docs.docker.com
After=network-online.target firewalld.service
Wants=network-online.target
[Service]
Type=notify
#the default is not to use systemd for cgroups because the delegate issues still
#exists and systemd currently does not support the cgroup feature set required
#for containers run by docker
ExecStart=/usr/bin/dockerd
ExecReload=/bin/kill -s HUP $MAINPID
#Having non-zero Limit*s causes performance problems due to accounting overhead
#in the kernel. We recommend using cgroups to do container-local accounting.
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity
#Uncomment TasksMax if your systemd version supports it.
#Only systemd 226 and above support this version.
#TasksMax=infinity
TimeoutStartSec=0
#set delegate yes so that systemd does not reset the cgroups of docker containers
Delegate=yes
#kill only the docker process, not all processes in the cgroup
KillMode=process
#restart the docker process if it exits prematurely
Restart=on-failure
StartLimitBurst=3
StartLimitInterval=60s
[Install]
WantedBy=multi-user.target
EOF
```
5. 重载UNIT配置文件
```bash
systemctl daemon-reload
```
6. 设置开机启动
```bash
systemctl enable docker.service
```
7. 启动docker
```bash
systemctl start docker
```



ip address |sed -rn '/state UP/{n;n;s#^ *inet (.*)/.*$#\1#gp}'
yum deplist wget | grep provider | awk '{print $2}'
# 离线安装kubernetes
# 备份源仓库
cp -p /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.$(date +%Y%m%d%S)

# 使用阿里云镜像源
curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo

# 更新缓存
yum clean all && yum makecache

# 添加阿里云Docker源
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo



# 下载离线包
yum install --downloadonly --downloaddir=. \
    createrepo yum-utils nfs-utils wget                     \
    yum-utils  nfs-utils wget                               \
    device-mapper-persistent-data lvm2                      \
    docker-ce-19.03.5 docker-ce-cli-19.03.5 containerd.io   \
    chrony                                                  \
    haproxy keepalived

# 添加kubernetes源
tee /etc/yum.repos.d/kubernetes.repo << EOF
[kubernetes]
name=Kubernetes
baseurl=http://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=http://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
       http://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF


yum install --downloadonly --downloaddir=. kubelet-1.17.1 kubeadm-1.17.1 kubectl-1.17.1
yum install --downloadonly --downloaddir=. kubelet kubeadm kubectl



https://www.jianshu.com/p/fd9f1076ea2d


# 修改tag
docker images \
    | grep registry.cn-shanghai.aliyuncs.com/k8s-deps \
    | sed 's/registry.cn-hangzhou.aliyuncs.com\/lfy_k8s_images/k8s.gcr.io/' \
    | awk '{print "docker tag " $3 " " $1 ":" $2}' \
    | sh

# 删除源镜像
docker images \
    | grep registry.cn-shanghai.aliyuncs.com \
    | awk '{print "docker rmi " $1 ":" $2}' \
    | sh

# k8s集群依赖
docker pull registry.cn-shanghai.aliyuncs.com/k8s-deps/kube-apiserver:v1.21.0
docker pull registry.cn-shanghai.aliyuncs.com/k8s-deps/kube-controller-manager:v1.21.0
docker pull registry.cn-shanghai.aliyuncs.com/k8s-deps/kube-scheduler:v1.21.0
docker pull registry.cn-shanghai.aliyuncs.com/k8s-deps/kube-proxy:v1.21.0
docker pull registry.cn-shanghai.aliyuncs.com/k8s-deps/pause:3.4.1
docker pull registry.cn-shanghai.aliyuncs.com/k8s-deps/etcd:3.4.13-0
docker pull registry.cn-shanghai.aliyuncs.com/k8s-deps/coredns:v1.8.0

# calico网络插件
curl https://docs.projectcalico.org/manifests/calico-typha.yaml -o calico.yaml
docker pull docker.io/calico/typha:v3.18.1
docker pull docker.io/calico/cni:v3.18.1
docker pull docker.io/calico/pod2daemon-flexvol:v3.18.1
docker pull docker.io/calico/node:v3.18.1
docker pull docker.io/calico/kube-controllers:v3.18.1

# dashboard可视化
curl https://raw.githubusercontent.com/kubernetes/dashboard/v2.2.0/aio/deploy/recommended.yaml -o dashboard.yaml
docker pull kubernetesui/dashboard:v2.0.0-rc5
docker pull kubernetesui/metrics-scraper:v1.0.3

# kuboard可视化
curl https://kuboard.cn/install-script/kuboard.yaml -o kuboard.yaml
docker pull eipwork/kuboard







## 3、安装

### 1、理解

安装方式

- 二进制方式（建议生产环境使用）
- MiniKube.....
- kubeadm引导方式（官方推荐）
  - GA







大致流程

- 准备N台服务器，**内网互通**，
- 安装Docker容器化环境【k8s放弃dockershim】
- 安装Kubernetes
  - 三台机器安装核心组件（**kubeadm(创建集群的引导工具)**,  ***kubelet***，**kubectl（程序员用的命令行）**  ）
  - kubelet可以直接通过容器化的方式创建出之前的核心组件（api-server）【官方把核心组件做成镜像】
  - 由kubeadm引导创建集群



### 2、执行

#### 1、准备机器

- 开通三台机器，内网互通，配置公网ip。centos7.8/7.9，基础实验2c4g三台也可以
- 每台机器的hostname不要用localhost，可用k8s-01，k8s-02，k8s-03之类的【不包含下划线、小数点、大写字母】（这个后续步骤也可以做）

#### 2、安装前置环境（都执行）

##### 1、基础环境

```sh
#########################################################################
#关闭防火墙： 如果是云服务器，需要设置安全组策略放行端口
# https://kubernetes.io/zh/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#check-required-ports
systemctl stop firewalld
systemctl disable firewalld

# 修改 hostname
hostnamectl set-hostname k8s-01
# 查看修改结果
hostnamectl status
# 设置 hostname 解析
echo "127.0.0.1   $(hostname)" >> /etc/hosts

#关闭 selinux： 
sed -i 's/enforcing/disabled/' /etc/selinux/config
setenforce 0

#关闭 swap：
swapoff -a  
sed -ri 's/.*swap.*/#&/' /etc/fstab 

#允许 iptables 检查桥接流量
#https://kubernetes.io/zh/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#%E5%85%81%E8%AE%B8-iptables-%E6%A3%80%E6%9F%A5%E6%A1%A5%E6%8E%A5%E6%B5%81%E9%87%8F
## 开启br_netfilter
## sudo modprobe br_netfilter
## 确认下
## lsmod | grep br_netfilter

## 修改配置


#####这里用这个，不要用课堂上的配置。。。。。。。。。
#将桥接的 IPv4 流量传递到 iptables 的链：
# 修改 /etc/sysctl.conf
# 如果有配置，则修改
sed -i "s#^net.ipv4.ip_forward.*#net.ipv4.ip_forward=1#g"  /etc/sysctl.conf
sed -i "s#^net.bridge.bridge-nf-call-ip6tables.*#net.bridge.bridge-nf-call-ip6tables=1#g"  /etc/sysctl.conf
sed -i "s#^net.bridge.bridge-nf-call-iptables.*#net.bridge.bridge-nf-call-iptables=1#g"  /etc/sysctl.conf
sed -i "s#^net.ipv6.conf.all.disable_ipv6.*#net.ipv6.conf.all.disable_ipv6=1#g"  /etc/sysctl.conf
sed -i "s#^net.ipv6.conf.default.disable_ipv6.*#net.ipv6.conf.default.disable_ipv6=1#g"  /etc/sysctl.conf
sed -i "s#^net.ipv6.conf.lo.disable_ipv6.*#net.ipv6.conf.lo.disable_ipv6=1#g"  /etc/sysctl.conf
sed -i "s#^net.ipv6.conf.all.forwarding.*#net.ipv6.conf.all.forwarding=1#g"  /etc/sysctl.conf
# 可能没有，追加
echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf
echo "net.bridge.bridge-nf-call-ip6tables = 1" >> /etc/sysctl.conf
echo "net.bridge.bridge-nf-call-iptables = 1" >> /etc/sysctl.conf
echo "net.ipv6.conf.all.disable_ipv6 = 1" >> /etc/sysctl.conf
echo "net.ipv6.conf.default.disable_ipv6 = 1" >> /etc/sysctl.conf
echo "net.ipv6.conf.lo.disable_ipv6 = 1" >> /etc/sysctl.conf
echo "net.ipv6.conf.all.forwarding = 1"  >> /etc/sysctl.conf
# 执行命令以应用
sysctl -p


#################################################################

```

##### 2、docker环境

```sh
sudo yum remove docker*
sudo yum install -y yum-utils
#配置docker yum 源
sudo yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
#安装docker 19.03.9
yum install -y docker-ce-3:19.03.9-3.el7.x86_64  docker-ce-cli-3:19.03.9-3.el7.x86_64 containerd.io

#安装docker 19.03.9   docker-ce  19.03.9
yum install -y docker-ce-19.03.9-3  docker-ce-cli-19.03.9 containerd.io

#启动服务
systemctl start docker
systemctl enable docker

#配置加速
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
    "registry-mirrors": [
        "https://ustc-edu-cn.mirror.aliyuncs.com/",
        "http://hub-mirror.c.163.com"
    ]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```



#### 3、安装k8s核心（都执行）

```sh
# 配置K8S的yum源
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=http://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=http://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
       http://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF

# 卸载旧版本
yum remove -y kubelet kubeadm kubectl

# 查看可以安装的版本
yum list kubelet --showduplicates | sort -r

# 安装kubelet、kubeadm、kubectl 指定版本
yum install -y kubelet-1.21.0 kubeadm-1.21.0 kubectl-1.21.0

# 开机启动kubelet
systemctl enable kubelet && systemctl start kubelet
```



#### 4、初始化master节点（master执行）

```sh
############下载核心镜像 kubeadm config images list：查看需要哪些镜像###########

####封装成images.sh文件
#!/bin/bash
images=(
  kube-apiserver:v1.21.0
  kube-proxy:v1.21.0
  kube-controller-manager:v1.21.0
  kube-scheduler:v1.21.0
  coredns:v1.8.0
  etcd:3.4.13-0
  pause:3.4.1
)
for imageName in ${images[@]} ; do
    docker pull registry.cn-hangzhou.aliyuncs.com/lfy_k8s_images/$imageName
done
#####封装结束

chmod +x images.sh && ./images.sh


# registry.cn-hangzhou.aliyuncs.com/lfy_k8s_images/coredns:v1.8.0

##注意1.21.0版本的k8s coredns镜像比较特殊，结合阿里云需要特殊处理，重新打标签
docker tag registry.cn-hangzhou.aliyuncs.com/lfy_k8s_images/coredns:v1.8.0 registry.cn-hangzhou.aliyuncs.com/lfy_k8s_images/coredns/coredns:v1.8.0

########kubeadm init 一个master########################
########kubeadm join 其他worker########################
kubeadm init \
--apiserver-advertise-address=10.170.11.8 \
--image-repository registry.cn-hangzhou.aliyuncs.com/lfy_k8s_images \
--kubernetes-version v1.21.0 \
--service-cidr=10.96.0.0/16 \
--pod-network-cidr=192.168.0.0/16
## 注意：pod-cidr与service-cidr
# cidr 无类别域间路由（Classless Inter-Domain Routing、CIDR）
# 指定一个网络可达范围  pod的子网范围+service负载均衡网络的子网范围+本机ip的子网范围不能有重复域




######按照提示继续######
## init完成后第一步：复制相关文件夹
To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

## 导出环境变量
Alternatively, if you are the root user, you can run:

  export KUBECONFIG=/etc/kubernetes/admin.conf


### 部署一个pod网络
You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/
  ##############如下：安装calico#####################
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml


### 命令检查
kubectl get pod -A  ##获取集群中所有部署好的应用Pod
kubectl get nodes  ##查看集群所有机器的状态
 

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 172.24.80.222:6443 --token nz9azl.9bl27pyr4exy2wz4 \
	--discovery-token-ca-cert-hash sha256:4bdc81a83b80f6bdd30bb56225f9013006a45ed423f131ac256ffe16bae73a20 
```

#### 5、初始化worker节点（worker执行）

```sh
## 用master生成的命令即可

kubeadm join 172.24.80.222:6443 --token nz9azl.9bl27pyr4exy2wz4 \
	--discovery-token-ca-cert-hash sha256:4bdc81a83b80f6bdd30bb56225f9013006a45ed423f131ac256ffe16bae73a20 
	
	

##过期怎么办
kubeadm token create --print-join-command
kubeadm token create --ttl 0 --print-join-command
kubeadm join --token y1eyw5.ylg568kvohfdsfco --discovery-token-ca-cert-hash sha256: 6c35e4f73f72afd89bf1c8c303ee55677d2cdb1342d67bb23c852aba2efc7c73
```



![1619100578888](assets/1619100578888.png)

#### 6、验证集群

```sh
#获取所有节点
kubectl get nodes

#给节点打标签
## k8s中万物皆对象。node:机器  Pod：应用容器
###加标签  《h1》
kubectl label node k8s-02 node-role.kubernetes.io/worker=''
###去标签
kubectl label node k8s-02 node-role.kubernetes.io/worker-


## k8s集群，机器重启了会自动再加入集群，master重启了会自动再加入集群控制中心
```



#### 7、设置ipvs模式

k8s整个集群为了访问通；默认是用iptables,性能下（kube-proxy在集群之间同步iptables的内容）



```sh
#1、查看默认kube-proxy 使用的模式
kubectl logs -n kube-system kube-proxy-28xv4
#2、需要修改 kube-proxy 的配置文件,修改mode 为ipvs。默认iptables，但是集群大了以后就很慢
kubectl edit cm kube-proxy -n kube-system
修改如下
   ipvs:
      excludeCIDRs: null
      minSyncPeriod: 0s
      scheduler: ""
      strictARP: false
      syncPeriod: 30s
    kind: KubeProxyConfiguration
    metricsBindAddress: 127.0.0.1:10249
    mode: "ipvs"
 ###修改了kube-proxy的配置，为了让重新生效，需要杀掉以前的Kube-proxy
 kubectl get pod -A|grep kube-proxy
 kubectl delete pod kube-proxy-pqgnt -n kube-system
### 修改完成后可以重启kube-proxy以生效
```



#### 8、让其他客户端kubelet也能操作集群

```sh
#1、master获取管理员配置
cat /etc/kubernetes/admin.conf
#2、其他节点创建保存
vi ~/.kube/config
#3、重新测试使用
```



## 4、急速安装方式

- 1、三台机器设置自己的hostname（不能是localhost）。云厂商注意三台机器一定要通。
  - 青云需要额外设置组内互信
  - 阿里云默认是通的
  - 虚拟机，关闭所有机器的防火墙

```sh
# 修改 hostname;  k8s-01要变为自己的hostname
hostnamectl set-hostname k8s-01
# 设置 hostname 解析
echo "127.0.0.1   $(hostname)" >> /etc/hosts
```

- 2、所有机器批量执行如下脚本

- ```sh
  #先在所有机器执行 vi k8s.sh
  # 进入编辑模式（输入i），把如下脚本复制
  # 所有机器给脚本权限  chmod +x k8s.sh
  #执行脚本 ./k8s.sh
  ```

```sh
#/bin/sh

#######################开始设置环境##################################### \n


printf "##################正在配置所有基础环境信息################## \n"


printf "##################关闭selinux################## \n"
sed -i 's/enforcing/disabled/' /etc/selinux/config
setenforce 0
printf "##################关闭swap################## \n"
swapoff -a  
sed -ri 's/.*swap.*/#&/' /etc/fstab 

printf "##################配置路由转发################## \n"
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
br_netfilter
EOF
echo 'net.ipv4.ip_forward = 1' >> /etc/sysctl.d/k8s.conf

## 必须 ipv6流量桥接
echo 'net.bridge.bridge-nf-call-ip6tables = 1' >> /etc/sysctl.d/k8s.conf
## 必须 ipv4流量桥接
echo 'net.bridge.bridge-nf-call-iptables = 1' >> /etc/sysctl.d/k8s.conf
echo "net.ipv6.conf.all.disable_ipv6 = 1" >> /etc/sysctl.d/k8s.conf
echo "net.ipv6.conf.default.disable_ipv6 = 1" >> /etc/sysctl.d/k8s.conf
echo "net.ipv6.conf.lo.disable_ipv6 = 1" >> /etc/sysctl.d/k8s.conf
echo "net.ipv6.conf.all.forwarding = 1"  >> /etc/sysctl.d/k8s.conf
modprobe br_netfilter
sudo sysctl --system
	
	
printf "##################配置ipvs################## \n"
cat <<EOF | sudo tee /etc/sysconfig/modules/ipvs.modules
#!/bin/bash
modprobe -- ip_vs
modprobe -- ip_vs_rr
modprobe -- ip_vs_wrr
modprobe -- ip_vs_sh
modprobe -- nf_conntrack_ipv4
EOF

chmod 755 /etc/sysconfig/modules/ipvs.modules 
sh /etc/sysconfig/modules/ipvs.modules


printf "##################安装ipvsadm相关软件################## \n"
yum install -y ipset ipvsadm




printf "##################安装docker容器环境################## \n"
sudo yum remove docker*
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
yum install -y docker-ce-19.03.9  docker-ce-cli-19.03.9 containerd.io
systemctl enable docker
systemctl start docker

sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  ###在这里配置自己的阿里云加速
    "registry-mirrors": [
        "https://ustc-edu-cn.mirror.aliyuncs.com/",
        "http://hub-mirror.c.163.com"
    ]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker


printf "##################安装k8s核心包 kubeadm kubelet kubectl################## \n"
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=http://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=http://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
   http://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF

###指定k8s安装版本
yum install -y kubelet-1.21.0 kubeadm-1.21.0 kubectl-1.21.0

###要把kubelet立即启动。
systemctl enable kubelet
systemctl start kubelet

printf "##################下载api-server等核心镜像################## \n"
sudo tee ./images.sh <<-'EOF'
#!/bin/bash
images=(
kube-apiserver:v1.21.0
kube-proxy:v1.21.0
kube-controller-manager:v1.21.0
kube-scheduler:v1.21.0
coredns:v1.8.0
etcd:3.4.13-0
pause:3.4.1
)
for imageName in ${images[@]} ; do
docker pull registry.cn-hangzhou.aliyuncs.com/lfy_k8s_images/$imageName
done
## 全部完成后重新修改coredns镜像
docker tag registry.cn-hangzhou.aliyuncs.com/lfy_k8s_images/coredns:v1.8.0 registry.cn-hangzhou.aliyuncs.com/lfy_k8s_images/coredns/coredns:v1.8.0
EOF
   
chmod +x ./images.sh && ./images.sh
   
### k8s的所有基本环境全部完成
```

- 3、使用kubeadm引导集群（参照初始化master继续做）

```sh

#### --apiserver-advertise-address 的地址一定写成自己master机器的ip地址
#### 虚拟机或者其他云厂商给你的机器ip  10.96  192.168
#### 以下的只在master节点执行
kubeadm init \
--apiserver-advertise-address=10.170.11.8 \
--image-repository registry.cn-hangzhou.aliyuncs.com/lfy_k8s_images \
--kubernetes-version v1.21.0 \
--service-cidr=10.96.0.0/16 \
--pod-network-cidr=192.168.0.0/16


```

- 4、master结束以后，按照控制台引导继续往下

```sh
## 第一步
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

##第二步
export KUBECONFIG=/etc/kubernetes/admin.conf

##第三步 部署网络插件
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml



##第四步，用控制台打印的kubeadm join 去其他node节点执行
kubeadm join 10.170.11.8:6443 --token cnb7x2.lzgz7mfzcjutn0nk \
	--discovery-token-ca-cert-hash sha256:00c9e977ee52632098aadb515c90076603daee94a167728110ef8086d0d5b37d
```

- 5、验证集群

```sh
#等一会，在master节点执行
kubectl get nodes
```


- 6、设置kube-proxy的ipvs模式

```sh
##修改kube-proxy默认的配置
kubectl edit cm kube-proxy -n kube-system
## 修改mode: "ipvs"

##改完以后重启kube-proxy
### 查到所有的kube-proxy
kubectl get pod -n kube-system |grep kube-proxy
### 删除之前的即可
kubectl delete pod 【用自己查出来的kube-proxy-dw5sf kube-proxy-hsrwp kube-proxy-vqv7n】  -n kube-system

###

```