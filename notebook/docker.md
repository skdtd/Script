#### [docker安装](https://www.runoob.com/docker/centos-docker-install.html) [docker命令](https://www.runoob.com/docker/docker-command-manual.html)
```shell
# {容器名}: 容器的自定义名称
# {网络名}: 网络的自定义名称
# {镜像名}: 镜像的名称
# {服务名}: 服务名称
# {HOST_PATH}: 主机上的地址
# {WORK_DIR}: 工作目录
# {TOKEN}: token
```
# 常用命令
```shell
# 查看容器的详细信息
docker inspect {容器名}
```

# docker网络类型
```shell
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
```shell
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
# 启动命令
```shell
# tomcat(pache-tomcat-9.0.8)
docker run -d -p 9000:8080 mytomcat \
-v /{HOST_PATH}/{WORK_DIR}:/usr/local/apache-tomcat-9.0.8/webapps/{WORK_DIR} \  # 挂载工程目录
-v /{HOST_PATH}/logs:/usr/local/apache-tomcat-9.0.8/logs \                      # 挂载日志目录
--privileged=true
mytomcat

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
```shell
# 在管理节点上初始化集群(--advertise-addr: 指定管理节点IP)
# 执行后会产生一个token,用来添加节点用
docker swarm init --advertise-addr 192.168.100.100

# 查看新增的网络驱动(overlay覆盖型网络)
docker network ls

# 查看集群信息(在管理节点上执行)
docker node ls
```
### 3.  向集群中添加节点
```shell
# 在工作节点上执行
docker swarm join --token {TOKEN} 192.168.100.100:2377
```
### 4.  部署服务
```shell
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
