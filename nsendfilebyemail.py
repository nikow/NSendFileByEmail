#!/usr/bin/env python

import sys
from smtplib import SMTP
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from getpass import getpass
import argparse

__author__ = 'nikow'
COMMASPACE = ', '

parser = argparse.ArgumentParser(description='Sending multiple files by multiple e-mails.')
parser.add_argument('-s', dest='smtp_address',
                    help='SMTP address')
parser.add_argument('-u', dest='smtp_username',
                    help='SMTP username')
parser.add_argument('-p', dest='smtp_password',
                    help='SMTP password')
parser.add_argument('-r', dest='return_address',
                    help='Return address')
parser.add_argument('-d', dest='destination_address', action='append',
                    help='Destination address (Can be multiple!)')
#parser.add_argument('--debug', action='store_true',
#    help='Turn on debug.')
#parser.add_argument('--gmail', '-g', action='store_true',
#    help='Turn on GMail mode.')
parser.add_argument('files', nargs='+',
                    help='Files to transfer')

arguments = parser.parse_args(sys.argv[1:])

#Sender
fromaddr = None
if arguments.return_address == None:
    print "Insert your e-mail address:"
    fromaddr = sys.stdin.readline()[:-1]#"youremail"
else:
    fromaddr = arguments.return_address

username = None
if arguments.smtp_username == None:
    print "Insert your username:"
    username = sys.stdin.readline()[:-1]#"youruser"
else:
    username = arguments.smtp_username

password = None
if arguments.smtp_password == None:
    password = getpass("Insert your password:\n")#"yourpassword"
else:
    password = smtp_password

smtp_addr = None
if arguments.smtp_address == None:
    print "Insert SMTP adress:"
    smtp_addr = sys.stdin.readline()[:-1]#"smtp_address"
else:
    smtp_addr = arguments.smtp_address

#Destination
destaddr = None
if arguments.destination_address == None:
    print "Insert destination adress:"
    destaddr = sys.stdin.readline()[:-1]#sys.argv[1]
else:
    destaddr = arguments.destination_address

print "Data collected."


def load_file(filename):
    file_pointer = open(filename, "rb")
    data = file_pointer.read()
    file_pointer.close()
    return data


def prepare_attachment(filename):
    data = load_file(filename)
    attachment = MIMEBase("application", "octet-stream")
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


def send_email(message, smtp_address, username, password, tls=True, debug=False):
    server = SMTP(smtp_address)
    server.set_debuglevel(debug)
    if tls:
        server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, destaddr, message.as_string())
    server.quit()


print "Prepared to send messages..."

for filename in arguments.files:
    print "Sending", filename, ": ",
    sys.stdout.flush()
    message = prepare_email(fromaddr, destaddr, filename)
    send_email(message, smtp_addr, username, password)
    print "[Done!]"
