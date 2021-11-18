# 入门
## 环境准备
> 本机可以安装sshpass方便先执行分发公钥之前的步骤
1. 设置节点地址为静态IP地址
2. 设置主机名
   </br><b>`hostnamectl set-hostname ${hostname}`</b>
   </br><b>`hostnamectl -H ${user}@${host} set-hostname ${hostname}`</b>
3. 添加主机映射(/etc/hosts)
   </br><b>`tee -a /etc/hosts << EOF`</b>
   </br><b>`${hostlist}`</b>
   </br><b>`EOF`</b>
4. 开放22端口用于远程连接
5. 节点间免密
   </br><b>`ssh-keygen -q -N "" -f `</b>
   </br><b>`for i in ${hosts};do ssh-copy-id -i  ${user}@$i;done`</b>
## hadoop生产集群搭建
> 通过<b>`--downloadonly --downloaddir=${path}`</b>来只下载安装包 之后统一分发安装
1. 创建模板
   1. 安装epel-release, vim, net-tool
   </br><b>`yum install epel-release`</b>
   </br><b>`yum install vim net-tool`</b>
   2. 关闭节点防火墙
   </br><b>`systemctl stop --now firewalld`</b>
   3. 创建hadoop操作用户, 并添加相关root权限
   </br><b>`useradd ${user}`</b>
   </br><b>`echo ${password} | passwd ${user} --stdin`</b> 
   </br><b>`sed -i "/^\%wheel.*/a ${user}  ALL=(ALL)       NOPASSWD: ALL" /etc/sudoers`</b> 
   4. java版本不正确时卸载java
   </br><b>`rpm -qa | grep -i java | xargs -n1 rpm -e --nodeps`</b>
   5. 虚拟机使用复制虚拟机的方式, 云节点使用脚本部署
## 常见错误解决方案
# HDFS(负责数据存储)
# MapReduce(负责数据计算)
# YARN(Yet Another Resource Negotiator)(负责资源管理)
# 生产调优手册
# Hadoop源码解析

起停dfs
start-dfs.sh
stop-dfs.sh
起停yarn
start-yarn.sh
stop-yarn.sh
起停日志
mapred --daemon start historyserver
mapred --daemon stop historyserver

单独起停节点
hdfs --daemon start/stop namenode/datanode/secondarynamenode
yarn --daemon start/stop resourcemanager/nodemanager


# 端口号对应
# 3.x 
hdfs namenode: 内部通信端口 8020/9000/9820
               用户查询端口 9870
yarn           查看任务运行 8088
               历史服务器   19888
# 2.x
hdfs namenode: 内部通信端口 8020/9000
               用户查询端口 50070
yarn           查看任务运行 8088
               历史服务器   19888

# 常用配置文件
core-site.xml
hdfs-site.xml
yarn-site.xml
mapred-site.xml
workers(3.x) / slaves(2.x)

# 生产环境不能连接外网时,需要时间同步
1. 安装ntp: yum install ntp.x86_64
2. 配置时间服务器: /etc/ntp.conf
   * #restrict 192.168.1.0 mask 255.255.255.0 nomodify notrap
   修改网段内可访问本机
   * server 0.centos.pool.ntp.org iburst
   关闭默认访问公网中时间服务器
   * 节点丢失网络连接依然使用本地时间为集群提供时间同步
   sed -ie 's/#restrict 192.168.1.0 mask 255.255.255.0 nomodify notrap/restrict 192.168.100.0 mask 255.255.255.0 nomodify notrap/g;s/^server/#server/g;$a server 127.127.1.0\nfudge 127.127.1.0 stratum 10' /etc/ntp.conf
3. 同时同步系统时间与硬件时间
   echo 'SYNC_HWCLOCK=yes' >> /etc/sysconfig/ntpd
4. 启动服务: systemctl enable --now ntpd
5. 关闭其他节点的ntpd服务(防止与公网时间同步),设置定时任务与主节点同步(crontab -e)
   echo '*/1 * * * * /usr/bin/ntpdate 192.168.100.101' > /var/spool/cron/root
6. 关闭节点每次同步之后提示新邮件
   echo "unset MAILCHECK" >> /etc/profile
   source /etc/profile

core-site.xml
```xml
<property>
  <name>fs.defaultFS</name>
  <value>hdfs://hd01:8020</value>
  <description>NameNode的地址</description>
</property>
<property>
  <name>hadoop.tmp.dir</name>
  <value>/opt/hadoop-3.3.1/data</value>
  <description>数据存储目录</description>
</property>
```
hdfs-site.xml
```xml
<property>
  <name>dfs.namenode.http-address</name>
  <value>hd01:9870</value>
  <description>
    NameNode Web端访问地址
  </description>
</property>
<property>
  <name>dfs.namenode.secondary.http-address</name>
  <value>hd03:9868</value>
  <description>
    Secondary NameNode 地址
  </description>
</property>
```
yarn-site.xml
```xml
<property>
   <description>指定yarm使用shuffle</description>
   <name>yarn.nodemanager.aux-services</name>
   <value>mapreduce_shuffle</value>
</property>
<property>
   <description>指定ResourceManager地址</description>
   <name>yarn.resourcemanager.hostname</name>
   <value>hd02</value>
</property>
<property>
   <description>
      基础系统环境变量(3.1版本需要配置HADOOP_MAPRED_HOME,3.2以上无需额外配置该项)
      # 3.3版本貌似还是需要配置
   </description>
   <name>yarn.nodemanager.env-whitelist</name>
   <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_HOME,PATH,LANG,TZ,HADOOP_MAPRED_HOME</value>
</property>
<property>
   <description>日志聚集</description>
   <name>yarn.log-aggregation-enable</name>
   <value>true</value>
</property>
<property>
   <description>
      设置日志聚集服务器地址
   </description>
   <name>yarn.log.server.url</name>
   <value>hd04:1988/jobhistory/logs</value>
</property>
<property>
   <description>
      日志保存时间(7天)
   </description>
   <name>yarn.log-aggregation.retain-seconds</name>
   <value>604800</value>
</property>
```
mapred-site.xml
```xml
<property>
  <name>mapreduce.framework.name</name>
  <value>yarn</value>
  <description>
   指定mapreduce运行在yarn上
  </description>
</property>
<property>
  <name>mapreduce.jobhistory.address</name>
  <value>hd04:10020</value>
  <description>历史服务器通信端口</description>
</property>
<property>
  <name>mapreduce.jobhistory.webapp.address</name>
  <value>hd04:19888</value>
  <description>历史服务器web端</description>
</property>
```


# shell操作
创建文件夹
hadoop fs -mkdir /input
上传文件
hadoop fs -put file /input

启动任务
hadoop jar /opt/hadoop-3.3.1/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.1.jar wordcount /input /out1

