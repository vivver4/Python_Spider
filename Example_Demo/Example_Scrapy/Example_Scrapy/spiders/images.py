import scrapy
from urllib.parse import urlencode
import json
from Example_Scrapy.items import ImageItem

class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['images.so.com']
    '''
    起始URL列表，如果没有实现start_requests()方法时，默认会从这里抓取
    '''
    start_urls = ['http://images.so.com/']

    def start_requests(self):
        '''
        主要功能就是将URL输入Request函数得到Response，再传递给parse()方法
        '''
        data={'ch':'photography', 'listtype':'new'}
        base_url='http://image.so.com/zj?'
        for page in range(1, self.settings.get('MAX_PAGE')+1):
            data['sn']=page*30
            params=urlencode(data)          #方便将字典整合入URL
            url=base_url+params
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        '''
        主要是接受start_requests()方法返回的response参数，并自己构建解析
        '''
        result=json.loads(response.text)
        for image in result.get('list'):
            item=ImageItem()
            item['id']=image.get('imageid')
            item['url']=image.get('qhimg_url')
            item['title']=image.get('group_title')
            item['thumb']=image.get('qhimg_thumb_url')
            yield item

