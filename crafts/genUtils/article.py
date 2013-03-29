#-*- coding: utf8 -*-
from datetime import datetime
import sqlite3 as sql
import sys
import os.path

CUR = os.path.abspath('db')

class Article:
	def __init__(self, title, create_d, last_d, posted = False, cate = 'magic', author = 'me', permalink = '', tags= []):
		self.tags = tags
		self.permalink = permalink
		self.author = author
		self.title = title
		self.create_d = create_d
		self.last_d = last_d
		self.posted = posted
		self.cate = cate

		self._init_db()

		self.new_article()

	def get_next(self):
		query = 'SELECT permalink FROM article WHERE id > %s AND cate_name = "%s" LIMIT 1' % (self.article_id, self.cate)
		self._cur.execute(query)
		link = self._cur.fetchone() 
		link = (link is None) and  'javascript:alert("已经是最后一篇！")' or link
		return link
	def get_prev(self):
		query = 'SELECT permalink FROM article WHERE id < %s AND cate_name = "%s" LIMIT 1' % (self.article_id, self.cate)
		self._cur.execute(query)
		link = self._cur.fetchone() 
		link = (link is None) and 'javascript:alert("已经是第一篇！")' or link
		return link
	def str_date(self, d):
		return datetime.strftime(d, "%Y%m%d%H%M")
	def format_date(self):
		return datetime.strftime(self.create_d, '%d %b %Y %H:%M').upper()
	def add_tags(self, tags):
		self.tags = tags
	def _init_db(self):
		self._db = sql.connect(os.path.join(CUR, 'sniky.blog.sqlite'))
		try:
			self._db = sql.connect(os.path.join(CUR, 'sniky.blog.sqlite'))
		except:
			sys.exit('\nFailed to connect database\n')
		self._cur = self._db.cursor()
	def new_article(self):
		self._cur.execute("SELECT id FROM article WHERE title = '%s'" % self.title)
		res = self._cur.fetchone()
		if not res:
			query = "INSERT INTO article(title, create_date, last_update, posted, cate_name, permalink) VALUES('%s', '%s', '%s', %s, '%s', '%s')" % (self.title, self.str_date(self.create_d), self.str_date(self.last_d), self.posted, self.cate, self.permalink)
			self._cur.execute(query)
			self._db.commit()
			for tag in self.tags:
				query_seltag = "SELECT id FROM tag WHERE name = '%s' LIMIT 1" % tag
				self._cur.execute(query_seltag)
				res = self._cur.fetchone()
				if not res:
					query = "INSERT INTO tag(name, count) VALUES('%s', 1)" % tag
					self._cur.execute(query)
					self._db.commit()
					self._cur.execute(query_seltag)
					res = self._cur.fetchone()
				else:
					query = "UPDATE tag SET count = count + 1"
					self._cur.execute(query)
					self._db.commit()
				tagid = res[0]
				query = "INSERT INTO atmap(article_id, tag_id, cate_name) VALUES(%s, %s, '%s')" % (self.article_id, tagid, self.cate)
				self._cur.execute(query)
				self._db.commit()
		else:
			self._cur.execute("SELECT id FROM article WHERE title = '%s'" % self.title)
			self.article_id = self._cur.fetchone()[0]
