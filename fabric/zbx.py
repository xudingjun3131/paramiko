import  os,sys
from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.console import confirm

hosts_file = 'remote_zbx_hosts.txt'

with open(hosts_file, encoding='UTF-8') as file_object:
    contents = file_object.readlines()
    env.passwords = {}
    for content in contents:
        line = content.rstrip().lstrip().split(';')
        key = line[1]+'@'+line[0]+':22'
        value = line[2]
        env.passwords[key] = value

local_path = 'E:\Python\paramiko_work\sftp\zabbix.tar.gz'
remote_path = '/home/zabbix/zabbix.tar.gz'

@task
def for_read_hosts():
    with open(hosts_file, encoding='UTF-8') as file_object:
        contents = file_object.readlines()
        for content in contents:
            line = content.rstrip().lstrip().split(';')
            hostsname= line[3]
            run("mkdir -p /home/zabbix")
            with cd("/home/zabbix"):
                with settings(warn_only=True):
                    result = put(local_path, remote_path)
                    if result.failed and not confirm("put file failed,Continue[Y/N]?"):
                        abort("Aborting file put task!")
                run("tar -zxvf " + remote_path)
                with cd("zabbix"):
                    conf_modify = "sed -ri 's/FEEIMT_UATA_APP1/" + hostsname + "/g' ./conf/zabbix_agentd.conf"
                    run(conf_modify)
                    run("sh start.sh")

#if __name__ == '__main__':
#    print("1：注意，本地的路径最后加‘\’表示上传包括本地的路径；最后不加‘/’表示上传本地目录下的子文件夹和文件；远程的路径最后要加‘/’！！！")
#    print("2：该小脚本实现从Windows或者Linux主机上传文件包括目录到linux服务器上！！！")
#    print("3：请在同级目录下，新建远程主机列表文件remote_hosts.txt,每一列代表一个远程服务器")
#    print("4：每一列中元素以分号';'分割，每一列的第一个填写ip，第二个填写登录用户名，第三个填写用户密码，第四个写远程主机hostname（可不填）")
#    #local_path = input("☆请输入本地需要上传文件或文件夹的路径：")
#    #remote_path = input("☆请输入远程需要上传的路径：")
#    local_path = 'E:\Python\paramiko_work\sftp\zabbix.tar.gz'
#    remote_path = '/home/zabbix/zabbix.tar.gz'
#    for_read_hosts(local_path,remote_path)