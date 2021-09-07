# 升级软件包(分发出去的由于是用格rpm安装,需要添加--force强制覆盖安装)
INSTMP=$(mktemp -d)
grep -q "^keepcache" /etc/yum.conf && sed -i "s/^keepcache.*/keepcache=1/" /etc/yum.conf || echo "keepcache=1" >> /etc/yum.conf
mkdir ${INSTMP}/updates
yum update -y --exclude=kernel* --downloadonly --downloaddir=${INSTMP}/updates

# 升级内核
mkdir ${INSTMP}/kernel
rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
yum install -y https://www.elrepo.org/elrepo-release-7.el7.elrepo.noarch.rpm
yum install epel-release # jq工具包下载库
yum --enablerepo=elrepo-kernel install kernel-lt --downloadonly --downloaddir=${INSTMP}/kernel
<!-- https://elrepo.org/linux/kernel/el7/x86_64/RPMS/  # 下载内核包 x86_64 -->
<!-- curl -sSL https://elrepo.org/linux/kernel/el7/x86_64/RPMS/ | grep -Po "kernel-lt-\d.*?el7\.elrepo\.x86_64\.rpm" | uniq | sort | tail -1 -->
awk -F\' '$1=="menuentry " {print i++ " : " $2}' /etc/grub2.cfg
sed -i 's/saved/0/g' /etc/default/grub
grub2-mkconfig -o /boot/grub2/grub.cfg
reboot

# 关闭防火墙
systemctl stop firewalld && systemctl disable firewalld

# 设置host
hostnamectl set-hostname k8s-01
hostnamectl set-hostname k8s-02
hostnamectl set-hostname k8s-03

hostnamectl status
echo "127.0.0.1   $(hostname)" >> /etc/hosts

# 添加所有主机映射
vi /etc/hosts


# 关闭selinux安全机制
setenforce 0 && sed -i 's#SELINUX=enforcing#SELINUX=disabled#g' /etc/sysconfig/selinux /etc/selinux/config

# 关闭swap
swapoff -a && sysctl -w vm.swappiness=0 && sed -ri 's/.*swap.*/#&/' /etc/fstab

# 修改流量转发(有则修改,无则添加)
CMD='grep -q "^${key}" /etc/sysctl.conf && sed -i "s/^${key}.*/${key}=1/" /etc/sysctl.conf || echo "${key}=1" >> /etc/sysctl.conf'
cat << EOF | while read key; do eval "$CMD";done
net.ipv4.ip_forward
net.bridge.bridge-nf-call-ip6tables
net.bridge.bridge-nf-call-iptables
net.ipv6.conf.all.disable_ipv6
net.ipv6.conf.default.disable_ipv6
net.ipv6.conf.lo.disable_ipv6
net.ipv6.conf.all.forwarding
EOF

sysctl -p



# 修改limit
ulimit -SHn 65535
sed -i '$c* soft nofile 655360\n* hard nofile 131072\n* soft nproc 655350\n* hard nproc 655350\n* soft memlock unlimited\n* hard memlock unlimited\n\n# End of file' /etc/security/limits.conf

* soft nofile 655360
* hard nofile 131072
* soft nproc 655350
* hard nproc 655350
* soft memlock unlimited
* hard memlock unlimited




# master对所有节点免密设置
cat << EOF | while read i; do ssh-copy-id -i .ssh/id_rsa.pub $i;done
192.168.100.101
192.169.100.102
192.168.100.103
EOF


# 安装常用工具(master)
mkdir ${INSTMP}/tools
yum install vim wget git jq psmisc net-tools yum-utils device-mapper-persistent-data lvm2 -y --downloadonly --downloaddir=${INSTMP}/tools

# 安装ipvs,替换iptables作为kube-proxy的实现
mkdir ${INSTMP}/ipvs
yum install ipvsadm ipset sysstat conntrack libseccomp -y --downloadonly --downloaddir=${INSTMP}/ipvs

# 安装docker
mkdir ${INSTMP}/docker
DOKCER_URL='https://download.docker.com/linux/static/stable/x86_64/'
DOCKER_VERSION=$(curl -sSL ${DOKCER_URL} | grep -Po "docker-(\d+\.){2}(\d+)" | uniq | grep -Ev "ce|rootless" | sed -n '$p') && echo ${DOCKER_VERSION}
curl -OC - ${DOKCER_URL}${DOCKER_VERSION}.tgz
tar -zvxf ${DOCKER_VERSION}.tgz -C ${INSTMP}/docker
cp ${INSTMP}/docker/docker/* /usr/bin/


/etc/systemd/system/docker.service

mkdir /etc/docker
/etc/docker/daemon.json


chmod +x /etc/systemd/system/docker.service
systemctl enable --now docker

# 下载cfssl
CFSSL_URL='https://github.com/cloudflare/cfssl/releases/'
CFSSL_VERSION=$(curl -sS ${CFSSL_URL}latest | sed -r 's#.*tag/v(.*)">redirected.*#\1#g')
curl --remote-name-all -LC - ${CFSSL_URL}download/v${CFSSL_VERSION}/{cfssl-certinfo,cfssl,cfssljson}_${CFSSL_VERSION}_linux_amd64
for name in `ls cfssl*`; do chmod +x $name; mv $name /usr/bin/${name%_${CFSSL_VERSION}_linux_amd64};  done

# 下载etcd
mkdir ${INSTMP}/etcd
ETCD_URL='https://github.com/etcd-io/etcd/releases/'
ETCD_VERSION=$(curl -sS ${ETCD_URL}latest | sed -r 's#.*tag/(.*)">redirected.*#\1#g')
curl -OC - ${ETCD_URL}download/${ETCD_VERSION}/etcd-${ETCD_VERSION}-linux-amd64.tar.gz
tar -zxvf etcd-${ETCD_VERSION}-linux-amd64.tar.gz --strip-components=1 -C /usr/local/bin etcd-${ETCD_VERSION}-linux-amd64/etcd{,ctl}
/usr/lib/systemd/system/etcd.service
systemctl enable --now etcd

journalctl -u etcd   启动有问题用该命令排查

# 下载k8s服务(master需要全部组件,node节点只需要 /usr/local/bin kubelet、kube-proxy)
K8S_VERSION=$(curl -sSL https://dl.k8s.io/release/stable.txt)
K8S_URL='https://dl.k8s.io/'
curl -LOC - ${K8S_URL}${K8S_VERSION}/kubernetes-server-linux-amd64.tar.gz
tar -xvf kubernetes-server-linux-amd64.tar.gz  --strip-components=3 -C /usr/local/bin kubernetes/server/bin/kube{let,ctl,-apiserver,-controller-manager,-scheduler,-proxy}

curl --remote-name-all -LC - "${K8S_URL}release/${K8S_VERSION}/bin/linux/amd64/kube{let,ctl,-apiserver,-controller-manager,-scheduler,-proxy}" # 单独下载组件


# 创建服务文件
/usr/lib/systemd/system/kubelet.service
/etc/systemd/system/kubelet.service.d/10-kubelet.conf
/etc/kubernetes/kubelet-conf.yml                        # clusterDNS 为service网络的第10个ip值,改成自己的。如：10.96.0.10
/usr/lib/systemd/system/kube-apiserver.service
/usr/lib/systemd/system/kube-scheduler.service 
/etc/kubernetes/kube-proxy.yaml




systemctl enable --now kube{let,ctl,-apiserver,-controller-manager,-scheduler,-proxy}
systemctl enable --now kubelet
systemctl enable --now kube-apiserver
systemctl enable --now kube-controller-manager
