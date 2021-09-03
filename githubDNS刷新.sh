#!/bin/bash -e

# 作成临时文件
read IP SITE <<< "$(mktemp) $(mktemp)"
tee ${SITE} << EOF &> /dev/null
github.com
github.global.ssl.fastly.net
EOF
echo 临时文件作成完毕
# 从站长之家查IP
echo $(curl -sSL http://ip.tool.chinaz.com/{github.com,github.global.ssl.fastly.net}) | grep -Po "AiWenIpData\(.*?\)" | cut -d "'" -f 2 > ${IP}

echo IP获取完毕
# 删除原有的github映射
sed -i "/.*github.*/d" '/mnt/c/Windows/System32/drivers/etc/hosts'

# 写入Windows的hosts 
# todu 没写入权限
paste -d " " ${IP} ${SITE} >> '/mnt/c/Windows/System32/drivers/etc/hosts'

# 删除临时文件
rm -f ${IP} ${SITE}

echo IP写入完成
# 刷新Windows的DNS换成
cmd.exe /C ipconfig /flushdns 

echo -e "\033[1;46;33mGithub的hosts映射更新完成\033[0m"