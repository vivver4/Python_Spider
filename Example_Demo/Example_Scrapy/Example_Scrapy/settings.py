#DEFAULT部分
BOT_NAME = 'Example_Scrapy'
SPIDER_MODULES = ['Example_Scrapy.spiders']
NEWSPIDER_MODULE = 'Example_Scrapy.spiders'


#启动pipelines模块用
ITEM_PIPELINES = {
    'Example_Scrapy.pipelines.MongoPipeline': 301,
}


#pipelines模块中指定MongoDB连接的地址和数据库名称用
MONGO_URI='localhost'
MONGO_DB='images360'


#是否要遵守robotstxt
ROBOTSTXT_OBEY = False


MAX_PAGE=50
KEYWORDS=['iPad']
#
# DEFAULT_REQUEST_HEADERS={
#     'Host':'image.so.com',
#     'Referer':'https://image.so.com/z?ch=photography',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
#     'X-Requested-With': 'XMLHttpRequest'
# }
