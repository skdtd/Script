# 执行远程命令
```shell
#!/usr/bin/expect
set IP     [lindex $argv 0]
set USER   [lindex $argv 1]
set PASSWD [lindex $argv 2]
set CMD    [lindex $argv 3]
 
spawn ssh $USER@$IP $CMD
expect {
    "(yes/no)?" {
        send "yes\r"
        expect "password:"
        send "$PASSWD\r"
        }
    "password:" {send "$PASSWD\r"}
    "* to host" {exit 1}
    }
expect eof
```

# ssh 常用-o参数
```shell
#ConnectTimeout=3                   连接超时时间，3秒
#ConnectionAttempts=5               连接失败后重试次数，5次
#PasswordAuthentication=no          不使用密码认证,没有互信直接退出
#StrictHostKeyChecking=no           自动信任主机并添加到known_hosts文件
#UserKnownHostsFile=/dev/null       使用指定的known_hosts文件
```
