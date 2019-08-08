'''
对于应用了极验验证码的网站，如果直接模拟表单提交，加密参数的构造是个问题。所以采用直接模拟浏览器动作的方式，可以使用Selenium
完全模拟人的行为来完成验证，整个识别验证分为：
一、获取按钮位置（查看Bilibili的网站可以发现鼠标移动到点击按钮上就会出现图片）
二、截图
三、点击按钮
四、再次截图
五、两次截图对比识别缺口位置
六、模拟拖动按钮
'''
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from io import BytesIO
from PIL import Image

EMAIL='sqda_yy@hotmail.com'
PASSWORD='femininity3'
BORDER=6

class CrackBilibili():
    def __init__(self):
        self.url='https://passport.bilibili.com/login'
        self.browser=webdriver.Chrome()
        self.wait=WebDriverWait(self.browser, 5)
        self.email=EMAIL
        self.password=PASSWORD
    '''
    打开网页，输入账号密码以备使用
    '''
    def open(self):
        self.browser.get(self.url)
        email=self.wait.until(EC.presence_of_element_located((By.ID, 'login-username')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'login-passwd')))
        email.send_keys(self.email)
        password.send_keys(self.password)
    '''
    获取按钮位置
    '''
    def get_botton(self):
        click_botton=self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.gt_slider_knob')))
        ActionChains(self.browser).move_to_element(click_botton).perform()
        return click_botton
    '''
    获取图片坐标位置
    '''
    def get_position(self):
        img=self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.gt_cut_fullbg.gt_show')))
        time.sleep(2)
        location=img.location
        size=img.size
        top, bottom, left, right=location['y'], location['y']+size['height'], location['x'], location['x']+size['width']
        return (top, bottom, left, right)
    '''
    获取整个网页的截图
    '''
    def get_screenshot(self):
        screenshot=self.browser.get_screenshot_as_png()      #这里得到的二进制流包含utf-8外的内容，无法读取
        screenshot=Image.open(BytesIO(screenshot))           #所以全写入内存变为Unicode处理
        return screenshot

    '''
    从网页截图中裁剪图片
    '''
    def get_bilibili_image(self):
        top, bottom, left, right =self.get_position()
        print('验证码位置：', top, bottom, left, right)
        screenshot=self.get_screenshot()
        captcha=screenshot.crop((left, top, right, bottom))
        return captcha

    def is_pixel_equal(self, image1, image2, x, y):
        pixel1=image1.load()[x, y]
        pixel2=image2.load()[x, y]
        threshold=60
        if abs(pixel1[0]-pixel2[0])<threshold and abs(pixel1[1]-pixel2[1])<threshold and abs(pixel1[2]-pixel2[2])<threshold:
            return True
        else:
            return False

    def get_gap(self, image1, image2):
        left=60
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left=i
                    return left
        return left

    def get_track(self, distance):
        #移动轨迹
        track=[]
        #当前位移
        current=0
        #减速阈值
        mid=distance*4/5
        #计算间隔
        t=0.2
        #初速度
        v=0
        while current<distance:
            if current<mid:
                a=4
            else:
                a=-4
            v0=v
            v=v0+a*t
            move=v0*t+1/2*a*t*t
            current+=move
            track.append(round(move))
        return track

    def move_to_gap(self, slider, tracks):
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in tracks:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(1.5)
        ActionChains(self.browser).release().perform()

    def crack(self):
        self.open()
        botton = self.get_botton()
        image1 = self.get_bilibili_image()
        botton.click()
        time.sleep(1)
        image2 = self.get_bilibili_image()
        gap=self.get_gap(image1, image2)
        gap-=BORDER
        track=self.get_track(gap)
        self.move_to_gap(botton, track)

a=CrackBilibili()
a.crack()

