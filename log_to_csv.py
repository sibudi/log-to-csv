#!/usr/bin/python

import glob
import os
import smtplib
from datetime import date, timedelta
from email.mime.text import MIMEText


yesterday = date.today() - timedelta(1)
directory = "/Users/sty/"
filename = "read_cdr_*_" + yesterday.strftime('%Y%m%d') + ".log"
logfile = "/tmp/email.log"

sender = "setiyabudi@xxx.com" # only need 1 email address
# separate email address receivers with a space only
receivers = "xxx@xxx.com xxx@yyy.com"
SMTPSERVER = "10.0.0.117" # webmail2.smartfren.com



open(logfile, 'w').close() #empty file log
file = glob.glob(os.path.join(directory, filename))
if file:
    for file_name in file:
        with open(file_name, "r") as fp:
            for line in fp:
                file_name = os.path.basename(file_name)
                
                if 'Start Load' in line:
                    #20150501|sby|23|2015-05-07 00:34:46|395367|2015-05-07 00:37:46
                    var = file_name[13:-4] + "|" + file_name[9:12] + "|" + line[14:16] + "|" + line[19:-1] + "|"

                if 'INSERT' in line:
                    var += line.split()[2] + "|"

                a = ['ERROR', 'error', 'command']
                if any(x in line for x in a): #if all the strings from the list are found, use all instead of any
                    var += "|"

                if 'END Load' in line:
                    var += line[17:-1]
                    #print ''.join(var.splitlines()) #remove whitespaces
                    print var
                    
                    with open(logfile, "a") as fp:
                        fp.write(var + "\n")

# read from file, then sent to mail
with open ("/tmp/email.log", "r") as myfile:
    data = myfile.read()

receivers = receivers.split()

msg = MIMEText(data)
msg['Subject'] = "CDR Log"
msg['From'] = sender
msg['To'] = ", ".join(receivers)
"""
try:
    smtpObj = smtplib.SMTP(SMTPSERVER.split(' ')[0])
    smtpObj.sendmail(sender, receivers, msg.as_string())         
    print "Successfully sent email"
        
except smtplib.SMTPException:
    print "Error: unable to send email"
"""
