# Redis

## 安装
### 安装前准备(gcc)
```bash
# centos
yum install -y gcc
# ubuntu
sudo apt install gcc
```
### centos
```bash
yum install -y http://rpms.famillecollet.com/enterprise/remi-release-7.rpm
yum --enablerepo=remi install -y redis
systemctl status redis # 查看状态
systemctl start redis  # 启动
# 默认配置文件: /etc/redis.conf
```
### ubuntu
```bash
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
sudo apt-get update
sudo apt-get install redis

sudo service redis-server start # 启动服务端, redis-cli为客户端
```
### 源码方式安装
```bash
wget https://download.redis.io/redis-stable.tar.gz
# 或者
curl -SL -O https://download.redis.io/redis-stable.tar.gz
tar -xzvf redis-stable.tar.gz
cd redis-stable
make
make install

redis-server # 启动服务端, redis-cli为客户端
```
## 启停命令
```bash
redis-server <redis.conf>   # 启动(加载配置文件)
redis-cli                   # 启动客户端
redis-cli shutdown          # 停止服务端
info server                 # client中执行, 可以获取当前服务实例的信息
```
## 配置文件
### INCLUDES
```bash
# 加载另外一个文件, 便于配置信息管理, 不同场景中包含不同配置信息
# 后声明的配置会覆盖先声明的, 包括后include
include /path/to/fragments/*.conf   # 加载其他配置文件
```
### MODULES
```bash
# 启动时加载模块
loadmodules /path/to/my_module.so
```
### NETWORK
```bash
# 需要其他节点访问时需要监听所有主机,同时关闭保护模式
bind 127.0.0.1 -::1             # 注释掉此行可以监听所有主机访问

protected-mode <yes/no>         # 是否打开保护模式(允许来自未认证的节点访问)

port 6379                       # 端口号

# tcp队列, 出现慢连接时会影响性能, 由linux的内核参数somaxconn决定, 取somaxconn和redis中配置值中最小值, 生产中特别为高并发场景中, 该值最好稍大一些(cat /proc/sys/net/core/somaxconn)
# 修改/etc/sysctl.conf中的net.core.somaxconn=4096, 修改完毕后通过sysctl -p来重载配置
tcp-backlog 511                 

timeout 0                       # 连接空闲查过时间后自动断开, 设置为0时为无限制

tcp-keepalive 300               # 服务端检测客户端是否存活间隔, 两次检测不存活时关闭连接
# socket-mark-id 0
```
### GENERAL
```bash
daemonize <yes/no>                      # 是否以守护进程形式启动

pidfile /run/redis.pid                  # pid文件

loglevel <debug/verbose/notice/warning> # 日志级别

logfile /var/log/redis/redis-server.log # 日志文件, 设置为空串时, 日志会显示到控制台(需要关闭守护进程方式启动)

databases 16                            # 数据库数量
```
### SECURITY
```bash
requirepass <xxxx>          # 访问密码(客户端中需要使用: auth xxxx来输入密码)

# 禁用flushall和flushdb
rename-command flushall ""  # 重命名一个命令, 重命名为""时则命令不可用
rename-command flushdb ""   # 重命名一个命令, 重命名为""时则命令不可用
```
### CLIENTS
```bash
maxclients 10000            # 最大可连接客户端数量(与ulimit -n的值之间取小值)
# 当redis以集群方式部署时, 每个节点间通信还会占用两个连接
```
### MEMORY MANAGEMENT
```bash
maxmemory <bytes>               # 指定最大内存量

maxmemory-policy noeviction     # 内存使用率达到极限时采取的移除策略
# volatile-lru                  -> 在有设置过期值的key中, 移除一个最近最少使用的
# allkeys-lru                   -> 在所有key中, 移除一个最近最少使用的
# volatile-lfu                  -> 在有设置过期值的key中, 移除一个最少使用的
# allkeys-lfu                   -> 在所有key中, 移除一个最少使用的
# volatile-random               -> 在有设置过期值的key中, 随机移除一个key
# allkeys-random                -> 在所有key中, 随机移除一个key
# volatile-ttl                  -> 在所有key中, 移除一个最接近过期时间
# noeviction                    -> 不做任何移除, 只会返回一个错误消息

maxmemory-samples 5             # 挑选要移除的样本数量,数量越少, 速度越快, 数量越大, 精度越高

maxmemory-eviction-tenacity 10  # 移除容忍度, 移除时的延迟, 除非出现异常大的写操作, 一般采用默认值即可
```
### LAZY FREEING
```bash
# 以非阻塞形式删除数据, 默认会以阻塞形式删除(DEL) 当一个key较大时使用DEL可能会花费较多时间, 可以改变配置使用非阻塞的方式删除(UNLINK)
lazyfree-lazy-eviction no       # 惰性移除
lazyfree-lazy-expire no         # 惰性过期
lazyfree-lazy-server-del no     # 服务器惰性删除
replica-lazy-flush no           # 惰性清空
lazyfree-lazy-user-del no       # 用户惰性删除
lazyfree-lazy-user-flush no     # 用户惰性清空
```
### THREADED I/O
```bash

io-threads 4                    # 如果遇上性能瓶颈时, 再考虑是否需要开启多线程, 开启后线程皆用于写操作,为系统预留1-2个核心即可, 线程数设置超过8基本不会再有性能提升, 通过命令(lscpu)查看核心数
io-threads-do-reads no          # 在开启多线程后支持线程用于读操作, 通常情况下, 多线程读操作对性能没有帮助
```
## 命令
控制台操作命令, 略

## 数据类型
### [Strings](https://redis.io/docs/data-types/#strings)
> 字符型数据
* 共享session
* 防Dos攻击(无法防止DDos攻击)
### [Lists](https://redis.io/docs/data-types/#Lists)
> 列表数据
* 队列(FIFO)
* 栈(FILO)
* 阻塞队列
* 阻塞栈
### [Sets](https://redis.io/docs/data-types/#sets)
> 集合数据
### [Hashes](https://redis.io/docs/data-types/#hashes)
> 哈希数据(类似python的dict)
* 在对象传输时,不需要进行序列号就可以存储,取用时也无需反序列化
### [Sorted sets](https://redis.io/docs/data-types/#sorted-sets)
> 有序集合数据
### [Streams](https://redis.io/docs/data-types/#streams)
> 流
### [Geospatial indexes](https://redis.io/docs/data-types/#geospatial-indexes)
### [Bitmaps](https://redis.io/docs/data-types/#Bitmaps)
### [Bitfields](https://redis.io/docs/data-types/#Bitfields)
### [HyperLogLog](https://redis.io/docs/data-types/#HyperLogLog)