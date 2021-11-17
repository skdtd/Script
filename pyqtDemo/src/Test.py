import paramiko

sc = paramiko.SSHClient()
sc.connect('192.168.100.102',22,'root',pkey='C:/Users/zhaozhiy/.ssh/id_rsa')
sc.set_missing_host_key_policy(paramiko.AutoAddPolicy())
stdin, stdout, stderr = sc.exec_command('ls')
print(stdout.read())
print(stderr.read())
sc.close()