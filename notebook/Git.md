
Git命令
```bash
# 配置全局Git信息
git config --global user.name "Your Name"               # 添加名称
git config --global user.email "email@example.com"      # 添加邮箱
git config --global color.ui true                       # 终端颜色支持
git config --global alias.st status                     # 配置别名(将status配置为st)
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
# 初始化仓库
git init

# 添加文件到Git管理
git add <文件名>
git add -f <文件名>     # 强制添加文件(无视.gitignore规则)

# 提交修改
git commit -m "<消息>"

# 查看当前仓库状态
git status

# 查看文件改动
git diff <文件名>

# 查看当前版本与工作区中文件改动
git diff HEAD -- <文件名>

# 查看提交历史
# --stat 显示每次更新的文件修改统计信息
# --shortstat 只显示--stat中最后的行数修改添加移除统计
# --name-only 仅在提交信息后显示已修改的文件清单
# --name-status 显示新增、修改、删除的文件清单
# --abbrev-commit 仅显示SHA-1的前几个字符,而非所有的40个字符
# --relative-date 使用较短的相对时间显示(比如,"2 weeks ago")
# --graph 显示 ASCII 图形表示的分支合并历史
# --pretty 使用其他格式显示历史提交信息可用的选项包括oneline,short,full,fuller和format(后跟指定格式)
# -(n)	仅显示最近的 n 条提交
# --since, --after 仅显示指定时间之后的提交
# --until, --before 仅显示指定时间之前的提交
# --author 仅显示指定作者相关的提交
# --committer 仅显示指定提交者相关的提交
git log --pretty=oneline
git log --graph

# 回滚到已提交的版本
# HEAD^     : 回滚到上一个版本
# HEAD^^    : 回滚到上上一个版本
# HEAD~100  : 回滚到上100个版本
# 1094adb...: 回滚到指定版本(只输入部分版本号会自动去匹配,可以通过版本号撤销回滚)
git reset --hard HEAD^
git reset --hard 1094adb...

# 查看命令历史
git reflog

# 撤销当前工作区的修改到上一次commit或add
git checkout -- <文件名>

# 从版本库中删除一个文件(先手动删除文件,然后使用git rm <文件名>和git add<文件名>效果是一样的)
git rm <文件名>

# 添加远程仓库节点
git remote add origin git@github.com:<用户名>/<仓库名>.git

# 提交代码到远程仓库(-u: 关联本地与远程仓库)
git push -u origin master

# 查看远程库信息
git remote -v

# 删除远程库
git remote rm <name>

# 重命名远程库
git remote rename <old> <new>

# 克隆远程仓库
git clone <仓库地址>

# 创建并切换到分支
git checkout -b <分支名>
git switch -c <分支名>

# 创建分支
git branch <分支名>
git switch <分支名>

# 删除分支
git branch -d <分支名>

# 删除一个没有被合并过的分支
git branch -D <分支名>

# 切换分支
git checkout <分支名>

# 查看当前所处分支
git branch

# 合并某分支到当前分支
# --no-ff: 禁用Fast forward快速合并,保持原有分支信息
git merge <分支名>

# 储藏当前工作区修改
git stash

# 查看所有储藏的修改
git stash list

# 应用储藏的修改但不删除
git stash apply <tag>

# 删除储藏的修改
git stash drop <tag>

# 应用并删除储藏的修改
git stash pop <tag>

# 将指定的提交复制到当前分支
git cherry-pick <commit>

# 重构提交(把本地未push的分叉提交历史整理成直线)
git rebase

# 查看所有标签
git tag

# 删除标签
git tag -d <标签名>
git push origin :refs/tags/<标签名> # 可以删除一个远程标签

# 为当前commit设置标签
git tag <标签名>

# 为指定commit设置标签
git tag <标签名> <commit>

# 为标签添加描述
git tag -a <标签名> -m "消息" <commit>

# 查看标签信息
git show <标签名>

# 推送标签到远程
git push origin <标签名>   # 推送指定标签
git push origin --tags      # 推送所有标签

# 检查文件
git check-ignore -v <文件名>
```


# 搭建git服务器
```bash
# 安装git
yun -y install git
# 添加用户
useradd git
# 初始化仓库
git init --bare sample.git
# 设置仓库权限
chown -R git:git sample.git
# 修改git用户禁止bash登录(/etc/passwd)
git:x:1001:1001:,,,:/home/git:/bin/bash
# 改成
git:x:1001:1001:,,,:/home/git:/usr/bin/git-shell
# 节点上克隆仓库
git clone git@{IP}:/{PATH}/sample.git
# 免密: 将公钥添加到/home/git/.ssh/authorized_keys
```
[权限控制](https://github.com/sitaramc/gitolite)
[公钥管理](https://github.com/res0nat0r/gitosis)
