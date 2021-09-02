# 参数传递
1.  $#   传递到脚本的参数个数
2.  $$   脚本运行的当前进程ID号
3.  $!   后台运行的最后一个进程的ID号
4.  $-   显示Shell使用的当前选项, 与set命令功能相同.
5.  $?   显示最后命令的退出状态.0表示没有错误, 其他任何值表明有错误.
6.  $*   以一个单字符串显示所有向脚本传递的参数.如"$*"用「"」括起来的情况、以"$1 $2 … $n"的形式输出所有参数.
7.  $@   与$*相同, 但是使用时加引号, 并在引号中返回每个参数.如"$@"用「"」括起来的情况、以"$1" "$2" … "$n" 的形式输出所有参数.
8.  $*和$@
```
相同点：
都是引用所有参数.

不同点：
只有在双引号中体现出来.假设在脚本运行时写了三个参数 1、2、3, 则 " * " 等价于 "1 2 3"(传递了一个参数), 而 "@" 等价于 "1" "2" "3"(传递了三个参数).
```
# 文件测试(前面加!表示非)
1.   -b file  检测文件是否是块设备文件
2.   -c file  检测文件是否是字符设备文件
3.   -d file  检测文件是否是目录
4.   -f file  检测文件是否是普通文件(既不是目录, 也不是设备文件)
5.   -g file  检测文件是否设置了SGID位 
6.   -k file  检测文件是否设置了粘着位(Sticky Bit)
7.   -p file  检测文件是否是有名管道
8.   -u file  检测文件是否设置了 SUID 位
9.   -r file  检测文件是否可读
10.  -w file  检测文件是否可写
11.  -x file  检测文件是否可执行
12.  -s file  检测文件是否为空(文件大小是否大于0)
13.  -e file  检测文件(包括目录)是否存在
14.  -S file  判断某文件是否 socket
15.  -L file  检测文件是否存在并且是一个符号链接
16.  -z var   检测变量是否为空
17.  -n var   检测变量是否非空


# 命令
1.  echo 输出一行信息, 如需用\n换行需要加-e参数
2.  read 从标准输入读取一行

```
-p 输入提示文字
-n 输入字符长度限制
-t 输入限时
-s 隐藏输入内容
```
3.   重定向
```
> 重定向输出到某个位置,替换原有文件的所有内容
>> 重定向追加到某个位置,在原有文件的末尾添加内容
< 重定向输入某个位置文件
2> 重定向错误输出
2>> 重定向错误追加输出到文件末尾
&> 混合输出错误的和正确的都输出
```

| 左对齐 | 右对齐 | 居中对齐|
| :-----| ----: | :----: |
| 单元格 | 单元格 | 单元格 |
| 单元格 | 单元格 | 单元格 |


# 字符串切片
## 返回字符串长度
${#var} : 返回字符串变量var的长度
${var:offset}：返回字符串变量var中从第offset个字符后（不包括第offset个字符）的字符开始，到最后的部分，offset的取值在0到${#var}-1之间（bash4.2后，允许为负值）
${var:offset:number}:返回字符串变量var中从第offset个字符后（不包括第offset个字符）的字符开始，长度为number的部分
${var: -length}:取字符串的最右侧几个字符    注意：冒号后必须有一个空白字符
${var:offset:-length}: 从最左侧跳过offset字符，一直向右取到距离最右侧length个字符之前的内容
${var: -length:-offset}:先从最右侧向左取到length个字符开始，在向右取到距离最右侧offset个字符之间的内容  注意：冒号后必须有一个空白字符

${var#*word}:其中word可以是指定的任意字符     自左向右，查找var变量所存储的字符串中，第一次出现的word,删除字符串开头至第一次出现word字符之间的所有字符
${var##*word}:同上，贪婪模式，不同的是，删除的是字符串开头至最后一次由work指定的字符之间的所有内容
${var%word*}:其中word可以是指定的任意字符     自右而左，查找var变量所存储的字符串中，第一次出现的word，删除字符串最后一个字符向左至第一次出现word字符之间的所有字符
${var%%word*}:同上，只不过删除字符串最右侧的字符向左直至最后一次出现word字符之间的所有字符

${var/pattern/substr}: 查找var所表示的字符串中，第一次被pattern所匹配到的字符串，以substr替换之
${var//pattern/substr}:查找var所表示的字符串中，所有能被pattern所匹配到的字符串，以substr替换之
${var/#pattern/substr}:查找var所表示的字符串中，行首被pattern所匹配到的字符串，以substr替换之
${var/%pattern/substr}:查找var所表示的字符串中，行尾被pattern所匹配到的字符串，以substr替换之

${var/pattern}: 删除var所表示的字符串中第一次被pattern所匹配到的字符串
${var//pattern}:删除var所表示的字符串中所有被pattern所匹配到的字符串
${var/#pattern}:删除var所表示的字符串中所有以pattern为行首所匹配到的字符串
${var/%pattern}:删除var所表示的字符串中有所以pattern为行尾所匹配到的字符串

${var^^}:把var中的所有小写字母转换为大写
${var,,}:把var中的所有大写字母转换为小写

${var:-word}    如果var为空或者未设定，返回word，var不变
${var:=word}    如果var为空或者未设定，返回word，且var=word
${var:+word}    如果var有值，返回word，var不变
${var:?word}    如果变量var为空或者未设定，返回word并退出shell，word没有值则输出：parameter null or not set，用于检测var是否被正常赋值
${var-word}     如果var未设定，返回word，如果var未空或者有值，返回var


# shell变量一般是无类型的，但是bash shell提供了declare和typeset(将要淘汰)两个命令用于指定变量的类型，两个命令是等价的(bash不支持浮点数就是小数点)

vi +':w ++ff=dos' +':q' filename


大于 -gt (greater than)
小于 -lt (less than)
大于或等于 -ge (greater than or equal)
小于或等于 -le (less than or equal)
不相等 -ne （not equal）


# expect用法
expect << EOF
set timeout 30
spawn ssh root@192.168.1.1
expect {
    "yes/no" { send "yes\n" }
}
expect {
    "password:" { send "root\n" }
}
expect "*]#"
send "df -Th\n"
expect "*]#"
send "exit\n"
expect eof
EOF




# grep
grep -w  # 精确匹配
grep -c  # 统计行数
grep -v  # 排除行
grep [a]bc  # 只统计abc的行,不统计grep本身的进程