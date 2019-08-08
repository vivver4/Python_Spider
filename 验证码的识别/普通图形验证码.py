'''
安装tesserocr的时候用pip intall tesserocr pillow总是发生错误，用
conda install -c simonflueckiger tesserocr可以成功，-c直接从https://conda.anaconda.org搜索
simonflueckiger的tesserocr库安装

这个内容需要复制到C盘符下的scratch.py中运行，具体原因不清楚
'''
import tesserocr
from PIL import Image
image=Image.open('C:/Users/shangya/Desktop/a.jpg')


'''
转灰度处理
'''
image=image.convert('L')

'''
二值化处理
这里设置阈值为140效果较好，默认为127
'''
threshold=140
table=[]
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
image=image.point(table, '1')
image.show()

result=tesserocr.image_to_text(image)
print(result)
