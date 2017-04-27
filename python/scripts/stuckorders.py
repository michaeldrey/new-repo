##Purpose of this script: This script will check to see if 
##there are orders that are stuck in UO/FP/AN queue
##Currently it will check every 30 minutes for stuck orders..
##It will check of submitted orders that are 30 mins or older. If it finds
##Stuck orders it will email the orders that are stuck out to the team.

##Author: Mike Dreyfus
##Last Updated: 4/27/17

##Will add pagerduty API integration after testing with email

# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# Import datetime to do simple comparisions (I dont think we need this)
import datetime
# Import Oracle module to open the connection to the DB
import cx_Oracle
##To be implemented
# Import pagerduty api module
#import pygerduty
#pager = pygerduty.PagerDuty()
#pager.trigger_incident

#######################################################################
# Create connection to database

#Connection strings to DBs. Using readonly accts
connectstrings = []
#Create dictionary for orders that are stuck. Key: Brand Value: Order
stucklist ={}
for j in connectstrings:
    try:
        connectionstring = j[0]
#   create connection object
        con = cx_Oracle.connect(connectionstring)
#   execute SQL query using execute() method.
        cursor = con.cursor()
#   Build the query since each table is slighty different
        query = 'SELECT ORDER_ID, SUBMITTED_DATE FROM '+j[1]+' WHERE (state=\'SUBMITTED\' OR state=\'RESUBMIT_TO_EMS\') ORDER BY submitted_date DESC'
        cursor.execute(query)
#   use fetchall() method to fetch multiple rows and store the result in a list variable.
        data = cursor.fetchall()
#   Close the cursor since we do not need it anymore.
        cursor.close()
#   disconnect from server.
        con.close()
##########################################################################
# check the delta on the datetime with the current time-30 minutes.
# If it's greater than 30 mins, we have a stuck order
        for i in data:
            #generates a time delta that we will use to see if the order is in fact stuck
            m = datetime.datetime.now() - datetime.timedelta(minutes=30)
            #if the time 30 minutes ago is "greater"/ more recent than the order's, then the order is stuck
            if m > i[1]:
            #order is stuck. Now we grab the order and which brand/dc and add it to the dictionary
                stuckcontent = []
                key = j[2].strip()
                stucklist.setdefault(key, stuckcontent)
                stucklist[key].append(i[0].strip())

    except Exception as e: 
        #print "Failed on " + j[0]
        print e
##########################################################################################
# begin parsing email into a list so it can be converted into a string. We do this because
# you cannot encode lists/dict. Doing it this way also puts the orders together so they can 
# be copied and pasted easily
if stucklist: 
    parselist = []
    for x in stucklist:
        parselist.append('\n'+x+': ')
        tmp = ",".join([str(y) for y in stucklist[x]])
        parselist.append(tmp)
    str1 = ''.join(parselist)
    # Build the email header
    me= "ALERT"
    you = "TeamEmail@email.com"
    msg = MIMEMultipart()
    msg['From'] = me
    msg['To'] = you
    msg['Subject'] = "THERE ARE STUCK ORDERS"
#Create the body of the email to be sent
    text = 'These orders have been in the queue for more than 30 minutes and may need to be resubmitted (if it\'s a ton of orders you might be better off restarting the service):\
        \n' + str1 + '\n\n Copy and paste the order(s) to the appropiate Link. The links are below: \n \
        \n FP Order Resubmit \n\
    (PHL) <Link> \n\
    (RNO) <Link> \
    \n ANTHRO Order Resubmit\n\
    (PHL) <Link> \n\
    (RNO) <Link> \
    \n UO Order Resubmit\n\
    (PHL) <Link> \n\
    (RNO) <Link> \n\
    \n\n For more information see <Link>'

#Encode our body, attach the message and send
    part1 = MIMEText(text, 'plain')
    msg.attach(part1)
    s = smtplib.SMTP('localhost')
    s.sendmail(me, [you], msg.as_string())
    s.quit()
