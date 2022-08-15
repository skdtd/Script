# expect
### 安装
```bash
yum install expect
```
### 脚本
```bash
# 声明
#!/usr/bin/expect

# 获取命令行参数
set 变量名1 [lindex $argv 0]        # 获取第一个命令行参数

# 发送CTRL+C
send "\003"

# 获取当前时间
set current_time [clock format [clock seconds] -format "%Y-%m-%d,%H:%M:%S"]

# 与shell的变量交互

###### 在expect中使用shell变量:
# 方法1: 先export,再在expect中使用
#!/bin/bash
export VAR="VALUE"
expect << EXPECT
set var $::env(VAR)
EXPECT
# 方法2: 子shell调用
#!/usr/bin/expect
set a [exec sh -c {echo $a}]

###### 在shell中使用expect变量:
set ::env(VAR) VALUE
```

# 参数
|参数 |说明|
|:-   |:-| 
|-c   |可执行命令的前置符, 其后的命令应该被引起来, 该选项可以使用多次, 每个-c可以跟多个以分号分隔的命令.</br>命令按照出现的顺序执行,例如: `expect -c "puts first\n; puts second" -c "puts three"`|
|-d   |输出一些诊断信息, 命令执行时的内部动作. 当你写的脚本和预期不符时, 可用此项来调试脚本|
|-D   |交互式的调试器, 类似gdb. 适合专业人士使用|
|-f   |指定Expect读取的文件, 如果文件是-, 则表示是从标准输入读取. </br>该选项会将文件一次性全部读入内存, 该选项是可选的|
|-b   |类似-f选项, 只是每次只读取一行|
|-i   |以交互的方式运行expect, 等效直接敲expect|
|--   |可以用来界定选项的结束, 此项可以用在当你想传递一个类似选项的参数时, 防止Expect误认为是选项|
|-N\-n|如果`$exp_library/expect.rc`和`~/.expect.rc`存在, Expect会分别自动读取, </br>若要阻止此过程则需要分别指定-N和-n. 此项一般用不上. |
|-v   |输出版本号并退出|

# 变量
|变量                               |说明|
|:----------------------------------|:-|
|`spawn_id`                         |表示了当前进程|
|`expect_out(buffer)`               |获取上一次send命令以后的远端输出结果, 在当前或者下一个`{}`中有效|
|`expect_out(<数字>,string)`        |数字可以`0-9`,储存每次被匹配到的字符串|
## 变量使用示例
```bash
#!/usr/bin/expect
set IP     [lindex $argv 0]
set USER   [lindex $argv 1]
set PASSWD [lindex $argv 2]
set CMD    [lindex $argv 3]
 
spawn ssh $USER@192.168.100.102
set MY_ID2 $spawn_id
expect {
    # 全局变量在{}内时使用形式,如需修改变量使用set $::<var> <value>
    -i $::MY_ID2
    "yes/no"    {send "yes\r"       ; exp_continue}
    "password:" {send "$PASSWD\r"}
}
expect -i $::MY_ID2 "#"
send -i $::MY_ID2 "touch 111\r"

spawn ssh $USER@192.168.100.103
set MY_ID3 $spawn_id
expect {
    -i $::MY_ID3
    "yes/no"    {send "yes\r"       ; exp_continue}
    "password:" {send "$PASSWD\r"}
}
expect -i $::MY_ID3 "#"
send -i $::MY_ID2 "touch 222\r"

send -i $::MY_ID3 "exit\r"
send -i $::MY_ID2 "exit\r"
expect eof
```

# 命令
## spawn
### 参数
|选项   |说明|
|:------|:-|
|-noecho|默认情况下, spawn会回显命令名和参数.此选项可以取消回显.|
|-ignore|指定在spawned process种要忽略的信号.|
### 格式
```bash
spawn [args] program [args]
# 示例
spawn -noecho ssh root@192.168.100.101 ls -l
```

## expect
等待, 直到模式patn匹配到spawn打开的进程的输出, 超过指定的时间, 或遇到EOF.
字串中可以使用`^`匹配起始串, 用`$`匹配结尾串.
### 参数
|选项        |说明|
|:-----------|:-|
|-gl         |保护以"-"开始的模式不被认为是选项|
|-re         |正则表达式, 在单项前面指定|
|-ex         |匹配确切的字串, 不对`*`,`^`和`$`等特殊字符进行翻译|
|-nocase     |不区分大小写|
|-timeout    |设置当前expect的超时时间, 而不是使用变量timeout的时间|
### 格式
```bash
expect [[-opts] pat1 body1] ... [-opts] patn [bodyn]
# 示例
expect -timeout 3 {                                     # 设置该匹配专用的超时时间
    timeout         {send_user "Connect timeout!\n"}    # 设置超时之后的处理
    "yes/no"        {send "yes\r"; exp_continue}
    "password:"     {send "$passwd\r"}
    default         {exit}                              # 当timeout和eof没有被设置时,碰上超时或者eof时执行
}
expect eof          {send_user "End of interaction\n"}  # 交互结束返回原用户
```

## exp_continue
允许expect继续执行自身而不是往下执行, 默认情况下, exp_continue会重置timeout, 如果不想重置timeout, 使用-continue_timer选项.
### 格式
```bash
exp_continue [-continue_timer]
```

## expect_user
类似expect, 不过是从标准输入读取字符, 行必须以回车结尾, 以使expect能识别它们.
### 格式
```bash
expect_user [expect_args]
# 示例
send_user "\ninput:\n"
expect_user -re "(.*)\n" {
    send "echo $expect_out(0,string)\r"
    send "exit\r"
}
```

## interact
将当前进程的控制权交付给用户.
### 参数
|选项        |说明|
|:-----------|:-|
|-ex         |防止以"-"开头的模式被翻译成选项|
|-re         |用正则匹配的模式翻译string, 此选项下匹配的子串被保存在变量interact_out中. 类似expect的expect_out.|
|-echo       |回显每一个字符, 即使这个字符会被匹配中|
### 格式
```bash
interact [string1 body1] ... [stringn [bodyn]]
# 示例
interact {
    "abc" {send_user "you typed abc\n"}
    "123" {send_user "you typed 123\n"}
}
```

## sleep
脚本进入睡眠模式, 睡眠时间单位为秒
### 格式
```bash
sleep seconds
```

## send
发送字符到当前进程, 字符会立即被发送, 尽管那些行缓冲的程序只会在有回车键时才读取, 回车键用'\r'表示.
### 参数
|选项        |说明|
|:----------|:-|
|--         |其后的参数被强制解释成字串, 而不是选项. |
|-i         |选项说明字串发送给spawn_id. |
|-s\-h      |慢的输入\类人的输入方式, 可以提供输入的间隔设置. 具体参见man手册|
### 格式
```bash
send [-flags] string
# 示例
send_user "\ninput:\n"
send "echo hello world\r"
```

## send_error
类似send, 不过输出发送到标准错误, 而不是当前进程
### 格式
```bash
send_error [-flags] string
```

## send_log
类似send, 不过string只发送到log文件. (see log_file)
### 格式
```bash
send_log [--] string
```

## send_tty
类似send, 不过输出发送到/dev/tty而不是当前进程. 
### 格式
```bash
send_tty [-flags] string
```

## send_user
类似send, 不过输出发送到标准输出, 而不是当前进程. 
### 格式
```bash
send_user [-flags] string
```

## puts
回显内容
### 格式
```bash
puts string
```

## close
关闭连接到当前进程的连接
### 参数
|选项        |说明|
|:-----------|:-|
|-i         |指定关闭名为spawn_id的进程|
|-onexec    |检测是否有新打开的进程或进程是否有重叠, 若有, 0:保持打开, 1:强制关闭|
|-slave     |关闭spawn_id关联的子进程|
### 格式
```bash
close [-slave] [-onexec 0|1] [-i spawn_id]
```
## exec
在expect中执行shell命令
### 格式
```bash
exec command args
# 示例
exec bash -c "touch 123"
```

## wait
回收子进程句柄,每次eof或者close时只是子线程结束,使用wait将句柄回收防止大量连接操作时内存溢出
### 参数
|选项        |说明|
|:-----------|:-|
|-nowait     |立即回收|


## exit
Expec退出




# 可用脚本
## 执行远程命令
```bash
########################################
# cmdName <地址> <用户名> <密码> <命令> #
########################################

#!/usr/bin/expect
set IP     [lindex $argv 0]
set USER   [lindex $argv 1]
set PASSWD [lindex $argv 2]
set CMD    [lindex $argv 3]
 
spawn ssh $USER@$IP $CMD
expect {
    "yes/no"    {send "yes\r"; exp_continue}
    "password:" {send "$PASSWD\r"}
    "* to host" {exit 1}
}
expect eof
```
## 自动登录
```bash
#################################
# cmdName <地址> <用户名> <密码> #
#################################

#!/usr/bin/expect -f
set IP     [lindex $argv 0]
set USER   [lindex $argv 1]
set PASSWD [lindex $argv 2]
set timeout 10
 
spawn ssh $username@$ip
expect {
    "yes/no"    {send "yes\r"; exp_continue}
    "password:" {send "$PASSWD\r"}
} 
interact
```