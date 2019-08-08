'''
这个模块主要负责清理HTML数据，保存爬取结果到数据库等
具体的调用发生在Spider产生之后，当Spider解析完response之后，Item就会传递到这里，然后顺次调用定义的组件
'''
import pymongo

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri=mongo_uri
        self.mongo_db=mongo_db

    '''
    这个模块的一个类方法，主要是为了获得全局配置的信息，在全局配置settings.py中，可以定义MONGO_URI
    和MONGO_DB来指定MongoDB连接的地址和数据库名称
    '''
    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'),
                   mongo_db=crawler.settings.get('MONGO_DB'))

    def open_spider(self, spider):
        self.client=pymongo.MongoClient(self.mongo_uri)
        self.db=self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.db[item.collection].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()