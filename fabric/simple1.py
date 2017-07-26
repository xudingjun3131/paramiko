from fabric.api import *
env.user = 'root'
env.hosts = 'localhost'
env.password = '123456'

@runs_once
def local_task():
    local("ver")

def remote_task():
    with cd("/home/"):
        run("ls -l")