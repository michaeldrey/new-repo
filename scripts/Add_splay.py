# Mike Dreyfus
#purpose of script: Add splay to the bottom of the puppet.conf file. If it is a proxy server it will 
#set the runinterval to 300 ms. Found that the majority of hosts created did not have this option set 
#in the puppet conf. Because of this we are seeing a stampede of hosts checking in at the same time. This
#causes CPU to spike significantly on our puppet master.

import csv
import mmap
import re
from pexpect import pxssh

fail_list = []

##Reads from CSV file
try:
    with open('testlist.csv', 'rb') as f:
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
 #removed check for proxy for now. 
 #       if HOST.find('proxy') > -1:  ## checks whether it's a proxy server or not and if it is will set runinterbal instead of splay
##Since it's pexpect you have to send bash. This is a quick if statement to check for spaly
        s.sendline('if ! sudo grep -q -i splay \'/etc/puppet/puppet.conf\' && ! sudo grep -q -i runinterval \'/etc/puppet/puppet.conf\'; then sudo echo \"       splay           = true\" >> /etc/puppet/puppet.conf; fi')
   #     else:
      #      s.sendline('if ! sudo grep -q -i splay \'/etc/puppet/puppet.conf\'; then sudo echo \"       runinterval     = 300\" >> /etc/puppet/puppet.conf; fi')
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
