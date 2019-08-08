'''
模拟登陆的逻辑在于：浏览器实际登陆网页的时候，不仅仅需要账号密码，还要提交其他的信息，包括User-Agent等。

分析点击登陆以后的session发现，登陆申请提交的Form Data中有5个重要信息，其中只有authenticity_token不方便自己构建，而这个在
网页源代码中可以找到。另外在Request Headers中发现重要的只有Cookie，Host，User-Agent，其中只有Cookie不
方便自己构建，但是通过查看登陆前的login网址，发现Cookie是一样的，而登录前的login网址不需要登陆，所以可以通过requests模块中
的Session（）方法保持Cookie。

Reference: Python3 网络爬虫开发实战，Page 379
'''

from pyquery import PyQuery as pq
import requests
class Login():
    def __init__(self):
        self.headers={
            'Referer':'https://github.com/login',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'Host':'github.com'
        }

        self.login_url='https://github.com/login'                 #登录前的网址
        '''
        需要下面另一个网址的原因主要是登陆后查看F12的Network可以发现一个302的重定向状态码，
        转到了一个新的网址
        '''
        self.post_url='https://github.com/session'                #提交登陆信息的网址
        self.logined_url='https://github.com/settings/profile'    #登陆后的网址
        self.session = requests.Session()                         #用Session（）方法维持Cookie，就不用考虑Cookie了

    def token(self):
        response=self.session.get(self.login_url, headers=self.headers)
        selector=pq(response.text)
        token=selector('div form input').eq(1).attr('value')
        return token

    def login(self, email, password):
        post_data={
            'commit':'Sign in',
            'utf-8': '√',
            'authenticity_token': self.token(),
            'login': email,
            'password': password
        }
        response=self.session.post(self.post_url, data=post_data, headers=self.headers)   #登陆账号密码
        print(response.status_code)
        response=self.session.get(self.logined_url, headers=self.headers)
        self.profile(response.text)

    def profile(self, html):
        selector=pq(html)
        name=selector('div.application-main form dd input').eq(1).attr('value')
        print(name)

if __name__ == '__main__':
    test=Login()
    test.login(email='sqda_yy@hotmail.com', password='I3crossover')


