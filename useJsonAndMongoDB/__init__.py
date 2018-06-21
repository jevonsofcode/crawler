"""
用json爬虫and MongoDB

2018年6月19日01:41:05  还需要完善 以及 这个网站源码一直改变

今日头条好麻烦 图片不在表面html中，在Doc文件的url的js中 流程{
① 抓取索引页内容；② 抓取详情页内容；③ 下载保存
}

最后一次更新2018年6月21日23:31:55
author:jevons.code@gmail.com
"""
import pymongo
import re
from urllib.parse import urlencode
import json

from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import requests

MONGO_URL='localhost'
MONGO_DB='toutiao'
MONGO_TABLE='toutiao'

# from config import *
# pycharm 导入的时候加个点 也不对
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

header = {
'user-agent': 'Mozilla / 5.0(Windows NT 10.0; WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 53.0.2785.104Safari / 537.36Core / 1.53.4882.400QQBrowser / 9.7.13059.400'
}


def get_page_index(offset, keyword):  # 抓取索引页
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 1,
        'from': 'search_tab'
    }  # 把请求的参数变成字典 值在Query String Parameter中
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)  # urllib库提供的方法
    try:
        r = requests.get(url, headers = header)
        if r.status_code == 200:  # 判断是否成功
            return r.text
        return None
    except RequestException:
        print('请求索引出错')
        return None

def parse_page_index(html):  # 解析
    data = json.loads(html)  # 用json.loads让其变成对象
    if data and 'data' in data.keys(): # dict.keys()函数以列表返回一个字典所有的键
        for item in data.get('data'): # 如果有data这个信息 把data遍历
            yield item.get('article_url') # 把每一个item的article_url提取出来 yield构造一个生成器

def get_page_detail(url1):  # 抓取详情页
    try:
        response = requests.get(url1, headers = header)
        if response.status_code == 200:  # 判断是否成功
            return response.text
        return None
    except RequestException:
        print('请求详情页出错!', url1)
        return None

# s = []
def parse_page_detail(html1):
    soup = BeautifulSoup(html1, 'lxml')  # lxml HTML 解析器
    title = soup.select('title')[0].get_text()

    print(title, type(title))
    # images_url = soup.select('div.image-item-inner img')[0].attrs['src']
    # print(images_url)

# def parse_html_detail(html):
#     i_p = re.findall('original_page_url\": \".*?\", \"img\": \"(.*?)\",', html)  # 一直改  明明URL就有
#     # print(i_p)
#     # result = re.search(i_p, html)  # 匹配 正则表达式 在不在 html 中
#     if i_p:
#         for i in i_p:
#             print(i)
#     else:
#         print('正则表达式过期了')

def save_to_mongo(title):
    if db[MONGO_TABLE].insert(title):
        print('储存到MONGODB成功', title)
        return True
    return False

def main():
    html = get_page_index(0, '街拍')
    # parse_html_detail(html)  ##### 这个正则表达式还需要改
    for url1 in parse_page_index(html):
        if type(url1) != str:   #  如果没抓到就跳过了
            continue
        # print(url1)
        html1 = get_page_detail(url1)
        # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',html,'--------------------------------------------------------')
        if html1:
            parse_page_detail(html1)
            # save_to_mongo(title)
            # print(title)
# 2018年6月21日00:50:49 写到这里感觉自己好机智 (#^.^#)
if __name__ == '__main__':
    main()