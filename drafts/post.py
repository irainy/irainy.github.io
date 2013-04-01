#!/usr/bin/python

import yaml
import sqlite3
from jinja2 import Template

f = open('config.yaml')
c = f.read()
f.close()

y = yaml.load(c)

con = sqlite3.connect('db/sniky.blog.sqlite')
cur = con.cursor()

cur.execute('select * from article order by create_date desc limit 1')
r = cur.fetchone()

v = {'title': r[1], 'permalink': r[6]}

cur.execute('select count(*) from article')
r = cur.fetchone()

v['n'] = r[0]

print Template(y['weibo']['post']).render(v)
