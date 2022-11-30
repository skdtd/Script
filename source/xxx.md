# 页面(h5, js, nginx)
* 登录
> POST `login`
>> request
>> ```json
>> {
>>     "username": "username",
>>     "password": "password"
>> }
>> ```
>> response
>>> success
>>> ```json
>>> "OK"
>>> ```
>>> failed
>>> ```json
>>> "NG"
>>> ```
* 执行指令(指令选择)
> POST `exec`
>> request
>> ```json
>> {
>>     "exec": "cmd",
>>     "args": [
>>         "a",
>>         "b",
>>         "c"
>>     ],
>>     "kwargs":{
>>         "A": "1",
>>         "B": "2",
>>         "C": "3"
>>     }
>> }
>> ```
>> response
>>> success
>>> ```json
>>> "OK"
>>> ```
>>> failed
>>> ```json
>>> "NG"
>>> ```
* 查看各节点状态(内存,cppu占用,指定程序运行状态)
> GET `status`
>> response
>>> success
>>> ```json
>>> {
>>>     "nodes": [
>>>         {
>>>             "nodename": "a",
>>>             "memory_used": "1024",
>>>             "memory_max": "10240",
>>>             "cpu": "50"
>>>         }
>>>     ]
>>> }
>>> ```
>>> failed
>>> ```json
>>> "NG"
>>> ```
<!-- * 查看各节点当前屏幕(截取当前屏幕) -->
* 查看单节点屏幕
>> POST `screen`
>> response
>>> success
>>> ```json
>>> "OK"
>>> ```
>>> failed
>>> ```json
>>> "NG"
>>> ```
* 查看节点运行记录
> GET `node_history`
>> response
>>> success
>>> ```json
>>> {
>>>     "node": "::1",
>>>     "date": "2022/01/02",
>>>     "timestamp": "20:20:20:020",
>>>     "operation": "cmd",
>>>     "arguments": "a,b,c",
>>>     "result" : "OK"
>>> }
>>> ```
>>> failed
>>> ```json
>>> "NG"
>>> ```
* 查看报警记录
> GET `alert_history`
>> response
>>> success
>>> ```json
>>> {
>>>     "node": "::1",
>>>     "date": "2022/01/02",
>>>     "timestamp": "20:20:20:020",
>>>     "alert": "disconnection",
>>>     "content": "掉线"
>>> }
>>> ```
>>> failed
>>> ```json
>>> "NG"
>>> ```
* 添加/删除命令集
> POST ``
>> request
>> ```json
>>{
>>    "operation": "add",
>>    "exec": "screenshot",
>>    "argument_count": 1,
>>    "generate_file": "c:\\result",
>>}
>> ```
>> response
>>> success
>>> ```json
>>> "OK"
>>> ```
>>> failed
>>> ```json
>>> "NG"
>>> ```
* 传送/删除文件
> POST `file`
>> request
>> ```json
>> {
>>    "operation": "add",
>>    "node": ["a", "b"],
>>    "file_num": 3,
>>    "target_dir": "c:\\files"
>> }
>> ```
>> response
>>> success
>>> ```json
>>> "OK"
>>> ```
>>> failed
>>> ```json
>>> "NG"
>>> ```

# 服务端(python | rust)
## [redis](https://docs.rs/redis/latest/redis/), [h2](https://docs.rs/h2/latest/h2/), [RPC](https://crates.io/search?q=axum)
* 管理员登陆(h2, redis)
* 各节点死活监视(redis)
* [操作记录(h2)](https://crates.io/crates/log)
* 用户管理(h2)
* 转发来自页面的指令到指定客户端,并接受返回消息(server)
* 命令集管理(h2)
* 更新缓存(redis)

# 客户端(python | rust)
* 开机自启动(本地功能)
* 向服务端发送心跳
* 向服务端报警
* 接受来自服务端的文件
* 记录执行日志
* 接受并执行服务端的指令,并返回消息(所有指令以子文件形式存在)