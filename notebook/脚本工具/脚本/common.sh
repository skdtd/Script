#!/bin/bash
################################################
#
# 通过yum仅下载rpm包用于分发, 通过yum install安装
# example:
#   yumd vim  =>  yum install --downloadonly --downloaddir=~/package/pkg
#                 生成vim.log记录所有下载的包
#
################################################
function yumd(){
    DOWNLOADPATH="${HOME}/package/pkg/"
    [[ -d ${DOWNLOADPATH} ]] || mkdir -p ${DOWNLOADPATH}
    for pkg in $@
    do
        LOGPATH="${HOME}/package/${pkg}.log"
        yum install --downloadonly --downloaddir=${DOWNLOADPATH} ${pkg} | tee ${LOGPATH}
        if [[ $(grep -E "(No package)|(Nothing to do)" ${LOGPATH}) ]];then
            rm -f ${LOGPATH}
        else
            TEXT=$(awk '{if($0~"^=+$"){flg=1}if($0~"^Total.*size"){flg=0;print $0}if(flg==1){print $0}}' ${LOGPATH})
            echo "${TEXT}" > ${LOGPATH}
        fi
    done
}

################################################
#
# 从选项中获取参数
#
################################################
function getParameter(){
    # 参数收集
    local TEMP=$(getopt -o rd:k:v:f:  --long reverse,delimiter,key:,value:,file: -n 'error' -- "$@")
    if [ $? != 0 ] ; then usage "Terminating..." >&2 ; fi
    # 参数重排
    eval set -- "$TEMP"
    # 参数定义
    while true ; do
        case "$1" in
            -r|--reverse)   local REVERSE=on     ; shift 2 ;;
            -d|--delimiter) local DELIMITER=$2   ; shift 2 ;;
            -k|--key)       local KEY=$2         ; shift 2 ;;
            -v|--value)     local VALUE=$2       ; shift 2 ;;
            -f|--file)      local FILE=$2        ; shift 2 ;;
            --) shift ; break ;;
            *) usage "Internal error!" ;;
        esac
    done
}


################################################
#
# 检查当前进程是否双重启动, 如果进程已经在运行则退出当前进程
#
################################################
function doubleCheck(){
    local checkitem="$0"
    local let procCnt=$(ps -A --format='%p%P%C%x%a' --width 2048 -w --sort pid \
                | grep "$checkitem" \
                | grep -v grep \
                | grep -v " -c sh " \
                | grep -v "$$" \
                | grep -c sh \
                | awk '{printf("%d",$1)}'
    )
    if [[ ${procCnt} -gt 0 ]];then
        echo -e "\033[;32m$(basename $0)\033[0m" "is running, this operation will be suspended"
        exit 1;
    fi
}

################################################
#
# 彩色字(颜色自行调试)
# cecho <pattern> [text]
# example:
#   cecho 0019 $@  =>  echo -e -n "\033[0;41;39m$@\033[0m"
# pattern   : 4位数字
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
    ${ECHOCMD} -e "\033[${EFFECT};4${BACKCOLOR};3${FONTCOLOR}m$@\033[0m"
}

################################################
#
# 计时器
# timer 函数名 函数的参数
# 毫秒: ${COST::-6}ms
# 微秒: ${COST::-3}μs
# 纳秒: ${COST::-0}ns 
#
################################################
function timer(){
    local BEGIN=$(date +%s%N)
    local FUNC=$1
    shift; ${FUNC} $@
    local END=$(date +%s%N)
    local COST=$(($END-$BEGIN))
    echo "Cost: ${COST::-3}ms"
}

################################################
#
# kl: 显示当前终端启动的所有进程
# kk: 杀死当前终端所有启动的进程
#
################################################
function kl(){
    ps -f | grep -vE '\-bash|ps \-f'
}
function kk(){
    ps -f | grep -vE '\-bash|ps \-f' | awk 'NR>1{system("kill -9 "$2)}'
}

################################################
#
# 进度条
# progress <step> <text>
#
################################################
function progress(){
    TOTAL=50
    SPEED=$(( $1 * ${TOTAL} / 100 ))
    TEXT=$2
    [[ ${SPEED} -ge ${TOTAL} ]] && SPEED=${TOTAL} && TEXT='Completion!\n'
    L=$(perl -E "say'=' x ${SPEED}")
    R=$(perl -E "say' ' x $((${TOTAL} - ${SPEED}))")
    echo -ne "\r[${L}${R}]${TEXT}"
}

################################################
#
# 发送文件
#
################################################
function xyc()
{
    if [[ ! -f ~/hostlist ]]; then
        echo 'no host list';
        return 1;
    fi;
    file=$(readlink -m $1);
    while read host; do
        echo $host;
        rsync -avrzhP $file $host:$file;
    done < ~/hostlist
}

################################################
#
# 染色追踪文件
#
# \e[\参数一;\2m\$参数二\e[0m
# 参数一
# 0:正常
# 1:亮色
# 2:暗色
# 3:斜体
# 4:下划线  
# 56:暗色闪烁
# 7:底色镂空字
# 8:透明字
# 9:删除线

# 参数二
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
# 
################################################
function ctail(){
    SET=(
        'ERROR,1,31'
        'WARN,1,35'
        'INFO,1,33'
        'DEBUG,1,36'
    )

    for (( i=0; i<${#SET[@]}; i++ ))
    do
        KEYS=$KEYS$(echo ${SET[$i]} | sed -r 's/^(.*),.*,.*/(\1)|/')
        let j=i+1
        COLORS=$COLORS$(echo ${SET[$i]} | sed -r "s/^.*,(.*),(.*)/\\\e[\1;\2m\$$j\\\e[0m/")
    done

    tail -fn10 $1 | perl -pe "s/(?i)$KEYS/$COLORS/g"
}