# Mike Dreyfus
#purpose of script. Grab the output of /etc/home, print users who are still active
#and of those active users, print who has sudo access. Needed to audit users who have left the
#company but still had access on systems. Finding that some puppet isn't running on some boxes and 
#is not updating user access.
import csv
from pexpect import pxssh

master_access = {}  #uses list_common
master_sudo = {}  #uses sortlist
fail_list = []

try:
    with open('', 'rb') as f:
        temp_server_list = []
        temp_server_list = [str(row) for row in csv.reader(f.read().splitlines())]
    server_list = []
    for stuff in temp_server_list:
        new = stuff[2:-2]
        server_list.append([new])
except ValueError:
    print "Error: Could not open CSV."

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
        s.sendline('ls -l /home|awk \'{print $3}\'')   # Grab owner
        s.prompt()
        owner = s.before
        s.sendline('ls -l /home | awk \'{print $9}\'')  # Grab the directory name
        s.prompt()
        directory = s.before
        s.sendline('cat /etc/group| grep wheel |cut -d: -f4')  #grab users in wheel group
        s.prompt()
        sudolist = s.before
        s.sendline()

        newowner = owner.splitlines()  #parse lists to be sortable
        newdirectory = directory.splitlines()
        list_common = []  #Sorts both lists. If the owner name is in the directory name, the user exists
        for name1, name2 in zip(newowner, newdirectory):
            if name1 == name2:
                list_common.append(name1)
        sortlist = []  #Find out who has sudo access
        for user in list_common:
            if user in sudolist:
                sortlist.append(user)
        for n in list_common:                        #Adds users to dictionary as key value. If they are not in the dictionary, add them as a Key
            if n not in master_access:               #After they are in the dictionary, check if they are in the list, and if so appened the host name to them
                master_access[n] = []
            for key, value in master_access.items():
                if n == key:
                    value.append(HOST)

        print str(HOST) + " done."
        s.logout()  #End SSH session
        s.close()   #Cleans object/garbage collects
    except (AttributeError, TypeError, pxssh.ExceptionPxssh) as e:
        print "Failed on " + HOST + "... Probably because SSH failed."
        print e
        fail_list.append(HOST)

master_access.pop('', 0)  #removes blank user
print ""
print "Exporting all to CSV"   #Begin CSV export
master_fail = []
master_fail.append(fail_list)  #Adds fail list to a list to be parsed correctly by csv writer
res = master_access
csvfile = "useradit.csv"
with open('useraudit.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in master_access.items():
        writer.writerow([key] + master_access[key])
    writer.writerow("")
    writer.writerow(["I could not connect to the following hosts: "])
    writer.writerow("")
    for val in master_fail:
        for i in val:
            writer.writerow([i.rstrip()])
        #writer.writerow(''.join(val))
print ""
print "Completed."
print ""
print "I could not connect to the following hosts (they're included in the spreadsheet): "
for i in fail_list:
    print ''.join(i).rstrip()
