from pyquery import PyQuery as pq

html='''
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

'''
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>是一个元素
，里面的<span class="bold">third item</span>也是一个元素
'''
'''
简单的CSS选择器演示
'''
doc=pq(html)
print(doc('li'))             #元素选择器
print('-'*60)
print(doc('.item-0'))        #class选择器
print('-'*60)
print(doc('#container'))     #id选择器
print('-'*60)
print(doc('#container .list li'))     #三种选择器叠加使用（CSS选择器），先选择id为container的节点，在选取class为list的节点，再选取所有li节点
print('-'*60)
print(doc('.item-0 > a'))             #子元素选择器，用">"分隔，匹配class为item-0元素下的所有直接a子元素
print('-'*60)
print(doc('.item-0 a'))              #后代选择器，用空格分隔，匹配class为item-0元素下的所有a子元素，不管什么层级
print('-'*60)
print(doc('li.item-0'))               #选择class为item-0的li元素
print('-'*60)
print(doc('.active'))                 #选择class为active的元素，在HTML中，一个class值可以指定多个值，多种样式会叠加应用
print('-'*60)
print(doc('li a[href="link3.html"]')) #选择href属性为link3.html的a元素
print('-'*60)
print(doc('li a').eq(1))              #选择索引号为1的a元素


'''
常用的查询函数
'''
items=doc('.list')
print(doc.find('li'))        #find会返回每个元素的后代，所以这里能找到
print(doc.children('li'))    #children仅遍历儿子辈，doc里只有一个ul元素，没有li元素
print('-'*60)


'''
单元素获取信息
'''
a=doc('.item-0.active a')
print(a, type(a))         #首先选中class为item-0和active的li节点内的a节点
print(a.attr('href'))     #再调用attr（）方法，传入属性名称，就可以得到属性值了
print(a.text())           #text()方法获取内部的文本信息，会忽略掉内部包含的所有HTML，只返回纯文字
print(a.html())           #若想包括节点内部的HTML文本，就要用html（）方法了
print('-'*60)


'''
多元素获取信息
'''
a_multiple=doc('a')
print(a_multiple)
for item in a_multiple.items():          #这里在调用items()方法后，会得到生成器，遍历一下就可以逐个得到a节点对象了
    print(item)
    print(item.attr('href'))             #在对多元素调用attr()方法时，需要遍历，否则只会得到第一个节点的属性

print(a_multiple.text())      #在对多元素调用text()方法时，不需要遍历，会返回全部纯文本
print(a_multiple.html())      #在对多元素调用html()方法时，需要遍历，否则只会得到第一个节点的HTML文本






