#Quick script to run rsync
##logs in and uses ssh key to rsync to mirror system in another datacenter. redacked company info such as vm names
###Ended up writing a bash script for this and set it as a cron job
from pexpect import pxssh
HOST = "<hostname>"
s = pxssh.pxssh()
try:
    username = "root"
    password = ""
    s.timeout = 5
    s.login(HOST, username, ssh_key='/root/.ssh/id_rsa')
    print "Login successful!"
    s.sendline('rsync -av --bwlimit=200000 /repo/srv <hostname>:/repo/srv')   #
    s.prompt()
    owner = s.before
    print owner
except (AttributeError, TypeError, pxssh.ExceptionPxssh) as e:
    print "Failed on " + HOST + "... Probably because SSH failed."
