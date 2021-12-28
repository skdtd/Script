#!/bin/bash

# \e[1;33m$2\e[0m\e[1;31m$3\e[0m
# 0:正常
# 1:亮色
# 2:暗色
# 3:斜体
# 4:下划线  
# 56:暗色闪烁
# 7:底色镂空字
# 8:透明字
# 9:删除线

# 31:红
# 32:绿
# 33:淡黄
# 34:蓝
# 35:紫
# 36:天蓝
# 37:白
# 38:蓝
# 39:蓝
# 40:蓝

SET=(
    'ERROR,1,31'
    'WARN,1,35'
    'INFO,1,33'
    'DEBUG,1,36'
)

for i in $(seq ${#SET[@]})
do
    KEYS=$KEYS$(echo ${SET[$i]} | sed -r 's/^(.*),.*,.*/(\1)|/')
    COLORS=$COLORS$(echo ${SET[$i]} | sed -r "s/^.*,(.*),(.*)/\\\e[\1;\2m\$$i\\\e[0m/")
done
tail -fn10 $1 | perl -pe "s/(?i)$KEYS/$COLORS/g"