# Flume流式日志传输框架
> [官网](flume.apache.org)
* 为兼容Hadoop3.x,删除`${FLUME_HOME}/lib/guava*`
* 环境变量中必须有`Java和Hadoop的变量`

## 配置文件
```conf
# Name the components on this agent
# a1: 当前agent的名称
# 当同时启动多个agent的时候,名称不能相同

# 数据源
a1.sources = r1
# 输出
a1.sinks = k1
# 通道
a1.channels = c1

# Describe/configure the source
# 配置数据源
# 数据源类型
a1.sources.r1.type = netcat
# 数据源地址
a1.sources.r1.bind = localhost
# 数据源端口
a1.sources.r1.port = 44444

# Describe the sink
# 配置输出
# 控制台打印
a1.sinks.k1.type = logger

# Use a channel which buffers events in memory
# 配置通道
# 通道类型
a1.channels.c1.type = memory
# 通道容量
a1.channels.c1.capacity = 1000
# 单个事务最大容量
a1.channels.c1.transactionCapacity = 100

# Bind the source and sink to the channel
# 绑定
a1.sources.r1.channels = c1
a1.sinks.k1.channel = c1
```
## 启动命令
```bash
# AGENT_NAME: 配置中设定的agent名称
# CONF_FILE : 配置文件
# -Dflume.root.logger=INFO,console: 打印到控制台
flume-ng agent -n $AGENT_NAME -c ${FLUME_HOME}/conf -f $CONF_FILE -Dflume.root.logger=INFO,console
```
# 配置样例
## taildir
> * 会生成json来记录文件信息
>> 1. inode: linux中文件唯一标识,重命名移动文件不会修改该值,除非删除文件重新创建
>> 2. pos: 当前偏移量
>> 3. path: 文件路径
```conf
# Name the components on this agent
# a1: 当前agent的名称
# 当同时启动多个agent的时候,名称不能相同

# 数据源
a1.sources = r1
# 输出
a1.sinks = k1
# 通道
a1.channels = c1

a1.sources.r1.type = TAILDIR
a1.sources.r1.positionFile = /opt/flume-1.9.0/job/taildir_position.json
a1.sources.r1.filegroups = flume hive
# 文件名要使用正则
a1.sources.r1.filegroups.flume = /opt/flume-1.9.0/logs/.*
a1.sources.r1.filegroups.hive = /opt/hive-3.1.2/logs/.*
a1.sources.r1.headers.flume.headerKey1 = flume
a1.sources.r1.headers.hive.headerKey1 = hive
a1.sources.r1.fileHeader = true
a1.sources.ri.maxBatchCount = 1000

a1.sinks.k1.type = hdfs
a1.sinks.k1.hdfs.path = hdfs://hd01:8020/flume/events/%y-%m-%d/%H%M/%S
a1.sinks.k1.hdfs.filePrefix = events-
# 设置文件滚动
a1.sinks.k1.hdfs.round = true
a1.sinks.k1.hdfs.roundValue = 1
a1.sinks.k1.hdfs.roundUnit = hour
a1.sinks.k1.hdfs.useLocalTimeStamp = true
a1.sinks.k1.hdfs.batchSize = 100
a1.sinks.k1.hdfs.fileType = DataStream
# 以下三个条件任意满足则生成新文件
# 每经过指定秒数生成一个新文件
a1.sinks.k1.hdfs.rollInterval = 3600
# 设置文件最大大小(略小于128M)
a1.sinks.k1.hdfs.rollSize = 134217700
# 按照事件量生成一个新文件(0: 代表不生成)
a1.sinks.k1.hdfs.rollCount = 0
# Use a channel which buffers events in memory
# 配置通道
# 通道类型
a1.channels.c1.type = memory
# 通道容量
a1.channels.c1.capacity = 1000
# 单个事务最大容量
a1.channels.c1.transactionCapacity = 100


# 绑定
a1.sources.r1.channels = c1
a1.sinks.k1.channel = c1
```
### 当监控log4j日志时,日志滚动更新,导致日志文件被重复读取
> 1. 改用logback框架
> 2. 修改源码,只使用inode来标识文件唯一性
```java
// 
// org.apache.flume.source.taildir.TailFile#updatePos
public boolean updatePos(String path, long inode, long pos) throws IOException {
// if (this.inode == inode && this.path.equals(path)) {
if (this.inode == inode) {
    setPos(pos);
    updateFilePos(pos);
    logger.info("Updated position, file: " + path + ", inode: " + inode + ", pos: " + pos);
    return true;
}
return false;
}

// org.apache.flume.source.taildir.ReliableTaildirEventReader#updateTailFiles(boolean)
  /**
   * Update tailFiles mapping if a new file is created or appends are detected
   * to the existing file.
   */
public List<Long> updateTailFiles(boolean skipToEnd) throws IOException {
updateTime = System.currentTimeMillis();
List<Long> updatedInodes = Lists.newArrayList();

for (TaildirMatcher taildir : taildirCache) {
    Map<String, String> headers = headerTable.row(taildir.getFileGroup());

    for (File f : taildir.getMatchingFiles()) {
    long inode;
    try {
        inode = getInode(f);
    } catch (NoSuchFileException e) {
        logger.info("File has been deleted in the meantime: " + e.getMessage());
        continue;
    }
    TailFile tf = tailFiles.get(inode);
    // if (tf == null || !tf.getPath().equals(f.getAbsolutePath())) {
    if (tf == null) {
        long startPos = skipToEnd ? f.length() : 0;
        tf = openFile(f, headers, inode, startPos);
    } else {
        boolean updated = tf.getLastUpdated() < f.lastModified() || tf.getPos() != f.length();
        if (updated) {
        if (tf.getRaf() == null) {
            tf = openFile(f, headers, inode, tf.getPos());
        }
        if (f.length() < tf.getPos()) {
            logger.info("Pos " + tf.getPos() + " is larger than file size! "
                + "Restarting from pos 0, file: " + tf.getPath() + ", inode: " + inode);
            tf.updatePos(tf.getPath(), inode, 0);
        }
        }
        tf.setNeedTail(updated);
    }
    tailFiles.put(inode, tf);
    updatedInodes.add(inode);
    }
}
return updatedInodes;
}

```