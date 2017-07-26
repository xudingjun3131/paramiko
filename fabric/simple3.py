from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.console import confirm

env.user = 'root'
env.gateway = '192.168.213.161'
env.hosts = '192.168.213.161'

env.passwords = {
    'root@192.168.213.161:22': '123456',
    'xudj@192.168.213.161:22': '123456',
    'amber@192.168.213.161:22': '123456'
}

lpackpath = 'E:\Python\paramiko_work\sftp'
rpackpath = '/tmp/'