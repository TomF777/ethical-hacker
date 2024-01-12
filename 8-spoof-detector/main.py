#!/usr/bin/env python

"""
Ver: Python3

It reads all traffic flowing through given interface  sniff("eth0")
Start the app and generate some traffic by calling a webpage to see traffic capture
It captures user logging data from not secured (http) webpages like:  http://testphp.vulnweb.com/login.php
"""


import scapy.all as scapy


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    # iface: hw interface,  store: store data in memory, prn: call back function

def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc
            print(packet.show())
            if real_mac != response_mac:
                print (" ARP spoofing is active !!! ")
        except IndexError:
            pass


sniff("eth0")
