#!/usr/bin/python
#-*- coding: utf8 -*-

import sqlite3 as sql
import os.path
from jinja2 import Template
import datetime, time

f = open('home_index.html')
c = unicode(f.read(), 'utf-8')

t = Template(c)

con = sql.connect('../db/sniky.blog.sqlite')
cur = con.cursor()

cur.execute('SELECT id, title, create_date, permalink FROM article WHERE posted = 1 ORDER BY create_date')
res = cur.fetchall()

#articles = ({'title': 123, 'dateline': 234, 'permalink': 345})
articles = []
for article in res:
	articles.append({
		'title': article[1],
		'dateline': time.strftime("%d %b %Y", time.strptime(str(article[2]), "%Y%m%d%H%M")).upper(),
		'permalink': article[3]
		})
print t.render(articles = articles)
print articles
