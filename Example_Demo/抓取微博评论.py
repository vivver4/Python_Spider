'''
抓取微博Ajax数据
有时候requests抓取的页面结果和浏览器中看到的不同：因为requests获取的都是原始的HTML文档，而浏览器的页面是经JavaScript处理数据后
生成的结果，可能是通过Ajax加载或者是JavaScript和特定算法计算生成的。
Ajax是利用JavaScript在保证页面不刷新、链接不改变的情况下与服务器交换数据：就是微博或者雪球下滑查看更多的选项
Ajax的请求类型叫xhr

Reference: Python3 网络爬虫开发实战，Page 233
'''
from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq



base_url='https://m.weibo.cn/api/container/getIndex?'
headers={
    'Host':'m.weibo.cn',
    'Referer':'https://m.weibo.cn/u/2830678474',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


def get_page(page):
    params={
        'type':'uid',
        'value':'2830678474',
        'containerid':'1076032830678474',
        'page':page
    }
    url=base_url+urlencode(params)
    '''
    为了更加方便地构造参数，我们会事先用字典来表示，要转化为URL的参数时，只需要调用urlencode方法即可
    '''
    try:
        response=requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)


def parse_page(json):
    if json:
        items=json.get('data').get('cards')
        for item in items:
            item=item.get('mblog')
            weibo={}
            weibo['id']=item.get('id')
            weibo['text']=pq(item.get('text')).text()
            weibo['comments']=item.get('comments_count')
            '''
            html='{"name":"Bob","people":"white", "text":"Hallo<span>Json</span>"}'
            s=pq(html)
            r=json.loads(html)
            print(pq(r['text']).text())
            加pq是为了去除<span></span>这些HTML标签
            '''
            yield weibo


if __name__ == '__main__':
    for page in range(2, 11):
        json=get_page(page)
        results=parse_page(json)
        for result in results:
            print(result)