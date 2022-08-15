# 环境安装
```
SLB虚拟机(BIGIP-12.1.5-0.0.6):
Hyper安装:
1. 新建虚拟机->加载已有硬盘->完成
2. 启动虚拟机,登录(root/default),等待系统初始化完成
3. 通过"ifconfig eth0"命令获取连接地址(例如192.168.100.100)
4. 浏览器输入"https://192.168.100.100",登录用户名(admin/admin)
5. 选择"License"选项卡,点击"Activate..."
6. 在"Base Registration Key"中输入key,"Activation Method"选择"Manual",点击"Next..."
7. 复制"Step 1:Dossier"中字串,点击"Step 2: Licensing Server"中的超链接打开新窗口
8. 将7中复制的字串贴入"Enter your dossier"文本框,点击"Next"
9. 点击"Down License",打开下载的License,复制内容,贴入"Step 3: License"文本框中,点击"Next..."
10.一直"Next..."直到激活完成,返回虚拟机控制台显示已经从"NO LICENSE"变为"Active"则激活完成

ansible机(为python2.7安装f5-sdk):
wget https://pypi.python.org/packages/11/b6/abcb525026a4be042b486df43905d6893fb04f05aac21c32c638e939e447/pip-9.0.1.tar.gz#md5=35f01da33009719497f01a4ba69d63c9

tar -zxvf pip-9.0.1.tar.gz
cd pip-9.0.1
python setup.py install
python -m pip install f5-sdk
```
# 命令(创建MOCK数据)
```bash
# 查询ltm
tmsh list /ltm virtual

# 创建DEVICE-GROUP
tmsh create /cm device-group DEVICE-GROUP

# 创建devices
tmsh create /cm device tsaoym-esmslb01.local
tmsh create /cm device tsaoym-esmslb02.local
tmsh create /cm device tsaoym-ppmslb01.local
tmsh create /cm device tsaoym-ppmslb02.local

tmsh modify /cm device-group DEVICE-GROUP devices add { tsaoym-esmslb01.local { set-sync-leader } }
tmsh modify /cm device-group DEVICE-GROUP devices add { tsaoym-esmslb02.local { set-sync-leader } }
tmsh modify /cm device-group DEVICE-GROUP devices add { tsaoym-ppmslb01.local { set-sync-leader } }
tmsh modify /cm device-group DEVICE-GROUP devices add { tsaoym-ppmslb02.local { set-sync-leader } }

# 创建ltm
tmsh create /ltm virtual VS_BE_CPQR
tmsh create /ltm virtual VS_BE_ONQR
tmsh create /ltm virtual VS_SN_ONQR2
tmsh create /ltm virtual VS_BE_KON_ONQR
tmsh create /ltm virtual VS_BE_PMQR
tmsh create /ltm virtual VS_BE_PMQR_TEST

# 创建blue面
tmsh create /ltm pool POOL_BE_CPQR_BLUE members add { 2.2.2.2:80 2.2.2.3:80 } monitor tcp
tmsh create /ltm pool POOL_BE_ONQR_BLUE members add { 2.2.2.2:80 2.2.2.3:80 } monitor tcp
tmsh create /ltm pool POOL_SN_ONQR2_BLUE members add { 2.2.2.2:80 2.2.2.3:80 } monitor tcp
tmsh create /ltm pool POOL_BE_KON_ONQR_BLUE members add { 2.2.2.2:80 2.2.2.3:80 } monitor tcp
tmsh create /ltm pool POOL_BE_PMQR_BLUE members add { 2.2.2.2:80 2.2.2.3:80 } monitor tcp
tmsh create /ltm pool POOL_BE_PMQR_TEST_BLUE members add { 2.2.2.2:80 2.2.2.3:80 } monitor tcp

# 创建green面
tmsh create /ltm pool POOL_BE_CPQR_GREEN members add { 2.2.2.2:80 2.2.2.3:80 } monitor tcp
tmsh create /ltm pool POOL_BE_ONQR_GREEN members add { 2.2.2.2:80 2.2.2.3:80 } monitor tcp
tmsh create /ltm pool POOL_SN_ONQR2_GREEN members add { 2.2.2.2:80 2.2.2.3:80 } monitor tcp
tmsh create /ltm pool POOL_BE_KON_ONQR_GREEN members add { 2.2.2.2:80 2.2.2.3:80 } monitor tcp
tmsh create /ltm pool POOL_BE_PMQR_GREEN members add { 2.2.2.2:80 2.2.2.3:80 } monitor tcp
tmsh create /ltm pool POOL_BE_PMQR_TEST_GREEN members add { 2.2.2.2:80 2.2.2.3:80 } monitor tcp

# 切换到blue面
tmsh modify /ltm virtual VS_BE_CPQR { pool POOL_BE_CPQR_BLUE }
tmsh modify /ltm virtual VS_BE_ONQR { pool POOL_BE_ONQR_BLUE }
tmsh modify /ltm virtual VS_SN_ONQR2 { pool POOL_SN_ONQR2_BLUE }
tmsh modify /ltm virtual VS_BE_KON_ONQR { pool POOL_BE_KON_ONQR_BLUE }
tmsh modify /ltm virtual VS_BE_PMQR { pool POOL_BE_PMQR_BLUE }
tmsh modify /ltm virtual VS_BE_PMQR_TEST { pool POOL_BE_PMQR_TEST_BLUE }

# 切换到green面
tmsh modify /ltm virtual VS_BE_CPQR { pool POOL_BE_CPQR_GREEN }
tmsh modify /ltm virtual VS_BE_ONQR { pool POOL_BE_ONQR_GREEN }
tmsh modify /ltm virtual VS_SN_ONQR2 { pool POOL_SN_ONQR2_GREEN }
tmsh modify /ltm virtual VS_BE_KON_ONQR { pool POOL_BE_KON_ONQR_GREEN }
tmsh modify /ltm virtual VS_BE_PMQR { pool POOL_BE_PMQR_GREEN }
tmsh modify /ltm virtual VS_BE_PMQR_TEST { pool POOL_BE_PMQR_TEST_GREEN }

# 切换后保存状态
tmsh save sys config partitions all

tmsh modify /cm device-group DEVICE-GROUP devices modify { tsaoym-esmslb01.local { set-sync-leader } }
tmsh modify /cm device-group DEVICE-GROUP devices modify { tsaoym-esmslb02.local { set-sync-leader } }
tmsh modify /cm device-group DEVICE-GROUP devices modify { tsaoym-ppmslb01.local { set-sync-leader } }
tmsh modify /cm device-group DEVICE-GROUP devices modify { tsaoym-ppmslb02.local { set-sync-leader } }
```