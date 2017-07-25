import paramiko

hostname = '172.19.192.221'
username = 'xudj'
password = 'xudj'
paramiko.util.log_to_file('syslogin.log')  # 发送paramiko日志到syslogin.log文件
ssh = paramiko.SSHClient() # 创建一个ssh客户端client对象
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 获取客户端host_keys，默认 ~/.ssh/known_hosts，非默认路径需指定
ssh.connect(hostname=hostname,username=username,password=password) # 创建ssh连接
stdin,stdout,stderr=ssh.exec_command('free -m') # 调用远程执行命令方法exec_commmand()
print(stdout.read()) # 打印命令执行结果，得到Python列表形式，可以使用stdout.readlines()
ssh.close()
