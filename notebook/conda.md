[简书](https://www.jianshu.com/p/edaa744ea47d)

[cheat sheet](https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html#)

# 清华大学源
```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r/
```

# 显示安装的channels
```bash
conda config --set show_channel_urls yes 
```

# 查看已经添加的channels
```bash
conda config --get channels
```

# linux下创建软件的软链接使其可以在退出环境的情况下使用
```bash
# 将连接目录添加到环境变量
export PATH="~/.MySoft:$PATH"
# 创建连接到之前的目录
ln -s ~/miniconda3/bin/XXXX ~/.MySoft
```

# conda环境相关
```bash
# 查看查看当前所有环境
conda env list
# 或者
conda info --envs

# 创建一个环境
# -n: 设置新的环境的名字
# python=2 指定新环境的python的版本，非必须参数
# 这里也可以用一个-y参数，可以直接跳过安装的确认过程。
conda create -n python2 python=2

# 根据文件创建环境
conda create --name myenv --file environment.txt

# 删除一个环境
conda remove -n myenv --all

# 退出conda环境
conda deactivate

# 重命名一个环境(先克隆环境,再将原环境删除)
conda create -n python2 --clone py2
conda remove -n py2 --all
```


# 软件包系列指令
```bash
# 安装软件
conda install XXXX
# 安装特定的版本
conda install XXXX=VVVV
# 搜索软件
conda search XXXX
# 查看安装位置
which XXXX
# 查看已安装软件
conda list
# 更新指定软件
conda update XXXX
# 卸载指定软件
conda remove XXXX
```

# allias简化启动
```bash
echo "allias condaon='~/miniconda3/bin/activate'" >> ~/.bashrc
source ~/.bashrc
```