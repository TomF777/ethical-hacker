#!/usr/bin/env python

"""
Ver: Python3

it finds all paths (files and folders) in Website
"""

import requests

def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass

#target_url = "google.com"
target_url = "192.168.1.101/mutillidae/"
with open("files-and-dirs-wordlist.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        test_url = target_url + "/" + word
        #print(test_url)
        response = request(test_url)
        if response:
            print(" Discovered URL: " + test_url)
        else:
            pass
