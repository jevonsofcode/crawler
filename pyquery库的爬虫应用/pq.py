"""
pyquery 库的爬虫应用
根据 http://www.cnu.cc/ 内容写的pq
最后一次更新2018年6月17日15:37:40
author:jevons.code@gmail.com
"""

import requests

html = requests.get('http://www.cnu.cc/').text
# print(type(html),html)

from pyquery import PyQuery as pq
doc = pq(html)
items = doc('.bannerLi')
items1 = doc('h3')
items2 = doc('.selectedUL.pc h3') # 同时包含selectedUL pc 和js写法一样
''' ①
也可以写成pq(url='http://...')
本地文件写成pq(filename='')
'''

''' ②
print(doc('h3'))
print(doc('.workTitle'))
# 直接找标签 # 找ID（#）， class（.）
'''

''' ③
lis = items('.workContent').children('a')
print(lis)
# 子元素查询方法 children()中可以传值
'''

''' ④
parent = items1.parent()
print(parent)
# 返回两个值 parent()也可以传参
'''

'''
bro = items.siblings()
print(bro)
# siblings() 传参的话找的是兄弟元素有的
'''

'''
gen = items1.items()
# print(type(gen))
for g in gen:
    print(g)
# 用item()可以把对象变成generator元素来遍历 可以在for中单独为每一个对象进行操作
'''

# '''
text1 = items.text()
print(text1)
# text()获取文字 html()获取HTML attr()获取属性
# '''