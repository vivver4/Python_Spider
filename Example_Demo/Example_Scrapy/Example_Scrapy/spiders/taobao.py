# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote

class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']
    base_url = ['http://www.taobao.com/search?q=']

    def start_requests(self):
        for keyword in self.settings.get('KEYWORDS'):
            for page in range(1, self.settings.get('MAX_PAGE')+1):
                url=self.base_url+quote(keyword)
                yield scrapy.Request(url=url, callback=self.pase)
    def parse(self, response):
        pass
