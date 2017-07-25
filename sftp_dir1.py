import paramiko

import datetime

import os


hostname = '200.31.154.124'
username = 'xudj'
password = 'xudj'
port = 22

def upload(local_dir,remote_dir):
    try:
        t = paramiko.Transport((hostname,port))
        t.connect(username=username,password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        print('upload file start %s ' % datetime.datetime.now())
        for root,dirs,files in os.walk(local_dir):
            print('[%s][%s][%s]' % (root,dirs,files))
            for filespath in files:
                local_file = os.path.join(root,filespath)
                print(11,'[%s][%s][%s][%s]' % (root,filespath,local_file,local_dir))
                a = local_file.replace(local_dir,'').replace('\\','/').lstrip('/')
                print('01',a,'[%s]' % remote_dir)
                remote_file = os.path.join(remote_dir,a)
                print(22,remote_file)
                try:
                    sftp.put(local_file,remote_file)
                except Exception as e:
                    s = paramiko.SSHClient()
                    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    s.connect(hostname=hostname,username=username,password=password)
                    shell_cmd = 'mkdir -p '+ remote_dir
                    stdin,stdout,stderr = s.exec_command(shell_cmd)
                    #sftp.mkdir(os.path.split(remote_file)[0])
                    s.close()
                    sftp.put(local_file,remote_file)
                    print("66 upload %s to remote %s" % (local_file,remote_file))
            for name in dirs:
                local_path = os.path.join(root,name)
                print(0,local_path,local_dir)
                a = local_path.replace(local_dir,'').replace('\\','')
                print(1,a)
                print(1,remote_dir)
                remote_path = os.path.join(remote_dir,a)
                print(33,remote_path)
                try:
                    sftp.mkdir(remote_path)
                    print(44,"mkdir path %s" % remote_path)
                except Exception as e:
                    print(55,e)
        print('77,upload file success %s ' % datetime.datetime.now())
        t.close()
    except Exception as e:
        print(88,e)

if __name__=='__main__':
    local_dir = 'E:\Python\paramiko\zabbix_import'
    remote_dir = '/home/xudj/python/zabbix_import/'
    upload(local_dir,remote_dir)