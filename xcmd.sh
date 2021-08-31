zzcmd(){
    start_time=`date +%s`
    c=0
    [[ $1 == "" || $2 == "" ]] && cmd_usage && return
    ips="`echo \"$1\"|grep -Po '((\d{1,3}.){3}\d{1,3})'`"
    [[ $ips == "" ]] && ips="$(eval echo \"\$$1\")"
    [[ $ips == "" ]] && ips="`cat $1`"
    set +m
    nanoseconds=`date +%N`
    for ip in $ips
    do
        [[ $ip == "" || $ip == " " || ! $ip =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]] && redEcho "$ip ip invalid..." && continue
        # $2 命令中带参数无法被传入
        { timeout 15 ssh root@$ip "echo -e \"\e[41;37;1m ------------------- ${ip} -------------------\e[0m\n\";$2;exit" > ${nanoseconds}_$ip & } 2>/dev/null
        ((c++))
    done
    wait
    # 生成文件可能会因为没有权限而失败,改用临时变量
    cat ${nanoseconds}_*
    rm -f ${nanoseconds}_*
    set -m
    end_time=`date +%s`
    cost_time=$(($end_time-$start_time))
    #cost_time_pretty=`date -d@$cost_time +%M"min"%S`
    greenEcho "=================== 本次执行 $c 台机器，耗时 ${cost_time}s ==================="
}
cmd_usage(){
    echo this is usage
}

redEcho(){
    echo $1
}

greenEcho(){
    echo $1
}

zzcmd $@