# !/usr/bin/env python

"""
this program changes mac address of given NIC.
format for calling the program:
sudo python3 main.py -i ens33 -m 00:99:22:88:33:77

-i --interface: name of NIC
-m --mac: new mac address
"""

import subprocess
import optparse
import re


def get_arguments():
    """
    Get user arguments which were passed with app call

    :return: interface name and desired mac address
    """
    # create parser object
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="eth_interface", help=" Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="eth_new_mac", help=" New MAC address")

    # parsing of user input
    (options, arguments) = parser.parse_args()

    if not options.eth_interface:
        # error handler
        parser.error([" Specify an interface "])
    elif not options.eth_new_mac:
        # error handler
        parser.error([" Specify an new mac address "])
    return options


def change_mac(interface, new_mac):
    """
    Change MAC address for given NIC interface

    :param interface: NIC interface name
    :param new_mac:   desired MAC address
    :return:
    """
    print(f" Changing MAC address for {interface} to {new_mac}")

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    """
    Read MAC address from given NIC interface

    :param interface: NIC interface name
    :return:
    """
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print(" Could not read MAC address")


# get arguments from app call command (interface name , new mac address)
options = get_arguments()

# read current MAC address
current_mac = get_current_mac(options.eth_interface)
print(f"current MAC: {current_mac}")

# change MAC address to new one
change_mac(options.eth_interface, options.eth_new_mac)

# read MAC address after change
current_mac = get_current_mac(options.eth_interface)

if current_mac == options.eth_new_mac:
    print(f" MAC address successfully changed to {current_mac}")
else:
    print(" MAC address was not changed")

