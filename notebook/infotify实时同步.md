# infotify + rsync (目录全同步)
## inotifywait 参数说明
```
-m  --monitor	始终保持事件监听状态
-r  --recursive	递归查询目录
-q  --quiet     只打印监控事件的信息
    --excludei	排除文件或目录时，不区分大小写
-t, --timeout	超时时间
    --timefmt	指定时间输出格式
    --format	指定时间输出格式
-e  --event     后面指定删、增、改等事件
```
## inotifywait events事件说明
```
access          读取文件或目录内容
modify          修改文件或目录内容
attrib          文件或目录的属性改变
close_write     修改真实文件内容
close_nowrite
close
open            文件或目录被打开
moved_to        文件或目录移动到
moved_from      文件或目录从移动
move            移动文件或目录移动到监视目录
create          在监视目录下创建文件或目录
delete          删除监视目录下的文件或目录
delete_self	
unmount         卸载文件系统
```
## /proc/sys/fs/inotify下inotify的三个配置文件
```
max_queued_events       # 设置inotifywait或inotifywatch命令可以监视的文件数量(单进程)
max_user_instances      # 设置每个用户可以运行的inotifywait或inotifywatch命令的进程数
max_user_watches        # 设置inotify实例事件(event)队列可容纳的事件数量

echo 50000000 > /proc/sys/fs/inotify/max_user_watches       # 加入/etc/rc.local就可以实现每次重启都生效
```

## 服务端配置
```bash
# 添加模块信息
echo "uid = rsync
gid = rsync
use chroot = no
max connections = 200
timeout = 300
pid file = /var/run/rsyncd.pid
lock file = /var/run/rsync.lock
log file = /var/log/rsyncd.log

[backup]
path = /backup
fake super = yes
ignore errors
read only = false
list = false
auth users = rsync
secrets file=/etc/rsync.secrets" >> /etc/rsyncd.conf

# 创建认证文件
echo "rsync:rsync123" > /etc/rsync.secrets && chmod 600 /etc/rsync.secrets && ls -l /etc/rsync.secrets

# 创建虚拟管理用户
useradd rsync -s /sbin/nologin -M && id rsync

# 创建管理目录
mkdir -p /backup && chown -R rsync.rsync /backup

# 启动rsync进程
rsync --daemon --config=/etc/rsyncd.conf && netstat -lntup| grep 873

# 开机启动
echo '/usr/bin/rsync --daemon' >>/etc/rc.local
```
## 客户端配置
```bash
# 创建认证文件
echo "rsync123" > /etc/rsync.secrets && chmod 600 /etc/rsync.secrets && ls -l /etc/rsync.secrets
```



## 脚本
```bash
#!/bin/bash
src=/backup                             # 需要同步的源路径
des=backup                              # 目标服务器上 rsync --daemon 发布的名称
rsync_passwd_file=/etc/rsync.password   # rsync验证的密码文件
ip=192.168.100.100                      # 目标服务器
user=rsync                              # rsync --daemon定义的验证用户名
cd ${src}
/usr/bin/inotifywait -mrq --format  '%Xe====%w%f' -e modify,create,delete,attrib,close_write,move ./ | while read file
do
        INO_EVENT=$(echo $file | awk -F'====' '{print $1}')      # 事件类型
        INO_FILE=$(echo $file | awk -F'====' '{print $2}')       # 文件路径
        echo "-------------------------------$(date)------------------------------------"
        echo $file
        #增加、修改、写入完成、移动进事件
        if [[ $INO_EVENT =~ 'CREATE' ]] || [[ $INO_EVENT =~ 'MODIFY' ]] || [[ $INO_EVENT =~ 'CLOSE_WRITE' ]] || [[ $INO_EVENT =~ 'MOVED_TO' ]]
        then
                echo 'CREATE or MODIFY or CLOSE_WRITE or MOVED_TO'
                rsync -avzcR --password-file=${rsync_passwd_file} $(dirname ${INO_FILE}) ${user}@${ip}::${des}
        fi
        #删除、移动出事件
        if [[ $INO_EVENT =~ 'DELETE' ]] || [[ $INO_EVENT =~ 'MOVED_FROM' ]]
        then
                echo 'DELETE or MOVED_FROM'
                rsync -avzR --delete --password-file=${rsync_passwd_file} $(dirname ${INO_FILE}) ${user}@${ip}::${des}
                # 目录越浅,效率越低
        fi
        #修改属性事件 指 touch chgrp chmod chown等操作
        if [[ $INO_EVENT =~ 'ATTRIB' ]]
        then
                echo 'ATTRIB'
                if [ ! -d "$INO_FILE" ] # 只在更新目录中文件时更新目录,单独修改目录属性不更新
                then
                        rsync -avzcR --password-file=${rsync_passwd_file} $(dirname ${INO_FILE}) ${user}@${ip}::${des}
                fi
        fi
done
```