from paramiko import *
t = Transport(("172.19.192.221",22))
t.connect(username="xudj",password="xudj")
sftp = SFTPClient.from_transport(t)
localpath = 'E:\Python\paramiko\zabbix_import'
remotepath = '/home/xudj/python/zabbix_import'
sftp.put(localpath,remotepath)