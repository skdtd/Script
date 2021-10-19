# 升级软件包(分发出去的由于是用格rpm安装,需要添加--force强制覆盖安装)
INSTMP=${INSTMP:="$(mktemp -d)"}
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

/etc/sysctl.d/k8s.conf

sysctl --system






# 修改limit(提高服务器并发)
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
## 所有节点配置ipvs模块,执行以下命令，在内核4.19+版本改为nf_conntrack， 4.18下改为nf_conntrack_ipv4
modprobe -- ip_vs
modprobe -- ip_vs_rr
modprobe -- ip_vs_wrr
modprobe -- ip_vs_sh
modprobe -- nf_conntrack
## 修改ipvs配置，加入以下内容
vi /etc/modules-load.d/ipvs.conf

ip_vs
ip_vs_lc
ip_vs_wlc
ip_vs_rr
ip_vs_wrr
ip_vs_lblc
ip_vs_lblcr
ip_vs_dh
ip_vs_sh
ip_vs_fo
ip_vs_nq
ip_vs_sed
ip_vs_ftp
ip_vs_sh
nf_conntrack
ip_tables
ip_set
xt_set
ipt_set
ipt_rpfilter
ipt_REJECT
ipip

## 启动
systemctl enable --now systemd-modules-load.service
lsmod | grep -e ip_vs -e nf_conntrack

tee /etc/sysctl.d/k8s.conf <<-'EOF'
net.ipv4.ip_forward = 1
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
fs.may_detach_mounts = 1
vm.overcommit_memory=1
net.ipv4.conf.all.route_localnet = 1

vm.panic_on_oom=0
fs.inotify.max_user_watches=89100
fs.file-max=52706963
fs.nr_open=52706963
net.netfilter.nf_conntrack_max=2310720

net.ipv4.tcp_keepalive_time = 600
net.ipv4.tcp_keepalive_probes = 3
net.ipv4.tcp_keepalive_intvl =15
net.ipv4.tcp_max_tw_buckets = 36000
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_max_orphans = 327680
net.ipv4.tcp_orphan_retries = 3
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 16768
net.ipv4.ip_conntrack_max = 65536
net.ipv4.tcp_timestamps = 0
net.core.somaxconn = 16768
EOF
sysctl --system
reboot
lsmod | grep -e ip_vs -e nf_conntrack

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
for name in `ls cfssl*`; do chmod +x $name; mv $name ${name%_${CFSSL_VERSION}_linux_amd64}; done
mv cfssl* /usr/bin/

# 下载etcd
mkdir ${INSTMP}/etcd
ETCD_URL='https://github.com/etcd-io/etcd/releases/'
ETCD_VERSION=$(curl -sS ${ETCD_URL}latest | sed -r 's#.*tag/(.*)">redirected.*#\1#g')
curl -LOC - ${ETCD_URL}download/${ETCD_VERSION}/etcd-${ETCD_VERSION}-linux-amd64.tar.gz
tar -zxvf etcd-${ETCD_VERSION}-linux-amd64.tar.gz --strip-components=1 -C /usr/local/bin etcd-${ETCD_VERSION}-linux-amd64/etcd{,ctl}
/usr/lib/systemd/system/etcd.service
systemctl enable --now etcd

journalctl -u etcd   启动有问题用该命令排查

# 下载k8s服务(master需要全部组件,node节点只需要 /usr/local/bin kubelet、kube-proxy)
mkdir ${INSTMP}/k8s
K8S_VERSION=$(curl -sSL https://dl.k8s.io/release/stable.txt)
K8S_URL='https://dl.k8s.io/'
curl -LOC - ${K8S_URL}${K8S_VERSION}/kubernetes-server-linux-amd64.tar.gz
tar -xvf kubernetes-server-linux-amd64.tar.gz --strip-components=3 -C /usr/local/bin kubernetes/server/bin/kube{let,ctl,-apiserver,-controller-manager,-scheduler,-proxy}

curl --remote-name-all -LC - "${K8S_URL}release/${K8S_VERSION}/bin/linux/amd64/kube{let,ctl,-apiserver,-controller-manager,-scheduler,-proxy}" # 单独下载组件


# 创建服务文件
/usr/lib/systemd/system/kubelet.service
/etc/systemd/system/kubelet.service.d/10-kubelet.conf
/etc/kubernetes/kubelet-conf.yml                        # clusterDNS 为service网络的第10个ip值,改成自己的。如：10.96.0.10
/usr/lib/systemd/system/kube-apiserver.service
/usr/lib/systemd/system/kube-scheduler.service
/usr/lib/systemd/system/kube-proxy.service
/etc/kubernetes/kube-proxy.yaml




systemctl enable --now kube{let,ctl,-apiserver,-controller-manager,-scheduler,-proxy}
systemctl enable --now kubelet
systemctl enable --now kube-apiserver
systemctl enable --now kube-controller-manager






# 创建证书机构(ca根配置)
mkdir -p /etc/kubernetes/pki
tee /etc/kubernetes/pki/ca-config.json <<-'EOF'
{
    "signing": {
        "default": {
            "expiry": "87600h"
        },
        "profiles": {
            "server": {
                "expiry": "87600h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "server auth"
                ]
            },
            "client": {
                "expiry": "87600h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "client auth"
                ]
            },
            "peer": {
                "expiry": "87600h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "server auth",
                    "client auth"
                ]
            },
            "kubernetes": {
                "expiry": "87600h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "server auth",
                    "client auth"
                ]
            },
            "etcd": {
                "expiry": "87600h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "server auth",
                    "client auth"
                ]
            }
        }
    }
}
EOF
# 提交证书申请
tee /etc/kubernetes/pki/ca-csr.json <<-'EOF'
{
  "CN": "kubernetes",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "Shanghai",
      "L": "Shanghai",
      "O": "Kubernetes",
      "OU": "Kubernetes"
    }
  ],
  "ca": {
    "expiry": "87600h"
  }
}
EOF

# 初始化ca机构(测试)
cfssl gencert -initca ca-csr.json | cfssljson -bare ca -


# ETCD推荐资源配置
https://etcd.io/docs/v3.5/op-guide/hardware/#example-hardware-configurations

# etcd证书配置
tee /etc/kubernetes/pki/etcd-ca-csr.json <<-'EOF'
{
  "CN": "etcd",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",
      "ST": "Shanghai",
      "L": "Shanghai",
      "O": "etcd",
      "OU": "etcd"
    }
  ],
  "ca": {
    "expiry": "87600h"
  }
}
EOF
# 生成etcd根证书
cfssl gencert -initca etcd-ca-csr.json | cfssljson -bare /etc/kubernetes/pki/etcd/ca -


# etcd证书申请
tee /etc/kubernetes/pki/etcd-test.json <<-'EOF'
{
    "CN": "etcd-test",
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "hosts": [  
        "127.0.0.1",
        "os1",
        "os2",
        "os3",
        "192.168.100.101",
        "192.168.100.102",
        "192.168.100.103"
    ],
    "names": [
        {
            "C": "CN",
            "L": "shanghai",
            "O": "etcd",
            "ST": "shanghai",
            "OU": "System"
        }
    ]
}
EOF
# 签发itdachang的etcd证书
cfssl gencert \
   -ca=/etc/kubernetes/pki/etcd/ca.pem \
   -ca-key=/etc/kubernetes/pki/etcd/ca-key.pem \
   -config=/etc/kubernetes/pki/ca-config.json \
   -profile=etcd \
   etcd-test.json | cfssljson -bare /etc/kubernetes/pki/etcd/etcd


# 把生成的etcd证书，复制给其他机器
for i in os2 os3;do scp -r /etc/kubernetes/pki/etcd root@$i:/etc/kubernetes/pki;done

# 创建配置文件(高可用)
mkdir -p /etc/etcd
tee /etc/etcd/etcd.yaml << EOF

# 作成etcd服务自启动
/usr/lib/systemd/system/etcd.service



> 测试etcd访问

```sh
# 查看etcd集群状态
etcdctl --endpoints="192.168.100.101:2379,192.168.100.102:2379,192.168.100.103:2379" --cacert=/etc/kubernetes/pki/etcd/ca.pem --cert=/etc/kubernetes/pki/etcd/etcd.pem --key=/etc/kubernetes/pki/etcd/etcd-key.pem  endpoint status --write-out=table


# 以后测试命令
export ETCDCTL_API=3
HOST_1=k8s-01
HOST_2=k8s-02
HOST_3=k8s-03
ENDPOINTS=$HOST_1:2379,$HOST_2:2379,$HOST_3:2379

## 导出环境变量，方便测试，参照https://github.com/etcd-io/etcd/tree/main/etcdctl
export ETCDCTL_DIAL_TIMEOUT=120s
export ETCDCTL_CACERT=/etc/kubernetes/pki/etcd/ca.pem
export ETCDCTL_CERT=/etc/kubernetes/pki/etcd/etcd.pem
export ETCDCTL_KEY=/etc/kubernetes/pki/etcd/etcd-key.pem
export ETCDCTL_ENDPOINTS=$HOST_1:2379,$HOST_2:2379,$HOST_3:2379
# 自动用环境变量定义的证书位置
etcdctl  member list --write-out=table

#如果没有环境变量就需要如下方式调用
etcdctl --endpoints=$ENDPOINTS --cacert=/etc/kubernetes/pki/etcd/ca.pem --cert=/etc/kubernetes/pki/etcd/etcd.pem --key=/etc/kubernetes/pki/etcd/etcd-key.pem member list --write-out=table


## 更多etcdctl命令，https://etcd.io/docs/latest/demo/#access-etcd
```
