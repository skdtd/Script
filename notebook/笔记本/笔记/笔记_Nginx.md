# Nginx版本

[官方基础版](http://nginx.org/en/) 基础版本

[官方商业版](https://www.nginx.com/products/nginx) 商业版

[OpenResty](http://openresty.org/cn/) 基于lua脚本语言拓展

[Tengine](https://tengine.taobao.org/) 基于C语言拓展


# 下载最新版Nginx
```bash
# 官方基础版
curl -sS http://nginx.org/download/ | grep 'tar.gz' | grep -v 'asc'| sed  -r 's/.*>(.*?)<.*> +([0-9]{2})-([A-Za-z]{3})-([0-9]{4}) ([0-9]{2}):([0-9]{2}).*/\1\t\4\t\3\t\2\t\5\t\6/' | awk 'BEGIN{T["Jan"]=1;T["Feb"]=2;T["Mar"]=3;T["Apr"]=4;T["May"]=5;T["Jun"]=6;T["Jul"]=7;T["Aug"]=8;T["Sep"]=9;T["Oct"]=10;T["Nov"]=11;T["Dec"]=12}{gsub($3,T[$3]);print $1"\t"mktime($2" "$3" "$4" "$5" "$6" 00")}' | sort -rnk2 | head -1 | cut -f1 | xargs -I{} curl -O http://nginx.org/download/{}

# OpenResty
curl -sS https://openresty.org/en/download.html | grep -A2 'Lastest release' | tail -1 | sed -r s'/.*href="(.*?)" .*/\1/' | xargs -I{} curl -O {}

# Tengine
curl -sS https://tengine.taobao.org/download.html | awk -v RS='.tar.gz' '{print $0}' | grep '">Tengine-' |head -1 | awk -F'-' '{print $2}' | xargs -I{} curl -O https://tengine.taobao.org/download/tengine-{}.tar.gz
```

# 安装
```bash
# 依赖gcc
yum install -y gcc-c++ pcre-devel zlib-devel
./configure --prefix=/usr/local/nginx
make && make install
```

# 防火墙设置
```bash
# 开启防火墙
systemctl enable --now firewalld

# 关闭防火墙
systemctl disable --now firewalld

# 查看防火墙开放的端口
firewall-cmd --zone=public --list-ports

# 放行80/tcp端口
firewall-cmd --zone=public --add-port=80/tcp --permanent

# 重载防火墙配置
firewall-cmd --reload
```

# 启停命令
```bash
# 启动
./nginx

# 立即停止
./nginx -s stop

# 优雅停止
./nginx -s quit

# 重新加载配置
./nginx -s reload
```

# 安装服务
> 服务文件`/usr/lib/systemd/system/nginx.service`
> 
> 重新加载系统服务`systemctl daemon-reload`
> 
> 开机启动`systemctl enable --now nginx`
```conf
[Unit]
Description=The nginx HTTP and reverse proxy server
After=network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
PIDFile=/usr/local/nginx/logs/nginx.pid
ExecStartPre=/usr/local/nginx/sbin/nginx -t -c /usr/local/nginx/conf/nginx.conf
ExecStart=/usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf
ExecReload=/usr/local/nginx/sbin/nginx -s reload
ExecStop=/usr/local/nginx/sbin/nginx -s stop
ExecQuit=/usr/local/nginx/sbin/nginx -s quit
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

# 配置文件
```conf
# 工作进程数(worker进程数量)(对应节点CPU数)
worker_processes  1;

events {
    # 每个worker可以创建的连接数
    worker_connections  1024;
}


http {
    # 引入外部配置文件
    include       mime.types; # 定义文件类型(告诉客户端如果解释对应文件类型)
    default_type  application/octet-stream; # 默认文件类型

    # 数据0拷贝
    # 是否将文件先读取到Nginx应用程序的内存中
    sendfile        on; 

    # 超时时间
    keepalive_timeout  65;

    # 虚拟主机(可以配置多个虚拟主机)
    # 从上往下匹配 如果都没匹配到则显示第一个
    server {

        # 多个虚拟主机的端口号与主机名不可完全相同
        # 监听端口号
        listen       80;

        # 当前主机的主机名(可以配置为域名或者主机名)
        # 可以使用正则(~^[0-9]\.test\.com$;)
        server_name  localhost;

        # 匹配URI
        location / {
            # 静态资源主目录
            root   /opt/site/www;
            # 默认页
            index  index.html index.htm;
        }

        # 服务器端错误时返回页
        error_page   500 502 503 504  /50x.html;
        # 定义指定页面的位置
        location = /50x.html {
            root   html;
        }
    }
    
    # 定义服务器组可以与proxy_pass搭配实现负载均衡
    # weight: 负载均衡权重
    # down: 不参与负载均衡
    # backup: 当其他节点都不可用时使用
    upstream testgroup{
        server 192.168.10.102:80 weight=8 down;
        server 192.168.10.103:80 weight=2;
        server 192.168.10.104:80 weight=1 backup;
    }


    server {
        listen       80;
        server_name  proxy.test.com;

        location / {
            # proxy_pass与root只能二选一, 需要填写完整域名,缺少www时可能会出现302重定向
            # 不能反向代理到https的网站
            # 反向代理带内网服务器(http://192.168.10.101)
            # 可以与upstream搭配实现负载均衡(http://testgroup)
            proxy_pass http://www.test.com
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }

        # 动静分离, 将静态文件请求指向本机目录, 多少个目录要配置多少个location
        # 或者使用正则匹配 ~: 使用正则, *: 不区分大小写
        location ~*/(css|js|img) {
            root   /opt/site/www;
            index  index.html index.htm;
        }
        
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
    
    server {
        listen       80;
        server_name  test.com;

        location / {
            root   /opt/site/www;
            index  index.html index.htm;
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
}
```

# 反向代理
## 隧道式传输(带宽限制明显)
## DR模型(请求经过代理服务器,响应由应用服务器直接返回)(解决响应占用带宽)
