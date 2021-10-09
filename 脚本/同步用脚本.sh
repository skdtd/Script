#!/bin/bash


#####################################################################
# 参数
#####################################################################
LOCK=$(readlink -e $(basename $0))  # 二重启动锁


#####################################################################
# 防止二重启动
#####################################################################
run(){
    local TONKE=$1
    local CMD=$2
    shift 2
    [ "${FLOCKER}" != "${TONKE}" ] && exec env FLOCKER="${TONKE}" flock -en "${TONKE}" -c "${CMD}" "$@" || :
}


#####################################################################
# 执行rsync操作
#####################################################################
rsyncInvoke(){
    case $1 in
    "D")
        shift 1
        for HOST in ${HOSTLIST[@]}
        do
            rsync -qac --rsync-path="rm -rf $* && rsync" ${HOST}:
        done
    ;;
    "M")
        shift 1; DIR=$1;shift 1
        for HOST in ${HOSTLIST[@]}
        do
            rsync -qac --rsync-path="mkdir -p ${DIR} && rsync" "$@" ${HOST}:"${DIR}"
        done
    ;;
    esac
}

#####################################################################
# LOG预处理
#####################################################################
headleThead(){
    # while可以一次性全部读出,而不会分段读取
    while read -t 1 LINE
    do
        echo $LINE
    done <&1023 | awk '$3==""{next}
    sub($1$3" ","",dlist)
    sub($1$3" ","",mlist[$1])
    $2~/DELETE|MOVED_FROM/{dlist=$1$3" "dlist}
    $2~/CREATE|CLOSE_WRITE|MOVED_TO|ATTRIB/{mlist[$1]=$1$3" "mlist[$1]}
    END{
        if(dlist != ""){print "D",dlist};
        for(dir in mlist){if(mlist[dir] != ""){print "M",dir,mlist[dir]}};
    }' | xargs -P3 -L1 -I {} bash -c 'rsyncInvoke $@' _ {}  # 最高3线程并发
}



#####################################################################
# 监控变动
#####################################################################
monitorThead(){
    # 创建管道
    local UUID=$(cat /proc/sys/kernel/random/uuid)
    local PIPE=/tmp/.${UUID}
    mkfifo $PIPE
    exec 1023<>$PIPE              # 1023: 文件描述符(需统一)
    rm -rf $PIPE
    # 开始监控
    inotifywait -mrqe attrib,close_write,move,create,delete --format '%w %e %f' ${MONIT_DIR[@]} | \
    while read LINE
    do
        echo $LINE >&1023 
        run ${LOCK} headleThead & # 启动后台进程在延迟过后处理管道中的数据
    done
}


# 设置为全局函数(回调)
export -f rsyncInvoke headleThead



MONIT_DIR="/opt/"
export HOSTLIST="root@192.168.100.102 root@192.168.100.103"
export DELAYTIME=1                  # 延迟启动(秒): 超过这个时间没有新的数据改动就触发同步操作


monitorThead