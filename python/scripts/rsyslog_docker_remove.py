## Mike Dreyfus
## Purpose of script: Removes docker conf file in rsyslog, restarts rsyslog and then removes the docker.log. How the conf is configured is causing all daemon.* logging to goto docker.log.

import csv
import mmap
import re
from pexpect import pxssh

fail_list = []

##Reads from CSV file
try:
    with open('testfile.csv', 'rb') as f:
        temp_server_list = []
        temp_server_list = [str(row) for row in csv.reader(f.read().splitlines())]
    server_list = []
    for stuff in temp_server_list:
        new = stuff[2:-2]
        server_list.append([new])
except ValueError:
    print "Error: Could not open CSV."

##Logs into the server and executes bash script
for i in server_list: 
    HOST = ' '.join(i).rstrip()
    print "Trying: " + HOST
    s = pxssh.pxssh()
    try:
        username = ""
        password = ""
        s.timeout = 5
        s.login(HOST, username, password)
        print "Login successful!"
        #Check if splay is already there
        s.sendline('sudo su')
        s.prompt
        print s.before
        s.sendline('if sudo find /etc -iname "10-docker.conf";then sudo rm -f /etc/rsyslog.d/10-docker.conf && sudo systemctl restart rsyslog && sudo rm -f /var/log/docker.log;fi')
        s.prompt()
        owner = s.before
        print owner
    except (AttributeError, TypeError, pxssh.ExceptionPxssh) as e:
        #Keep track of hosts the script failed on
        print "Failed on " + HOST + "... Probably because SSH failed."
        print e
        fail_list.append(HOST)
print ""
print "Completed."
print ""
print "I could not connect to the following hosts: "
##Print hosts that it failed to connect to
for i in fail_list:
    print ''.join(i).rstrip()
