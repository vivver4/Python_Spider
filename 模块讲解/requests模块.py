import requests
import re

'''
requests模块最简单演示
'''

r=requests.get('http://httpbin.org/get')
print(r.text)
print(r.json()) #网页的返回类型实际上是str类型，但是它很特殊，是JSON格式的。如果想直接解析返回结果，得到字典格式的话，直接调用json()方法

'''
requests模块抓取知乎网页
'''

headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}           #浏览器标识信息，如果不加知乎会禁止抓取
r=requests.get('https://www.zhihu.com/explore', headers=headers)
pattern=re.compile('explore-feed.*?question_link.*?>(.*?)</a>', re.S)
titles=re.findall(pattern, r.text)
print(titles)


