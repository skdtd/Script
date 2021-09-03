# 配置相关
## 若要多次执行同一个role
1.  传入参数不同
2.  设置role的allow_duplicates属性: 在meta/main.yml文件中写入allow_duplicates：true

# 判断语句
## 路径是否存在
```yaml
- debug: msg="haha"
  when: '"/etc/ansible" is not exists'
```
## defined|undefined|none 判断变量值 是否定义|是否未定义|是否为空
```yaml
- debug: msg="haha"
  when: 'dhaksld is defined'
```
## success,succeeded|failure,failed|change,changed|skip,skipped 判断任务返回信息 是否成功|失败|改变|跳过
```yaml
- debug: msg="hahah"
  when: haha is not none
  register: res
- debug: msg="lueluelue"
  when: res is skip
```

## file|directory|link|mount|exists 判断ansible主机上的路径 是否为文件|目录|软连接|挂载点/存在
```yaml
- debug: msg="hahah"
  when: /etc/ansible is exists
```
## lower|upper 判断字符串 是否全为小写|大写
```yaml
- raw: echo "hahaha"
  register: res
- debug: var=res
  when: res.stdout is upper
```
## even|odd|divisibleby(num) 判断数值 是否为偶数|奇数|num的倍数
```yaml
- raw: echo 3
  register: res
- debug: var=res
  when: res.rc is even
```
## subset|superset 判断一个list是否为另一个list的子集|父集
```yaml
- debug: msg="lueluelue"
  when: aa is subset(bb)
```
## string|number 判断是否为 字符串|数字
```yaml
- debug: msg="lueluelue"
  when: aa is string
```
# tags标签
1.  tags 在命令行中用--tags指定需要运行的tasks, always表示总是执行, never表示总是跳过(只有被指定时才执行)
2.  ansible-playbook --skip-tags=t1 跳过指定标签
3.  ansible-playbook --tags=t1 执行指定标签
4.  ansible-playbook --list-tags 查看playbook中的tag
```yaml
- debug: msg="lueluelue"
  tags: t1
- debug: msg="hahaha"
  tags: t2
- debug: msg="gugugu"
  tags: [t1, t3]
- debug: msg="hehehe"
  tags: t2, t4
```
## 总是执行除非t5被指定跳过
```yaml
- debug: msg="gagaga"
  tags: t5, always
```
## 总是不执行除非t6被指定执行
```yaml
- debug: msg="heiheihei"
  tags: t6, never
```
# handlers
1.  在task中用notify调用handler,默认会按照声明顺序执行(与notify顺序无关),重复的handler只会执行1次
2.  \- meta: flush_handlers可以让前面的handler执行完之后再继续执行task
```yaml
tasks:
- name: t1
  raw: echo t1 > /etc/ansible/test
  notify: h2
- meta: flush_handlers
- name: t2
  raw: echo t2 >> /etc/ansible/test
  notify: h1
- meta: flush_handlers
- name: t3
  raw: echo t3 >> /etc/ansible/test
  notify: hg
handlers:
- name: h1
  listen: hg
  raw: echo h1 >> /etc/ansible/test
- name: h2
  listen: hg
  raw: echo h2 >> /etc/ansible/test
```

# 模块相关
## 出错立即停止程序
```yaml
  any_errors_fatal: true
  max_fail_percentage: 容忍一部分主机出错
```
## 引入role
```yaml
- include_role:
    name: test_role
  with_items: '{{ echo_list }}'
```
## task只执行一次
```yaml
- debug: 
    msg: "{{ (name1 == 'John') | ternary(1,0) | bool }}"
  run_once: yes
  delegate_to: localhost
```
## serial 设置并发数
```yaml
---
- name: test
  hosts: all
  serial: 1
  roles:
    - { role: test }
```
## 变量嵌套
```yaml
---
- name: test
  hosts: all
  become: yes
  gather_facts: no
  vars:
    group:
      var1:
        - "a"
        - "b"
      var2:
        - "c"
        - "d"
    func: var1
  tasks:
    - include_role:
        name: test_role
      with_list: '{{group[func]}}'
```
## 错误捕获 
1.  ansible_failed_task.name:失败的任务名 
2.  ansible_failed_result:失败信息,类似用register获取出错的tasks信息
```yaml
tasks:
  - name: Attempt and graceful roll back demo
    block:
      - debug:
          msg: 'I execute normally'
        changed_when: yes
        notify: run me even after an error
      - command: /bin/false
    rescue:
      - name: make sure all handlers run
        meta: flush_handlers
    always:
      - debug:
          msg: "This always executes, :-)"
handlers:
  - name: run me even after an error
    debug:
      msg: 'This handler runs even on error'
```