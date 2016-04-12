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


def get_site_html(url):
    """urlopen() で取得したHTMLを返す"""
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        return None
    except URLError as e:
        print("The server could not be found!")
        return None
    else:
        return html


def get_garupan_anime_title():
    url = "https://ja.wikipedia.org/wiki/%E3%82%AC%E3%83%BC%E3%83%AB%E3%82%BA%26%E3%83%91%E3%83%B3%E3%83%84%E3%82%A1%E3%83%BC"
    pandas_obj = pandas.io.html.read_html(url)
    print(pandas_obj[3][0] + " " + pandas_obj[3][0])


def get_anime_title_from_wikipedia(url):
    html = get_site_html(url)

    if html:
        html_contents = html.read()
        bs_obj = BeautifulSoup(html_contents, 'lxml')
        site_title = bs_obj.body.h1.get_text()
        pandas_obj = pandas.io.html.read_html(html_contents)
        
        # アニメタイトルっぽいリストのインデックスを抽出
        title_idx_list = []
        for idx, dataframe in enumerate(pandas_obj):
            if dataframe[0][0] == "話数" and dataframe[1][0] == "サブタイトル":
                title_idx_list.append(idx)

        # 対象のインデックスからタイトルを抽出して表示
        print("## {}".format(site_title))
        for title_idx in title_idx_list:
            not_nan_idx = (pandas_obj[title_idx][1].isnull() != True)
            title_list = pandas_obj[title_idx][0][not_nan_idx].values + \
                         " " + pandas_obj[title_idx][1][not_nan_idx].values
            # タイトル出力。[0]は "話数"、 "サブタイトル" なので除外
            for title_name in title_list[1:]:
                print("\t{}".format(title_name))
            print("\n")


if __name__ == '__main__':
    pass
    # exec_beautifulsoup_sample()
    # getTitle("http://www.pythonscraping.com/pages/page1.html")
    # getTitle("http://wwww.pythonscraping.com/pages/page1.html")
    # bsObj = get_site_html("http://www.pythonscraping.com/pages/warandpeace.html")
    
    
