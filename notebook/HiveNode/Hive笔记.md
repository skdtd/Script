# Hive基础
## 数据仓库客户端, 将SQL翻译成MapReduce程序用于处理分布式存储集群上的数据
## 优缺点
> 优点
>> * 使用类SQL语法
>> * 擅长处理实时性不高的海量数据
>> * 可以自定义函数
>
> 缺点
>> * HQL表达能力有限, 不能做迭代式算法
>> * 不擅长数据挖掘, 基于MapReduce的数量处理流程, 无法实现效率更高的算法
>> * 自动生成的MapReduce作业通常不够智能化
>> * 调优困难, 粒度较粗, 需要在MapReduce程序上进行调优
## 架构
![Hive架构图](./pic/Hive架构图.png)
# [Hive安装启动](https://cwiki.apache.org/confluence/display/Hive/GettingStarted)
## 下载地址
> * [Hive](https://dlcdn.apache.org/hive/)
> * [MySQL5.7](https://mirrors.tuna.tsinghua.edu.cn/mysql/downloads/MySQL-5.7/mysql-5.7.34-el7-x86_64.tar.gz)
> * [MySQL驱动(Java)](https://mirrors.tuna.tsinghua.edu.cn/mysql/downloads/Connector-J/)
## 解压hive并配置环境变量
```bash
# 环境变量
export HIVE_HOME=
export PATH=${PATH}:%{HIVE_HOME}/bin

# 解压
tar -zxvf <Hive压缩包> -C ${HIVE_HOME}

# 解决日志冲突
mv ${HIVE_HOME}/lib/log4j-slf4j-impl-2.10.0.jar ${HIVE_HOME}/lib/log4j-slf4j-impl-2.10.0.jar.bak

# 启动客户端, 启动前需要初始化元数据
hive
```
### 初始化元数据
1. derby(默认)
```bash
## 在同一个目录下只允许一个实例执行,并会在目录下生成metastore_db文件夹
## FAILED: HiveException java.lang.RuntimeException: Unable to instantiate org.apache.hadoop.hive.ql.metadata.SessionHiveMetaStoreClient
cd ${HIVE_HOME} && schematool -dbType derby -initSchema
```
2. MySQL
> [安装](https://www.linuxidc.com/Linux/2019-12/161832.htm)
>> * [下载MySQL5.7](https://mirrors.tuna.tsinghua.edu.cn/mysql/downloads/MySQL-5.7/mysql-5.7.34-el7-x86_64.tar.gz)
>> * [下载libaio](https://mirrors.aliyun.com/centos/7.9.2009/os/x86_64/Packages/libaio-0.3.109-13.el7.x86_64.rpm)
```bash
#!/bin/bash

# MySQL安装包位置
MYSQL_SRC='./mysql-5.7.34-el7-x86_64.tar.gz'

# MySQL安装目录
MYSQL_WORKSPACE='/usr/local/mysql'
# MySQL数据保存目录
MYSQL_DATA_DIR='/usr/local/mysql/data'
# MySQL日志目录
MYSQL_LOG_DIR='/usr/local/mysql/log'
# MySQL日志文件名
MYSQL_LOG_FILE='mysql.log'

# 用户组
MYSQL_USER='mysql'
MYSQL_GOURP='mysql'

# 包下载地址
MYSQL_URL='https://mirrors.tuna.tsinghua.edu.cn/mysql/downloads/MySQL-5.7/mysql-5.7.34-el7-x86_64.tar.gz'
LIBAIO_URL='https://mirrors.aliyun.com/centos/7.9.2009/os/x86_64/Packages/libaio-0.3.109-13.el7.x86_64.rpm'

# 检查MySQL安装包位置, 如不存在则下载
if [[ ! -f "${MYSQL_SRC}" ]];then
    echo "can not found MySQL Installation package: []"
    echo "Starting to download MySQL installation package"
    curl -L "${MYSQL_URL}" -o "/tmp/$(basename ${MYSQL_URL})"
    MYSQL_SRC="/tmp/$(basename ${MYSQL_URL})"
    echo "Download complete! file path: /tmp/$(basename ${MYSQL_URL})"
fi

# 检查安装目录是否已经存在
if [[ -d "${MYSQL_WORKSPACE}" ]];then
    echo "The installation directory already exists: ${MYSQL_WORKSPACE}"
    exit 1
fi

if [[ -d "${MYSQL_DATA_DIR}" ]];then
    echo "The data directory already exists: ${MYSQL_DATA_DIR}"
    exit 1
fi

echo "Start creating directories and log files"
# 创建目录
mkdir -p  "${MYSQL_WORKSPACE}" "${MYSQL_DATA_DIR}" "${MYSQL_LOG_DIR}"
# 创建日志文件
touch "${MYSQL_LOG_DIR}/${MYSQL_LOG_FILE}"


# 开始解压文件
echo "Start extracting files"
tar -zxf "${MYSQL_SRC}" --strip-components=1 -C "${MYSQL_WORKSPACE}"
if [[ $? != 0 ]];then
    echo "Failed to unzip the file"
    exit 1
fi

# 检查MySQL依赖是否安装, 如未安装则下载
echo "Start checking whether libaio exists"
(yum list installed libaio || rpm -qa | grep libaio) >& /dev/null
if [[ $? != 0 ]];then
    echo "Attempting to install libaio using Yum"
    yum install -y libaio >& /dev/null
    if [[ $? != 0 ]];then
        echo "Failed to install using yum. Start downloading libaio installation package"
        curl -L LIBAIO_URL -o "/tmp/$(basename ${LIBAIO_URL})"
        echo "Download complete! file path: /tmp/$(basename ${LIBAIO_URL})"
        echo "Start installing libaio"
        rpm -i "/tmp/$(basename ${LIBAIO_URL})"
        if [[ $? != 0 ]];then
            echo "Installation failed"
            echo "Exit installation!"
            exit 1
        else
            echo "Installation succeeded"
        fi
    fi
fi

# 创建用户组
echo "Start creating user groups and users"
groupadd "${MYSQL_GOURP}" >& /dev/null
if [[ $? != 0 ]];then
    echo "The ${MYSQL_GOURP} user group exists, it will be reused"
fi
useradd -g "${MYSQL_GOURP}" "${MYSQL_USER}" >& /dev/null
if [[ $? != 0 ]];then
    echo "The ${MYSQL_USER} user exists, it will be reused"
fi

# 修改文件权限
chown -R "${MYSQL_USER}:${MYSQL_GOURP}" "${MYSQL_WORKSPACE}" "${MYSQL_DATA_DIR}" "${MYSQL_LOG_DIR}" "${MYSQL_LOG_DIR}/${MYSQL_LOG_FILE}"
chmod -R 755 "${MYSQL_WORKSPACE}" "${MYSQL_DATA_DIR}" "${MYSQL_LOG_DIR}" "${MYSQL_LOG_DIR}/${MYSQL_LOG_FILE}"

# 生成配置文件
echo "Generate basic configuration file"
if [[ -f /etc/my.cnf ]];then
    echo "The existing configuration file was found and renamed /etc/my.cnf.bak"
    cp -p /etc/my.cnf /etc/my.cnf.bak
fi
cat > /etc/my.cnf << EOF
[client]    
port=3306
socket=/tmp/mysql.sock

[mysqld]
user=mysql
port=3306
socket=/tmp/mysql.sock
basedir=${MYSQL_WORKSPACE}
datadir=${MYSQL_DATA_DIR}
pid-file=${MYSQL_DATA_DIR}/mysql.pid
character-set-server=utf8
symbolic-links=0
EOF

# 初始化MySQL
if [[ $(find "${MYSQL_DATA_DIR}" -type f | wc -l) != 0 ]];then
    echo "There are files in the data folder before initialization, unable to initialize"
    exit 1
fi
echo "Start initializing MySQL"
${MYSQL_WORKSPACE}/bin/mysqld --user=mysql --basedir=${MYSQL_WORKSPACE} --datadir=${MYSQL_DATA_DIR} --initialize

# 设置开机启动并启动MySQL
echo "Set startup and start MySQL"
cp "${MYSQL_WORKSPACE}/support-files/mysql.server" "/etc/init.d/mysql"
chkconfig mysql on
service mysql start

echo "installation is complete!"
echo "Please use the command to log in to MySQL and enter the initial password: ${MYSQL_WORKSPACE}/bin/mysql -uroot -p"
echo "Update your password: alter user user() identified by 'yourpassword';"
```



```bash
# 卸载系统自带的MySQL
sudo rpm -qa | grep mariadb
sudo rpm -e --nodeps mariadb-libs
```
> 配置
${HIVE_HOME}/conf/hive-site.xml
```xml
<property>
  <name>javax.jdo.option.ConnectionURL</name>
  <value>jdbc:mysql://hd01:3306/metastore?useSSL=false</value>
  <description>元数据库连接的URL</description>
</property>
<property>
  <name>javax.jdo.option.ConnectionDriverName</name>
  <value>com.mysql.jdbc.Driver</value>
  <description>元数据库连接的Driver</description>
</property>
<property>
  <name>javax.jdo.option.ConnectionUserName</name>
  <value>APP</value>
  <description>元数据库用户名</description>
</property>
<property>
  <name>javax.jdo.option.ConnectionPassword</name>
  <value>mine</value>
  <description>元数据库密码</description>
</property>
<property>
  <name>hive.metastore.schema.verification</name>
  <value>false</value>
  <description>元数据存储版本验证</description>
</property>
<property>
  <name>hive.metastore.event.db.notification.api.auth</name>
  <value>false</value>
  <description>元数据存储授权</description>
</property>
<property>
  <name>hive.metastore.warehouse.dir</name>
  <value>/user/hive/warehouse</value>
  <description>默认HDFS的存储目录</description>
</property>
```