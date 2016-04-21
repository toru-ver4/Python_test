#!/usr/bin/env python3
#-*- coding: utf-8 -*-
 
"""
test for request module.
"""

import os
import sys
from urllib.request import urlopen
from urllib.error import HTTPError
import urllib.parse
from bs4 import BeautifulSoup
import pandas
import re

const_html_cache_dir = './html_cache'
const_fillna_str = " "
const_exclusion_title_set = frozenset(["アニサン劇場", 
                                       "カード・バトルZERO",
                                       "新あたしンち",
                                       "スタミュ",
                                       "DIABOLIK_LOVERS",
                                       "DIABOLIK_LOVERS_MORE,BLOOD",
                                       "北斗の拳_イチゴ味"
])
wikipedia_title_pattern = re.compile(r"https://ja.wikipedia.org/wiki/(.*$)")
err_title_list = []

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


def get_each_story_list_from_url(url, title=""):

    # html の cache を確認
    cache_file_name = os.path.join(const_html_cache_dir, title)
    if os.path.isfile(cache_file_name):
        with open(cache_file_name, 'rb') as f:
            print("read from cache")
            html_contents = f.read()
    else:
        html = get_site_html(url)
        if html:
            html_contents = html.read()
            if not os.path.isdir(const_html_cache_dir):
                os.mkdir(const_html_cache_dir)
            with open(cache_file_name, 'wb') as f:
                f.write(html_contents)
        else:
            print("anime each story list is not found ad {}".format(title))
            return None

    bs_obj = BeautifulSoup(html_contents, 'lxml')
    site_title = bs_obj.body.h1.get_text()
    pandas_obj = pandas.io.html.read_html(html_contents)

    # アニメタイトルが含まれるページか判別
    if not bs_obj.find(text="各話リスト"):
        print("{} is not anime page".format(site_title))
        return None

    # デバッグ出力。困ったら使おう
    # print(pandas_obj)

    # アニメタイトルっぽいリストのインデックスを抽出
    title_idx_list = []
    for idx, dataframe in enumerate(pandas_obj):
        for inter_idx in range(dataframe.shape[1] - 1):
            dataframe[inter_idx] = dataframe[inter_idx].fillna(const_fillna_str)
            dataframe[inter_idx + 1] = dataframe[inter_idx + 1].fillna(const_fillna_str)
            wa_check = ((dataframe[inter_idx].str.contains("話")).sum() > 0)
            wa_check_2 = ((dataframe[inter_idx].str.contains("#")).sum() > 0)
            sub_title_check = ((dataframe[inter_idx + 1].str.contains("タイトル")).sum() > 0)

            if (wa_check or wa_check_2) and sub_title_check:
                story_idx = inter_idx
                story_title_index = inter_idx + 1
                title_idx_list.append(idx)

    # バグ解析コード ← 後で消す
    if len(title_idx_list) == 0:
        err_title_list.append(site_title)
        print(site_title)
        sys.exit(0)

    # 対象のインデックスからタイトルを抽出して表示
    print("## {}".format(site_title))
    for title_idx in title_idx_list:
        not_nan_idx = (pandas_obj[title_idx][story_title_index] != const_fillna_str)
        not_nan_idx_2 = ~(pandas_obj[title_idx][story_title_index].str.contains("タイトル"))
        not_nan_idx = not_nan_idx & not_nan_idx_2
        title_list = pandas_obj[title_idx][story_idx][not_nan_idx].values + \
                     " " + pandas_obj[title_idx][story_title_index][not_nan_idx].values
        for title_name in title_list:
            print("\t{}".format(title_name))
        print("\n")


def get_anime_page_link_from_wikipedia(url, link_array=[]):
    html = get_site_html(url)
    if html:
        html_contents = html.read()
        bs_obj = BeautifulSoup(html_contents, 'lxml')
        href_list = bs_obj.find("div", {"id":"mw-pages"}).find("div", {"class":"mw-content-ltr"}).findAll("a")

        if href_list:
            for href_element in href_list:
                if 'href' in href_element.attrs:
                    link_array.append('https://ja.wikipedia.org' + href_element.attrs['href'])
        else:
            print("href is not found.")
            return None

        next_page_list = bs_obj.find("div", {"id":"mw-pages"}).findAll("a")
        for next_page in next_page_list:
            if next_page.get_text() == "次のページ":
                if 'href' in next_page.attrs:
                    next_url = 'https://ja.wikipedia.org' + next_page.attrs['href']
                    link_array = get_anime_page_link_from_wikipedia(next_url, link_array)
                    break
                
    return link_array


def get_each_story_list_from_url_list(url_list):
    for url in url_list:
        match_obj = wikipedia_title_pattern.search(url)
        if match_obj:
            encoded_str = match_obj.group(1)
            anime_title = urllib.parse.unquote(encoded_str)
            
            # タイトルに特殊記号があったら置換
            anime_title = anime_title.translate(anime_title.maketrans("?", "？"))
            anime_title = anime_title.translate(anime_title.maketrans("!", "！"))
            anime_title = anime_title.translate(anime_title.maketrans(":", "_"))
            anime_title = anime_title.translate(anime_title.maketrans("/", "_"))
            anime_title = anime_title.translate(anime_title.maketrans("*", "_"))
            anime_title = anime_title.translate(anime_title.maketrans("@", "_"))

            # リストが空だったら飛ばす
            if not anime_title:
                print("error on {}".format(url))
                continue

            # NGリストに該当するアニメは飛ばす
            if anime_title in const_exclusion_title_set:
                print("{} is included the exclusion list.".format(anime_title))
                continue

            get_each_story_list_from_url(url, title=anime_title)
    

if __name__ == '__main__':

    url_2015 = "https://ja.wikipedia.org/wiki/Category:2015%E5%B9%B4%E3%81%AE%E3%83%86%E3%83%AC%E3%83%93%E3%82%A2%E3%83%8B%E3%83%A1"
    anime_url_list = get_anime_page_link_from_wikipedia(url_2015)
    get_each_story_list_from_url_list(anime_url_list)

    # url = "https://ja.wikipedia.org/wiki/%E3%81%82%E3%81%9F%E3%81%97%E3%83%B3%E3%81%A1"
    # get_each_story_list_from_url(url, title="unchi3")
    
    # exec_beautifulsoup_sample()
    # getTitle("http://www.pythonscraping.com/pages/page1.html")
    # getTitle("http://wwww.pythonscraping.com/pages/page1.html")
    # bsObj = get_site_html("http://www.pythonscraping.com/pages/warandpeace.html")
    
    
