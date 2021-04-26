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
