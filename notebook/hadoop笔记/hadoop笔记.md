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

101: NameNode






core-site.xml
```xml
<!-- NameNode的地址 -->
<property>
  <name>fs.defaultFS</name>
  <value>file:///</value>
  
  <description>The name of the default file system.  A URI whose
  scheme and authority determine the FileSystem implementation.  The
  uri's scheme determines the config property (fs.SCHEME.impl) naming
  the FileSystem implementation class.  The uri's authority is used to
  determine the host, port, etc. for a filesystem.</description>
</property>
<!-- 数据存储目录 -->
<property>
  <name>hadoop.tmp.dir</name>
  <value>/tmp/hadoop-${user.name}</value>
  <description>A base for other temporary directories.</description>
</property>
```
hdfs-site.xml
```xml
<!-- NameNode Web端访问地址 -->
<property>
  <name>dfs.namenode.http-address</name>
  <value>0.0.0.0:9870</value>
  <description>
    The address and the base port where the dfs namenode web ui will listen on.
  </description>
</property>
<!-- Secondary NameNode Web端访问地址 -->
<property>
  <name>dfs.namenode.secondary.http-address</name>
  <value>0.0.0.0:9868</value>
  <description>
    The secondary namenode http server address and port.
  </description>
</property>
```
yarn-site.xml
```xml
<!-- 指定yarm使用shuffle -->
<property>
   <description>A comma separated list of services where service name should only
   contain a-zA-Z0-9_ and can not start with numbers</description>
   <name>yarn.nodemanager.aux-services</name>
   <value></value>
   <!--<value>mapreduce_shuffle</value>-->
</property>
<!-- 指定ResourceManager地址 -->
<property>
   <description>The hostname of the RM.</description>
   <name>yarn.resourcemanager.hostname</name>
   <value>0.0.0.0</value>
</property>
<!-- 基础系统环境变量(3.1版本需要配置HADOOP_MAPRED_HOME,3.2以上无需额外配置该项) -->
<property>
   <description>Environment variables that containers may override rather than use NodeManager's default.</description>
   <name>yarn.nodemanager.env-whitelist</name>
   <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_HOME,PATH,LANG,TZ,HADOOP_MAPRED_HOME</value>
</property>
```
mapred-site.xml
```xml
<!-- 指定mapreduce运行再yarn上 -->
<property>
  <name>mapreduce.framework.name</name>
  <value>yarn</value>
  <description>The runtime framework for executing MapReduce jobs.
  Can be one of local, classic or yarn.
  </description>
</property>
```