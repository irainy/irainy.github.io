---
layout: post
title: "图像处理的第一步：选择并抽取正确的特征"
description: "选取正确的、适合任务的图像特征对于图像处理至关重要，本文以OpenCV定位图像文本位置为例，对比不同的颜色空间对定位任务的影响。"
tags: [OpenCV; Python; Vision]
category: main
keywords: HSV, Lab色彩空间, CMYK
---

> **特征提取**是计算机视觉和图像处理中的一个概念...特征提取的结果是把图像上的点分为不同的子集，这些子集往往属于孤立的点、连续的曲线或者连续的区域([Wiki](http://zh.wikipedia.org/wiki/%E7%89%B9%E5%BE%81%E6%8F%90%E5%8F%96))。

基本上来说，图像处理任务首先都是要选取与任务相关的特征（如人脸识别中人脸的特征、边缘检测中边缘的特征等），然后将这些特征从复杂多变的背景信息中分离出来，再进行更进一步的处理。因而选择一个好的特征至关重要，后续的精细加工都是基于前面定位、过滤、抽取出来的较为单纯的特征信息，以图像中文字定位为例来说，常用的方法大致可以分为两种类型：基于连通域的方法和基于纹理的方法（脚注没修好，这里就不引用参考文献了），实际上就是针对于图像中的文字通常具有“在相对连续区域内颜色相同”以及“笔画之间夹杂细小缝隙的纹理或空间频率特征”。

常用的图像特征有颜色特征、纹理特征、形状特征、空间关系特征等([Ref-1](http://blog.sina.com.cn/s/blog_4e6680090100d2s9.html))。但是如何从这些特征中去选取最合适当前任务的特征呢？我们知道有一种“机器”在图像处理任务中做得非常出色，那就是人的视觉系统，David Marr 的经典著作 《*[Vision](http://book.douban.com/subject/5273663/)*》中也有提到，在最初人们想要用计算机去处理图像信息时并没有多少人想到这会有多难，毕竟对我们人类来说这些都是非常直觉、简单的加工过程，甚至在我们都还没有意识到的情况下视觉、认知系统已经完成了对图像的深度加工。而当人们真正着手去做的时候才发现，即使是最简单的 feature detector 要实现也是困难重重，在毫无头绪与经验的情况下所能采取的一种方法就是厚着脸皮不停尝试，正如 David Marr 所描述的 `unashamedly empirical approach :P`。

还是以文字定位为例，基于连通域的方法关键在于让文字区域的颜色或灰度值能够与不同图像的背景分离开来，因此采用什么样的颜色空间、取多大的阈值分离背景、通过怎样的形态学变化填充、联通文字所在的区域就成了算法需要调整的关键参数（这只是我基于多次尝试、对比得出的结论，因而未必最优，也没有理论的基础）。首先是颜色空间的选择，在尝试了[HSV](http://zh.wikipedia.org/wiki/HSV%E8%89%B2%E5%BD%A9%E5%B1%9E%E6%80%A7%E6%A8%A1%E5%BC%8F)、[CMYK](http://zh.wikipedia.org/wiki/CMYK)等之后，最后转向了[Lab色彩空间](http://zh.wikipedia.org/wiki/Lab%E8%89%B2%E5%BD%A9%E7%A9%BA%E9%97%B4)([Ref-2](http://www.cnblogs.com/skyseraph/archive/2011/08/11/2135291.html)):

{% highlight py linenos%}
'''
OpenCV-python codes
'''

from cv2 import *
import numpy as np

org = imread(fname, 1)
src = cvtColor(org, COLOR_BGR2LAB)

imshow('org', org)
imshow('src', src)
waitKey(0)
destroyAllWindows()
{% endhighlight %}

结果如下：

![](/assets/imgs/blog/sicp.png)

Wiki 中提到：
> 不像RGB和CMYK色彩空间，Lab颜色被设计来接近人类视觉。

不知道这是不是巧合，但可以肯定的是即便如此 Lab颜色也不会适合所有的处理任务。接下来通过阈值化、形态学变化等进一步分离特征：

{% highlight py linenos%}
from random import randint

_, res = threshold(res, 157, 255, THRESH_BINARY)
res = morphologyEx(res, MORPH_OPEN, getStructuringElement(MORPH_RECT, (7, 7)))
res = morphologyEx(res, MORPH_CLOSE, getStructuringElement(MORPH_RECT, (3, 3)))

fc = res.copy()
contours, hierarchy = findContours(fc, 1,1)
for c in contours:
    cnt = c
    x,y,w,h = boundingRect(cnt)
    if(w < 15 or h > 50 or w / h < 2):
        continue
    rectangle(org,(x,y),(x+w,y+h),(randint(1,255), randint(1,255), randint(1,255)),2)
{% endhighlight %}

结果如下：

![](/assets/imgs/blog/sicp_res.png)

后面的阈值化等操作的分离效果很大程度上来说并不取决于参数的选取，尤其是考虑到不同的图像中文字颜色、尺寸及其与背景噪音的对比，能否将特征分离出来更多还是取决于颜色空间的选取。
