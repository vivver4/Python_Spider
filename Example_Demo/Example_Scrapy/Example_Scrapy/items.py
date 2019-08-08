'''
定义了爬取结果的数据结构，爬取的数据会被赋值成该Item对象
'''

import scrapy


class QuoteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text=scrapy.Field()
    author=scrapy.Field()
    tags=scrapy.Field()

class ImageItem(scrapy.Item):
    collection='image'
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    thumb = scrapy.Field()

class ProductItem(scrapy.Item):
    collection='products'
    image = scrapy.Field()
    price = scrapy.Field()
    deal = scrapy.Field()
    title = scrapy.Field()
    shop = scrapy.Field()
    location = scrapy.Field()