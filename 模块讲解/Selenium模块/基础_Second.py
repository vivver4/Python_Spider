from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

'''
延时等待
在Selenium中，get（）方法会在网页框架加载结束后结束执行，此时如果获取page_source，可能
不是浏览器完全加载完成的页面。所以，这里需要延时等待一定时间，确保节点已经加载出来。
'''
'''
隐式等待
当查找节点而节点没有立即出现的时候，隐式等待将等待一段时间再查找
'''
browser=webdriver.Chrome()
browser.implicitly_wait(10)
browser.get('https://www.zhihu.com/explore')
input=browser.find_element_by_css_selector('#zu-top-add-question')
print(input)
browser.close()

'''
显式等待
指定要查找的节点，然后指定一个最长等待时间。如果在规定时间内加载出这个节点，就返回查找节点；如果
到了规定时间没有加载出来，则抛出超时异常

这里首先引入WebDriverWait这个对象，指定最长等待时间，然后调用它的until（）方法，传入要等待条件
expected_conditions。比如，在这里传入了presence_of_element_located这个条件，代表节点出现的意思，
也就是ID为q的节点搜索框。
这样可以做到的效果就是，在10秒内如果ID为q的节点成功加载出来，就返回该节点；如果超过10秒还没有加载出来，就
抛出异常
对于按钮，可以更改一下等待条件，改为element_to_be_clickable，如果10秒内可点击，也就是成功加载出来了，就
返回该按钮节点，否则抛出异常
'''
browser=webdriver.Chrome()
browser.get('https://www.taobao.com/')
wait=WebDriverWait(browser, 10)
input=wait.until(EC.presence_of_element_located((By.ID, 'q')))
button=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-search')))
print(input, button)
browser.close()


'''
前进和后退
'''
browser=webdriver.Chrome()
browser.get('http://www.baidu.com/')
browser.get('http://www.taobao.com/')
browser.get('http://www.python.org/')
browser.back()
time.sleep(3)
browser.forward()
browser.close()


'''
选项卡管理
'''
browser=webdriver.Chrome()
browser.get('https://www.baidu.com')
browser.execute_script('window.open()')
print(browser.window_handles)                            #获取当前开启的所有选项卡
browser.switch_to.window(browser.window_handles[1])
browser.get('https://www.taobao.com')
time.sleep(2)
browser.switch_to.window(browser.window_handles[0])
browser.get('https://python.org')