'''
抓取今日头条的图片
打开开发者工具查看Response，如果页面内容是根据第一个请求渲染的，那么第一个请求的源代码中必然包括页面结果中的文字，比如可以搜索“路人“
二字，结果可以发现，网页源代码中并没有包含这两个字。初步可以判断是由Ajax加载，然后用JavaScript渲染出来的。
'''
import requests
from urllib.parse import urlencode
import os
from hashlib import md5
import re


def get_page(offset):
    params={
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
        'from': 'search_tab'
    }
    url='http://www.toutiao.com/search_content/?'+urlencode(params)
    try:
        response=requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None


def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            title=item.get('title')
            if item.get('image_list'):
                images=item.get('image_list')
                for image in images:
                    url=image.get('url')
                    url_tempo = re.match('(//.*?)/list/(.*)', url)
                    url_final = 'http:' + url_tempo.group(1) + '/large/' + url_tempo.group(2)
                    yield {
                        'image': url_final,
                        'title': title
                    }

                    '''
                    用到正则表达式是因为返回的Ajax的json文档里面的'image_list'都是小图片，观察得知把url里的'/list/'换成
                    '/large/'即可

                    用yield是因为如果用return会结束循环，需要把url_final和title额外存到一个字典里再return，还不如直接yield，
                    然后在后续main函数中遍历
                    '''

def save_image(item):
    try:
        if not os.path.exists(item.get('title')):
            os.mkdir(item.get('title'))
            '''
            这里会在当前的D:/Python_Spider目录下检查图片名称的文件夹，没有的话就建立
            '''
        response=requests.get(item.get('image'))
        if response.status_code == 200:
            file_path='{0}/{1}.{2}'.format(item.get('title'), md5(response.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('Already Download')
    except:
        print('Failed to save')


def main(offset):
    json=get_page(offset)
    for item in get_images(json):
        save_image(item)

