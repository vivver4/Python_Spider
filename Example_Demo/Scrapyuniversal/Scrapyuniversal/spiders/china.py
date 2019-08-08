# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Scrapyuniversal.items import NewsItem

class ChinaSpider(CrawlSpider):
    name = 'china'
    allowed_domains = ['tech.china.com']
    start_urls = ['http://tech.china.com/']
    rules = (
        Rule(LinkExtractor(allow='article\/.*\.html',
                           restrict_xpaths='//div[@id="left_side"]//div[@class="con_item"]'),
                           callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@id="pageStyle"]//a[contain(., "下一页")]'))
    )
    '''
    Spider会根据每一个Rule来提取这个页面内的超链接，去生成进一步的Request
    第一个Rule的LinkExtractor指定了每一条具体的新闻链接（理论上只用LinkExtractor就够了，但是
    为了防止文章中还有一些其他的超链接被提取，用allow加以限定），并用回调函数parse_item去解析
    
    第二个Rule的LinkExtractor指定了下一页，并用follow参数为True代表跟进匹配分析（继续像上述情况一样分析），不过不加也可以，因为
    当没有callback函数时，follow默认为True
    '''

    def parse_item(self, response):
        item=NewsItem()
        item['title']=response.xpath('//hi[@id="chan_newsTitle"]/text()').extract_first()
        item['url']=response.url
        item['text']=''.join(response.xpath('//div[@id="chan_newsDetail"]//text()').extract()).strip()
        item['datetime']=response.xpath('//div[@id="chan_newsInfo"]/text()').re_first('\d+-\d+-\d+\s\d+:\d+:\d+')
        item['website']='中华网'
        '''
        具体extract的用法可以看书中484页的内容，join方法将文章段落连接，再用strip()去除首尾空格
        '''
        yield item
