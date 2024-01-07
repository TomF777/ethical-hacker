#!/usr/bin/env python

import smtplib, ssl
from email.mime.text import MIMEText


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


send_email("tommy1978@wp.pl", "***", " new version 2 of script")