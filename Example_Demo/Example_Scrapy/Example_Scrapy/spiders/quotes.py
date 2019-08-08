'''
Spider模块是最核心的模块，主要定义了爬取的逻辑和网页的解析规则，主要负责解析响应并生成提取结果和新的请求
'''

import sys
import scrapy
sys.path.append('D:/Python_Spider/Example_Demo/Example_Scrapy')
from Example_Scrapy.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        '''
        这个模块的一个方法，主要是接受start_urls里的链接返回的response参数
        可以尝试print(response.text)来查看命令行输出
        '''
        quotes=response.css('.quote')
        for quote in quotes:
            item=QuoteItem()
            item['text']=quote.css('.text::text').extract_first()
            item['author']=quote.css('.author::text').extract_first()
            item['tags']=quote.css('.tags .tag::text').extract()
            yield item
        next=response.css('.pager .next a::attr(href)').extract_first()
        url=response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse)
