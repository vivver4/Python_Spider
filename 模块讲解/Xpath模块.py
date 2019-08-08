from lxml import etree

text='''
<div id="container">
<ul class="list">
<li class="item-0">first item</li>        
<li class="item-1"><a href="link2.html">second item</a></li>
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
<li class="item-0"><a href="link3.html"><span class="bold">third item</span></a></li>
<li class="item-1 active"><a href="link4.html">fourth item</a></li>                  
<li class="item-0"><a href="link5.html">fifth item</a></li>
<li class="item-0"><b href="link6.html">fifth item<a class="extra"></a></b></li>
</ul>
</div>
'''

html=etree.HTML(text)
print(html.xpath('//li'))       #//开头来选取所有符合要求的节点
print('-'*60)
print(html.xpath('//li/a'))       #//li选中所有li节点，/a用于选中所有直接子节点a，所以最后一个a节点没有选中，因为不是直接子节点
print('-'*60)
print(html.xpath('//li//a'))      #//li选中所有li节点，//a选中所有子孙节点a，所以最后一个a节点也选中了
print('-'*60)
print(html.xpath('//li[@class="item-0"]'))   #属性匹配
print('-'*60)
print(html.xpath('//li/a[contains(@href, "link5.html")]/text()'))  #如此存在属性多值的话，用contains来获取
print('-'*60)
print(html.xpath('//li/text()'))  #/直接选中子节点，所以只读取到了first item，或者可以直接用//读取所有的子孙节点
print('-'*60)
print(html.xpath('//li/a/@href')) #这里通过@href来获取节点的属性，和属性匹配获取节点不同
print('-'*60)
print(html.xpath('//li/a[contains(., "fifth item")]'))
