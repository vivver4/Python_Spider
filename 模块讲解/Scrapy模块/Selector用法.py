from scrapy import Selector

response='''
<html>
<head>
<base href='http://example.com/' />
<title>Example website</title>
</head>
<body>
<div id='images'>
<a href='image1.html'>Name: My image 1 <br> Haha </br><img src='image1_thumb.jpg' /></a>
<a href='image2.html'>Name: My image 2 <br /><img src='image2_thumb.jpg' /></a>
<a href='image3.html'>Name: My image 3 <br /><img src='image3_thumb.jpg' /></a>
<b href='image4.html'>Name: My image 4 <br /><a src='image4_thumb.jpg' /></b>
</div>
</body>
</html>
'''


'''
XPath选择器
'''
selector=Selector(text=response)                   #构建Selector对象

print(selector.xpath('//a'))                       #选中所有a节点，不管在什么位置
print('-'*60)
print(selector.xpath('//a/text()'))                #选中所有a节点的文本
print('-'*60)
print(selector.xpath('//a/text()').extract())      #提取所有文本
print('-'*60)
print(selector.xpath('//a/img'))                   #选中所有a节点下的img节点
print('-'*60)
print(selector.xpath('//a[@href="image1.html"]'))  #用属性限制了匹配的范围
print('-'*60)

'''
CSS选择器
'''
print(selector.css('a'))                           #选中所有a节点，不管在什么位置
print('-'*60)
print(selector.css('a').extract())                 #提取a节点的内容（不是文本内容）
print('-'*60)
print(selector.css('a::text').extract())           #提取a节点的文本内容
print('-'*60)
print(selector.css('a::attr(href)').extract())     #提取a节点的属性内容



