import paramiko
import datetime
import os

hostname = '200.31.154.124'
username = 'xudj'
password = 'xudj'
port = 22



def upload(local_dir,remote_dir):
    local_dir = local_dir.replace('\\','/')
    remote_dir = remote_dir.replace('\\','/')
    try:
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname=hostname, username=username, password=password)
        print("3：判断远程目录" +remote_dir+"是否存在，存在则备份为后缀加_bak_时间的文件夹")
        dir_if = 'ls -d ' + remote_dir
        stdin, stdout, stderr = s.exec_command(dir_if)
        result = stdout.read()
        if result is not None:
            shell_dir_bak = 'mv ' + remote_dir.rstrip('/') + ' ' + remote_dir.rstrip('/') +'_bak_`date +%Y%m%d_%H%M%S`'
            stdin, stdout, stderr = s.exec_command(shell_dir_bak)
        shell_cmd = 'mkdir -p ' + remote_dir
        stdin, stdout, stderr = s.exec_command(shell_cmd)
        print(stdout.read())
        s.close()
        t = paramiko.Transport((hostname,port))
        t.connect(username=username,password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        print('upload file start at %s ' % datetime.datetime.now())
        for root,dirs,files in os.walk(local_dir):
            for file in files:
                local_file = os.path.join(root,file)
                a = local_file.replace(local_dir,'')
                remote_file = os.path.join(remote_dir,a.lstrip('\\').replace('\\','/'))
                try:
                    sftp.put(local_file,remote_file)
                except Exception as e:
                    sftp.mkdir(os.path.split(remote_file)[0])
                    sftp.put(local_file,remote_file)
            for name in dirs:
                local_path = os.path.join(root,name)
                a = local_path.replace(local_dir,'')
                remote_path = os.path.join(remote_dir,a.lstrip('\\').replace('\\','/'))
                try:
                    sftp.mkdir(remote_path)
                except Exception as e:
                    print(e)
        print('upload file success at %s ' % datetime.datetime.now())
        t.close()
    except Exception as e:
        print(e)

if __name__=='__main__':
    print("1：注意，local_dir的路径最后不加\或者/；remote_dir的路径最后要加/。。。")
    print("2：该小脚本实现从Windows或者Linux上上传文件包括目录到linux服务器上！！！")
    local_dir = 'E:\Python\paramiko\zabbix_import'
    remote_dir = '/home/xudj/paramiko/python/zabbix_import/'
    upload(local_dir,remote_dir)