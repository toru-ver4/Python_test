#!/usr/bin/env python3
#-*- coding: utf-8 -*-
 
"""
test for request module.
"""

import os
import sys
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import pandas

def exec_beautifulsoup_sample():

    try:
        html = urlopen("http://www.pythonscraping.com/pages/page1.html")
    except HTTPError as e:
        print(e)
    except URLError as e:
        print("The server could not be found!")
    else:
        bsObj = BeautifulSoup(html.read(), 'lxml')
        print(bsObj.h1)


def getTitle(url):
    """try, except をきちんと書いてプログラムが止まらないように"""
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        return None
    try:
        bsObj = BeautifulSoup(html.read(), 'lxml')
        title = bsObj.body.h1
    except AttributeError as e:
        return None

    return title


def getSiteHTML(url):
    """HTMLを BeautifulSoup オブジェクトとして取得する"""
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        return None
    except URLError as e:
        print("The server could not be found!")
        return None
    else:
        bsObj = BeautifulSoup(html, 'lxml')

    return bsObj


def get_garupan_anime_title():
    url = "https://ja.wikipedia.org/wiki/%E3%82%AC%E3%83%BC%E3%83%AB%E3%82%BA%26%E3%83%91%E3%83%B3%E3%83%84%E3%82%A1%E3%83%BC"
    pandas_obj = pandas.io.html.read_html(url)
    print(pandas_obj[3][0] + " " + pandas_obj[3][0])


if __name__ == '__main__':
    # exec_beautifulsoup_sample()
    # getTitle("http://www.pythonscraping.com/pages/page1.html")
    # getTitle("http://wwww.pythonscraping.com/pages/page1.html")
    bsObj = getSiteHTML("http://www.pythonscraping.com/pages/warandpeace.html")
    
    
