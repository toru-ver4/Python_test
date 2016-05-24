#!/usr/bin/env python3
#-*- coding: utf-8 -*-
 
"""
test for request module.
"""

import os
import sys
import time
import json
import requests
from selenium import webdriver
from bs4 import BeautifulSoup

NICO_LOGIN_URL = "https://account.nicovideo.jp/api/v1/login?site=niconico&next_url="
NICO_TOP_URL = "http://www.nicovideo.jp/"

def print_cp932(in_str):
    out_str = in_str
    print(out_str)

if __name__ == '__main__':

    with open('login_info.json', 'r') as fin:
        json_data = json.load(fin)

    s = requests.Session()
    driver = webdriver.PhantomJS()
    driver.get("https://account.nicovideo.jp/login")
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "lxml")
    auth_token = soup.find(attrs={'name': 'auth_id'}).get('value')
    print(auth_token)
#    json_data['auth_id'] = str(auth_token) # it is not needed... OMG.
    r = s.post(NICO_LOGIN_URL, data=json_data)
    print(r.text.find('taku-ver4'))

