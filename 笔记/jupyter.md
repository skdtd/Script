```bash
# jupyter-notebook切换中文
echo "export LANG='zh_CN.UTF8'" >> ~/.bashrc

# jupyter-lab切换中文
pip install jupyterlab-language-pack-zh-CN
```



```python
# jupyter-lab 配置
c.ServerApp.ip = '*'
c.ServerApp.allow_remote_access = True
c.ServerApp.root_dir = '/root/data/notebook'
c.ServerApp.password = u'sha1:99cb284c7992:685e06fe4f24004b7ad704099915d8e840f7e564' # 117788
c.ServerApp.password_required = False
c.ServerApp.quit_button = False
c.ServerApp.allow_root = True
c.ServerApp.open_browser = False
```

# jupyter 作为服务()
```bash
touch /lib/systemd/system/jupyter.service # 贴入下面ini内容
systemctl daemon-reload
systemctl enabe --now jupyter
```
```ini
[Unit]
Description=Jupyter Lab

[Service]
Type=simple
PIDFile=/run/jupyter.pid
ExecStart=/opt/miniconda3/envs/jpy/bin/jupyter-lab --config=~/.jupyter/jupyter_lab_config.py
User=root
Group=root
WorkingDirectory=/root/data/notebook
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

# [安装jupyter](https://lyric.im/c/the-craft-of-selfteaching/T-appendix.jupyter-installation-and-setup)
```shell
pip install jupyterlab
```

# 如果pywin32出问题, 安装225版
```shell
pip install pywin32==225
```

# 插件

## [代码格式化](https://github.com/ryantam626/jupyterlab_code_formatter)
```shell
pip install jupyterlab_code_formatter black isort
```

## [kite](https://github.com/kiteco/jupyterlab-kite)
```shell
pip install "jupyterlab-kite>=2.0.2"
```

## [系统资源监控](https://github.com/jtpio/jupyterlab-system-monitor)
```shell
pip install jupyterlab-system-monitor
```
```python
# ~/.jupyter/jupyter_notebook_config.py
c = get_config()
# memory
c.ResourceUseDisplay.mem_limit = <size_in_GB> *1024*1024*1024
# cpu
c.ResourceUseDisplay.track_cpu_percent = True
c.ResourceUseDisplay.cpu_limit = <number_of_cpus>
```

## [查看excel(只读)](https://github.com/quigleyj97/jupyterlab-spreadsheet)
```shell
jupyter labextension install jupyterlab-spreadsheet
```

## [cell执行时间](https://github.com/deshaw/jupyterlab-execute-time)
```shell
pip install jupyterlab_execute_time
# 修改配置
# Settings->Advanced Settings Editor -> Notebook: {"recordTiming": true}
```
## [debugger](https://github.com/jupyterlab/debugger)
```shell
jupyter labextension install @jupyterlab/debugger
```

## [思维导图](https://github.com/QuantStack/jupyterlab-drawio)
```shell
pip install jupyterlab-drawio
```
## [github](https://github.com/jupyterlab/jupyterlab-github)

## [sql](https://github.com/pbugnion/jupyterlab-sql)

## [变量检查器](https://github.com/lckr/jupyterlab-variableInspector)
```shell
pip install lckr-jupyterlab-variableinspector
```

## [lsp(查看变量定义)](https://github.com/krassowski/jupyterlab-lsp)
### [所有语言支持](https://jupyterlab-lsp.readthedocs.io/en/latest/Language%20Servers.html)
```shell
pip install jupyterlab-lsp
# python支持
pip install 'python-language-server[all]'
```
