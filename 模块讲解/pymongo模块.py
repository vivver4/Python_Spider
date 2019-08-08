'''
先安装好MongoDB，再安装PyMongo。现在在安装MongoDB的过程中可以直接配置系统服务和Directory，不需要
再通过进入MongoDB安装目录下的bin目录，运行mongod --dbpath "C:\Program Files\MongoDB\Server\4.0\data\db"
'''
import pymongo

'''
插入数据
'''
client=pymongo.MongoClient(host='localhost')  #连接MongoDB
db=client.test                                #指定数据库，MongoDB中可以建立多个数据库，这里指定test数据库
collection=db.students                        #每个数据库包含许多集合（collection)，这里申明一个collection对象为students集合
student1={'id':'20170101', 'name':'Jordan', 'age': 20, 'gender': 'male'}
student2={'id':'20170202', 'name':'Mike', 'age': 21, 'gender': 'male'}
student3={'id':'19930154', 'name':'James', 'age':20, 'gender': 'male'}
student4={'id':'20161121', 'name':'Jenny', 'age':30, 'gender': 'female'}
result=collection.insert_many([student1, student2, student3, student4])
print(result)


'''
查询数据
find()方法返回的是生成器
'''
client=pymongo.MongoClient(host='localhost')
db=client.test
collection=db.students
results=collection.find({'age':20})                #等于20
results2=collection.find({'age': {'$gt':20}})      #大于20，$lt是小于
results3=collection.find({'name': {'$regex': 'M.*'}})  #用正则表达式
for result in results:
    print(result)
print('*'*40)

for result in results2:
    print(result)
print('*'*40)

for result in results3:
    print(result)
