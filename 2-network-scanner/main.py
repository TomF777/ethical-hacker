#!/usr/bin/env python

"""
this program scans given network target

format for calling the program:
sudo python3 main.py -t IP_ADDRESS
sudo python3 main.py --target IP_ADDRESS

-t --target: IP range to scan e.g. 192.168.1.1/24
"""

import scapy.all as scapy
import argparse


def get_argument():
    """
    Get user arguments which were passed with app call

    :return: IP address
    """
    # create parser object
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--target", dest="ip_target", help=" target IP / IP range")

    # parsing of user input
    options = parser.parse_args()

    if not options.ip_target:
        # error handler
        parser.error([" Specify the target IP range "])
    return options


def scan(ip):
    # scapy.arping(ip)

    # send arp request
    arp_request = scapy.ARP(pdst=ip)

    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    arp_request_broadcast = broadcast / arp_request

    answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]

    clients_list = []

    for idx in answered_list:
        client_dict = {"ip": idx[1].psrc, "mac": idx[1].hwsrc}
        clients_list.append(client_dict)

    return clients_list


def print_result(results_lists):
    print("IP\t\t\t MAC Address \n ---------------------------------------")
    for client in results_lists:
        print(client["ip"] + "\t\t" + client["mac"])


# get argument from app call command (IP range)
options = get_argument()

scan_result = scan(options.ip_target)
print_result(scan_result)
