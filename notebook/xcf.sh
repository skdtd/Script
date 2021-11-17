#!/bin/bash

# 设置参数默认值
USER="${USER:=$(id -nu)}"
PORT='22'
IDENTITY="~/.ssh/id_rsa"
TIMEOUT='60'
IRS='{&n}'

# 参数收集
TEMP=$(getopt -o h:u:p:i:t: --long host:,user:,port:,identity:,timeout: -n 'error' -- "$@")
[[ $? != 0 ]] && echo "Terminating..." && exit 1
# 参数重排
eval set -- "$TEMP"
# 参数定义
while :
do
    case "$1" in
        -h|--host)      HOSTLIST="$2 ${HOSTLIST[@]}"    ; shift 2 ;;
        -u|--user)      USER=$2                         ; shift 2 ;;
        -p|--port)      PORT=$2                         ; shift 2 ;;
        -i|--identity)  IDENTITY=$2                     ; shift 2 ;;
        -t|--timeout)   TIMEOUT=$2                      ; shift 2 ;;
        --)             shift                           ; break   ;;
        *) echo "Internal error!"                       ; exit  1 ;;
    esac
done

################################################
#
# 帮助
#
################################################
function usage(){
    cat <<< """Usage:
    $(basename $0) [命令]
    $(basename $0) [文件]
    """
}

################################################
#
# 执行命令
#
################################################
function xmd(){
    for HOST in ${HOSTLIST[@]}
    do
        CWD=$(pwd)
        { timeout "${TIMEOUT}" ssh \
            -p "${PORT}" \
            -i "${IDENTITY}" \
            "${USER}@${HOST}" \
            "echo -e \"\033[43;31mNode: ${HOST}\033[0m\";cd ${CWD} && $@;exit" | \
            awk -v ORS="${IRS}" '{print $0}' >&1023;echo >&1023 & } 2>/dev/null
    done
    wait
    while :
    do
        read -t 0.1 -u1023 LINE
        [[ "${LINE}" == "" ]] && break
        awk -v RS="${IRS}" '{print $0}' <<< "${LINE/%${IRS}/}"
    done
}

################################################
#
# 分发文件
#
################################################
function xyc(){
    which rsync >& /dev/null
    if [[ $? != 0 ]];then
        which scp >& /dev/null
        if [[ $? != 0 ]];then
            echo "error: can not send"
            exit 1
        fi
        echo "warming: use scp"
        _scp $@
    else
        _rsync $@
    fi
}

function _rsync(){
    for HOST in ${HOSTLIST[@]}
    do
        echo -e "\033[43;31mNode: ${HOST}\033[0m"
        local F=$(readlink -m $1)
        rsync -arczP \
        -e "ssh -p ${PORT} -i ${IDENTITY}" \
        --rsync-path="mkdir -p $(dirname ${F}) && rsync" \
        "${F}" "${USER}@${HOST}:$(dirname ${F})"
    done
}

function _scp(){
    for HOST in ${HOSTLIST[@]}
    do
        echo -e "\033[43;31mNode: ${HOST}\033[0m"
        scp -r -p "${PORT}" -i "${IDENTITY}" "${FILE}" "${USER}@{HOST}:${FILE}"
    done
}

[[ $# == 0 ]] && usage && exit 0
[[ -z "${HOSTLIST}" ]] && echo "plese set hostlist" && exit 1
# 开启管道
UUID=$(cat /proc/sys/kernel/random/uuid).fifo
mkfifo /tmp/.${UUID}
exec 1023<>/tmp/.${UUID}
rm -rf /tmp/.${UUID}
if [[ -f $1 || -d $1 ]];then
    xyc $@
else
    xmd $@
fi

# hostlist 所有节点需要配置免密