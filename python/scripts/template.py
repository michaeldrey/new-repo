#Mike Dreyfus

#Purpose: quick commands that I use on a regular basis.


##First started scripting using fabric. Was great to get started with but had a lot of limitations
##Also didn't know how to read from file so it was a lot of work getting an arry of 100+ vms in here
## Redacted company info/vms/etc.
from fabric.api import env, run, sudo
import argparse

parser = argparse.ArgumentParser(description='List of premade methods that can be used to run against multiple VMS')
#define passable arguements

#hosts to run command against
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')


parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))

#hosts to remove from puppet


#default


env.user = ''
env.password = ''
env.hosts=['insert hosts here,serpated by a comma']
puppetlist=['insert hosts here, seperated by a comma']
#Define commands down below

## Tail out the last 50 lines of /var/log/messages
def tailmessages():
	env.warn_only = True
	sudo('tail -n 50 /var/log/messages')

## Stops splunk
def splunkstop():
        env.warn_only = True
        sudo('service splunk stop')

## Starts splunk
def splunkstart():
        env.warn_only = True
        sudo('service splunk start')

## Checks to see what docker containers are running
def dockerverify():
        env.warn_only = True
        sudo('docker ps -a')

## Reboots VM
def restart():
       env.warn_only = True
       sudo('shutdown -r now')

## Shuts down VM
def shutdown():
       env.warn_only = True
       sudo('shutdown -h now')

## Just prints out disk space
def diskspacecheck():
        env.warn_only = True
        sudo('df -ah')

## Uses facter to find what you want.
def facter():
	env.warn_only =True
	sudo('facter -p|grep virtual')

## Kicks off a puppet run
def puppetrun():
       env.warn_only = True
       sudo('puppet agent -t')

## Enables puppet to start on boot
## Turns puppet on if it is off. Note that this will also kick off a puppet run
def puppeton():
       env.warn_only = True
       sudo('/sbin/chkconfig puppet on')
       sudo('service puppet start')

## Will patch and reboot vm
## Note that it will do a FSCHECK on reboot. Remove -F flag if you do not want this
def patchandreboot():
       env.warn_only = True
       sudo('yum -y upgrade && /sbin/shutdown -r -F now')
## Prints contents of eth0
def subnetcheck():
       env.warn_only = True
       sudo('cat /etc/sysconfig/network-scripts/ifcfg-eth0')
## Adds vms to zabbix WITH FQDN. Make sure zabbix discovery feature is enabled
#def addzabbix_rno():
#       env.warn_only = True
#       sudo('sed -i -e \'s/ServerActive=127.0.0.1/ServerActive=<IP>9/g\' /etc/zabbix/zabbix_agentd.conf && service zabbix-agent restart')

#def addzabbix_phl():
#	env.warn_only = True
#	sudo('sed -i -e \'s/ServerActive=127.0.0.1/ServerActive=<IP>/g\' /etc/zabbix/zabbix_agentd.conf && service zabbix-agent restart')
############################################
####  Adds systems to zabbix without FQDN
def addzabbix_DC2():
       env.warn_only = True
       sudo('sed -i -e \'s/ServerActive=127.0.0.1/ServerActive=<IP>/g\' /etc/zabbix/zabbix_agentd.conf && sed -i "s/# HostnameItem=system.hostname/HostnameItem=system.run[hostname -s |tr \\\'[:lower:]\\\' \\\'[:upper:]\\\']/" /etc/zabbix/zabbix_agentd.conf  && service zabbix-agent restart')

def addzabbix_DC1():
	env.warn_only = True
	sudo('sed -i -e \'s/ServerActive=127.0.0.1/ServerActive=<IP>/g\' /etc/zabbix/zabbix_agentd.conf && sed -i "s/# HostnameItem=system.hostname/HostnameItem=system.run[hostname -s |tr \\\'[:lower:]\\\' \\\'[:upper:]\\\']/" /etc/zabbix/zabbix_agentd.conf  && service zabbix-agent restart')

## Removes retired systems from puppet master
## Create a puppetlist list and add vms you want to remove to it
def removefrompuppet():
        env.user = ''
        env.password = '[::'
        env.host="puppetmaster-hostname"
        x ="DC1"
        y ="DC2"

        for i in puppetlist:
                if x in i:
                        print "puppet cert clean " + i + "DC1.FQDN"
        else:
                if y in i:
                        print "puppet cert clean " + i + "DC2.FQDN"


