#-*- coding: utf8 -*-
from genUtils.dbCore import DB

class Updates(DB):
	def __init__(self, blog, tpl):
		DB.__init__(self)
	def dump(self, cate = 'home'):
		if cate == 'home':
			query = 'SELECT id, title, create_date, cate_name, permalink FROM article ORDER BY create_date DESC'
		else:
			query = 'SELECT id, title, create_date, cate_name, permalink FROM article WHERE cate_name = "%s" ORDER BY create_date DESC' % cate
		self.cur.execute(query)
		reses = self.cur.fetchall()
		return reses
