#!/usr/bin/python
#-*- coding: utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8') 

import misaka
import re
import yaml
from jinja2 import Template

mdf = open('./How-to-blog-on-github-pages.md')
#wrf = open('index.html')


#wrapper = wrf.read()

content = mdf.read()

res = re.findall(r'(<conf[\s\S]*>([\s\S]*)<\/conf>)', content)
conf = res[0][1]
content = unicode(content[len(res[0][0]):], 'utf-8')

conf_obj = yaml.load(conf)

tags = conf_obj['tags'].split(', ')

print highlight(content, lexer, formatter)
blog_body = misaka.html(content)
print blog_body

#tmplate = Template(unicode(wrapper, 'utf-8'))
#resultHTML = tmplate.render(blog_body = unicode(blog_body, 'utf-8'))
#resultHTML = tmplate.render(blog_body = blog_body)

#title = conf_obj['title']
#blog = open(title + '.html','w')
#blog.write(resultHTML.decode('utf-8'))

mdf.close()
#wrf.close()
#blog.close()
