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
parser.add_argument('-nt', '--no-tls', dest='smtp_tls', action='store_false',
                    help="Disable TLS during SMTP connection.")
parser.add_argument('--debug', dest='smtp_debug', action='store_true',
                    help='Turn on SMTP connection debuging messages.')
parser.add_argument('-r', dest='return_address',
                    help='Return address')
parser.add_argument('-d', dest='destination_address', action='append',
                    help='Destination address (Can be multiple!)')
parser.add_argument('--gmail', '-g', dest='smtp_gmail', action='store_true',
                    help='Turn on GMail mode. (overwrites -s)')
parser.add_argument('files', nargs='+',
                    help='Files to transfer')

arguments = parser.parse_args(sys.argv[1:])

smtp_debug = arguments.smtp_debug
smtp_tls = arguments.smtp_tls

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
    password = arguments.smtp_password

smtp_addr = None
if arguments.smtp_gmail:
    smtp_addr = 'smtp.gmail.com:587'
elif arguments.smtp_address == None:
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
    destaddr = COMMASPACE.join(arguments.destination_address)

filenames = arguments.files

print "Data collected."
print len(filenames), "files in queue"


def load_data_from_file(filename):
    file_pointer = open(filename, "rb")
    data = file_pointer.read()
    file_pointer.close()
    return data


def prepare_attachment(filename):
    data = load_data_from_file(filename)
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

for file_num in xrange(0, len(filenames)):
    print "(%d/%d) Sending" % (file_num+1, len(filenames)), filenames[file_num], ": ",
    sys.stdout.flush()
    message = prepare_email(fromaddr, destaddr, filenames[file_num])
    send_email(message, smtp_addr, username, password, debug=smtp_debug, tls=smtp_tls)
    print "[Done!]"
