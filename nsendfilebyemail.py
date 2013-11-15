import os
import sys
from smtplib import SMTP
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

__author__ = 'nikow'
COMMASPACE = ', '

#Sender
fromaddr = "youremail"
username = "youruser"
password = "yourpassword"
smtp_addr = "smtp_address"

#Receiver
recvaddr = sys.argv[1]

def load_file(filename):
    file_pointer = open(filename, "rb")
    data = file_pointer.read()
    file_pointer.close()
    return data

def prepare_attachment(filename):
    data = load_file(filename)
    attachment = MIMEBase("application","octet-stream")
    attachment.set_payload(data)
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename=filename)
    return attachment

def prepare_email(fromaddr, recvaddr, filename):
    message = MIMEMultipart()
    message['Subject'] = filename
    message['To'] = recvaddr
    message['From'] = fromaddr

    attachment = prepare_attachment(filename)
    message.attach(attachment)
    return message

def send_email(message, smtp_address, username, password, debug=False):
    server = SMTP(smtp_address)
    server.set_debuglevel(debug)
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, recvaddr, message.as_string())
    server.quit()

for filename in sys.argv[2:]:
    print "Sending", filename,": ",
    message = prepare_email(fromaddr, recvaddr, filename)
    send_email(message, smtp_addr, username, password)
    print"[Done!]"
