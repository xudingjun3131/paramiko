from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.console import confirm

env.user = 'xudj'
env.hosts = '192.168.213.161'
env.password = '123456'

@task
@runs_once
def tar_task():
    with lcd("/root/python_work/sftp"):
        local("tar -czf sftp.tar.gz *")

@task
def put_task():
    run("mkdir -p /home/xudj/python_test")
    with cd("/home/xudj/python_test"):
        with settings(warn_only=True):
            result = put("/root/python_work/sftp/sftp.tar.gz","/home/xudj/python_test/sftp.tar.gz")
        if result.failed and not confirm("put file failed,Continue[Y/N]?"):
            abort("Aborting file put task!")

@task
def check_task():
    with settings(warn_only=True):
        lmd5 = local("md5sum /root/python_work/sftp/sftp.tar.gz",capture=True).split(' ')[0]
        rmd5 = run("md5sum /home/xudj/python_test/sftp.tar.gz").split(' ')[0]
    if lmd5==rmd5:
        print("OK")
    else:
        print("ERROR")
