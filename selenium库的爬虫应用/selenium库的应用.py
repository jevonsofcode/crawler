"""
selenium 库的爬虫应用
最后一次更新2018年6月18日18:14:49
author:jevons.code@gmail.com
"""

from selenium import webdriver
from selenium.webdriver.common.by import By

# browser = webdriver.Chrome()
# browser.get('https://www.baidu.com')
# print(browser.page_source)
# browser.close()
# 简单的访问页面

# f = browser.find_element(By.ID, 'kw') #from selenium.webdriver.common.by import By
# print(f)
# browser.close()
# 访问单个元素

# css_f = browser.find_elements(By.CSS_SELECTOR,'.mnav')
''' 没有写 form selenium.webdriver.common.by import By 的话
    就写成：
    .find_elements_by_css_selector('.mnav') 
'''

# print(css_f)
# browser.close()
# # 访问多个元素

''' 元素交互操作
import time
bro = webdriver.Chrome()
bro.get('https://www.taobao.com')
i = bro.find_element(By.NAME,'q') # 淘宝的搜索框
i.send_keys('iphone') # 输入字符串
time.sleep(3) # time.sleep(t) t=推迟秒数
i.clear() # clear
i.send_keys('iPad')
btn = bro.find_element_by_class_name('btn-search') # 淘宝的搜索button
btn.click() # 点击
time.sleep(2)
bro.close()
'''

''' 交互动作
from selenium.webdriver import ActionChains

br = webdriver.Chrome()
url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
br .get(url)
br.switch_to.frame('iframeResult') # 切换到frame
s = br.find_element_by_css_selector('#draggable')
t = br.find_element_by_css_selector('#droppable')
act = ActionChains(br) # 模拟鼠标类
act.drag_and_drop(s, t) # 拖拽元素
act.perform()
'''

''' 执行JavaScript
from selenium import webdriver

b = webdriver.Chrome()
b.get('https://www.zhihu.com/explore')
b.execute_script('window.scrollTo(0, document.body.scrollHeight)')
b.execute_script('alert("TO BOTTON")')
'''

''' 获取元素信息
from selenium import webdriver

b = webdriver.Chrome()
b.get('https://www.zhihu.com/explore')
logo = b.find_element_by_id('zh-top-link-logo')
print(logo)
print(logo.get_attribute('class')) # 元素信息
print(logo.text) # 文本值
print(logo.id) # id
print(logo.location) # location
print(logo.tag_name) # 标签name
print(logo.size) # size
'''

''' Frame frame之外的要用.parent_frame()切换到父级才能用
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

b = webdriver.Chrome()
b.get('http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')
b.switch_to.frame('iframeResult')
s = b.find_element_by_css_selector('#draggable')
print('source:', s)
try:
    logo = b.find_element_by_class_name('logo')
except NoSuchElementException:
    print('NO LOGO')
b.switch_to.parent_frame()
logo = b.find_element_by_class_name('logo')
print(logo)
print(logo.text)
'''

'''  前进 后退 演示  .back() && .forward()
import time
from selenium import webdriver

b = webdriver.Chrome()
b.get('http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')
b.get('https://www.zhihu.com/explore')
b.get('http://www.google.com/')
time.sleep(1.5)
b.back()
time.sleep(1.5)
b.forward()
time.sleep(1.5)
b.close()
'''

''' 浏览器的选项卡管理'''
import time
from selenium import webdriver

b = webdriver.Chrome()
b.get('http://www.google.com/')
i = b.find_element_by_id('lst-ib')
i.send_keys('python')
b.execute_script('window.open()')
b.switch_to.window(b.window_handles[1])
b.get('http://www.google.com/')
i = b.find_element_by_id('lst-ib')
i.send_keys('javascript')
time.sleep(1)
b.switch_to.window(b.window_handles[0])