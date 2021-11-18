#!/bin/bash

# 提升ssh连接速度
# sed -ie 's/^#UseDNS.*/UseDNS no/;s/.*GSSAPIA.*/GSSAPIAuthentication no/g' /etc/ssh/sshd_config && systemctl restart sshd
# 设置免密
# for host in $XCFHOSTLIST;do ssh-copy-id -o StrictHostKeyChecking=no $(id -nu)@${host};done

# 设置参数默认值
USER="${USER:=$(id -nu)}"               # 执行用户, 默认当前操作用户
PORT='22'                               # ssh默认端口
IDENTITY="~/.ssh/id_rsa"                # ssh默认密钥
TIMEOUT='60'                            # ssh默认超时时间
IRS='{&n}'                              # 换行符替代符号
TAGSTYLE='1136'                         # 标签字样式
ERRSTYLE='1119'                         # 错误字样式
TIPSTYLE='1183'                         # 提示字样式

# 参数收集
TEMP=$(getopt -o h:u:p:i:t: --long host:,user:,port:,identity:,timeout: -n '无效参数' -- "$@")
[[ $? != 0 ]] && exit 1
# 参数重排
eval set -- "$TEMP"
# 参数定义
while :
do
    case "$1" in
        -h|--host)      XCFHOSTLIST=$2                  ; shift 2 ;;
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
    第一个参数被识别为文件或者文件夹时,将文件/文件夹传输到所有节点相同位置:
    (只会使用rsync和scp两个模块进行传输,优先使用rsync)
        $(basename $0) [文件]
    此外所有情况将后续参数识别为命令,将在所有节点当前目录上执行命令,并回显消息
    (错误消息不会显示)
        $(basename $0) [命令]
        如: 在主节点的/opt目录中执行$(basename $0) ls
            将会在所有节点的/opt目录中执行ls命令
    当发送的命令带有以'-'开头的参数时使用'--',如:
        $(basename $0) -- ls -l
        
    -h  --host          指定节点列表(优先于环境变量)
                            $(basename $0) -h 'host1 host2 host3 ...' [文件/命令]
                        或者将节点列表设置为环境变量XCFHOSTLIST
                            XCFHOSTLIST='host1 host2 host3 ...'
    -u  --user          指定执行用户,默认为当前操作用户
    -p  --port          指定ssh使用的端口,默认22
    -i  --identity      指定ssh使用的密钥文件,默认'~/.ssh/id_rsa'
    -t  --timeout       指定命令执行超时时间(单位:秒),默认60秒
    """
}

################################################
#
# 生成彩色字符串,用"echo -e"执行(只生成字串,方便发送到节点执行)
#   第一位: 为"0"代表不换行, 等于"echo -n", 
#   第二位: 文本效果, 0-9可选
#   第三位: 文字颜色, 0-9可选
#   第四位: 背景颜色, 0-9可选
#
################################################
function cecho(){
    KEYS=$1
    shift
    ECHOCMD="echo"
    [[ ${KEYS:0:1} == '0' ]] && ECHOCMD=$ECHOCMD" -n "
    read EFFECT FONTCOLOR BACKCOLOR <<< "${KEYS:1:1} ${KEYS:2:1} ${KEYS:3:1}"
    echo "\033[${EFFECT};4${BACKCOLOR};3${FONTCOLOR}m$@\033[0m"
}

################################################
#
# 执行命令
#
################################################
function xmd(){
    # 开启管道
    UUID=$(cat /proc/sys/kernel/random/uuid).fifo
    mkfifo /tmp/.${UUID}
    exec 1023<>/tmp/.${UUID}
    rm -rf /tmp/.${UUID}
    for HOST in ${XCFHOSTLIST[@]}
    do
        CWD=$(pwd)
        { timeout "${TIMEOUT}" ssh \
            -o StrictHostKeyChecking=no \
            -o GSSAPIAuthentication=no \
            -p"${PORT}" -i"${IDENTITY}" \
            "${USER}@${HOST}" \
            "echo -e \"$(cecho ${TAGSTYLE} Node: ${HOST})\";cd ${CWD} && $@;exit" | \
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
            echo -e $(cecho ${ERRSTYLE} "找不到rsync和scp模块,传输中止")
            exit 1
        fi
        echo -e $(cecho ${TIPSTYLE} "提示: 当前使用正在scp模块传输")
        _scp $@
    else
        _rsync $@
    fi
}

function _rsync(){
    for HOST in ${XCFHOSTLIST[@]}
    do
        echo -e $(cecho ${TAGSTYLE} "Node: ${HOST}")
        local FILE=$(readlink -m $1)
        local DIR=$(dirname ${FILE})
        rsync -arzcP \
        -e "ssh -o GSSAPIAuthentication=no -o StrictHostKeyChecking=no -p ${PORT} -i ${IDENTITY}" \
        --rsync-path="mkdir -p ${DIR} && rsync" \
        "${FILE}" "${USER}@${HOST}:${DIR}"
    done
}

function _scp(){
    for HOST in ${XCFHOSTLIST[@]}
    do
        echo -e $(cecho ${TAGSTYLE} "Node: ${HOST}")
        local FILE=$(readlink -m $1)
        local DIR=$(dirname ${FILE})
        scp -o StrictHostKeyChecking=no \
            -o GSSAPIAuthentication=no \
            -r -p"${PORT}" -i"${IDENTITY}" "${FILE}" \
            "${USER}@${HOST}:${DIR}"
    done
}

[[ $# == 0 ]] && usage && exit 0
[[ -z "${XCFHOSTLIST}" ]] && \
    echo -e $(cecho ${ERRSTYLE} "找不到执行节点,请以数组的形式在'-h'参数中指定,或者设置为变量'XCFHOSTLIST'") && \
    exit 1
if [[ -f $1 || -d $1 ]];then
    xyc $@
else
    xmd $@
fi
