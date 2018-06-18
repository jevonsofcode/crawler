"""
用re正则表达式爬取猫眼top100电影
最后一次更新2018年6月19日01:41:05
author:jevons.code@gmail.com
"""

import requests
import json
from requests import RequestException as RE1
# from selenium import webdriver
import re
from multiprocessing import Pool  # 引用多进程

header = {"user-agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}

def get_one_page(url):
    try:
        res = requests.get(url, headers = header) # 现在猫眼电影有反爬虫了要加headers
        if res.status_code == 200:
            return res.text
        return None
    except RE1:
        return None

def parse_one_page(u):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'+'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'+'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, u)
    for item in items:
        yield{
            'index' : item[0],
            'image' : item[1],
            'title' : item[2],
            'actor' : item[3].strip()[3:],
            'time' : item[4].strip()[5:],
            'score' : item[5]+item[6]
        }

def wr(con): # 现在con是字典形式
    with open('MOVtop100.txt', 'a', encoding='utf-8') as f: # a是追加
        f.write(json.dumps(con, ensure_ascii=False) + '\n') # 把con转换为字符串

def main(n):

    # for n in range(0, 100, 10): # ② 这样不用多次调用 但可以被多进程代替
        url = 'http://maoyan.com/board/4?offset=' + str(n)

        u = get_one_page(url)
        for item in parse_one_page(u):
            print(item)
            wr(item)

if __name__ == '__main__':
    # # for i in range(10): # ① 这样传给main（）10次效率太低
    # #     main(i*10)
    # main()
    p = Pool()
    p.map(main, [i*10 for i in range(10)]) # ③ 但是多进程抓的是乱序的