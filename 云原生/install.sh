#!/bin/bash


# 检查节点免密是否可用
# 从文件读取列表
while read line
do
    line=($(echo $line | grep -v "^#"))
    if [[ -z ${line} ]];then 
        continue 
    fi
    read host status user passwd <<< ${line[@]}
    echo $host
    echo $status
    echo $user
    echo $passwd
done < $1






# 获取版本号用的URL
DOCKER_VERSION_URL='https://download.docker.com/linux/static/stable/x86_64/'
KUBERNETES_VERSION_URL='https://dl.k8s.io/release/stable.txt'

# 检查是否已经有现成压缩包
# docker压缩包
DOCKER_ARCHIVE=
# k8s压缩包
K8S_ARCHIVE=


