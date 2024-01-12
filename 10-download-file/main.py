#!/usr/bin/env python

"""
Ver: Python3
"""

import requests

def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    print(file_name)
    # write to binary file
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


download("https://www.powertrafic.fr/wp-content/uploads/2023/04/image-ia-exemple.png")


