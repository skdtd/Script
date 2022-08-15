#!/bin/bash

usage(){
    cat <<< """Usage:
    hadoop集群起停
    $(basename $0) [start/stop]"""
}

[[ $# == 0 ]] && usage  && exit 0

# 检查是否root运行
[[ $(id -nu) == 'root' ]] && echo 'Do not run with root' && exit 1
# 检查是否设置HADOOP_HOME
[[ -z "${HADOOP_HOME}" ]] && echo 'Environment variable "HADOOP_HOME" was not initialized' && exit 1

# 检查第一个参数是否是起停指令
ACT="start stop"
[[ ! "${ACT[@]}" =~ "$1" || "$1" =~ ' ' ]] && echo 'The first parameter can only be start or stop' && exit 1
ACT="$1"

declare -A CONFS
# 从配置文件中获取各个节点地址
CONFS=(
    ["NAMENODE"]='fs.defaultFS'
    ["RESOURCEMANAGER"]='yarn.resourcemanager.hostname'
    ["SECONDARYNAMENODE"]='dfs.namenode.secondary.http-address'
    ["HISTORYSERVER"]='yarn.log.server.url'
)

for NODE in ${!CONFS[@]}
do
    # 从配置文件中取出各个主机地址
    TMP=$(awk -v ORS="" '{print $0}' $(find ${HADOOP_HOME}/etc/hadoop/* -type f) | \
    awk -v RS='<property>' '{print $0}' | \
    grep "${CONFS[$NODE]}" | \
    sed -r 's#.*<value>(.*)</value>.*#\1#g')
    TMP=${TMP%*:*}
    TMP=${TMP##*/}
    CONFS[$NODE]=$TMP
done

# 连接对应节点
connect(){
    local HOST="${CONFS[$1]}"
    shift
    ssh -o StrictHostKeyChecking=no \
        -o GSSAPIAuthentication=no \
        "$(id -nu)@${HOST}" "$@"
}

# 群起/群停
{ connect "NAMENODE" "${HADOOP_HOME}/sbin/${ACT}-dfs.sh" & }
{ connect "RESOURCEMANAGER" "${HADOOP_HOME}/sbin/${ACT}-yarn.sh" & }
{ connect "HISTORYSERVER" "${HADOOP_HOME}/bin/mapred --daemon ${ACT} historyserver" & }
wait