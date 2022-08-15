```shell
# 网卡信息
vim /etc/udev/rules.d/70-persistent-net.rules
# 修改静态ip
vim /etc/sysconfig/network-scripts/ifcfg-eth0
# 修改主机名
vim /etc/sysconfig/network
# 添加hosts
vim /etc/hosts
```


# 环境

```shell
## maven
export MAVEN_HOME=/opt/softwave/apache-maven-3.6.3

## ant
export ANT_HOME=/opt/softwave/apache-ant-1.10.9
export PATH=$PATH:$MAVEN_HOME/bin:$ANT_HOME/bin

## hadoop
export HADOOP_HOME=
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
```


# 编译hadoop

```shell
# 下载ant maven 打包工具
wget https://mirrors.tuna.tsinghua.edu.cn/apache/ant/binaries/apache-ant-1.10.9-bin.tar.gz
wget https://mirrors.bfsu.edu.cn/apache/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.tar.gz


# 下载hadoop源码  protobuf2.5.0(序列化框架)
wget https://downloads.apache.org/hadoop/common/hadoop-2.10.1/hadoop-2.10.1-src.tar.gz
wget https://github.com/protocolbuffers/protobuf/releases/download/v2.5.0/protobuf-2.5.0.tar.gz

# 解压到指定文件夹
for pkg in *;do tar -zxvf ${pkg} -C /opt/softwave/;done

tar tf apache-ant-1.10.9-bin.tar.gz | head -n 1 | cut -d "/" -f 1| awk '{cmd="echo \"export ANT_HOME=/opt/softwave/\""$0"/bin >> /etc/profile";system(cmd)}'

tar tf apache-maven-3.6.3-bin.tar.gz | head -n 1 | cut -d "/" -f 1| awk '{cmd="echo \"export MAVEN_HOME=/opt/softwave/\""$0"/bin >> /etc/profile";system(cmd)}'


# 安装glibc-headers g++ make cmake openssl-devel ncurses-devel java patch
yum -y install glibc-headers gcc-c++ make cmake openssl-devel ncurses-devel java-1.8.0-openjdk-devel patch.x86_64
# 安装protobuf
./configure
make
make check
make install
ldconfig
# 配置环境
export LD_LIBRARY_PATH=/opt/softwave/protobuf-2.5.0
export PATH=$PATH:$LD_LIBRARY_PATH

# 确认环境protoc2.5.0 maven ant
protoc --version
mvn -version
ant -version
# 解压hadoop源码开始编译
mvn package -Pdist,native -DskipTests -Dtar
```


# 配置规划
||hadoop101|hadoop102|hadoop103|
|-|-|-|-|
|HDFS|NameNode||SecondaryNameNode|
||DateNode|DateNode|DateNde|
|YARN||ResourceManager||
||NodeManager|NodeManager|NodeManager|

NameNode、SecondaryNameNode、ResourceManager不在同一节点

# 配置文件
hadoop-env.sh yarn-env.sh mapred-env.sh

```shell
export JAVA_HOME=
```


core-site.xml

```xml
<!-- 指定HDFS中NameNode的地址 -->
<property>
    <name>fs.defaultFS</name>
    <value>hdfs://hadoop101:9000</value>
</property>
<!-- 指定Hadoop运行时产生文件的存储目录 -->
<property>
    <name>hadoop.tmp.dir</name>
    <value>/opt/softwave/hadoop-2.10.1/data/tmp</value>
</property>
```


hdfs-site.xml

```xml
<!-- 备份数 -->
<property>
    <name>dfs.replication</name>
    <value>3</value>
</property>
<property>
      <name>dfs.namenode.name.dir</name>
      <value>${hadoop.tmp.dir}/data/tmp/dfs/name</value>
</property>
<!-- 指定hadoop辅助名称节点主机配置 -->
<property>
    <name>dfs.namenode.secondary.http-address</name>
    <value>hadoop103:50090</value>
</property>

```


yarn-site.xml

```xml
<!-- Reducer获取数据的方式 -->
<property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
</property>
<!-- 指定yarn的ResourceManager的地址 -->
<property>
    <name>yarn.resourcemanager.hostname</name>
    <value>hadoop102</value>
</property>
<!-- 开启日志聚集 -->
<property>
    <name>yarn.log-aggregation-enable</name>
    <value>true</value>
</property>
<property>
    <name>yarn.log-aggregation.retain-seconds</name>
    <value>604800</value>
</property>
```


mapred-site.xml

```xml
<!-- 指定MR运行在yarn上 -->
<property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
</property>
<!-- 开启日志服务器 -->
<property>
    <name>mapreduce.jobhistory.address</name>
    <value>h101:10020</value>
</property>
<!-- 日志服务器访问地址 -->
<property>
    <name>mapreduce.jobhistory.webapp.address</name>
    <value>h101:19888</value>
</property>
```


# 启动
(首次启动删除所有的date/ logs/)

```shell
# 格式化namenode
bin/hdfs namenode -format

# 单节点启停(start/stop)
sbin/hadoop-daemon.sh start namenode
sbin/hadoop-daemon.sh start datenode
sbin/hadoop-daemon.sh start secondarynamenode
sbin/yarn-daemon.sh start resourcemanager
sbin/yarn-daemon.sh start nodenamager



```


hadoop101:50070打开浏览器

```shell
# 群起
# 添加所有节点host到/etc/hadoop/slaves

# 启动所有HDFS节点
sbin/start-dfs.sh

# 停止所有HDFS节点
sbin/stop-dfs.sh

# 启动yarn(必须在ResourceManager节点上执行启动)
sbin/start-yarn.sh

# 停止yarn(必须在ResourceManager节点上执行启动)
sbin/stop-yarn.sh

```


# 控制端执行的脚本

```shell
#!/bin/bash
set -e

temp_dir=`date +%Y%H%M%S`
mkdir ${temp_dir}
cd ${temp_dir}

node_list=../hostlist
cmd="rm -rf /root/123"
while read line
do
	node=(${line})
	host=${node[0]}
	username=${node[1]}
	password=${node[2]}
	# 执行命令
	expect << EOF
	spawn ssh root@172.30.150.101 -oStrictHostKeyChecking=no
	expect  "*password:" { send "1212\r" }
	EOF
done < ${node_list}

cd ..
rm -rf ${temp_dir}
echo ""
```


# 发送到远程的运行脚本

```shell
#!/bin/bash


cat > command << PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
#!/bin/bash

# 错误退出
set -e
# debug模式
set -x

# 更换阿里云
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
curl -o /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-7.repo
yum clean all && yum makecache

# 安装基础包
yum -y install openssh.x86_64 openssh-clients.x86_64 openssh-server.x86_64 vim wget net-tools.x86_64

# 安装java
yum -y install java-1.8.0-openjdk-devel
echo "export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk" >> /etc/profile
PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
```

