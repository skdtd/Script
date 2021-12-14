> 查看所有已经安装的磁盘
>> fdisk –l
>
> 添加分区
>> fdisk /dev/sdb</br>
>> 输入n,p,1,直到最后w退出
>
> 格式化分区
>> mkfs -t ext4 -c /dev/sdb1</br>
>> -t指定分区类型, -c检查坏道(新磁盘可以省略)
>
> 创建挂载目录
>> mkdir /disk
>
> 添加永久挂载
>> echo "/dev/sda1 /ssd ext4 defaults 0 0" >> /etc/fstab
>
> 使挂载文件生效
>> mount -a