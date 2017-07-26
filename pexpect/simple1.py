import pexpect
import sys
child = pexpect.spawnu('ssh root@192.168.213.161')
fileout = file('mylog.txt','w')
#child.logfile = fileout
child.logfile = sys.stdout

child.expect("Password:")
child.sendline("123456")
child.expect('#')
child.sendline('ls /home')
child.expect('#')