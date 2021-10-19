#!/bin/bash
# rsync Github: https://github.com/inotify-tools/inotify-tools/releases/latest
# rsyncd.conf: https://download.samba.org/pub/rsync/rsyncd.conf.5
# inotify-tools: https://github.com/inotify-tools/inotify-tools/wiki
#####################################################################
# 帮助
#####################################################################
usage(){
    cat <<< """Usage:
        基于rsync将指定目录的变更(增删改)自动同步到其他已经设置免密的节点相同目录

        $(basename $0) <host>
        $(basename $0) <dir> <host>

        同时监控多个目录或同步到多个节点时使用以下方式
        $(basename $0) -t <host1> -t <host2> -m <dir1> -m <dir2>
        $(basename $0) -t '<host1> <host2>' -m '<dir1> <dir2>'

        For example: 
            $(basename $0) /opt root@192.168.100.101
            $(basename $0) -t root@192.168.100.101 -t root@192.168.100.102 -m /opt -m /etc

        -q, --quiet             不显示变更记录
        -d, --delaytime         启动延迟(秒;默认:1秒)(超过指定时间未发生更改,则启动同步线程)
        -t, --target            同步的对象主机([USER]@HOST)
        -m, --monit-dir         监控的本地文件夹(默认:.)
        -i, --identity-file     连接的密钥文件
        -h, --help              帮助信息
        """
}

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
        for HOST in ${HOST_LIST[@]}
        do
            rsync -qac -e "ssh ${RSH}" --rsync-path="rm -rf $* && rsync" ${HOST}:
        done
    ;;
    "M")
        shift 1; DIR=$1;shift 1
        for HOST in ${HOST_LIST[@]}
        do
            rsync -qac -e "ssh ${RSH}" --rsync-path="mkdir -p ${DIR} && rsync" "$@" ${HOST}:"${DIR}"
        done
    ;;
    esac
}

#####################################################################
# LOG预处理
#####################################################################
headleThead(){
    # while可以一次性全部读出,而不会分段读取
    while read -t ${DELAYTIME} LINE
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
    exec 1023<>$PIPE
    rm -rf $PIPE
    # 开始监控
    inotifywait -mrqe attrib,close_write,move,create,delete --format '%w %e %f' ${MONIT_DIR[@]} | \
    while read LINE
    do
        [[ -z ${QUIET} ]] && echo "$(date +%Y-%m-%d\ %T) $LINE"
        echo $LINE >&1023 
        run ${LOCK} headleThead &
    done
}


##############################################################################################################
# 主流程
##############################################################################################################

# 设置为全局函数(回调)
export -f rsyncInvoke headleThead

# 参数收集
TEMP=$(getopt -o qd:t:d:i:h  --long quiet,delaytime:,target:,monit-dir:,identity-file:help -n 'error' -- "$@")
if [ $? != 0 ] ; then echo "Terminating..." >&2 ; fi
# 参数重排
eval set -- "$TEMP"
# 参数定义
while true ; do
    case "$1" in
        -q|--quiet)         QUIET=1                     ; shift 1 ;;
        -d|--delaytime)     DELAYTIME=$2                ; shift 2 ;;
        -t|--target)        HOST_LIST="${HOST_LIST} $2" ; shift 2 ;;
        -m|--monit-dir)     MONIT_DIR="${MONIT_DIR} $2" ; shift 2 ;;
        -i|--identity-file) RSH=" -i $2"                ; shift 2 ;;
        -h|--help)          usage                       ; exit  0 ;;
        --) shift ; break ;;
        *) usage; echo "Internal error!"; exit 1 ;;
    esac
done

# 未用'-'指定参数时
# 参数个数大于1, 第一个参数作为MONIT_DIR, 第二个参数作为HOST_LIST, 第三个参数起全部丢弃
[[ $# > 1 ]] && MONIT_DIR=${MONIT_DIR:=$1} && HOST_LIST=${HOST_LIST:=$2}
# 参数个数等于1, 当前执行目录作为MONIT_DIR, 参数作为HOST_LIST
[[ $# == 1 ]] && MONIT_DIR=${MONIT_DIR:=$(pwd)} && HOST_LIST=${HOST_LIST:=$1}

# HOST_LIST未被设定时退出
[[ -z ${HOST_LIST} ]] && echo "$(basename $0) error: No host specified to transfer" && exit 1

LOCK=$(readlink -e $(basename $0))  # 二重启动锁

export HOST_LIST
export DELAYTIME=${DELAYTIME:=1} RSH # 延迟启动(秒): 超过这个时间没有新的数据改动就触发同步操作

# 全量更新
for HOST in ${HOST_LIST[@]}
do
    for DIR in ${MONIT_DIR[@]}
    do
        rsync -qac -e "ssh ${RSH}" ${DIR} ${HOST}:${DIR}
        rsync -qac -e "ssh ${RSH}" --delete ${DIR} ${HOST}:${DIR}
    done
done

monitorThead