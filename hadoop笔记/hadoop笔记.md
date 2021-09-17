# 入门
## 环境准备
> 本机可以安装sshpass方便先执行分发公钥之前的步骤
1. 设置节点地址为静态IP地址
2. 设置主机名
   </br><b>`hostnamectl set-hostname ${hostname}`</b>
   </br><b>`hostnamectl -H ${user}@${host} set-hostname ${hostname}`</b>
3. 添加主机映射(/etc/hosts)
   </br><b>`tee -a /etc/hosts << EOF`</b>
   </br><b>`${hostlist}`</b>
   </br><b>`EOF`</b>
4. 开放22端口用于远程连接
5. 节点间免密
   </br><b>`ssh-keygen -q -N "" -f `</b>
   </br><b>`for i in ${hosts};do ssh-copy-id -i  ${user}@$i;done`</b>
## hadoop生产集群搭建
> 通过<b>`--downloadonly --downloaddir=${path}`</b>来只下载安装包 之后统一分发安装
1. 创建模板
   1. 安装epel-release, vim, net-tool
   </br><b>`yum install epel-release`</b>
   </br><b>`yum install vim net-tool`</b>
   2. 关闭节点防火墙
   </br><b>`systemctl stop --now firewalld`</b>
   3. 创建hadoop操作用户, 并添加相关root权限
   </br><b>`useradd ${user}`</b>
   </br><b>`echo ${password} | passwd ${user} --stdin`</b> 
   </br><b>`sed -i "/^\%wheel.*/a ${user}  ALL=(ALL)       NOPASSWD: ALL" /etc/sudoers`</b> 
   4. java版本不正确时卸载java
   </br><b>`rpm -qa | grep -i java | xargs -n1 rpm -e --nodeps`</b>
   5. 虚拟机使用复制虚拟机的方式, 云节点使用脚本部署
## 常见错误解决方案
# HDFS(负责数据存储)
# MapReduce(负责数据计算)
# YARN(Yet Another Resource Negotiator)(负责资源管理)
# 生产调优手册
# Hadoop源码解析