#!/bin/bash

##########################################
#
# 彩色字(颜色自行调试)
# colorEcho <pattern> [text]
# pattern   : 4位数字
#   第一位: 为"0"代表不换行, 等于"echo -n"
#   第二位: 文本效果, 0-9可选
#   第三位: 文字颜色, 0-9可选
#   第四位: 背景颜色, 0-9可选
#
##########################################
colorEcho(){
    KEYS=$1
    shift
    ECHOCMD="echo"
    [[ ${KEYS:0:1} == '0' ]] && ECHOCMD=$ECHOCMD" -n "
    read EFFECT FONTCOLOR BACKCOLOR <<< "${KEYS:1:1} ${KEYS:2:1} ${KEYS:3:1}"
    ${ECHOCMD} -e "\033[${EFFECT};4${BACKCOLOR};3${FONTCOLOR}m$@\033[0m"
}

##########################################
#
# 帮助
#
##########################################
usage(){
    cat <<< """Usage:
    $(basename $0) [options] [args...] +- commad
    For example: 
        $(basename $0) -t 192.168.0.1 -t 192.168.0.2 -u +- ls -alh
        $(basename $0) -t 192.168.0.1,192.168.0.2 -u +- ls -alh

    -t, --target       执行命令的目标主机

    -u, --username     在目标主机上执行命令的用户, 所有主机必须使用同一个用户

    -f, --file         当不用-t或者--target指定主机时, 用文件指定主机

    -i, --identity     免密连接时如果密钥不是默认的~/.ssh/id_rsa, 则需要手动指定

    -p, --password     非免密连接时使用密码登录, 需要安装sshpass模块, 不推荐使用

    --timeout          超过指定时间(单位: 秒)未完成连接并执行完命令则结束退出远程主机ssh, 默认: 15
    """
    colorEcho 1019 $@
    exit 1
}





##########################################
#
# 显示本次执行的基本信息
#
##########################################
infos(){
    colorEcho 1039 "=====INFOS=================================================="
    colorEcho 0039 "="
    [[ -z ${TARGET} ]] && echo ' HOSTSFILE:' ${FILE:-'null'} || echo ' HOSTS    :' ${TARGET[@]}
    colorEcho 0039 "="
    echo ' USERNAME :' ${USERNAME:-'null'}
    colorEcho 0039 "="
    [[ ! -z ${PASSWORD} ]] && echo ' IDENTITY :' ${IDENTITY:-'~/.ssh/id_rsa'} && colorEcho 0039 "="
    echo ' TIMEOUT  :' ${TIMEOUT:-15}
    colorEcho 0039 "="
    echo ' COMMAND  :' ${CMD}
    colorEcho 1039 "=====INFOS=================================================="
}




##########################################
#
# 获取执行命令
# 命令行参数"+-"之后的全部参数
# 对以下全局变量赋值:
# CMD           # 需要被执行的命令, 参数中通过"+-"来分割, 该符号之后的所有参数被视为整个命令
#
##########################################
getCmd(){
    # 根据"+-"切分参数, "+-"符号之后作为整个命令, 解决getopt解析所有参数的问题
    TEMP="$*"
    CMD=${TEMP#*+-}
    # 检查
    local MSG="Use \"+-\" to specify the command to execute."
    [[ -z $CMD ]] && usage ${MSG}
}


##########################################
#
# 读取参数并设置
# 需要的参数, 命令行参数"+-"之前的全部参数
# 对以下全局变量赋值:
# TARGET     -t, --target       # 执行命令的目标主机
# USERNAME   -u, --username     # 在目标主机上执行命令的用户, 所有主机必须使用同一个用户
# FILE       -f, --file         # 当不用"-t"或者"--target"指定主机时, 用文件指定主机
# IDENTITY   -i, --identity     # 免密连接时如果密钥不是默认的"~/.ssh/id_rsa", 则需要手动指定
# PASSWORD   -p, --password     # 非免密连接时使用密码登录, 需要安装"sshpass"模块, 不推荐使用
# TIMEOUT    --timeout          # 超过指定时间(单位: 秒)未完成连接并执行完命令则结束退出远程主机ssh, 默认: 15
#
##########################################
setOption(){
    # 收集所有-t和--target的参数合成数组
    collectHosts(){
        [[ "$2" =~ ^-.* ]] && usage "$1 missing parameter"
        local TEMP=(${2//,/ })
        local REG='^((2(5[0-5]|[0-4][0-9]))|[0-1]?[0-9]{1,2})(\.((2(5[0-5]|[0-4][0-9]))|[0-1]?[0-9]{1,2})){3}$'
        for ip in ${TEMP[@]}
        do  
            [[ ! ${ip} =~ ${REG} ]] && usage "ip $ip invalid..."
        done
        TARGET=(${TARGET[@]} ${TEMP[@]})
    }

    # 检查是否携带参数
    checkAndSet(){
        if [[ "$3" =~ ^-.* ]];then
            usage "$2 missing parameter"
        else
            eval "$1"=$3
        fi
    }


    # 参数收集
    local TEMP=$(getopt -o qt:u:p:f:i:  --long help,quiet,target:,username:,password:,file:,timeout: -n 'error' -- "$@")
    if [ $? != 0 ] ; then usage "Terminating..." >&2 ; fi
    
    # 参数重排
    eval set -- "$TEMP"

    # 参数定义
    while true ; do
        case "$1" in
            -t|--target)    collectHosts          $@ ; shift 2 ;;
            -u|--username)  checkAndSet USERNAME  $@ ; shift 2 ;;
            -p|--password)  checkAndSet PASSWORD  $@ ; shift 2 ;;
            -f|--file)      checkAndSet FILE      $@ ; shift 2 ;;
            -i|--identity)  checkAndSet IDENTITY  $@ ; shift 2 ;;
            --timeout)      checkAndSet TIMEOUT   $@ ; shift 2 ;;
            --) shift ; break ;;
            *) usage "Internal error!" ;;
        esac
    done

    # 最终检查
    local MSG='The target must be set in the form of hosts(-t) or file(-f)'
    [[ -z $TARGET && -z $FILE ]] && usage ${MSG}

    MSG='Targets cannot be set through both hosts(-t) or file(-f)'
    [[ ! -z $TARGET && ! -z $FILE ]] && usage ${MSG}

    MSG='You can only log in to the target host with a key(-i) or password(-p)'
    [[ ! -z $PASSWORD && ! -z $IDENTITY ]] && usage ${MSG}
    
    MSG='The "sshpass" module is required to log in with a password(-p), but "/usr/bin/sshpass" was not found'
    [[ ! -z $PASSWORD && ! -f '/usr/bin/sshpass' ]] && usage ${MSG}

    MSG='The module "/usr/bin/sshpass" was found but does not have execution permission'
    [[ ! -z $PASSWORD && ! -x '/usr/bin/sshpass' ]] && usage ${MSG}

}

##########################################
#
# 计时器
# timer 函数名 函数的参数
#
##########################################
timer(){
    start_time=$(date +%s)
    count=0
    set +m
    nano=$(date +%N)
    local FUNC=$1
    shift
    $FUNC $@
    cat ~/${nano}_*
    rm -f ~/${nano}_*
    set -m
    end_time=$(date +%s)
    cost_time=$(($end_time-$start_time))
    TEXT="Execution completed on ${count} nodes, cost: ${cost_time}s"
    colorEcho 1132 ${TEXT}
}

##########################################
#
# 执行命令
# 需要CMD参数, 该参数由getCmd()获得
#
##########################################
xcmd(){
    for ip in ${TARGET[@]}
    do
        { timeout ${TIMEOUT:=15} ssh -i {IDENTITY:='~/.ssh/id_rsa'} ${USERNAME}@${ip} "echo -e \"\033[43;31mNode: ${ip}\033[0m\";$@;exit" > ~/${nano}_$ip & } 2>/dev/null
        ((count++))
    done
    wait
}

##########################################
#
# 主逻顺序
#
##########################################
main(){
    [[ $# == 0 ]] && usage
    getCmd $@
    PARS="$*"
    PARS=${PARS%+-*}
    setOption ${PARS[@]}
    infos
    timer xcmd ${CMD}
}

main $@


# todo 文件读取 ymal读取 记录失败节点
