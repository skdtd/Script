# 入门
## [文档及初始配置文件](https://hadoop.apache.org/docs/current/)
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
> 没有到主机的路由
* 防火墙未配置或者workers
> Does not contain a valid host:port authority: http:
* 不要在配置文件中指定http协议
# HDFS(负责数据存储)
## 起停基本命令(在对应的节点上执行)
> 起停dfs
* <b>`${HADOOP_HOME}/sbin/start-dfs.sh`</b>
* <b>`${HADOOP_HOME}/sbin/stop-dfs.sh`</b>
> 起停yarn
* <b>`${HADOOP_HOME}/sbin/start-yarn.sh`</b>
* <b>`${HADOOP_HOME}/sbin/stop-yarn.sh`</b>
> 单节点起停
* <b>`hdfs --daemon start <node>`</b>
* <b>`hdfs --daemon stop <node>`</b>
* <b>`yarn --daemon start <node>`</b>
* <b>`yarn --daemon stop <node>`</b>
* <b>`mapred --daemon start <node>`</b>
* <b>`mapred --daemon stop <node>`</b>

| HDFS                | YARN               | HISTORY         |
| :------------------ | :----------------- | :-------------- |
| `namenode`          | `nodemanager`      | `historyserver` |
| `datanode`          | `resourcemanager`  |
| `secondarynamenode` | registrydns        |
| sps                 | proxyserver        |
| zkfc                | router             |
| nfs3                | sharedcachemanager |
| portmap             | timelineserver     |
dfsrouter
diskbalancer
httpfs
journalnode
mover
balancer
## 内部使用端口
### 3.x
功能                 | 端口号
:-                   | :-
HDFS内部通信端口      | 8020/9000/`9820`
HDFS用户查询端口      | `9870`
YARN查看任务运行      | 8088
YARN任务通信端口      | 8032
YARN历史服务器        | 19888/10020
YARN历史服务器通信端口 |10020
### 2.x
功能             | 端口号
:--------------- | :-
HDFS内部通信端口 | 8020/9000
HDFS用户查询端口 | `50070`
YARN查看任务运行 | 8088
YARN历史服务器   | 19888
## 常用配置文件
workers
```
hd01
hd02
hd03
hd04
```
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
<property>
  <name>io.compression.codecs</name>
  <value></value>
  <description>
    设置Map输入阶段压缩
    集群执行(hadoop checknative)查看可选参数
  </description>
</property>
```
hdfs-site.xml
```xml
<property>
  <name>dfs.replication</name>
  <value>3</value>
  <description>默认副本数</description>
</property>
<property>
  <name>dfs.storage.policy.enabled</name>
  <value>true</value>
  <description>是否打开文件存储策略</description>
</property>
<property>
  <name>dfs.namenode.http-address</name>
  <value>hd01:9870</value>
  <description>NameNode Web端访问地址</description>
</property>
<property>
  <name>dfs.namenode.secondary.http-address</name>
  <value>hd03:9868</value>
  <description>Secondary NameNode 地址</description>
</property>
<property>
  <name>dfs.namenode.checkpoint.period</name>
  <value>3600s</value>
  <description>检查点检查时间(2nn)</description>
</property>
<property>
  <name>dfs.namenode.checkpoint.txns</name>
  <value>1000000</value>
  <description>检查点检查数据量(2nn)</description>
</property>
<property>
  <name>dfs.namenode.checkpoint.check.period</name>
  <value>60s</value>
  <description>检查数据量轮询时间(2nn)</description>
</property>
<property>
  <name>dfs.blockreport.intervalMsec</name>
  <value>21600000</value>
  <description>定时汇报dn的块信息</description>
</property>
<property>
  <name>dfs.datanode.directoryscan.interval</name>
  <value>21600s</value>
  <description>定时扫描本机节点快信息</description>
</property>
<property>
  <name>dfs.namenode.heartbeat.recheck-interval</name>
  <value>300000</value>
  <description>
    心跳检查超时时间(ms)
    超时(2 * 心跳检查超时时间 + 10 * 心跳检查间隔)之后,判定节点离线
  </description>
</property>
<property>
  <name>dfs.heartbeat.interval</name>
  <value>3s</value>
  <description>
    心跳检查间隔
    (ms(millis), s(sec), m(min), h(hour), d(day))
  </description>
</property>

```
yarn-site.xml
## 如果服务器配置不一致,则需要单独节点进行配置
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
      (3.3版本貌似还是需要配置)
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
   <description>设置日志聚集服务器地址</description>
   <name>yarn.log.server.url</name>
   <value>hd04:1988/jobhistory/logs</value>
</property>
<property>
   <description>日志保存时间(7天)</description>
   <name>yarn.log-aggregation.retain-seconds</name>
   <value>604800</value>
</property>
<property>
  <description>
    配置调度器,默认容量调度器
    容量调度器: org.apache.hadoop.yarn.server.resourcemanager.scheduler.capacity.CapacityScheduler
    公平调度器: org.apache.hadoop.yarn.server.resourcemanager.scheduler.fair.FairScheduler
  </description>
  <name>yarn.resourcemanager.scheduler.class</name>
  <value>org.apache.hadoop.yarn.server.resourcemanager.scheduler.capacity.CapacityScheduler</value>
</property>
<property>
  <description>指定公平调度器配置文件</description>
  <name>yarn.scheduler.fair.allocation.file</name>
  <value>/fair-scheduler.xml</value>
</property>
<property>
  <description>禁止队列间资源抢占</description>
  <name>yarn.scheduler.fair.preemption</name>
  <value>false</value>
</property>
<property>
  <description>处理客户端的请求线程数,不要超过CPU总线程数</description>
  <name>yarn.resourcemanager.resource-tracker.client.thread-count</name>
  <value>50</value>
</property>
<property>
  <description>是否将虚拟CPU核数当作CPU核数</description>
  <name>yarn.nodemanager.resource.count-logical-processors-as-cores</name>
  <value>false</value>
</property>
<property>
  <description>虚拟CPU核数与物理CPU核数的比例</description>
  <name>yarn.nodemanager.resource.pcores-vcores-multiplier</name>
  <value>1.0</value>
</property>
<property>
  <description>启用自动检测节点功能,如内存和CPU。</description>
  <name>yarn.nodemanager.resource.detect-hardware-capabilities</name>
  <value>false</value>
</property>
<property>
  <description>物理内存检测,默认打开</description>
  <name>yarn.nodemanager.pmem-check-enabled</name>
  <value>true</value>
</property>
<property>
  <description>虚拟内存检查,默认打开(CentOS与Java8之间内存使用政策不同,需要关闭)</description>
  <name>yarn.nodemanager.vmem-check-enabled</name>
  <value>false</value>
</property>
<property>
  <description>
    nodemanager使用的内存量,默认8G
    如果设置为-1且yarn.nodemanager.resource.detect-hardware-capabilities为true,则会自动计算该值(对于Windows和Linux)
  </description>
  <name>yarn.nodemanager.resource.memory-mb</name>
  <value>-1</value>
</property>
<property>
  <description>
    nodemanager使用的CPU核数,默认8核
    如果设置为-1且yarn.nodemanager.resource.detect-hardware-capabilities为true,则会自动计算该值(对于Windows和Linux)
  </description>
  <name>yarn.nodemanager.resource.cpu-vcores</name>
  <value>-1</value>
</property>
<property>
  <description>容器最小内存使用量</description>
  <name>yarn.scheduler.minimum-allocation-mb</name>
  <value>1024</value>
</property>
<property>
  <description>容器最大内存使用量</description>
  <name>yarn.scheduler.maximum-allocation-mb</name>
  <value>8192</value>
</property>
<property>
  <description>容器最小CPU核数</description>
  <name>yarn.scheduler.minimum-allocation-vcores</name>
  <value>1</value>
</property>
<property>
  <description>容器最大CPU核数</description>
  <name>yarn.scheduler.maximum-allocation-vcores</name>
  <value>4</value>
</property>
<property>
  <description>开启优先级等级(0: 没有优先级, 任意数字代表多少个优先级等级)</description>
  <name>yarn.cluster.max-application-priority</name>
  <value>0</value>
</property>
```
mapred-site.xml
```xml
<property>
  <name>mapreduce.framework.name</name>
  <value>yarn</value>
  <description>指定mapreduce运行在yarn上</description>
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
<property>
  <name>mapreduce.map.output.compress</name>
  <value>false</value>
  <description>是否开启Map输出阶段压缩</description>
</property>
<property>
  <name>mapreduce.map.output.compress.codec</name>
  <value>org.apache.hadoop.io.compress.DefaultCodec</value>
  <description>当开启Map输出阶段压缩时,选择何种压缩方式</description>
</property>
<property>
  <name>mapreduce.output.fileoutputformat.compress</name>
  <value>false</value>
  <description>是否开启Reduce输出阶段压缩</description>
</property>
<property>
  <name>mapreduce.output.fileoutputformat.compress.codec</name>
  <value>org.apache.hadoop.io.compress.DefaultCodec</value>
  <description>当开启Reduce输出阶段压缩时,选择何种压缩方式</description>
</property>
```
capacity-scheduler.xml
```xml
<property>
  <name>yarn.scheduler.capacity.maximum-applications</name>
  <value>10000</value>
  <description>最多支持多少任务同时等待或者运行</description>
</property>
<property>
  <name>yarn.scheduler.capacity.maximum-am-resource-percent</name>
  <value>0.1</value>
  <description>单任务可占用最大资源比</description>
</property>
<property>
  <name>yarn.scheduler.capacity.root.queues</name>
  <value>{队列名称},{队列名称}</value>
  <description>队列名称(用逗号分隔)</description>
</property>
<property>
  <name>yarn.scheduler.capacity.root.{队列名称}.capacity</name>
  <value>100</value>
  <description>队列占总资源的比例(0-100)</description>
</property>
<property>
  <name>yarn.scheduler.capacity.root.{队列名称}.user-limit-factor</name>
  <value>1</value>
  <description>单用户可使用集群最大资源比例(0.0-1.0)</description>
</property>
<property>
  <name>yarn.scheduler.capacity.root.{队列名称}.maximum-capacity</name>
  <value>100</value>
  <description>队列最大容量(队列资源不足时向其他队列借用资源时)</description>
</property>
<property>
  <name>yarn.scheduler.capacity.root.{队列名称}.state</name>
  <value>RUNNING</value>
  <description>队列状态(RUNNING or STOPPED)</description>
</property>
<property>
  <name>yarn.scheduler.capacity.root.{队列名称}.acl_submit_applications</name>
  <value>*</value>
  <description>可以向该队列提交任务的用户</description>
</property>
<property>
  <name>yarn.scheduler.capacity.root.{队列名称}.acl_administer_queue</name>
  <value>*</value>
  <description>拥有队列操作权限的用户(查看,结束任务等等)</description>
</property>
<property>
  <name>yarn.scheduler.capacity.root.{队列名称}.acl_application_max_priority</name>
  <value>*</value>
  <description>可以设置队列优先级的用户</description>
</property>
<property>
  <name>yarn.scheduler.capacity.root.{队列名称}.maximum-application-lifetime
  </name>
  <value>-1</value>
  <description>任务最大可以执行时间(用户指定无法超过该时长)</description>
</property>
<property>
  <name>yarn.scheduler.capacity.root.{队列名称}.default-application-lifetime
  </name>
  <value>-1</value>
  <description>默认任务最大执行时间</description>
</property>
```
[fair-scheduler.xml](https://blog.cloudera.com/untangling-apache-hadoop-yarn-part-4-fair-scheduler-queue-basics/)
```xml
<allocations>
  <!-- 单个队列中Application Master占资源的最大比例(0.0-1.0) -->
  <queueMaxAMShareDefault>0.5</queueMaxAMShareDefault>
  <!-- 单个队列最大资源的默认值 -->
  <queueMaxResourcesDefault>40000 mb,0vcores</queueMaxResourcesDefault>
  <queue name="sample_queue">
    <!-- 队列最小资源 -->
    <minResources>10000 mb,0vcores</minResources>
    <!-- 队列最大资源 -->
    <maxResources>90000 mb,0vcores</maxResources>
    <!-- 队列最大允许同时运行任务 -->
    <maxRunningApps>50</maxRunningApps>
    <!-- 队列中Application Master占用资源的最大比例 -->
    <maxAMShare>0.1</maxAMShare>
    <!-- 权重 -->
    <weight>2.0</weight>
    <!-- 队列策略 -->
    <schedulingPolicy>fair</schedulingPolicy>
    <queue name="sample_sub_queue">
      <aclSubmitApps>charlie</aclSubmitApps>
      <minResources>5000 mb,0vcores</minResources>
    </queue>
    <queue name="sample_reservable_queue">
      <reservation></reservation>
    </queue>
  </queue>
  <!-- Queue 'secondary_group_queue' is a parent queue and may have
       user queues under it -->
  <queue name="secondary_group_queue" type="parent">
  <weight>3.0</weight>
  <maxChildResources>4096 mb,4vcores</maxChildResources>
  </queue>

  <user name="sample_user">
    <maxRunningApps>30</maxRunningApps>
  </user>
  <userMaxAppsDefault>5</userMaxAppsDefault>

  <queuePlacementPolicy>
    <rule name="specified" />
    <rule name="primaryGroup" create="false" />
    <rule name="nestedUserQueue">
        <rule name="secondaryGroupExistingQueue" create="false" />
    </rule>
    <rule name="default" queue="sample_queue"/>
  </queuePlacementPolicy>
</allocations>
```
## 生产环境不能连接外网时,需要时间同步
1. 安装ntp: `yum install ntp.x86_64`
2. 配置时间服务器: `/etc/ntp.conf`
   * #restrict 192.168.1.0 mask 255.255.255.0 nomodify notrap
   </br>修改网段内可访问本机
   * server 0.centos.pool.ntp.org iburst
   </br>关闭默认访问公网中时间服务器
   * 节点丢失网络连接依然使用本地时间为集群提供时间同步
   ```bash
   sed -ie 's/#restrict 192.168.1.0 mask 255.255.255.0 nomodify notrap/restrict 192.168.100.0 mask 255.255.255.0 nomodify notrap/g;s/^server/#server/g;$a server 127.127.1.0\nfudge 127.127.1.0 stratum 10' /etc/ntp.conf
   ```
3. 同时同步系统时间与硬件时间
   `echo 'SYNC_HWCLOCK=yes' >> /etc/sysconfig/ntpd`
4. 启动服务: systemctl enable --now ntpd
5. 关闭其他节点的ntpd服务(防止与公网时间同步),设置定时任务与主节点同步(crontab -e)
   ```bash
   echo '*/1 * * * * /usr/bin/ntpdate 192.168.100.101' > /var/spool/cron/root
   ```
6. 关闭节点每次同步之后提示新邮件
   ```bash
   echo "unset MAILCHECK" >> /etc/profile
   source /etc/profile
   ```
## shell的操作
```bash
# 创建文件夹
hadoop fs -mkdir /input
# 上传文件
hadoop fs -put file /input

# 启动任务
# -D mapreduce.job.queuename={队列名称} 提交任务到指定队列
# -D mapreduce.job.priority={优先级}    提交任务指定优先级
# 代码中直接conf.set("mapreduce.job.queuename","{队列名称}")指定提交队列
hadoop jar ${HADOOP_HOME}/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.1.jar wordcount -D mapreduce.job.queuename=default -D mapreduce.job.priority=5 /input /out
```
## API的操作
> [编译windows版本](https://cwiki.apache.org/confluence/display/HADOOP2/Hadoop2OnWindows)
# MapReduce(负责数据计算)
## 数据序列化对照
Java类型  |Hadoop Writable类型
:-        |:-
boolean   |BooleanWritable
byte      |ByteWritable
int       |IntWritable
float     |FloatWritable
long      |LongWritable
double    |DoubleWritable
String    |Text
Map       |MapWritable
Array     |ArrayWritable
Null      |NullWritable

# YARN(Yet Another Resource Negotiator)(负责资源管理)
## 工作机制
## 调度器

1.  FIFO/容量/公平
2.  apache默认调度器:容量, CDH默认调度器: 公平
3.  公平/容量默认一个队列: default, 多队列需要手动创建
4.  多队列好处: 解耦 降级使用 降低风险
5.  每个调度器特点:
      相同点: 支持多队列,可以借调资源,支持多用户
      不同点: 容量调度器优先满足先进入的任务执行, 公平调度器在队列中的任务公平享有队列资源
6.  对并发要求不高的选择容量调度器, 对并发要求高的选择公平调度器
## 命令
```bash
# 查看任务状态
yarn application -list -appStates <tag>
# tag: all new new_saving submitted accepted running finished failed killed

# 结束任务
yarn application -kill <application_id>

# 查看Application日志
yarn logs -applicationId <application_id>

# 查看Container日志
yarn logs -applicationId <application_id> -containerId <container_id>

# 查看尝试运行的任务
yarn applicationattempt -list <application_id>

# 打印尝试运行的任务状态
yarn applicationattempt -status <application_id>

# 查看容器
yarn container -list <application_id>

# 打印容器状态
yarn container -status <container_id>

# 更新任务执行时间
yarn application -appId <application_id> -updateLifetime <timeout>

# 更新任务执行优先级
yarn application -appId <application_id> -updatePriority <priority>

# 刷新yarn队列
yarn rmadmin -refreshQueues
```
# HDFS生产调优
## HDFS核心参数配置
> namenode内存计算
>> 每个文件块大小为150byte,假设可用内存为128G时,可以存储的文件为128(GB) * 1024(MB) * 1024(KB) * 1024(Byte) / 150(Byte) 约等于 9.1 亿
namenode最小值为1G,每增加100万个block时,增加1G`(集群中)`
datenode最小值为4G,副本总数低于400万时,调整为4G. 超过400万,每增加100万个副本数时,增加1G`(节点中)`
```bash
# 修改etc/hadoop/hadoop-env.sh文件
# namenode修改方式
export HDFS_NAMENODE_OPTS="-Dhadoop.security.logger=INFO,RFAS -Xmx1024"
# datanode修改法昂是
export HDFS_DATANODE_OPTS="-Dhadoop.security.logger=ERROR,RFAS -Xmx1024"
```
## namenode心跳并发配置
hdfs-site.xml
```xml
<property>
  <name>dfs.namenode.handler.count</name>
  <value>10</value>
  <description>工作线程池大小</description>
</property>
```
```bash
# 计算最佳线程池大小
CLUSTER_SIZE= # 集群大小
python << EOF
import math
print int(20 * math.log(${CLUSTER_SIZE}))
EOF
```
## 开启回收站
core-site.xml
```xml
<property>
  <name>fs.trash.interval</name>
  <value>0</value>
  <description>0: 禁用回收站, 任意数字: 表示文件在回收站中存留的分钟数</description>
</property>
<property>
  <name>fs.trash.checkpoint.interval</name>
  <value>0</value>
  <description>
    检查回收站的间隔时间,
    如果为0则表示与fs.trash.interval一致,
    不能大于fs.trash.interval的值
    只有在命令行中使用hadoop fs -rm命令删除的文件才会进入回收站,
    web页面和代码中删除不会进入回收站
  </description>
</property>
```
```java
// 代码中删除文件移动到回收站的方式
Trash trash = new Trash(conf);
trash.moveToTrash(Path)
// 撤销删除的话移动回收站中的文件路径即可
```
## HDFS集群压测
```bash
# 使用自带jarbao压测(数量确保每个节点都有启动task即可)
hadoop jar ${HADOOP_HOME}/share/hadoop/mapreduce/hadoop-mapreduce-client-jobclient-3.3.1-tests.jar TestDFSIO -write -nrFiles 10 -fileSize 128MB
hadoop jar ${HADOOP_HOME}/share/hadoop/mapreduce/hadoop-mapreduce-client-jobclient-3.3.1-tests.jar TestDFSIO -read -nrFiles 10 -fileSize 128MB
```
## namenode多目录
hdfs-site.xml
```xml
<property>
  <name>dfs.namenode.name.dir</name>
  <value>file://${hadoop.tmp.dir}/dfs/name1,file://${hadoop.tmp.dir}/dfs/name2</value>
  <description>namenode多目录</description>
</property>
```
## datanode多目录
> 扩容空间
hdfs-site.xml
```xml
<property>
  <name>dfs.datanode.data.dir</name>
  <value>[SSD]file://${hadoop.tmp.dir}/dfs/data1,[RAM_DISK]file://${hadoop.tmp.dir}/dfs/data2</value>
  <description>
    datanode多目录,
    可以主动声明存储类型来指定文件夹的存储介质
    RAM_DISK, SSD, DISK, ARCHIVE
  </description>
</property>
```
## 磁盘数据均衡
```bash
# 1. 生成均衡计划(多硬盘才可以生成)
hdfs diskbalancer -plan <host>
# 2. 执行均衡计划
hdfs diskbalancer -execute <host>.plan.json
# 3. 查看当前均衡任务的执行情况
hdfs diskbalancer -query <host>
# 4. 取消均衡任务
hdfs diskbalancer -cancel <host>.plan.json
```
## HDFS集群扩容和缩容
> 配置白名单与黑名单
>> 白名单: 白名单之外的节点`可以访问集群`,但是集群`不会将数据存储在白名单之外的节点`上</br>
>>> 服役新节点时,添加好环境加入白名单刷新namenode即可</br>
>>> 服役新节点后可以进行数据均衡来平衡空间利用率,尽量在比较`空闲的`节点上执行</br>
>>
>> 黑名单: 集群`不会将数据存储在黑名单之内的节点`上,但是黑名单之内的节点`可以访问集群`</br>
>>> 退役节点时将节点添加到黑名单后刷新namenode即可</br>
>>> 可以在退役之后进行数据均衡
* 第一次配置时候必须重启集群, 往后只需要刷新namenode, 命令`hdfs dfsadmin -refreshNodes`
```bash
# 启动数据均衡
start-balancer.sh -threshold 10  # -threshold 10: 节点之间利用率差额
# 停止数据均衡
stop-balancer.sh 
```
hdfs-site.xml
```xml
<property>
  <name>dfs.hosts</name>
  <value>${HADOOP_HOME}/etc/hadoop/whitelist</value>
  <description>白名单</description>
</property>
<property>
  <name>dfs.hosts.exclude</name>
  <value>${HADOOP_HOME}/etc/hadoop/blacklist</value>
  <description>黑名单</description>
</property>
```
## HDFS存储优化
> 纠删码
>> `为指定路径设置纠删策略`,所有往此路径下存储的文件将应用该策略</br>
>> 假设数据为300MB,将数据以1MB大小拆分,然后组合成3个100MB的数据单元,生成2个100M的校验单元</br>
>> 如果数据不足1MB,则直接生成1MB的数据单元,和2个1MB的校验单元</br>
>> 纠删码名称解释: `RS-3-2-1024k`</br>
>> RS:    使用RS编码</br>
>> 3-2:   每3个数据单元生成2个校验单元</br>
>> 1024k: 每个单元大小是1024 * 1024 = 1048576
```bash
# 查看所有可用策略
hdfs ec -listPolicies
# 为指定路径设置策略
hdfs ec -setPolicy -path <path> -policy <policy>
```
> 异构存储
>> 主要解决不同的数据存储在不同类型的硬盘中达到最佳性能的问题</br>
>> 存储类型:</br>
>>> `RAM_DISK`: 内存镜像文件系统</br>
>>> `SSD`: SSD固态硬盘</br>
>>> `DISK`: 普通硬盘,HDFS中如果没有主动声明数据目录存储类型,默认都是DISK</br>
>>> `ARCHIVE`: 没有特质那种存储介质,主要是计算能力比较弱而存储密度比较高的存储介质,用雷解决容量扩增的问题,一般用于归档</br>
>>
>> 存储粗略: (访问效率自上往下降低)
>>> 策略ID|策略名称      |副本分布              |解释
>>> :-    |:-           |:-                   |:-
>>> 15    |Lazy_Persist |RAM_DISK:1, DISK:n-1 |一个副本保存在内存RAM_DISK中,其他保存在磁盘中
>>> 12    |ALL_SSD      |SSD:n                |所有副本都保存在SSD中
>>> 10    |One_SSD      |SSD:1, DISK:n-1      |一个副本保存在SSD中,其余保存在磁盘中
>>> 7     |Hot(default) |DISK:n               |所有副本都包存在DISK中,这是默认的存储策略
>>> 5     |Warm         |DISK:1, ARCHIVE:n-1  |一个副本保存在磁盘上,其余的保存在归档存储上
>>> 2     |Cold         |ARCHIVE:n            |所有副本都保存在归档存储上
```bash
# 查看所有可用存储策略
hdfs storagepolicies -listPolicies
# 为指定路径(数据存储目录)设置指定的存储策略
hdfs storagepolicies -setStoragePolicy -path <path> -policy <policy>
# 为文件指定新的存储策略之后,移动文件至新的存储介质
hdfs mover <path>
# 获取指定路径(存储目录或文件)的存储策略
hdfs storagepolicies -getStoragePolicy -path <path>
# 取消存储策略(取消策略之后将使用父目录的策略,如果是根目录则重置为默认策略)
hdfs storagepolicies -unsetStoragePolicy -path <path>
# 查看文件快的分布
hdfs fsck <path> -files -blocks -locations
# 查看集群节点
hadoop dfsadmin -report
# 查看linux内存存储数据大小(max locked memory)
ulimit -a
```
```xml
<property>
  <name>dfs.datanode.max.locked.memory</name>
  <value>0</value>
  <description>
    当存储介质为RAM_DISK时,需要设定这个值,这个值需要大于dfs.block.size的值,
    否则会写入客户端所在的DataNode节点的DISK磁盘,其余数据写入其他节点的DISK磁盘
  </description>
</property>
```
## namenode故障处理
> 丢失namenode数据时,将secondarynamenode的文件复制到namenode上启动</br>
> 近期操作未来得及同步的数据将会丢失
## HDFS集群安全模式
> 集群处于安全模式时,不能执行重要操作(写). 集群启动完成后自动推出安全模式
```bash
# 查看安全模式状态
hdfs dfsadmin -safemode get
# 进入安全模式
hdfs dfsadmin -safemode enter
# 离开安全模式
hdfs dfsadmin -safemode leave
# 等待退出安全模式
hdfs dfsadmin -safemode wait
```
hdfs-site.xml
```xml
<property>
  <name>dfs.namenode.safemode.threshold-pct</name>
  <value>0.999f</value>
  <description>副本数达到最小要求的block占总block的百分比时,退出安全模式(默认:0.999f, 只允许丢1个块)</description>
</property>

<property>
  <name>dfs.namenode.safemode.min.datanodes</name>
  <value>0</value>
  <description>达到最小可用datanode数量时,推出安全模式(默认:0)</description>
</property>

<property>
  <name>dfs.namenode.safemode.extension</name>
  <value>30000</value>
  <description>稳定时间(达到条件后,再等待指定时间后,退出安全模式)</description>
</property>
```
## 慢磁盘监控
```bash
# 不要再系统所在磁盘测试,会导致系统崩溃
# 下载测试工具
yum install fio --downloadonly --downloaddir=./fio/
# 作成配置文件
tee fio.conf << EOF
[global]
ioengine=libaio
direct=1
thread=1
norandommap=1
randrepeat=0
runtime=60
ramp_time=6
size=1g
directory=/opt    # 修改为测试目录
[read4k-rand]
stonewall
group_reporting
bs=4k
rw=randread
numjobs=8
iodepth=32
[read64k-seq]
stonewall
group_reporting
bs=64k
rw=read
numjobs=4
iodepth=8
[write4k-rand]
stonewall
group_reporting
bs=4k
rw=randwrite
numjobs=2
iodepth=4
[write64k-seq]
stonewall
group_reporting
bs=64k
rw=write
numjobs=2
iodepth=4
EOF
# 执行测试
fio fio.conf
```
## 小文件归档
```bash
# 启动yarn进程
start-yarn.sh

# 归档文件
hadoop archive -archiveName <archiveName>.har -p <inputPath> <outputPath>

# 查看归档
hadoop fs -ls har:///<harPath>

# 解档文件
hadoop fs -cp har:///<harPath>/* <outputPath>
```
## 集群迁移
> apache集群之间迁移(同类型节点拷贝, NN->NN,DN->DN)
>> `hadoop distcp hdfs://hd01:8020/file hdfs://hd02:8020/file`
# MapReduce生产经验
> 自定义分区,减少数据倾斜
>> 定义类,继承Partitioner抽象类,重写getPartition方法</br>
>> 以下配置文件修改都为`mapred-site.xml`
>
> 减少溢写次数
>> 提高环形缓冲区大小和溢出阈值
```xml
<property>
  <name>mapreduce.task.io.sort.mb</name>
  <value>100</value>
  <description>环形缓冲区大小</description>
</property>
<property>
  <name>mapreduce.map.sort.spill.percent</name>
  <value>0.80</value>
  <description>环形缓冲区溢出阈值</description>
</property>
```
> 增加每次Merge合并次数
>> 提高合并次数
```xml
<property>
  <name>mapreduce.task.io.sort.factor</name>
  <value>10</value>
  <description>每次merge合并次数</description>
</property>
```
> 使用Combiner</br>
```java
job.setCombinerClass(XXXX.class)
```

> 减少磁盘IO
```java
conf.setBoolean("mapreduce.map.output.compress", true)
conf.setClass("mapreduce.map.output.compress.codec", SnappyCodec.class, CompressionCodec.class)
```
> 提高MapTask内存上限制
>> 原则上单个Task处理128MB数据需要1GB内存
```xml
<property>
  <name>mapreduce.map.memory.mb</name>
  <value>-1</value>
  <description>MapTask内存上限</description>
</property>
```
> 控制MapTask堆内存大小
>> 提高java虚拟机内存限制,防止出现OOM
```xml
<property>
  <name>mapreduce.map.java.opts</name>
  <value></value>
  <description>MapTask的java虚拟机内存</description>
</property>
```
> 提高MapTask的CPU核数
>> 计算密集型任务可以增加CPU核数提高效率
```xml
<property>
  <name>mapreduce.map.cpu.vcores</name>
  <value>1</value>
  <description>MapTask的CPU核数</description>
</property>
```
> 每个MapTask任务的最大重试次数
>> 根据机器性能适当提高
```xml
<property>
  <name>mapreduce.map.maxattempts</name>
  <value>4</value>
  <description>MapTask最大重试次数</description>
</property>
```
> 提高Reduce的并行数
```xml
<property>
  <name>mapreduce.reduce.shuffle.parallelcopies</name>
  <value>5</value>
  <description>Reduce的并行数</description>
</property>
```
> 提高Buffer占Reduce的比例
```xml
<property>
  <name>mapreduce.reduce.shuffle.input.buffer.percent</name>
  <value>0.70</value>
  <description>Buffer占Reduce的比例</description>
</property>
```
> 提高写出时数据占用比例
>> Buffer中数据达到指定比例时开始写入磁盘
```xml
<property>
  <name>mapreduce.reduce.shuffle.merge.percent</name>
  <value>0.66</value>
  <description>Buffer写出时数据比例</description>
</property>
```
> 提高ReduceTask的内存上限
>> 原则上单个Task处理128MB数据需要1GB内存
```xml
<property>
  <name>mapreduce.reduce.memory.mb</name>
  <value>-1</value>
  <description>ReduceTask的内存上限</description>
</property>
```
> 控制ReduceTask堆内存大小
>> 提高java虚拟机内存限制,防止出现OOM
```xml
<property>
  <name>mapreduce.reduce.java.opts</name>
  <value></value>
  <description>ReduceTask的java虚拟机内存</description>
</property>
```
> 提高ReduceTask的CPU核数
```xml
<property>
  <name>mapreduce.reduce.cpu.vcores</name>
  <value>1</value>
  <description>ReduceTask的CPU核数</description>
</property>
```
> 每个ReduceTask任务的最大重试次数
>> 根据机器性能适当提高
```xml
<property>
  <name>mapreduce.reduce.maxattempts</name>
  <value>4</value>
  <description>ReduceTask最大重试次数</description>
</property>
```
> 修改ReduceTask申请资源时机
```xml
<property>
  <name>mapreduce.job.reduce.slowstart.completedmaps</name>
  <value>0.05</value>
  <description>当MapTask完成一定百分比后ReduceTask开始申请资源</description>
</property>
```
> 调整Block状态超时时间
>> 如果每条数据的处理时间过长时,需要提高该参数
```xml
<property>
  <name>mapreduce.task.timeout</name>
  <value>600000</value>
  <description>Task处于Block状态时超时时间</description>
</property>
```
> 数据倾斜
>> 1. 过滤空值,或者自定义分区将空值加入随机值打散,再二次聚合
>> 2. map阶段提前处理,如: COmbiner, MapJoin
>> 3. 设置多个reduce数
# Yarn生产经验
> 参考上方
# 综合调优
> 1. 采集数据时,就将小文件或小批数据合并成大文件再上传HDFS
> 2. Hadoop Archive(存储方向),`文件归档为har`
> 3. CombnineTextInputFormat(计算方向),`将多个小文件在切片过程中生成数量较少的切片`
> 4. 开启uber模式
> mapred-site.xml
```xml
<property>
  <name>mapreduce.job.ubertask.enable</name>
  <value>false</value>
  <description>开启uber模式(用于处理小文件)</description>
</property>

<property>
  <name>mapreduce.job.ubertask.maxmaps</name>
  <value>9</value>jvm的最大重用次数(0-9)</description>
</property>

<property>
  <name>mapreduce.job.ubertask.maxreduces</name>
  <value>1</value>
  <description>最大Reduce数量(0-1)</description>
</property>

<property>
  <name>mapreduce.job.ubertask.maxbytes</name>
  <value></value>
  <description>最大数据输入量,不填则为dfs.block.size的值,(0-dfs.block.size)</description>
</property>
```
> MapReduce计算性能
```bash
# 使用RandomWriter产生随机数,每个节点运行10个MapTask,每个MapTask产生约1G大小的二进制随机数
hadoop jar ${HADOOP_HOME}/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.1.jar randomwriter random-data
# 执行sort程序
hadoop jar ${HADOOP_HOME}/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.1.jar sort random-data sorted-data
# 验证是否已经排好序
hadoop jar ${HADOOP_HOME}/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.1.jar testmapredsort -sortInput random-data -sortOutput sorted-data
```
# Hadoop源码解析
## NameNode启动流程
1. 启动9870端口服务
2. 加载镜像文件和编辑日志
3. 初始化NN的RPC服务器
4. NN启动资源检查
5. NN对心跳超时判断
6. 安全模式
## DataNode启动流程
1. 初始化DataXceiverServer
2. 初始化HTTP服务
3. 初始化DN的RPC服务器
4. DN向NN注册
5. 向NN发送心跳
## HDFS上传流程
> create创建过程
1. DN向NN发起创建请求
2. NN处理DN的创建请求
3. DataStreamer启动流程
> write上传过程
1. 向DataStreamer的队列里面写数据
2. 建立管道: 机架感知(块存储位置)
3. 建立管道: Socket发送
4. 建立管道: Socket接收
5. 客户端接收DN写数据应答Response
> YARN
1. Yarn客户端向RM提交作业
2. RM启动MRAppMaster
3. 调度器任务执行(YarnChild)
4. 
# Hadoop源码编译
在联网节点下编译(至少4G内存,防止OOM)
> 依赖包
>> * [hadoop源码](https://dlcdn.apache.org/hadoop/common)
>> * [JDK1.8](https://mirrors.tuna.tsinghua.edu.cn/AdoptOpenJDK/8/jdk/x64/linux/)
>> * [Maven](https://dlcdn.apache.org/maven/maven-3/)
>> * [Protocol](https://github.com/protocolbuffers/protobuf/releases/v2.5.0)
>> * [Cmake](https://github.com/Kitware/CMake/releases/latest)
>
> 环境变量
```bash
export JAVA_HOME=
export MAVEN_HOME=
export PROTOC_HOME=
export PATH=${PATH}:${MAVEN_HOME}/bin:${JAVA_HOME}/bin:${PROTOC_HOME}/bin
```
> 添加配置文件
```bash
# Maven仓库设置阿里源
sed -i "/<\/mirrors>/i <mirror>\n<id>aliyunmaven</id>\n<mirrorOf>*</mirrorOf>\n<name>阿里云公共仓库</name>\n<url>https://maven.aliyun.com/repository/public</url>\n</mirror>" settings.xml
```
> 安装环境
```bash
# 安装工具
yum install -y gcc* make snappy* bzip2* lzo* zlib* lz4* gzip* openssl* svn ncurses* autoconf automake libtool
yum install -y epel-release
yum install -y *zstd*
# 安装cmake(文件目录下)
./bootstrap
make && make install
cmake -version
# 安装Protocol(文件目录下)
./configure --prefix=<安装目录>
make && make install
```
> 开始编译(源码目录下)
```bash
mvn clean package -DskipTests -Pdist,native -Dtar
```


## 全程编译脚本
```bash
#!/bin/bash

declare -A DICT

# 下载地址
HADOOP_URL='https://dlcdn.apache.org/hadoop/common/hadoop-3.3.1/hadoop-3.3.1-src.tar.gz'
JDK_URL='https://mirrors.tuna.tsinghua.edu.cn/AdoptOpenJDK/8/jdk/x64/linux/OpenJDK8U-jdk_x64_linux_hotspot_8u312b07.tar.gz'
MAVEN_URL='https://dlcdn.apache.org/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.tar.gz'
CMAKE_URL='https://github.com/Kitware/CMake/releases/download/v3.22.1/cmake-3.22.1.tar.gz'
PROTOCOL_URL='https://github.com/protocolbuffers/protobuf/releases/download/v2.5.0/protobuf-2.5.0.tar.gz'


HADOOP_URL='/root/hadoop-3.3.1-src.tar.gz'
JDK_URL='/root/OpenJDK8U-jdk_x64_linux_hotspot_8u312b07.tar.gz'
MAVEN_URL='/root/apache-maven-3.6.3-bin.tar.gz'
CMAKE_URL='/root/cmake-3.22.1.tar.gz'
PROTOCOL_URL='/root/protobuf-2.5.0.tar.gz'


# 解压目录
WORKSPACE=/opt/hadoop_compile
HADOOP_DIR=hadoop_source
MAVEN_DIR=maven
JDK_DIR=jdk
CMAKE_DIR=cmake
PROTOCOL_DIR=protocol

DICT=(
    ["${HADOOP_DIR}"]="${HADOOP_URL}"
    ["${MAVEN_DIR}"]="${MAVEN_URL}"
    ["${JDK_DIR}"]="${JDK_URL}"
    ["${CMAKE_DIR}"]="${CMAKE_URL}"
    ["${PROTOCOL_DIR}"]="${PROTOCOL_URL}"
)

# 检查文件是否存在,不存在则下载
for DIR in "${!DICT[@]}"
do
    mkdir -p "${WORKSPACE}/${DIR}"
    echo "检查文件: ${DIR}"
    if [[ ! -f "${DICT[$DIR]}" || -f "${WORKSPACE}/${DIR}/$(basename ${DICT[$DIR]})" ]];then
        echo "没有找到文件: ${DIR}"
        echo "开始下载: ${DICT[$DIR]}"
        curl -Lo "${WORKSPACE}/${DIR}/$(basename ${DICT[$DIR]})" "${DICT[$DIR]}"
        echo -e "${DIR}下载完成\n"
        DICT[$DIR]="${WORKSPACE}/${DIR}/$(basename ${DICT[$DIR]})"
    fi
done

# 解压文件
for DIR in "${!DICT[@]}"
do
    if [[ $(find "${WORKSPACE}/${DIR}" -mindepth 1 -maxdepth 1 -type d | wc -l) == 0  ]];then
        echo "开始解压${DICT[$DIR]}"
        echo "解压到${WORKSPACE}/${DIR}"
        tar -zxvf "${DICT[$DIR]}" -C "${WORKSPACE}/${DIR}" >> /dev/null
    fi
    DICT[$DIR]=$(find "${WORKSPACE}/${DIR}" -mindepth 1 -maxdepth 1 -type d | tail -1)
done

# 安装工具
yum install -y gcc* make snappy* bzip2* lzo* zlib* lz4* gzip* openssl* svn ncurses* autoconf automake libtool
yum install -y epel-release
yum install -y *zstd*

# 安装Protocol
if [[ ! -d "$(dirname ${DICT[$PROTOCOL_DIR]})/protocol" ]];then
    cd ${DICT[$PROTOCOL_DIR]} && ./configure --prefix="$(dirname ${DICT[$PROTOCOL_DIR]})/protocol"
    cd ${DICT[$PROTOCOL_DIR]} && make && make install
fi

# 安装Cmake
cmake -version > /dev/null 2>&1
if [[ $? != 0 ]];then
    cd ${DICT[$CMAKE_DIR]} && ./bootstrap
    cd ${DICT[$CMAKE_DIR]} && make && make install
fi

# 写入环境变量
# tee /etc/profile.d/hadoop_compile.sh << EOF
export JAVA_HOME="${DICT[$JDK_DIR]}"
export MAVEN_HOME="${DICT[$MAVEN_DIR]}"
export PROTOC_HOME="$(dirname ${DICT[$PROTOCOL_DIR]})/protocol/protocol"
export PATH=${PATH}:${MAVEN_HOME}/bin:${JAVA_HOME}/bin:${PROTOC_HOME}/bin
# EOF

# 增加Maven阿里源
grep '阿里云公共仓库' "${DICT[$MAVEN_DIR]}/conf/settings.xml" > /dev/null 2>&1
if [[ $? != 0 ]];then
    sed -i "/<\/mirrors>/i <mirror>\n<id>aliyunmaven</id>\n<mirrorOf>*</mirrorOf>\n<name>阿里云公共仓库</name>\n<url>https://maven.aliyun.com/repository/public</url>\n</mirror>" "${DICT[$MAVEN_DIR]}/conf/settings.xml"
fi

# 开始编译
cd ${DICT[$HADOOP_DIR]} && mvn clean package -DskipTests -Pdist,native -Dtar


mkdir -p "${WORKSPACE}/dist"
cp -p "${DICT[$HADOOP_DIR]}/hadoop-dist/target/hadoop*" "${WORKSPACE}/dist"
```
