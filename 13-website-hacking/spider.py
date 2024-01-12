#!/usr/bin/env python


"""
Ver: Python3

it extracts useful data (links) from  a website
"""

import requests
import re
import urllib.parse

target_url = "http://192.168.1.101/mutillidae/"
# target_url = "https://zsecurity.org"
target_links = []


def extract_links_from(url):
    response = requests.get(url)
    href_links = re.findall('(?:href=")(.*?)"', response.content.decode(encoding='utf-8', errors="ignore"))
    return href_links
    # return response.content.decode


def crawl(url):
    links = extract_links_from(url)
    for link in links:
        # convert relative links to full links
        link = urllib.parse.urljoin(url, link)

        if "#" in link:
            link = link.split("#")[0]

        # ignore links which are not from a target website and take only unique links
        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link)


crawl(target_url)
