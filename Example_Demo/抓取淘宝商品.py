'''
上一个例子中成功尝试分析Ajax来抓取数据，但是并不是所有页面都可以分析Ajax来抓取，像淘宝虽然页面数据也是
通过Ajax获取的，但是这些Ajax接口参数复杂，可能包含加密密钥等。这种页面，最快捷的抓取方法就是通过Selenium。

Reference: Python3 网络爬虫开发实战，Page 289
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from pyquery import PyQuery as pq

browser=webdriver.Chrome()

wait=WebDriverWait(browser, 10)
KEYWORD='iPad'

def index_page(page):
    '''
    抓取索引页
    :param page:   页码
    '''
    print('正在爬取第 ', page, '页')
    try:
        url='https://s.taobao.com/search?q=' + quote(KEYWORD)
        browser.get(url)
        if page > 1:
            input=wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input'))
            )
            submit=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > \
                                    span.btn.J_Submit')))
            input.clear()
            input.send_keys(page)
            submit.click()
        '''
        以下两个wait只是用来等待网页加载完毕
        '''
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page))
        )                    #判断span元素中是否存在指定的str(page)文本

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
        get_products()
    except TimeoutError:
        index_page(page)


def get_products():
    '''
    提取商品数据
    '''
    html=browser.page_source
    doc=pq(html)
    items=doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product={
            'image':item.find('.pic .img').attr('data-src'),
            'price':item.find('.price').text(),
            'deal':item.find('.deal-cnt').text(),
            'title':item.find('.title').text(),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text()
        }
        print(product)
index_page(1)