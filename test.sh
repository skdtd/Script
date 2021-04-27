#/bin/bash

############################## 初始化变量值 ##############################
# 临时目录
temp_dir="/tmp"
# 时间戳
timestamp="$(date +%Y%m%d%S)"
# 临时文件
temp_file_list="$(mktemp ${temp_dir}/$0.temp_file_list.XXXXXXXXX)"


############################### 初始化方法 ###############################
# 彩色字
# 字体颜色 重置=0, 黑色=30, 红色=31, 绿色=32, 黄色=33, 蓝色=34, 洋红=35, 青色=36, 白色=37
# 背景颜色 重置=0, 黑色=40, 红色=41, 绿色=42, 黄色=43, 蓝色=44, 洋红=45, 青色=46, 白色=47
#
# 红色字: font 31 test
# 结果暂存的变量: 无
function font(){
    echo -e "\e[1;$1m$2\e[0m"
}

# 从yum读取版本列表,再返回选择的版本对应的安装包
# 获取docker-ce版本: get_version docker-ce
# 结果暂存的变量: result
function get_version(){
    # 置换'-'为'_'
    var=${1//-/_}
    # 生成临时文件
    tmp_file="$(mktemp $0.$1.XXXXXXXXX)"
    # 获取版本列表写入临时文件
    yum list "$1" --showduplicates | sort | grep "$1" > ${tmp_file}
    # 显示版本列表
    while read line
    do
        echo "${line}"
        newest="${line}"
    done < ${tmp_file}
    # 记录最近版本号
    newest=$(echo "${newest}" | awk '{print $2}')
    # 读取用户输入版本号
    read -p "请选择需要安装$(font 36 ${var})版本(默认: ${newest}):" ${var}_ver
    eval decision=\${${var}_ver}
    awk '{print $2}' ${tmp_file} | grep "${decision}"
    if [[ $? -ne 0 ]];then
        echo "不存在的版本号: $(font 41 ${decision}), 将使用最新版: $(font 36 ${newest})"
        unset decision
    fi
    if [[ $(grep "${decision}" ${tmp_file} | wc -l > /dev/null) -ne 1 ]];then
        echo "匹配的版本号出现多个: $(font 41 ${decision}), 将使用最新版: $(font 36 ${newest})"
        unset decision
    fi
    result=$(echo $1-"${decision:="${newest}"}" | sed s'/.://')
}




######################## 获取需要安装的docker-ce版本 ########################
yum list docker-ce --showduplicates | sort | grep docker > ${docker_ce_versions}
while read line
do
    echo "${line}"
    newest="${line}"
done < ${docker_ce_versions}
newest=$(echo "${newest}" | awk '{print $2}')
read -p "请选择需要安装$(redf 36 docker-ce)版本(默认: ${newest}):" docker_ce_ver
echo "${docker_ce_ver:=${newest}}"

######################### 输出所有docker-ce-cli版本 #########################
yum list docker-ce-cli --showduplicates | sort | grep docker > ${docker_ce_cli_versions}
while read line
do
    echo "${line}"
    newest="${line}"
done < ${docker_ce_cli_versions}
newest=$(echo "${newest}" | awk '{print $2}')
read -p "请选择需要安装$(redf 36 docker-ce-cli)版本(默认: ${newest}):" docker_ce_cli_ver
echo "${docker_ce_cli_ver:=${newest}}"

############################## 清理临时文件 ##############################
while read line
do
    rm -rf "${line}" > /dev/null
done < ${temp_file_list}
rm -rf ${temp_file_list}
