#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
 
import requests as req
import re

content = 'http://mitpress.mit.edu/sicp/full-text/book/book-Z-H-4.html'
urlpath = "http://mitpress.mit.edu/sicp/full-text/book/"

"""
res = req.get(content)
conFile = file('book-Z-H-4.html', 'wb+')
conFile.write(res.text)
conFile.close()

hrefs = re.findall(r'href="(.*?)"', res.text)

for i in xrange(0, len(hrefs)):
	hrefs[i] = hrefs[i].split('#')[0]
hrefs = list(set(hrefs))

for h in hrefs:
	section = urlpath + h.split('#')[0]
	print 'Writing to ' + h.split('#')[0]
	secFile = file(h.split('#')[0], 'wb+')
	secHtml = req.get(section)
	secFile.write(secHtml.text)
	secFile.close()
"""
## download images ##
grepResults = open('imgs', 'rb')
allImages = grepResults.read()

srcs = re.findall(r'<img src="(.*?)"', allImages)
srcs = list(set(srcs))

for s in srcs:
	imgUrl = urlpath + s
	image = req.get(imgUrl)
	imgFile = open(s, 'wb+')
	imgFile.write(image.content)
	imgFile.close()
