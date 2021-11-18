#!/bin/bash

usage(){
    cat <<< """Usage:
    hadoop集群起停
    $(basename $0) [start/stop] [all]
    $(basename $0) [start/stop] [nn/dn/sn/rm/nm/hs] [host]
    
    all  all
    nn   namenode
    dn   datanode
    sn   secondarynamenode
    rm   resourcemanager
    nm   nodemanager
    hs   historyserver"""
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

# 检查第二个参数是否为节点名字
declare -A NODES CONFS
NODES=(
    ["all"]="all"
    ["nn"]="namenode"
    ["dn"]="datanode"
    ["sn"]="secondarynamenode"
    ["rm"]="resourcemanager"
    ["nm"]="nodemanager"
    ["hs"]="historyserver"
)

[[ ! ${!NODES[@]} =~ "$2" ]] && echo -e \
'''Please select from the following options:
nn: namenode
dn: datanode
sn: secondarynamenode
rm: resourcemanager
nm: nodemanager
hs: historyserver
''' && exit 1

# 从配置文件中获取各个节点地址
CONFS=(
    ["NAMENODE"]='fs.defaultFS'
    ["RESOURCEMANAGER"]='yarn.resourcemanager.hostname'
    ["SECONDARYNAMENODE"]='dfs.namenode.secondary.http-address'
    ["HISTORYSERVER"]='yarn.log.server.url'
)

for NODE in ${!CONFS[@]}
do
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
    if [[ "${!CONFS[@]}" =~ "$1" ]];then
        local HOST="${CONFS[$1]}"
    else
        local HOST="$1"
    fi
    shift
    ssh -o StrictHostKeyChecking=no \
        -o GSSAPIAuthentication=no \
        "$(id -nu)@${HOST}" "$@"
}

if [[ "$2" == 'all' && "$3" == '' ]];then
    # 群起/群停
    { connect "NAMENODE" "${HADOOP_HOME}/sbin/${ACT}-dfs.sh" & }
    { connect "RESOURCEMANAGER" "${HADOOP_HOME}/sbin/${ACT}-yarn.sh" & }
    { connect "HISTORYSERVER" "${HADOOP_HOME}/bin/mapred --daemon ${ACT} ${NODES["hs"]}" & }
    wait
elif [[ "$3" != '' ]];then
    # 单节点起停
    connect $3 "${HADOOP_HOME}/bin/mapred --daemon ${ACT} ${NODES[$2]}"
else
    usage && exit 1
fi
