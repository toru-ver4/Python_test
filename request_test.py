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

NICO_LOGIN_URL = "https://account.nicovideo.jp/login/api/v1/login"
NICO_TOP_URL = "http://www.nicovideo.jp/"

def print_cp932(in_str):
    out_str = in_str
    print(out_str)

if __name__ == '__main__':

    with open('login_info.json', 'r') as fin:
        json_data = json.load(fin)

    s = requests.Session()
    r = s.post(NICO_LOGIN_URL, data=json_data)
    r = s.get(NICO_TOP_URL)
    txt = r.text
    print(txt.find('taku-ver4'))

