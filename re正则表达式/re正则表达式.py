"""
练习re正则表达式爬取网站html内容
根据 book.douban.com 内容写的正则表达式
最后一次更新2018年6月16日13:45:13
author:jevons.code@gmail.com
"""

import requests
import re

con = requests.get('https://book.douban.com/').text
# print(con)
pa = re.compile('<li.*?cover.*?href="(.*?)".?title="(.*?)".*?author">(.*?)</div>.*?year">(.*?)</span>', re.S)
results = re.findall(pa, con)
# print(results)
# file = open(r'db.txt','a',encoding='utf-8')
""" w 打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件
    a 打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。"""
for res in results:
    # 在这里不要把res写成re了，和引入名字一样会报错
    url, name, author, date = res

    # re.sub功能是对于一个输入的字符串，利用正则表达式，来实现字符串替换处理的功能返回处理后的字符串
    author_n = re.sub('\s', '', author)
    date_n = re.sub('\s', '', date)
    print(url, name, author_n, date_n)
    # file.writelines(url)
    # file.writelines('\n')
    # file.writelines(name)
    # file.writelines('\n')
    # file.writelines(author_n)
    # file.writelines('\n')
    # file.writelines(date_n)