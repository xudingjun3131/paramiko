from paramiko import *
import os
class ExportPrepare(object):
    def __init__(self):
       pass

    def sftp_con(self):
        t = Transport((self.ip,self.port))
        t.connect(username=self.username,password=self.password)
        return t

    # 找到所有你要上传的目录以及文件
    def __get_all_files_in_local_dir(self,local_dir):
        all_files = list()

        if os.path.exists(local_dir):
            files = os.listdir(local_dir)
            for x in files:
                filename = os.path.join(local_dir,x)
                print("filename:"+ filename)
                # isdir
                if os.path.isdir(filename):
                    all_files.extend(self.__get_all_files_in_local_dir(filename))
                else:
                    all_files.append(filename)
        else:
            print('{}does not exist'.format(local_dir))
        return all_files
    # Copy a local file (localpath) to the SFTP server as remotepath
    def sftp_put_dir(self):
        try:
    # 本地test目录上传到远程目录下
    local_dir = "E:/Python/paramiko/zabbix_import"
    remote_dir = '/home/xudj/python/zabbix_import'
        t = self.sftp_con()
        sftp = SFTPClient.from_transport(t)
        # sshclient
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(self.ip,port=seif.port,username=self.username,password=self.password,compress=True)
        ssh.exec_command('rm -rf ' + remote_dir)
        if remote_dir[-1]=='/';
            remote_dir = remote_dir[0:-1]
        all_files = self.__get_all_files_in_local_dir(local_dir)
        for x in all_files:
            filename = os.path.split(x)[-1]
            remote_file = os.path.split(x)[0].replace(local_dir,remote_dir)
            path = remote_file.replace('\\','/')
            stdin,stdout,stderr = ssh.exec_command('mkdir -p '+ path)
            print(stderr.read())
            remote_filename = path + '/' + filename
            sftp.put(x,remote_filename)
        ssh.close()
    except Exception,e:
        print(e)
if __name__ == '__main__':
    export_prepare = ExportPrepare()
    export_prepare.sftp_put_dir()