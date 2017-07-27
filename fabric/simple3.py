from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.console import confirm

env.user = 'xudj'
env.gateway = '192.168.213.161'
env.hosts = '192.168.213.161'
env.password = '123456'

env.passwords = {
    'zabbix@192.168.213.161:22': 'zabbix',
}

lpackpath = "/home/xudj/test/sftp.tar.gz"
rpackpath = "/home/zabbix"

@task
def put_task():
    run("mkdir -p /home/zabbix")
    with settings(warn_only=True):
        result = put(lpackpath,rpackpath)
    if result.failed and not confirm("put file failed,Continue[Y/N]?"):
        abort("Aborting file put task!")

@task
def run_task():
    with cd("/home/zabbix"):
        run("tar -zxvf sftp.tar.gz")
        with cd("zabbix/"):
            run("./start.sh")

@task
def go():
    put_task()
    run_task()