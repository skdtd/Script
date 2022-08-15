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
![[Hive架构图.png]]
# [Hive安装启动](https://cwiki.apache.org/confluence/display/Hive/GettingStarted)
## 下载地址
> * [Hive](https://dlcdn.apache.org/hive/)
## 解压hive并配置环境变量
```bash
# 环境变量
export HIVE_HOME=
export PATH=${PATH}:%{HIVE_HOME}/bin

# 解压
tar -zxvf <Hive压缩包> -C ${HIVE_HOME}

# 解决日志冲突
mv ${HIVE_HOME}/lib/log4j-slf4j-impl-2.10.0.jar ${HIVE_HOME}/lib/log4j-slf4j-impl-2.10.0.jar.bak

# 跟踪客户端日志
tail -fn0 /tmp/$(id -un)/hive.log
```
## 启动hive
```bash
# 启动客户端, 启动前需要初始化元数据
hive

# 参数配置的优先级
# hive-default.xml < hive-site.xml < 命令行 < 客户端内set(用户代码)

# hive会同通过环境变量获取hadoop配置信息,可以在hive中指定hadoop的配置

# 命令行形式
hive -hiveconf mapred.reduce.tasks=10

# 客户端内set形式
set mapred.reduce.tasks=10

# 客户端内查看配置信息
set mapred.reduce.tasks
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
>> * [MySQL驱动(Java)](https://mirrors.tuna.tsinghua.edu.cn/mysql/downloads/Connector-J/)
>> 安装完成之后使用`schematool -dbType mysql -initSchema -verbose`初始化元数据库
>
> MySQL授权登录(not allowed to connect to this MySQL server)
>> 让root用户从任何主机使用密码登录到mysql服务器
>>> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'password' WITH GRANT OPTION;
>>
>> 让root用户从192.168.100.100使用密码登录到mysql服务器
>>> GRANT ALL PRIVILEGES ON *.* TO 'root'@'192.168.100.100' IDENTIFIED BY 'password' WITH GRANT OPTION;
>>
>> 让root用户从192.168.100.100使用密码登录到mysql服务器的metastore数据库
>>> GRANT ALL PRIVILEGES ON metastore.* TO 'root'@'192.168.100.100' IDENTIFIED BY 'password' WITH GRANT OPTION;
>>
>> 最后都需要`FLUSH PRIVILEGES;`更新权限

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
DRIVER_URL='https://mirrors.tuna.tsinghua.edu.cn/mysql/downloads/Connector-J/mysql-connector-java-5.1.49.tar.gz'

# 卸载自带mariadb
echo "Uninstall mariadb"
rpm -e --nodeps mariadb-libs >& /dev/null

# 下载驱动
echo "download MySQL Driver"
curl -L "${DRIVER_URL}" -o "/tmp/$(basename ${DRIVER_URL})"
cd ${HIVE_HOME}/lib && tar -zxf "/tmp/$(basename ${DRIVER_URL})" "$(tar tf /tmp/$(basename ${DRIVER_URL})  | grep jar | sort | tail -1)" --strip-components=1 -C .
chown --reference=${HIVE_HOME}/lib ${HIVE_HOME}/lib/*

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
## 配置
hive-site.xml
```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
  <property>
    <name>javax.jdo.option.ConnectionURL</name>
    <value>jdbc:mysql://hd01:3306/metastore?useSSL=false</value>
    <description>
      元数据库连接的URL
      需要创建元数据库,数据库名一致
      create database metastore;
    </description>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionDriverName</name>
    <value>com.mysql.jdbc.Driver</value>
    <description>元数据库连接的Driver</description>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionUserName</name>
    <value>root</value>
    <description>元数据库用户名</description>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionPassword</name>
    <value>000000</value>
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
  <property>
    <name>hive.cli.print.current.db</name>
    <value>true</value>
    <description>客户端打印输出库</description>
  </property>
  <property>
    <name>hive.cli.print.header</name>
    <value>true</value>
    <description>客户端打印输出表头</description>
  </property>
</configuration>
```
## 使用元数据服务的方式访问Hive
hive-site.xml
```xml
<property>
  <name>hive.metastore.uris</name>
  <value>thrift://hd01:9083</value>
  <description>
    指定存储元数据要连接的地址
    hive --service metastore  
  </description>
</property>
```
## 使用JDBC方式访问Hive(需要元数据服务)
hive-site.xml
```xml
<property>
  <name>hive.server2.thrift.bind.host</name>
  <value>hd01</value>
  <description>hiveserver2连接主机</description>
</property>
<property>
  <name>hive.server2.thrift.port</name>
  <value>10000</value>
  <description>hiveserver2连接端口</description>
</property>
```
# 数据类型
## 基本类型(支持类型隐式类型提升,整型,单浮点及<b>符合格式的字符串</b>也可以隐式转化为双浮点)
Hive类型   |Java类型|长度           |示例
:-        |:-       |:-            |:-
TINYINT   |byte     |1byte有符号整数|90
SMALINT   |short    |2byte有符号整数|90
INT       |int      |4byte有符号整数|90
BIGINT    |long     |8byte有符号整数|90
BOOLEAN   |boolean  |true/false    |TRUE
FLOAT     |float    |单精度浮点     |3.14
DOUBLE    |double   |双精度浮点     |3.14
STRING    |String   |字符           |"hello"
TIMESTAMP |-        |时间类型       |-
BINARY    |-        |字节数组       |-
## 集合类型(可以嵌套)
类型    |描述                                      |语法
:-      |:-                                       |:-
STRUCT  |和C的struct类似,相当于java中的bean对象     |struct(),struct<street:string,city:string>
MAP     |kv对,可以用['last']这个key获取最后一个元素  |map(),map<string,int>
ARRAY   |数组,索引从0开始                           |Array(),array<string>
### 定义集合类型时的方式
```sql
-- tom,cary_lily,mary:12_tony:13,waitan_shanghai
-- mark,susu,lucy:11,chaoyang_beijing
create table test(
  name string,
  friends array<string>,
  children map<stringm int>,
  address struct<street:string, city:string>
)
row format delimited
fields terminated by ','
collection items terminated by '_'  -- 由于map和array用的分隔符需要统一,所以数据进入时需要进行数据清晰
map keys terminated by ':'
lines terminated by '\n';
```

# DDL
## 库相关操作
```sql
-- 创建库
create database [if not exists] <databaseName>
[comment 数据库描述]
[location 数据库路径] -- 路径需要加引号
[with dbproperties 描述属性]

-- 显示数据库
show databases;
show databases like 'db_*'; -- 显示'db_'开头的数据库

-- 显示数据库的描述信息
desc database <databaseName>
desc database extended <databaseName> -- 显示描述信息等额外信息

-- 修改数据库描述属性
alter database <databaseName> set dbproperties("createTime"="yyyy-MM-dd")

-- 删除数据库
drop database <databaseName>; -- 删除空数据库
drop database <databaseName> cascade; -- 强制删除非空数据库
```
## 表相关操作
```sql
-- 创建表
create [external] table [if not exists] <tableName> -- external: 外部表
[(colName dataType [comment colComment], ...)] -- 列名, 数据类型, 列注释
[comment tableComment] -- 表注释
[partitioned by (colName dataType [comment colComment], ...)] -- 分区表
[clustered by (colName dataType [comment colComment], ...)] -- 分桶表
[sorted by (colName [asc|desc], ...)] into numBuckets buckets -- 分桶表参数
[row format rowFormat] -- 定义行格式, 文件以逗号分隔字段示例示例: row format delimited fields terminated by ',';
[stored as fileFormat] -- 文件格式
[location hdfsPath] -- 指定表存储位置(一般会把此类表设置为外部表)
[tableproperties (key=value, ...)] -- 表额外属性
[as selectStatement] -- 查询方式建表(参考别的表形式来建表)

-- 删除表
drop table <tableName>;

-- 查看表属性
desc formatted <tableName>;

-- 修改表
-- 修改表为外部表,管理表则改为FALSE
alter table <tableName> set tblproperties('EXTERNAL'='TRUE'); -- 属性大小写敏感
-- 重命名表
alter table <tableName> rename to <newTableName>;
-- 修改列
alter table <tableName> change <oldCol> <newCol> <newType>;
-- 增加列
alter table <tableName> add (<col> <type>, ...)
-- 替换(所有)列
alter table <tableName> replace columns (<col> <type>, ...)

```
### 管理表和外部表
* 通过`external`关键字创建的表为外部表
* 管理表在删除表的时候`会删除元数据同步删除真实数据`
* 外部表在删除表的时候`只会删除元数据,不会删除真实数据`
# DML
## 数据导入
```sql
-- 加载数据
load data [local] inpath '<dataPath>' [overwrite] into table <tableName> [partition (partcol1=val1, ...)]
-- local: 是否从系统本地加载, 没有该参数时,会将HDFS目录上的指定文件剪切到表目录
-- inpath: 路径可以是全路径也可以是相对路径, 相对路径是以进入客户端的路径为基准
-- overwrite: 是否覆盖数据, 否则添加文件
-- partition: 上传到指定分区


-- 插入数据
insert into table <tableName> values (<data>),(<data>)...;

-- 根据表数据查询插入
insert overwrite table <tableName> <sqlSelect>
-- insert into: 追加方式插入到表或分区
-- insert overwrite: 覆盖已存在数据

-- 多表查询插入
from <tableName>
insert into table <tableName>
select ...
insert into table <tableName>
select ...
...;
```
## 数据导出
```sql
-- insert导出
insert overwrite [local] directory <localPath> -- local: 使用则导出到系统本地,否则导出到HDFS路径
row format delimited fields terminated by <separator> -- 如果不指定分隔符将会使用系统自带分隔符
<select ...>;

-- export导出到HDFS(配合import在两个hadoop集群间迁移)
export table <tableName> to <path>
```
```bash
# hadoop命令导出到本地
dfs -get <path>

# hive命令导出
hive -e '<select ...>' > <path>
```
## 数据清空
```sql
truncate table <tableName>; -- 内部表有效
```

## 查询
```sql
select [all|distinct] <>
from <tableName>
[where <condition>]
[group by <colList>]
[order by <colList>]
[cluster by <colList> | [disteribute by <colList>] [sort by <colList>]]
[limit <num>]
```
### 算数运算符
运算符|描述
:-    |:-
A+B  |加
A-B  |减
A*B  |乘
A/B  |除
A%B  |取模
A&B  |按位取与
A|B  |按位取或
A^B  |按位异或
~A   |取反
### 常用函数
```sql
count()
max()
min()
sum()
avg()
nvl(a,b): 当a为null,则输出b值

```
> 常用日期函数
```sql
unix_timestamp:返回当前或指定时间的时间戳	
select unix_timestamp();
select unix_timestamp("2020-10-28",'yyyy-MM-dd');

from_unixtime：将时间戳转为日期格式
select from_unixtime(1603843200);

current_date：当前日期
select current_date;

current_timestamp：当前的日期加时间
select current_timestamp;

to_date：抽取日期部分
select to_date('2020-10-28 12:12:12');

year：获取年
select year('2020-10-28 12:12:12');

month：获取月
select month('2020-10-28 12:12:12');

day：获取日
select day('2020-10-28 12:12:12');

hour：获取时
select hour('2020-10-28 12:12:12');

minute：获取分
select minute('2020-10-28 12:12:12');

second：获取秒
select second('2020-10-28 12:12:12');

weekofyear：当前时间是一年中的第几周
select weekofyear('2020-10-28 12:12:12');

dayofmonth：当前时间是一个月中的第几天
select dayofmonth('2020-10-28 12:12:12');

months_between： 两个日期间的月份
select months_between('2020-04-01','2020-10-28');

add_months：日期加减月
select add_months('2020-10-28',-3);

datediff：两个日期相差的天数
select datediff('2020-11-04','2020-10-28');

date_add：日期加天数
select date_add('2020-10-28',4);

date_sub：日期减天数
select date_sub('2020-10-28',-4);

last_day：日期的当月的最后一天
select last_day('2020-02-30');

date_format(): 格式化日期
select date_format('2020-10-28 12:12:12','yyyy/MM/dd HH:mm:ss');
```
> 常用取整函数
```sql
round： 四舍五入
select round(3.14);
select round(3.54);

ceil：  向上取整
select ceil(3.14);
select ceil(3.54);

floor： 向下取整
select floor(3.14);
select floor(3.54);
```
> 常用字符串操作函数
```sql
upper： 转大写
select upper('low');

lower： 转小写
select lower('low');

length： 长度
select length("atguigu");

trim：  前后去空格
select trim(" atguigu ");

lpad： 向左补齐，到指定长度
select lpad('atguigu',9,'g');

rpad：  向右补齐，到指定长度
select rpad('atguigu',9,'g');

regexp_replace：使用正则表达式匹配目标字符串，匹配成功后替换！
SELECT regexp_replace('2020/10/25', '/', '-');
```
> 集合操作
```sql
size： 集合中元素的个数
select size(friends) from test3;

map_keys： 返回map中的key
select map_keys(children) from test3;

map_values: 返回map中的value
select map_values(children) from test3;

array_contains: 判断array中是否包含某个元素
select array_contains(friends,'bingbing') from test3;

sort_array： 将array中的元素排序
select sort_array(friends) from test3;

grouping_set:多维分析
```
### 比较运算符
操作符                  |支持的数据类型|描述
:-                      |:-          |:-
A = B                   |基本型       |如果`A等于B`则返回TRUE,否则返回FALSE
A <=> B                 |基本型       |如果`A和B都为Null`则返回TRUE,否则返回FALSE
A <> B, A != B          |基本型       |A或B为Null则返回Null,如果`A不等于B`则返回TRUE,否则返回FALSE
A < B                   |基本型       |A或B为Null则返回Null,如果`A小于B`则返回TRUE,否则返回FALSE
A <= B                  |基本型       |A或B为Null则返回Null,如果`A小于等于B`则返回TRUE,否则返回FALSE
A > B                   |基本型       |A或B为Null则返回Null,如果`A大于B`则返回TRUE,否则返回FALSE
A >= B                  |基本型       |A或B为Null则返回Null,如果`A大于等于B`则返回TRUE,否则返回FALSE
A [NOT] BRTWEEN B AND C |基本型       |如果ABC任一为Null则返回Null,如果`A大于等于B且小于等于C`则返回TRUE,否则返回FALSE
### like和rlike
> like
>> * %:任意个字符
>> * _:代表一个字符
>
> rlike
>> 使用正则表达式
### 逻辑运算符
* and
* or
* not
### select执行顺序
```sql
(8)SELECT (9)DISTINCT  (11)<Top Num> <select list>
(1)FROM [left_table]
(3)<join_type> JOIN <right_table>
(2)        ON <join_condition>
(4)WHERE <where_condition>
(5)GROUP BY <group_by_list>
(6)WITH <CUBE | RollUP>
(7)HAVING <having_condition>
(10)ORDER BY <order_by_list>
```
顺序         | 描述
:-          |:-
FROM        |对FROM子句中的前两个表执行笛卡尔积（Cartesian product)(交叉联接），生成虚拟表VT1
ON          |对VT1应用ON筛选器。只有那些使<join_condition>为真的行才被插入VT2。
OUTER(JOIN) |如果指定了OUTER JOIN（相对于CROSS JOIN 或(INNER JOIN),保留表（preserved table左外部联接把左表标记为保留表，右外部联接把右表标记为保留表，完全外部联接把两个表都标记为保留表）中未找到匹配的行将作为外部行添加到 VT2,生成VT3.如果FROM子句包含两个以上的表，则对上一个联接生成的结果表和下一个表重复执行步骤1到步骤3，直到处理完所有的表为止。
WHERE       |对VT3应用WHERE筛选器。只有使<where_condition>为true的行才被插入VT4.
GROUP BY    |按GROUP BY子句中的列列表对VT4中的行分组，生成VT5.
CUBE|ROLLUP |把超组(Suppergroups)插入VT5,生成VT6.
HAVING      |对VT6应用HAVING筛选器。只有使<having_condition>为true的组才会被插入VT7.
SELECT      |处理SELECT列表，产生VT8.
DISTINCT    |将重复的行从VT8中移除，产生VT9.
ORDER BY    |将VT9中的行按ORDER BY 子句中的列列表排序，生成游标（VC10).
TOP         |从VC10的开始处选择指定数量或比例的行，生成表VT11,并返回调用者。
### join
> * 使用表别名可以简化查询
> * 使用表名前缀可以提高执行效率
> * on语句遗漏或者无效,会产生笛卡尔积

关键字     |描述
:-        |:-
join      |两个表中都存在与连接条件相匹配的数据时才会保留
left join |左表中符合where子句的数据将被全部保留
right join|右表中符合where子句的数据将被全部保留
full join |所有表中的数据都将被保留

### union
> 连接两张表的数据
* union: 连接两张表并`去重`
* union all: 连接两张表但是`不去重`
当两者结果一致时优先使用union all,执行效率更高

### sort by和order by
> `asd`升序: 默认
> `desc`降序
1. sort by: 可以指定`多个reduce程序`生成多个分区, 数据`随机分配`到各个分区, 仅保持`区内有序`
2. order by: 只能有`1个reduce程序`且只生成1个分区, `全局有序`
distribute by: 配合`sort by`使用, 使用该关键字指定的字段进行分区
cluster by: 当`distribute by`和`sort by`指定同一个字段时,可以用该字段代替, 但是会禁止使用`desc`关键字

### gtoup by
> 条件分组
> 
## 分区表
> 通过load加载的数据会自动创建分区元数据
```sql
-- 创建分区表
create table <tableName> (...)
partitioned by (col colType,...) -- 多级分区则添加多个字段
row format delimited fields terminated by '\t';
-- 查询对应分区只需要添加where子句即可

-- 加载数据
load data local inpath <localPath> into <tableName> partition(col='colName',..);

-- 增加分区
alter table <tableName> add partition(col='colName') ...;

-- 删除分区
alter table <tableName> drop partition(col='colName'), ...;

-- 显示分区
show partitions <tableName>;

-- 查看分区结构
desc formatted <tableName>;

-- 修复分区(检测HDFS目录修复元数据)
msck repair table <tableName>;

-- 动态分区(需要关闭分区严格模式: set hive.exec.dynamic.partition.mode=nonstrict)
-- 必须把分区字段放在select最后
insert into <tableName> partition(partName1, partName2)
select ...,<partName1>,<partName2>... from <tableName>

-- 分区相关参数设置
-- 所有节点最大可以创建动态分区总和(默认:1000)
hive.exec.max.dynamic.partitions
-- 单个节点最大可以创建动态分区数(默认:100)
hive.exec.max.dynamic.partitions.pernode
-- 整个MR任务中最大可以创建的文件数(默认:100000)
hive.exec.max.created.files
-- 当有空分区生成时,是否抛出异常(默认:false)
hive.error.on.empty.partition
```
> hive3.0新特性
>> 在分区严格模式下, 当查询插入时, 最后的字段为分区字段时, 会自动进行动态分区插入
```sql
insert into <tableName>
select ...,<partName1>,<partName2>... from <tableName>
```
## 分桶表
> 根据数据分配到不同的文件中
>> reduce个数设置为-1, 让job自行决定使用多少个reduce或者将reduce的个数设置为大于等于桶数
>> 尽量从hdfs中load到分桶表, 避免本地文件找不到的问题
>> 不要用本地模式
```sql
create table <tableName> (col colType...)
clustered by (col colType) -- 分桶字段必须存在于表字段
into <bucketNum> buckets
row format delimited fields terminated by '\t';
```
## 抽样查询
```sql
-- x: 从第x份样本开始抽样, x的值必须小于等于y的值
-- y: 将整体数据分为y份样本, 抽大约1/y的数据
select * from <tableName> tablesample(bucket <x> out of <y> on <colName>)
```

## hive函数
> 函数分为三大类(几进几出指多少行数据, 并非个数)
> * UDF: 一进一出
> * UDAF: 多进一出
> * UDTF: 一进多出
```sql
-- 显示所有内置函数
show functions;
-- 显示内置函数的用法
desc function <func>;
-- 显示内置函数的用法(详细)
desc function extended <func>;

-- 拼接字符串
concat(s1,s2...sN)          -- 将所有字符拼接在一起
concat_ws(sep,s1,s2...sN)   -- 以sep为分隔符,将所有字符拼接在一起

-- 接受一列数据生成一个Array类型字段
collect_set(col)
```
## 条件判断
```sql
CASE
    WHEN <expr1> THEN <res1>
    WHEN <expr2> THEN <res2>
    ...
    WHEN <exprN> THEN <resN>
    ELSE <res>
END
```
## 侧写
> `lateral view`
>> 将用函数炸裂出来的多行数据与原表数据进行关联
```sql
select
  <colName>,
  ...
  <newColName>
from <tableName>
lateral view <function> <tempTableName> as <newColName>
```
## 窗口函数
> over()

关键字                   | 描述
:-                      |:-
CURRENT ROW             |当前行
n PRECEDING             |往前n行数据
n FOLLOWING             |往后n行数据
UNBOUNDED               |起点
UNBOUNDED PRECEDING     |从起点开始
UNBOUNDED FOLLOWING     |到终点为止
```sql
-- partition by <colName> order by <colName>
-- distribte by <colName> sort by <colName>
-- 以上两种组合等价,但是组合不能打散混用
select
  <colName>,
  <colName> over(partition by <colName> order by <colName> rows BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
from <tableName>
-- partition by <colName>: 以该字段为基础进行开窗, 不同窗口间互不影响
-- order by <colName>: 窗口内数据以该字段进行排序
-- rows BETWEEN ... AND ...: 从窗口中的第...行开始到第...行结束, 默认从起点开始到当前行结束
-- 当order by的字段中有相同的数据, 相同的数据会被视为同一行
```
### 相关函数(必须与over()结合使用)
```sql
-- 往前第n行数据
LAG(col,n,default_val)

-- 往后第n行数据
LEAG(col,n,default_val)

-- 取窗口第一行数据
FIRST_VALUE()

-- 取窗口最后一行数据
LAST_VALUE()

-- 将有序窗口的行分发到指定数据组中, 各组有从1开始的编号, 该函数则返回此行所属组的编号
-- n必须为int型, n为多少即分为多少组
NTILE(n)

-- 排序函数
-- 排序相同时会重复, 总数不会变(即出现并列后不会跳过并列的行数对下一行计数)
RANK()
-- 排序相同时会重复, 总数会减少(即出现并列后跳过并列的行数对下一行计数)
DENSE_RANK()
-- 根据顺序计算(即出现并列后按照出现顺序计数)
-- MR任务中, 由于环形缓冲区的反向溢写, 相同排名的后出现的会排名在上, 可以通过关闭reduce任务解决
ROW_NUMBER()
```
### 自定义函数
```java
import org.apache.hadoop.hive.ql.exec.UDFArgumentException;
import org.apache.hadoop.hive.ql.metadata.HiveException;
import org.apache.hadoop.hive.ql.udf.generic.GenericUDF;
import org.apache.hadoop.hive.serde2.objectinspector.ObjectInspector;

/** 自定义UDF函数(计算输入字符长度): 一进一出 */
public class CustomFuncUDF extends GenericUDF {
    /** 数据校验 */
    public ObjectInspector initialize(ObjectInspector[] objectInspectors) throws UDFArgumentException {
        if (objectInspectors.length != 1)
            throw new UDFArgumentException("The number of parameters must be 1");
        return PrimitiveObjectInspectorFactory.javaIntObjectInspector;
    }
    /** 处理数据 */
    public Object evaluate(DeferredObject[] deferredObjects) throws HiveException {
        if (deferredObjects[0].get() == null)
            return 0;
        return deferredObjects[0].get().toString().length();
    }

    /** 执行计划时显示的字符串 */
    public String getDisplayString(String[] strings) {
        return null;
    }
}
```
```java
import org.apache.hadoop.hive.ql.exec.UDFArgumentException;
import org.apache.hadoop.hive.ql.metadata.HiveException;
import org.apache.hadoop.hive.ql.udf.generic.GenericUDTF;
import org.apache.hadoop.hive.serde2.objectinspector.ObjectInspector;
import org.apache.hadoop.hive.serde2.objectinspector.ObjectInspectorFactory;
import org.apache.hadoop.hive.serde2.objectinspector.StructObjectInspector;
import org.apache.hadoop.hive.serde2.objectinspector.primitive.PrimitiveObjectInspectorFactory;

import java.util.ArrayList;
import java.util.List;

/** 自定义UDTF函数(爆裂以逗号分割的字符串): 一进多出 */
public class CustomFuncUDTF extends GenericUDTF {
    List<String> output = new ArrayList<>();

    /** 数据校验 */
    @Override
    public StructObjectInspector initialize(StructObjectInspector argOIs) throws UDFArgumentException {
        // 输出数据的默认别名(可以被手动设置的别名替换)
        List<String> fieldNames = new ArrayList<>();
        // 输出数据的数据类型
        List<ObjectInspector> fieldOIs = new ArrayList<>();
        fieldNames.add("word");
        fieldOIs.add(PrimitiveObjectInspectorFactory.javaStringObjectInspector);
        // 最终返回值
        return ObjectInspectorFactory.getStandardStructObjectInspector(fieldNames, fieldOIs);
    }

    /** 处理输入数据 */
    public void process(Object[] args) throws HiveException {
        if (args[0] == null) {
            forward(output);
        } else {
            for (String word : args[0].toString().split(",")) {
                output.clear();     // 清空集合
                output.add(word);   // 数据放入集合
                forward(output);    // 写出集合
            }
        }
    }

    /** 收尾方法 */
    public void close() throws HiveException {

    }
}
```
```sql
-- 放在${HIVE_HOME}/lib里的jar包会在启动时加载

-- 在已经启动的客户端动态加载jar包
add jar <jarPath>;

-- 创建函数与java class关联
-- temporary: 创建临时函数, 客户端关闭后自动销毁
-- className: 全类名
create [temporary] function <funcName> as "<className>";
```
# 压缩和存储方式
> 需要在Hadoop中启用压缩
core-site.xml
```xml
<property>
  <name>io.compression.codecs</name>
  <value></value>
  <description>
    可选值:
    org.apache.hadoop.io.compress.DefaultCodec
    org.apache.hadoop.io.compress.GzipCodec
    org.apache.hadoop.io.compress.Bzip2Codec
    org.apache.hadoop.io.compress.Lz4Codec
  </description>
</property>
```
mapred-site.xml
```xml
<property>
  <name>mapreduce.map.output.compress</name>
  <value>false</value>
  <description>启用mapper输出压缩</description>
</property>

<property>
  <name>mapreduce.map.output.compress.codec</name>
  <value>org.apache.hadoop.io.compress.DefaultCodec</value>
  <description>mapper输出压缩编码</description>
</property>
<property>
  <name>mapreduce.output.fileoutputformat.compress</name>
  <value>false</value>
  <description>启用reducer输出压缩</description>
</property>

<property>
  <name>mapreduce.output.fileoutputformat.compress.type</name>
  <value>RECORD</value>
  <description>
    压缩输出类型:
    RECORD: 按行压缩
    BLOCK: 按块压缩
    NONE: 不压缩
  </description>
</property>

<property>
  <name>mapreduce.output.fileoutputformat.compress.codec</name>
  <value>org.apache.hadoop.io.compress.DefaultCodec</value>
  <description>reducer输出压缩编码</description>
</property>
```
hive客户端中开启压缩
```sql
-- 开启hive中间传输数据压缩功能
set hive.exec.compress.intermediate=true;
-- 开启mapreduce中map输出压缩功能
set mapreduce.map.output.compress=true;
-- mapreduce中map输出压缩编码
set mapreduce.map.output.compress.codec=org.apache.hadoop.io.compress.SnappyCodec

-- 开启hive最终输出压缩功能
set hive.exec.compress.output=true;
-- 开启mapreduce最终输出压缩
set mapreduce.output.fileoutputformat.compress=true;
-- 设置mapreduce最终输出压缩编码
set mapreduce.output.fileoutputformat.compress.codec=org.apache.hadoop.io.compress.SnappyCodec;
-- 设置mapreduce最终输出压缩为块压缩
set mapreduce.output.fileoutputformat.compress.type=BLOCK;
```
## ORC存储方式
* 这些参数需要卸载HQL的TBLPROPERTIES字段中
key                     |default  |notes
:-                      |:-       |:-
orc.compress            |ZLIB     |
orc.compress.size       |262144   |
orc.stripe.size         |268435456|
orc.row.index.stride    |10000    |
orc.create.index        |true     |
orc.bloom.filter.columns|""       |
orc.bloom.filter.fpp    |0.05     |
# 查看执行计划
> * HQL前加`explain`关键字
> * 可以用`explain extended`关键字获取更详细信息

# Fetch抓取
```xml
<property>
  <name>hive.fetch.task.conversion</name>
  <value>more</value>
  <description>
    0. none : disable hive.fetch.task.conversion
    1. minimal : SELECT STAR, FILTER on partition columns, LIMIT only
    2. more    : SELECT, FILTER, LIMIT only (support TABLESAMPLE and virtual columns)
  </description>
</property>
```

# 本地模式
> Hive可以通过本地模式在单台机器上处理所有的任务, 对于小数据集, 执行时间可以明显被缩短
```sql
-- 开启本地MR(默认: false)
set hive.exec.mode.local.auto=fasle;
-- 设置local MR的最大数据量, 低于这个值时采用本地模式(默认: 128M)
set hive.exec.mode.local.auto.inputbytes.max=134217728;
-- 设置local MR的最大输入文件个数, 低于这个值时采用本地模式(默认: 4)
set hive.exec.mode.local.auto.files.max=4;
```
```xml
<property>
  <name>hive.exec.mode.local.auto</name>
  <value>false</value>
  <description>开启本地MR(默认: false)</description>
</property>
<property>
  <name>hive.exec.mode.local.auto.inputbytes.max</name>
  <value>134217728</value>
  <description>设置local MR的最大数据量, 低于这个值时采用本地模式(默认: 128M)</description>
</property>
<property>
  <name>hive.exec.mode.local.auto.input.files.max</name>    <value>4</value>
  <description>设置local MR的最大输入文件个数, 低于这个值时采用本地模式(默认: 4)</description>
</property>
```
# 表的优化
## 大小表Join(MapJOIN)
> 3.x的hive已经对小表join大表和大表join小表进行了优化,小表位置已经没有区别
```xml
<property>
  <name>hive.auto.convert.join</name>
  <value>true</value>
  <description>始终保持小表Join大表</description>
</property>
<property>
  <name>hive.mapjoin.smalltable.filesize</name>
  <value>25000000</value>
  <description>设置大小表阈值(默认: 25M)</description>
</property>
```
### 空key过滤
> 使用场景
>> * 非inner join
>> * 不需要字段为Null的(先过滤再join,减少join时处理的数据集)
### 空key转化
> 注意添加的随机值不能满足join条件 

### SMBJoin(Sort Merge Bucket Join)
```sql
-- 是否开启桶Join
set hive.optimize.bucketmapjoin=true
-- 是否开启SMBJoin
set hive.optimize.bucketmapjoin.sortedmerge=true
-- 默认输入格式
set hive.input.format=org.apache.hadoop.hive.ql.io.BucketizedHiveInputFormat
```
```xml
<property>
  <name>hive.optimize.bucketmapjoin</name>
  <value>true</value>
  <description>是否开启桶Join</description>
</property>
<property>
  <name>hive.optimize.bucketmapjoin.sortedmerge</name>
  <value>true</value>
  <description>是否开启SMBJoin</description>
</property>
<property>
  <name>hive.input.format</name>
  <value>org.apache.hadoop.hive.ql.io.BucketizedHiveInputFormat</value>
  <description>默认输入格式</description>
</property>
```
### 数据倾斜(group by)
```sql
-- 是否在Map端进行聚合(默认true)
set hive.map.aggr=true
-- 在Map端进行聚合操作的条目数目
set hive.groupby.mapaggr.checkinterval=100000
-- 出现数据倾斜时进行负载均衡(默认false)(如果没有数据倾斜使用的话反而增加会执行时间)
-- 当设置为true时,查询计划会生成2个MRjob
-- 第一个job会将Map输出随机分配到reduce中并输出结果,避免相同key分配到同一个reduce中
-- 第二个job会根据预处理的数据按照指定的group by规则把数据分不到reduce中
set hive.groupby.skewindata=true
```
### Count(distinct)去重统计
> 数据量小的时候无所谓,数据量大的情况下,由于Count(distinct)操作需要用一个Reduce任务来完成,这一个Reduce需要处理的数据量太大,就会导致整个Job很难完成,`一般Count(distinct)使用先Group by在Count的方式替换`,注意数据倾斜的问题
### 行列过滤
> * 列处理: 在select中,只拿需要的列,如果又分区尽量使用分区过滤,避免使用'*'
> * 行处理: 在分区剪裁中,当使用外关联时,如果将副表的过滤条件写在where后面,那么就会先全表关联,再过滤(谓词下推: hive的优化机制会根据hql优化关键字执行顺序),但是在Hql过长的时候可能会导致谓词下推失效,所以尽可能主动优化
### 复杂文件增加Map数量
> 当input文件很大,`字段少而记录多,或者单行任务逻辑十分复杂`,map执行慢的时候可以考虑增加Map数量,使每个map处理的数据量减少,从而提高任务的执行效率
```sql
set mapreduce.input.fileinputformat.split.maxsize=100;
```
### 小文件合并
> 在map执行前合并小文件,减少map数量,以及在Map-Reduce任务结束时合并小文件
```sql
-- 设置输入小文件合并
set hive.input.format=org.apache.hadoop.hive.ql.io.CombineHiveInputFormat;
-- 在Map-only任务结束时合并小文件(默认: true)
set hive.merge.mapfiles=true;
-- 在Map-reduce任务结束时合并小文件(默认: false)
set hive.merge.mapredfiles=true;
-- 合并文件的大小(默认: 256M)
set hive.merge.size.per.task=268435456;
-- 当输出文件的平均大小小于该值时,启动一个独立的mMap-reduce任务进行merge
set hive.merge.smallfiles.avgsize=16777216;
```
### 调整reduce数量
```sql
-- 每个reduce处理的默认数据量(默认: 256M)
set hive.exec.reducers.bytes.per.reducer=256000000
-- 每个任务最大reduce数(默认: 1009)
set hive.exec.reducers.max=1009
-- 系统自动配置reduce数公式: min(<每个任务最大reduce数>, <总数据量>/<每个reduce处理的默认数据量>)

-- 直接设置reduce数
set mapreduce.job.reduces=15;
```
### 并行执行
```sql
-- 开启任务并行
set hive.exec.parallel=true;
-- 同一个sql最大并行度(默认: 8)
set hive.exec.parallel.thread.number=8;
```
### 严格模式
```sql
-- 分区表不使用分区过滤(默认: false)
-- 设置为true时,除非where语句包含分区字段,否则不允许执行
set hive.strict.checks.no.partition.filter=false;

-- 使用order by没有limit过滤(默认false)
-- 设置为true时,对使用了order by的语句必须使用limit语句
-- 会在每个map任务只输出指定limit的数据到reduce,在最后reduce中再取指定limit的数据
set hive.strict.checks.orderby.no.limit=false

-- 笛卡尔积(默认: false)
-- 设置为true时,不允许笛卡尔积查询
set hive.strict.checks.cartesian.product=false
```
### JVM重用
> 使用hadoop配置
```sql
-- 开启uber模式(用于处理小文件)(默认: false)
set mapreduce.job.ubertask.enable=true;
-- jvm的最大重用次数(0-9)
set mapreduce.job.ubertask.maxmaps=9;
-- 最大Reduce数量(0-1)
set mapreduce.job.ubertask.maxreduces=1;
-- 最大数据输入量,不填则为dfs.block.size的值,(0-dfs.block.size)
set mapreduce.job.ubertask.maxbytes;
```

# 配置文件样例
```conf
[client]    
port = 3306
socket = /tmp/mysql.sock

[mysqld]
# MySQL的管理用户
user = mysql
# 端口
port = 3306
# 启动的sock文件
socket = /tmp/mysql.sock
basedir = /usr/local/mysql
datadir = /usr/local/mysql/data/
log-bin = /usr/local/mysql/data/mysql-bin
pid-file = /usr/local/mysql/data/mysql.pid
bind-address = 0.0.0.0
server-id = 1 #表示是本机的序号为1,一般来讲就是master的意思

skip-name-resolve
# 禁止MySQL对外部连接进行DNS解析，使用这一选项可以消除MySQL进行DNS解析的时间。但需要注意，如果开启该选项，
# 则所有远程主机连接授权都要使用IP地址方式，否则MySQL将无法正常处理连接请求

#skip-networking

back_log = 600
# MySQL能有的连接数量。当主要MySQL线程在一个很短时间内得到非常多的连接请求，这就起作用，
# 然后主线程花些时间(尽管很短)检查连接并且启动一个新线程。back_log值指出在MySQL暂时停止回答新请求之前的短时间内多少个请求可以被存在堆栈中。
# 如果期望在一个短时间内有很多连接，你需要增加它。也就是说，如果MySQL的连接数据达到max_connections时，新来的请求将会被存在堆栈中，
# 以等待某一连接释放资源，该堆栈的数量即back_log，如果等待连接的数量超过back_log，将不被授予连接资源。
# 另外，这值（back_log）限于您的操作系统对到来的TCP/IP连接的侦听队列的大小。
# 你的操作系统在这个队列大小上有它自己的限制（可以检查你的OS文档找出这个变量的最大值），试图设定back_log高于你的操作系统的限制将是无效的。

max_connections = 1000
# MySQL的最大连接数，如果服务器的并发连接请求量比较大，建议调高此值，以增加并行连接数量，当然这建立在机器能支撑的情况下，因为如果连接数越多，介于MySQL会为每个连接提供连接缓冲区，就会开销越多的内存，所以要适当调整该值，不能盲目提高设值。可以过'conn%'通配符查看当前状态的连接数量，以定夺该值的大小。

max_connect_errors = 6000
# 对于同一主机，如果有超出该参数值个数的中断错误连接，则该主机将被禁止连接。如需对该主机进行解禁，执行：FLUSH HOST。

open_files_limit = 65535
# MySQL打开的文件描述符限制，默认最小1024;当open_files_limit没有被配置的时候，比较max_connections*5和ulimit -n的值，哪个大用哪个，
# 当open_file_limit被配置的时候，比较open_files_limit和max_connections*5的值，哪个大用哪个。

table_open_cache = 128
# MySQL每打开一个表，都会读入一些数据到table_open_cache缓存中，当MySQL在这个缓存中找不到相应信息时，才会去磁盘上读取。默认值64
# 假定系统有200个并发连接，则需将此参数设置为200*N(N为每个连接所需的文件描述符数目)；
# 当把table_open_cache设置为很大时，如果系统处理不了那么多文件描述符，那么就会出现客户端失效，连接不上

max_allowed_packet = 4M
# 接受的数据包大小；增加该变量的值十分安全，这是因为仅当需要时才会分配额外内存。例如，仅当你发出长查询或MySQLd必须返回大的结果行时MySQLd才会分配更多内存。
# 该变量之所以取较小默认值是一种预防措施，以捕获客户端和服务器之间的错误信息包，并确保不会因偶然使用大的信息包而导致内存溢出。

binlog_cache_size = 1M
# 一个事务，在没有提交的时候，产生的日志，记录到Cache中；等到事务提交需要提交的时候，则把日志持久化到磁盘。默认binlog_cache_size大小32K

max_heap_table_size = 8M
# 定义了用户可以创建的内存表(memory table)的大小。这个值用来计算内存表的最大行数值。这个变量支持动态改变

tmp_table_size = 16M
# MySQL的heap（堆积）表缓冲大小。所有联合在一个DML指令内完成，并且大多数联合甚至可以不用临时表即可以完成。
# 大多数临时表是基于内存的(HEAP)表。具有大的记录长度的临时表 (所有列的长度的和)或包含BLOB列的表存储在硬盘上。
# 如果某个内部heap（堆积）表大小超过tmp_table_size，MySQL可以根据需要自动将内存中的heap表改为基于硬盘的MyISAM表。还可以通过设置tmp_table_size选项来增加临时表的大小。也就是说，如果调高该值，MySQL同时将增加heap表的大小，可达到提高联接查询速度的效果

read_buffer_size = 2M
# MySQL读入缓冲区大小。对表进行顺序扫描的请求将分配一个读入缓冲区，MySQL会为它分配一段内存缓冲区。read_buffer_size变量控制这一缓冲区的大小。
# 如果对表的顺序扫描请求非常频繁，并且你认为频繁扫描进行得太慢，可以通过增加该变量值以及内存缓冲区大小提高其性能

read_rnd_buffer_size = 8M
# MySQL的随机读缓冲区大小。当按任意顺序读取行时(例如，按照排序顺序)，将分配一个随机读缓存区。进行排序查询时，
# MySQL会首先扫描一遍该缓冲，以避免磁盘搜索，提高查询速度，如果需要排序大量数据，可适当调高该值。但MySQL会为每个客户连接发放该缓冲空间，所以应尽量适当设置该值，以避免内存开销过大

sort_buffer_size = 8M
# MySQL执行排序使用的缓冲大小。如果想要增加ORDER BY的速度，首先看是否可以让MySQL使用索引而不是额外的排序阶段。
# 如果不能，可以尝试增加sort_buffer_size变量的大小

join_buffer_size = 8M
# 联合查询操作所能使用的缓冲区大小，和sort_buffer_size一样，该参数对应的分配内存也是每连接独享

thread_cache_size = 8
# 这个值（默认8）表示可以重新利用保存在缓存中线程的数量，当断开连接时如果缓存中还有空间，那么客户端的线程将被放到缓存中，
# 如果线程重新被请求，那么请求将从缓存中读取,如果缓存中是空的或者是新的请求，那么这个线程将被重新创建,如果有很多新的线程，
# 增加这个值可以改善系统性能.通过比较Connections和Threads_created状态的变量，可以看到这个变量的作用。(–>表示要调整的值)
# 根据物理内存设置规则如下：
# 1G  —> 8
# 2G  —> 16
# 3G  —> 32
# 大于3G  —> 64

query_cache_size = 8M
#MySQL的查询缓冲大小（从4.0.1开始，MySQL提供了查询缓冲机制）使用查询缓冲，MySQL将SELECT语句和查询结果存放在缓冲区中，
# 今后对于同样的SELECT语句（区分大小写），将直接从缓冲区中读取结果。根据MySQL用户手册，使用查询缓冲最多可以达到238%的效率。
# 通过检查状态值'Qcache_%'，可以知道query_cache_size设置是否合理：如果Qcache_lowmem_prunes的值非常大，则表明经常出现缓冲不够的情况，
# 如果Qcache_hits的值也非常大，则表明查询缓冲使用非常频繁，此时需要增加缓冲大小；如果Qcache_hits的值不大，则表明你的查询重复率很低，
# 这种情况下使用查询缓冲反而会影响效率，那么可以考虑不用查询缓冲。此外，在SELECT语句中加入SQL_NO_CACHE可以明确表示不使用查询缓冲

query_cache_limit = 2M
#指定单个查询能够使用的缓冲区大小，默认1M

key_buffer_size = 4M
#指定用于索引的缓冲区大小，增加它可得到更好处理的索引(对所有读和多重写)，到你能负担得起那样多。如果你使它太大，
# 系统将开始换页并且真的变慢了。对于内存在4GB左右的服务器该参数可设置为384M或512M。通过检查状态值Key_read_requests和Key_reads，
# 可以知道key_buffer_size设置是否合理。比例key_reads/key_read_requests应该尽可能的低，
# 至少是1:100，1:1000更好(上述状态值可以使用SHOW STATUS LIKE 'key_read%'获得)。注意：该参数值设置的过大反而会是服务器整体效率降低

ft_min_word_len = 4
# 分词词汇最小长度，默认4

transaction_isolation = REPEATABLE-READ
# MySQL支持4种事务隔离级别，他们分别是：
# READ-UNCOMMITTED, READ-COMMITTED, REPEATABLE-READ, SERIALIZABLE.
# 如没有指定，MySQL默认采用的是REPEATABLE-READ，ORACLE默认的是READ-COMMITTED

log_bin = mysql-bin
binlog_format = mixed
expire_logs_days = 30 #超过30天的binlog删除

log_error = /data/mysql/mysql-error.log #错误日志路径
slow_query_log = 1
long_query_time = 1 #慢查询时间 超过1秒则为慢查询
slow_query_log_file = /data/mysql/mysql-slow.log

performance_schema = 0
explicit_defaults_for_timestamp

#lower_case_table_names = 1 #不区分大小写

skip-external-locking #MySQL选项以避免外部锁定。该选项默认开启

default-storage-engine = InnoDB #默认存储引擎

innodb_file_per_table = 1
# InnoDB为独立表空间模式，每个数据库的每个表都会生成一个数据空间
# 独立表空间优点：
# 1．每个表都有自已独立的表空间。
# 2．每个表的数据和索引都会存在自已的表空间中。
# 3．可以实现单表在不同的数据库中移动。
# 4．空间可以回收（除drop table操作处，表空不能自已回收）
# 缺点：
# 单表增加过大，如超过100G
# 结论：
# 共享表空间在Insert操作上少有优势。其它都没独立表空间表现好。当启用独立表空间时，请合理调整：innodb_open_files

innodb_open_files = 500
# 限制Innodb能打开的表的数据，如果库里的表特别多的情况，请增加这个。这个值默认是300

innodb_buffer_pool_size = 64M
# InnoDB使用一个缓冲池来保存索引和原始数据, 不像MyISAM.
# 这里你设置越大,你在存取表里面数据时所需要的磁盘I/O越少.
# 在一个独立使用的数据库服务器上,你可以设置这个变量到服务器物理内存大小的80%
# 不要设置过大,否则,由于物理内存的竞争可能导致操作系统的换页颠簸.
# 注意在32位系统上你每个进程可能被限制在 2-3.5G 用户层面内存限制,
# 所以不要设置的太高.

innodb_write_io_threads = 4
innodb_read_io_threads = 4
# innodb使用后台线程处理数据页上的读写 I/O(输入输出)请求,根据你的 CPU 核数来更改,默认是4
# 注:这两个参数不支持动态改变,需要把该参数加入到my.cnf里，修改完后重启MySQL服务,允许值的范围从 1-64

innodb_thread_concurrency = 0
# 默认设置为 0,表示不限制并发数，这里推荐设置为0，更好去发挥CPU多核处理能力，提高并发量

innodb_purge_threads = 1
# InnoDB中的清除操作是一类定期回收无用数据的操作。在之前的几个版本中，清除操作是主线程的一部分，这意味着运行时它可能会堵塞其它的数据库操作。
# 从MySQL5.5.X版本开始，该操作运行于独立的线程中,并支持更多的并发数。用户可通过设置innodb_purge_threads配置参数来选择清除操作是否使用单
# 独线程,默认情况下参数设置为0(不使用单独线程),设置为 1 时表示使用单独的清除线程。建议为1

innodb_flush_log_at_trx_commit = 2
# 0：如果innodb_flush_log_at_trx_commit的值为0,log buffer每秒就会被刷写日志文件到磁盘，提交事务的时候不做任何操作（执行是由mysql的master thread线程来执行的。
# 主线程中每秒会将重做日志缓冲写入磁盘的重做日志文件(REDO LOG)中。不论事务是否已经提交）默认的日志文件是ib_logfile0,ib_logfile1
# 1：当设为默认值1的时候，每次提交事务的时候，都会将log buffer刷写到日志。
# 2：如果设为2,每次提交事务都会写日志，但并不会执行刷的操作。每秒定时会刷到日志文件。要注意的是，并不能保证100%每秒一定都会刷到磁盘，这要取决于进程的调度。
# 每次事务提交的时候将数据写入事务日志，而这里的写入仅是调用了文件系统的写入操作，而文件系统是有 缓存的，所以这个写入并不能保证数据已经写入到物理磁盘
# 默认值1是为了保证完整的ACID。当然，你可以将这个配置项设为1以外的值来换取更高的性能，但是在系统崩溃的时候，你将会丢失1秒的数据。
# 设为0的话，mysqld进程崩溃的时候，就会丢失最后1秒的事务。设为2,只有在操作系统崩溃或者断电的时候才会丢失最后1秒的数据。InnoDB在做恢复的时候会忽略这个值。
# 总结
# 设为1当然是最安全的，但性能页是最差的（相对其他两个参数而言，但不是不能接受）。如果对数据一致性和完整性要求不高，完全可以设为2，如果只最求性能，例如高并发写的日志服务器，设为0来获得更高性能

innodb_log_buffer_size = 2M
# 此参数确定些日志文件所用的内存大小，以M为单位。缓冲区更大能提高性能，但意外的故障将会丢失数据。MySQL开发人员建议设置为1－8M之间

innodb_log_file_size = 32M
# 此参数确定数据日志文件的大小，更大的设置可以提高性能，但也会增加恢复故障数据库所需的时间

innodb_log_files_in_group = 3
# 为提高性能，MySQL可以以循环方式将日志文件写到多个文件。推荐设置为3

innodb_max_dirty_pages_pct = 90
# innodb主线程刷新缓存池中的数据，使脏数据比例小于90%

innodb_lock_wait_timeout = 120 
# InnoDB事务在被回滚之前可以等待一个锁定的超时秒数。InnoDB在它自己的锁定表中自动检测事务死锁并且回滚事务。InnoDB用LOCK TABLES语句注意到锁定设置。默认值是50秒

bulk_insert_buffer_size = 8M
# 批量插入缓存大小， 这个参数是针对MyISAM存储引擎来说的。适用于在一次性插入100-1000+条记录时， 提高效率。默认值是8M。可以针对数据量的大小，翻倍增加。

myisam_sort_buffer_size = 8M
# MyISAM设置恢复表之时使用的缓冲区的尺寸，当在REPAIR TABLE或用CREATE INDEX创建索引或ALTER TABLE过程中排序 MyISAM索引分配的缓冲区

myisam_max_sort_file_size = 10G
# 如果临时文件会变得超过索引，不要使用快速排序索引方法来创建一个索引。注释：这个参数以字节的形式给出

myisam_repair_threads = 1
# 如果该值大于1，在Repair by sorting过程中并行创建MyISAM表索引(每个索引在自己的线程内) 

interactive_timeout = 28800
# 服务器关闭交互式连接前等待活动的秒数。交互式客户端定义为在mysql_real_connect()中使用CLIENT_INTERACTIVE选项的客户端。默认值：28800秒（8小时）

wait_timeout = 28800
# 服务器关闭非交互连接之前等待活动的秒数。在线程启动时，根据全局wait_timeout值或全局interactive_timeout值初始化会话wait_timeout值，
# 取决于客户端类型(由mysql_real_connect()的连接选项CLIENT_INTERACTIVE定义)。参数默认值：28800秒（8小时）
# MySQL服务器所支持的最大连接数是有上限的，因为每个连接的建立都会消耗内存，因此我们希望客户端在连接到MySQL Server处理完相应的操作后，
# 应该断开连接并释放占用的内存。如果你的MySQL Server有大量的闲置连接，他们不仅会白白消耗内存，而且如果连接一直在累加而不断开，
# 最终肯定会达到MySQL Server的连接上限数，这会报'too many connections'的错误。对于wait_timeout的值设定，应该根据系统的运行情况来判断。
# 在系统运行一段时间后，可以通过show processlist命令查看当前系统的连接状态，如果发现有大量的sleep状态的连接进程，则说明该参数设置的过大，
# 可以进行适当的调整小些。要同时设置interactive_timeout和wait_timeout才会生效。

[mysqldump]
quick
max_allowed_packet = 16M #服务器发送和接受的最大包长度

[myisamchk]
key_buffer_size = 8M
sort_buffer_size = 8M
read_buffer = 4M
write_buffer = 4M
```