import paramiko
import os, sys, datetime

port = 22
hosts_file = 'remote_hosts.txt'

# for循环读取所有远程服务器
def for_read_hosts(local_dir,remote_dir):
    with open(hosts_file, encoding='UTF-8') as file_object:
        contents = file_object.readlines()
    for content in contents:
        line = content.rstrip().lstrip().split(';')
        hostip = line[0]
        username = line[1]
        password = line[2]
        hostname = line[3]
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostip, username=username, password=password)
        ftp = paramiko.Transport((hostip, port))
        ftp.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(ftp)
        remote_dir_if(ssh,remote_dir)
        subdir_OR_pardir(hostip,ssh,ftp,sftp,local_dir, remote_dir)

# 判断远程目录是否存在
def remote_dir_if(ssh, remote_dir):
    remote_dir_if = 'ls -d ' + remote_dir
    stdin, stdout, stderr = ssh.exec_command(remote_dir_if)
    result = stderr.read()
    if (len(result) !=0):
        par_dir_mk = 'mkdir -p ' + remote_dir
        stdin, stdout, stderr = ssh.exec_command(par_dir_mk)

    # 判断是否需要上传父目录
def subdir_OR_pardir(hostip,ssh,ftp,sftp,local_dir,remote_dir):
    if (local_dir[-1] != '\\'):
        t = upload_file_OR_dir(local_dir)
        if ( t==local_dir ):
            upload_sub(hostip,ssh,ftp,sftp,local_dir,remote_dir)
        else:
            remote_only_file = remote_dir + t
            remote_file_if(ssh,remote_only_file,local_dir,remote_dir)
            try:
                sftp.put(local_dir,remote_only_file)
                ssh.close()
                ftp.close()
            except Exception as e:
                print(e)
    else:
        upload_par(hostip,ssh,ftp,sftp,local_dir,remote_dir)

# 判断上传的是文件还是目录
def upload_file_OR_dir(local_dir):
    if (os.path.isfile(local_dir)):
        file_only = os.path.split(local_dir)
        remote_file_only = file_only[1]
        return remote_file_only
    else:
        return local_dir

# 上传父文件夹
def upload_par(hostip,ssh,ftp,sftp,local_dir,remote_dir):
    local_dir = local_dir.rstrip('\\')
    kk = local_dir.split('\\')
    par_local_dir = kk[-1]
    remote_dir = remote_dir + par_local_dir + '/'
    print("!：判断远程目录" + remote_dir + "是否存在，存在则备份为后缀加 '_bak_时间' 的文件夹")
    remote_dir_if(ssh, remote_dir)
    upload_sub(hostip,ssh,ftp,sftp,local_dir, remote_dir)

# 上传子文件夹和文件
def upload_sub(hostip,ssh,ftp,sftp,local_dir,remote_dir):
    local_dir = local_dir.replace('\\', '/')
    remote_dir = remote_dir.replace('\\', '/')
    try:
         print("!!：判断远程目录" + remote_dir + "下文件夹和文件是否存在，存在则备份为后缀加 '_bak_时间' 的文件夹或者文件")
         sub_folders = listonlyDir_FisrtDir(local_dir)
         sub_files = listonlyFile_FirstDir(local_dir)
         for sub_folder in sub_folders:
             sub_dir_if = 'ls -d ' + remote_dir + sub_folder
             stdin, stdout, stderr = ssh.exec_command(sub_dir_if)
             result1 = stderr.read()
             if (len(result1)==0):
                 shell_dir_bak = 'mv ' + remote_dir + sub_folder.rstrip('/') + ' ' + remote_dir + sub_folder.rstrip('/') + '_bak_`date +%Y%m%d_%H%M%S`'
                 stdin, stdout, stderr = ssh.exec_command(shell_dir_bak)
                 print(stderr.read())
         for sub_file in sub_files:
             sub_file_if = 'ls -f ' + remote_dir + sub_file
             stdin, stdout, stderr = ssh.exec_command(sub_file_if)
             result2 = stderr.read()
             if (len(result2)==0):
                 shell_file_bak = 'mv ' + remote_dir + sub_file + ' ' + remote_dir + sub_file + '_bak_`date +%Y%m%d_%H%M%S`'
                 stdin, stdout, stderr = ssh.exec_command(shell_file_bak)
                 print(stderr.read())
         print('@主机' + hostip + '在 %s' % datetime.datetime.now() + ' 时刻开始上传文件')
         for root, dirs, files in os.walk(local_dir):
             for file in files:
                 local_file = os.path.join(root, file)
                 a = local_file.replace(local_dir, '')
                 remote_file = os.path.join(remote_dir, a.lstrip('\\').replace('\\', '/'))
                 try:
                     sftp.put(local_file, remote_file)
                 except Exception as e:
                     sftp.mkdir(os.path.split(remote_file)[0])
                     sftp.put(local_file, remote_file)
             for name in dirs:
                 local_path = os.path.join(root, name)
                 a = local_path.replace(local_dir, '')
                 remote_path = os.path.join(remote_dir, a.lstrip('\\').replace('\\', '/'))
                 try:
                     sftp.mkdir(remote_path)
                 except Exception as e:
                     print(e)
         print('@主机' + hostip + '在 %s' % datetime.datetime.now() + ' 时刻上传文件成功')
         ssh.close()
         ftp.close()
    except Exception as e:
        print(e)

# 判断远程文件是否存在，存在则备份
def remote_file_if(ssh,remote_only_file,local_dir,remote_dir):
    if (upload_file_OR_dir(local_dir) != local_dir):
        print("!!：判断远程目录" + remote_dir + "下的文件是否存在，存在则备份为后缀加 '_bak_时间' 的文件")
        sub_file_if = 'ls -f ' + remote_only_file
        stdin, stdout, stderr = ssh.exec_command(sub_file_if)
        result = stderr.read()
        if (len(result)==0):
            shell_file_bak = 'mv ' + remote_only_file + ' ' + remote_only_file + '_bak_`date +%Y%m%d_%H%M%S`'
            stdin, stdout, stderr = ssh.exec_command(shell_file_bak)

# 获取一级目录下的所有文件夹
def listonlyDir_FisrtDir(local_dir):
    dir_list = []
    if (os.path.exists(local_dir)):
        files = os.listdir(local_dir)
        for file in files:
            m = os.path.join(local_dir, file)
            if (os.path.isdir(m)):
                h = os.path.split(m)
                dir_list.append(h[1])
        return dir_list

# 获取一级目录下的所有文件
def listonlyFile_FirstDir(local_dir):
    file_list = []
    if (os.path.exists(local_dir)):
        all_files = os.listdir(local_dir)
        for all_file in all_files:
            n = os.path.join(local_dir, all_file)
            if (os.path.isfile(n)):
                j = os.path.split(n)
                file_list.append(j[1])
        return file_list

if __name__ == '__main__':
    print("1：注意，本地的路径最后加‘\’表示上传包括本地的路径；最后不加‘/’表示上传本地目录下的子文件夹和文件；远程的路径最后要加‘/’！！！")
    print("2：该小脚本实现从Windows或者Linux主机上传文件包括目录到linux服务器上！！！")
    print("3：请在同级目录下，新建远程主机列表文件remote_hosts.txt,每一列代表一个远程服务器")
    print("4：每一列中元素以分号';'分割，每一列的第一个填写ip，第二个填写登录用户名，第三个填写用户密码，第四个写远程主机hostname（可不填）")
    local_dir = input("☆请输入本地需要上传文件或文件夹的路径：")
    remote_dir = input("☆请输入远程需要上传的路径：")
    #local_dir = 'E:\Python\paramiko\sftp'
    #remote_dir = '/home/xudj/test/'
    for_read_hosts(local_dir,remote_dir)