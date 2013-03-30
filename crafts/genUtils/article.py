#-*- coding: utf8 -*-
from datetime import datetime
from genUtils.dbCore import DB
import sqlite3 as sql
import sys
import os.path

dbFile='/Users/rainy/Projects/sniky.github.com/crafts/db/sniky.blog.sqlite'

class Article(DB):
	def __init__(self, title, cate = 'magic', author = 'me', permalink = '', dateline = ''):
		DB.__init__(self, dbFile)

		self.title = title
		self.cate = cate
		self.author = author
		self.permalink = permalink
		self.dateline = dateline

		self.create_d = dateline
		self.last_d = dateline
		self.article_id = 0
		self.posted = 0
		self.tags = []
	def isnew(self):
		query = "SELECT id FROM article WHERE title = '%s'" % self.title
		self.cur.execute(query)
		res = self.cur.fetchone()
		if res is not None:
			self.article_id = res[0]
		return self.article_id
	def update(self):
		query = "UPDATE article SET last_update = '%s', posted = 0 WHERE id = %s" % (self.str_date(self.dateline), self.article_id)
		self.cur.execute(query)
		self.con.commit()
	def tag(self, tag):
		query_seltag = "SELECT id FROM tag WHERE name = '%s' LIMIT 1" % tag
		self.cur.execute(query_seltag)
		res = self.cur.fetchone()
		if not res:
			query = "INSERT INTO tag(name, count) VALUES('%s', 1)" % tag
			self.cur.execute(query)
			self.con.commit()

			self.cur.execute(query_seltag)
			res = self.cur.fetchone()
		else:
			query = "UPDATE tag SET count = count + 1"
			self.cur.execute(query)
			self.con.commit()
		tagid = res[0]
		query = "INSERT INTO atmap(article_id, tag_id, cate_name) VALUES(%s, %s, '%s')" % (self.article_id, tagid, self.cate)
		self.cur.execute(query)
		self.con.commit()

		self.tags.append(tag)
	def save(self):
		query = "INSERT INTO article(title, create_date, last_update, posted, cate_name, permalink) VALUES('%s', '%s', '%s', '%s', '%s', '%s')" % (self.title, self.str_date(self.dateline), self.str_date(self.dateline), self.posted, self.cate, self.permalink)
		self.cur.execute(query)
		self.con.commit()

		self.isnew()
	def get_next(self):
		query = 'SELECT permalink FROM article WHERE id > %s AND cate_name = "%s" LIMIT 1' % (self.article_id, self.cate)
		self.cur.execute(query)
		link = self.cur.fetchone() 
		link = (link is None) and  'javascript:alert("已经是最后一篇！")' or link[0]
		return link
	def get_prev(self):
		query = 'SELECT permalink FROM article WHERE id < %s AND cate_name = "%s" LIMIT 1' % (self.article_id, self.cate)
		self.cur.execute(query)
		link = self.cur.fetchone() 
		link = (link is None) and 'javascript:alert("已经是第一篇！")' or link[0]
		return link
	def str_date(self, d):
		return datetime.strftime(d, "%Y%m%d%H%M")
	def format_date(self):
		return datetime.strftime(self.dateline, '%d %b %Y %H:%M').upper()
	def add_tags(self, tags):
		self.tags = tags
