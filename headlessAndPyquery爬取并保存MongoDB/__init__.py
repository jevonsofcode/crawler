"""
项目名称：Headless + webdriver + pyquery 爬虫  保存到MongoDB
项目流程： 搜索关键字 -> 分析源码并翻页 -> 分析提取商品内容 -> 储存至MongoDB
注意：爬取的是淘宝中国地区， 不同搜索内容页面结构不一样（比如“ 手机”）
最后一次修改时间2018年6月23日11:44:56
author:jevons.code@gmail.com
"""
import re

# from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import pymongo

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

##############MONGODB
#  把这个写在其他文件下 导入文件最好 这次的pycharm不知道为什么导入本地文件报错 Google也没有解决
MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
MONGO_TABLE = 'produce'

sks = '树莓派'   # 第60行
#####################

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

# browser = webdriver.Chrome()  # 把真实浏览器换成虚拟浏览器
# browser = webdriver.PhantomJS()  # selenium 已经不支持 phantomjs 了
options = Options()
options.add_argument('-headless')  #无头参数

browser = Firefox(executable_path='C:\env\geckodriver\geckodriver.exe', firefox_options=options)  # 要装geckodriver 配了环境变量第一个参数就可以省了，不然传绝对路径

wait = WebDriverWait(browser, 10)

browser.set_window_size(1400, 900)

def search():
    print('搜索ing')
    try:
        browser.get('https://www.taobao.com/')
        # print('test0')
        # 接下来设置等待时间，参考 python selenium -> 5.Waits 文档
        input_box = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )  # 输入框
        # print('test1')
        #  等待到这个按钮是可以点击的时候【element_to_be_clickable】 更多等待条件看文档
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button'))
        )  # 搜索按钮
        # print('test2')
        # 动作：文档 -> 7.2 Action Chains
        input_box.send_keys(sks)  # 有的时候可以用send_value
        submit.click()
        total = wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, '.total'
                # mainsrp-pager > div > div > div > div.total
            ))
        )

        get_products()  # 等页面加载出来之后调用

        return total.text
    except TimeoutException:
        print('重新调用search')
        return search()

def next_page(page_number):
    print('翻页到：', page_number)
    try:
        input_box = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input"))
        )  # 输入数字框
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))
        )  # 确定按钮
        input_box.clear()
        input_box.send_keys(page_number)
        submit.click()
        # 判断文本框里的数字是高亮的那个数字
        wait.until(
            EC.text_to_be_present_in_element((
                By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number)
            )
        )
        get_products()  # 第二页之后
    except TimeoutException:  # 出错了就重新调用一下
        print('重新调用next_page')
        next_page(page_number)

def get_products():
    wait.until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR, '#mainsrp-itemlist .items .item'
        ))
    )  # 等待所有item加载完成
    html = browser.page_source  # 获取页面源码
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text().replace('\n', ''),
            'deal': item.find('.deal-cnt').text()[:-3],
            'title': item.find('.title').text().replace('\n', ''),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储成功！', result)
    except Exception:
        print('存储失败！', result)

def main():
    try:
        total = search()  # set recursion
        total = int(re.compile('(\d+)').search(total).group(1))
        for i in range(2, total + 1):  # page
            next_page(i)
    except Exception:
        print('ERROR!')
    finally:
        browser.close()

if __name__ == '__main__':
    main()