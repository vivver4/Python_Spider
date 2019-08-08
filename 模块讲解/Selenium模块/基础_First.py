'''
前面了解了Ajax的分析和抓取方式，这其实也是JavaScript动态渲染的页面的一种情形。不过JavaScript动态渲染的页面不止Ajax这一种，或者是即使
像淘宝这种是Ajax获取的数据，但是其Ajax接口有很多加密参数，很难直接分析Ajax来抓取。这时候就可以使用模拟浏览器运行的方式来实现，也就是可
见即可爬，就不需要去考虑内部JavaScript用了什么算法渲染页面。

Chromedriver配置：https://blog.csdn.net/qq_41429288/article/details/80472064
Chromedriver下载：http://npm.taobao.org/mirrors/chromedriver/
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

'''
声明浏览器对象并访问页面
'''
browser=webdriver.Chrome()          #或者Safari(); Edge()来打开不同的浏览器
browser.get('https://www.taobao.com')
print(browser.page_source)          #获取网页的源代码
browser.close()

'''
查找单节点
这里是想从淘宝页面中提取搜索框这个节点，观察源代码后可以发现他的id是q，name也是q。
'''
browser=webdriver.Chrome()
browser.get('https://www.taobao.com')
input_first=browser.find_element_by_id('q')               #根据id获取
input_second=browser.find_element_by_css_selector('#q')   #根据CSS选择器获取
input_third=browser.find_element(By.ID, 'q')              #通用方法find_element()，需要传入两个参数，等同于上面的
print(input_first, input_second, input_third)
browser.close()


'''
32为查找多节点，如果查找的目标在网页中只有一个，那么可以用find_element()方法，但如果有多个的话，再用这个方法只会
找到第一个节点，这时候就要用find_elements（）方法，比如查找淘宝左侧导航条的所有条目）
'''
browser=webdriver.Chrome()
browser.get('https://www.taobao.com')
lis=browser.find_elements_by_css_selector('.service-bd li') #查看F12可以发现导航条的li元素包含在class为service-bd的ul元素里
print(lis)
browser.close()

'''
节点交互
'''
browser=webdriver.Chrome()
browser.get('https://www.taobao.com')
input=browser.find_element_by_id('q')
input.send_keys('iPhone')
time.sleep(1)
input.clear()
input.send_keys('iPad')
button=browser.find_element_by_css_selector('.btn-search')  #找到搜索按钮并点击
button.click()
browser.close()

'''
执行JavaScript（下拉进度条）
'''
browser=webdriver.Chrome()
browser.get('http://www.zhihu.com/explre')
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
browser.execute_script('alert("To Bottom")')
browser.close()

'''
获取节点信息
（前面最初说过，可以用page_source属性获取网页源代码，接着可以用解析库（正则表达式、pyquery等）来提取信息
不过，既然Selenium已经提供了选择节点的方法，返回WebElement类型，就不需要通过解析源代码来提取信息了）
'''
browser=webdriver.Chrome()
browser.get('http://www.zhihu.com/explre')
logo=browser.find_element_by_css_selector('#zh-top-link-logo')
print(logo.get_attribute('class'))          #获取属性
input=browser.find_element_by_css_selector('#zu-top-add-question')
print(input.text)                           #获取文本值
browser.close()

