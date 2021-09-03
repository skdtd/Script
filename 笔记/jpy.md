# 安装node.js
```bash
conda install nodejs -c conda-forge
# 查看配置
npm config ls -l # 详细
npm config list # 简版
# 设置代理
npm config set proxy="http://localhost:8080"
# 查看现有源
npm config get registry
# 设置淘宝源
npm config set registry https://registry.npm.taobao.org
# 更新
npm update
```

# [安装jupyter](https://lyric.im/c/the-craft-of-selfteaching/T-appendix.jupyter-installation-and-setup)
```bash
pip install jupyterlab 
# 查看工作路径
jupyter --paths
```

# 如果pywin32出问题, 安装225版
```bash
pip install pywin32==225
```

# 安装内核
```bash
# 查看当前内核
jupyter kernelspec list

# 删除内核
jupyter kernelspec remove python

# 安装python内核
ipython kernel install --name python
```

# 插件

## [代码格式化](https://github.com/ryantam626/jupyterlab_code_formatter)
```bash
pip install jupyterlab_code_formatter black isort
```

## [系统资源监控](https://github.com/jtpio/jupyterlab-system-monitor)
```bash
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
```bash
jupyter labextension install jupyterlab-spreadsheet
```

## [cell执行时间](https://github.com/deshaw/jupyterlab-execute-time)
```bash
pip install jupyterlab_execute_time
# 修改配置
# Settings->Advanced Settings Editor -> Notebook: {"recordTiming": true}
```
## [debugger](https://github.com/jupyterlab/debugger)
```bash
jupyter labextension install @jupyterlab/debugger
```

## [思维导图](https://github.com/QuantStack/jupyterlab-drawio)
```bash
pip install jupyterlab-drawio
```
## [github](https://github.com/jupyterlab/jupyterlab-github)

## [sql](https://github.com/pbugnion/jupyterlab-sql)

## [变量检查器](https://github.com/lckr/jupyterlab-variableInspector)
```bash
pip install lckr-jupyterlab-variableinspector
```

## [lsp(查看变量定义)](https://github.com/krassowski/jupyterlab-lsp)
### [所有语言支持](https://jupyterlab-lsp.readthedocs.io/en/latest/Language%20Servers.html)
```bash
pip install jupyterlab-lsp
# python支持
pip install 'python-language-server[all]'
```

## [kite](https://github.com/kiteco/jupyterlab-kite)
```bash
pip install "jupyterlab-kite>=2.0.2"
```